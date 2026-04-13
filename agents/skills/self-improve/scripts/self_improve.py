#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sqlite3
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable


CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
STATE_DB = CODEX_HOME / "state_5.sqlite"
SKILLS_ROOT = CODEX_HOME / "skills"
SKILL_ROOTS = (
    CODEX_HOME / "skills",
    Path.home() / ".agents" / "skills",
)
GLOBAL_AGENTS = CODEX_HOME / "AGENTS.md"
REPO_SEARCH_ROOTS = (
    Path.home() / "dev",
    Path.home() / "code",
    Path.home() / "personal",
)

PREFERENCE_MARKERS = (
    "make sure",
    "default to",
    "prefer",
    "instead of",
    "do not",
    "don't",
    "never",
    "always",
    "should be",
    "should default",
    "i want you to",
    "i don't want",
    "preserve",
    "keep ",
    "lean on",
    "continue",
    "keep going",
    "don't stop",
    "come on",
    "can't you just",
)

SKIP_USER_MESSAGE_RE = re.compile(
    r"<INSTRUCTIONS>|#\s*AGENTS\.md instructions|PLEASE IMPLEMENT THIS PLAN",
    re.IGNORECASE,
)

COMMON_WORDS = {
    "about",
    "after",
    "again",
    "also",
    "because",
    "could",
    "default",
    "doing",
    "first",
    "have",
    "instead",
    "maybe",
    "please",
    "should",
    "that",
    "their",
    "there",
    "these",
    "thing",
    "things",
    "this",
    "those",
    "using",
    "want",
    "would",
    "write",
    "your",
}

NOISY_SNIPPET_RE = re.compile(
    r"```|^#+\s|^[-+]{1,3}|^comment:\s|^file:\s|^lines:\s|"
    r"^(key changes|implementation|summary|test plan|assumptions)\b|"
    r"diff hunk|review findings|my request for codex",
    re.IGNORECASE,
)

QUESTION_PREFIXES = (
    "okay, can you",
    "ok, can you",
    "what should",
    "how should",
    "how do you think",
    "also, what",
    "also what",
    "can you propose",
    "can you look",
    "could you look",
    "first can you",
    "i feel like",
    "they all",
    "they don't",
    "they do not",
)

PROJECT_CONTEXT_TOKENS = (
    "agnts.md",
    "agents.md",
    "readme",
    "outline",
    "packet",
    "this repo",
    "this project",
    "in the project",
    "in this project",
    "in this repo",
    "shadcn",
    "tailwind",
    "vite",
    "react",
    "package",
    "implementation",
    "component",
    "widget",
    "template",
    "api",
    "demo",
    "voice",
    "audio",
    "docs",
    "slack",
    "pending slack replies",
    "resolved threads",
    "none right now",
    "vault",
    "screenshot",
)

PROJECT_IMPLEMENTATION_TOKENS = (
    "activation gating",
    "app-local state",
    "dom-derived",
    "selected widget",
    "event handlers",
    "typed fields",
    "streaming tokens",
    "audio output",
    "system message",
)

TRANSIENT_ERROR_TOKENS = (
    "correct access rights and the repository exists",
    "fatal: could not read from remote repository",
    "repository not found",
)


@dataclass(frozen=True)
class ThreadRecord:
    thread_id: str
    title: str
    source: str
    cwd: str
    created_at: int
    updated_at: int
    archived: bool
    model: str
    reasoning_effort: str
    rollout_path: str
    agent_role: str
    agent_nickname: str


@dataclass(frozen=True)
class Evidence:
    thread_id: str
    title: str
    updated_at: int
    rollout_path: str
    cwd: str
    cluster_key: str


@dataclass
class Proposal:
    bucket: str
    target: str
    suggestion: str
    evidence: list[Evidence] = field(default_factory=list)

    @property
    def support(self) -> int:
        return len({item.cluster_key for item in self.evidence})

    @property
    def last_seen(self) -> int:
        return max((item.updated_at for item in self.evidence), default=0)

    @property
    def confidence(self) -> float:
        score = 0.42 + min(self.support, 6) * 0.12
        lowered = self.suggestion.lower()

        if lowered.startswith(("i ", "this ", "that ", "only ", "leave room for")):
            score -= 0.18
        if any(token in lowered for token in (" kind of ", " sort of ", " maybe ", " thing ", " stuff ")):
            score -= 0.08
        if any(token in lowered for token in ("create sub-agents", "keep improving the complexity", "let's just iterate")):
            score -= 0.24
        if "?" in self.suggestion:
            score -= 0.18
        if self.bucket == "Global AGENTS.md" and any(token in lowered for token in PROJECT_IMPLEMENTATION_TOKENS):
            score -= 0.22
        if "human-authored documentation" in lowered or "over-engineering" in lowered:
            score += 0.08
        if any(token in lowered for token in ("continue", "keep going", "don't stop", "frustration cues")):
            score += 0.08

        return max(0.0, min(0.99, score))


@dataclass(frozen=True)
class SkillRecord:
    name: str
    path: Path
    text: str
    aliases: tuple[str, ...]


def require_db(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Missing Codex state DB: {path}")


def to_utc(ts: int) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")


def shorten(value: str, width: int) -> str:
    value = " ".join((value or "").split())
    if not value:
        return ""
    if len(value) <= width:
        return value
    return f"{value[: max(width - 1, 1)]}…"


def normalize_source(source: str) -> str:
    source = source or ""
    if not source.startswith("{"):
        return source
    try:
        parsed = json.loads(source)
    except json.JSONDecodeError:
        return source
    subagent = parsed.get("subagent")
    if isinstance(subagent, str):
        return f"subagent:{subagent}"
    if isinstance(subagent, dict):
        spawn = subagent.get("thread_spawn") or {}
        role = spawn.get("agent_role") or "subagent"
        nickname = spawn.get("agent_nickname")
        parent = spawn.get("parent_thread_id")
        if nickname and parent:
            return f"{role}:{nickname}@{parent[:8]}"
        if parent:
            return f"{role}@{parent[:8]}"
        return role
    return source


def normalize_token_key(value: str) -> str:
    tokens = [
        token
        for token in re.findall(r"[a-z0-9]+", value.lower())
        if token not in COMMON_WORDS
    ]
    return "-".join(tokens[:12])


def normalize_tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.lower())
        if token not in COMMON_WORDS and len(token) > 2
    }


def thread_cluster_key(thread: ThreadRecord, target: str) -> str:
    day = datetime.fromtimestamp(thread.updated_at, tz=timezone.utc).strftime("%Y-%m-%d")
    title_key = normalize_token_key(thread.title) or normalize_token_key(thread.cwd) or thread.thread_id
    return f"{target}::{title_key}::{day}"


@lru_cache(maxsize=1)
def known_repo_roots() -> tuple[Path, ...]:
    roots: list[Path] = []
    vault_root = Path.home() / "vault"
    if vault_root.exists():
        roots.append(vault_root)

    for search_root in REPO_SEARCH_ROOTS:
        if not search_root.is_dir():
            continue
        for child in search_root.iterdir():
            if child.is_dir():
                roots.append(child)
    return tuple(roots)


def resolve_repo_root_name(repo_name: str, fallback: Path) -> Path:
    candidates = known_repo_roots()
    if not candidates:
        return fallback

    exact = next((candidate for candidate in candidates if candidate.name == repo_name), None)
    if exact is not None:
        return exact

    best_candidate = fallback
    best_score = 0.0
    for candidate in candidates:
        score = difflib.SequenceMatcher(None, repo_name, candidate.name).ratio()
        if candidate.name.endswith(repo_name) or repo_name.endswith(candidate.name):
            score += 0.15
        repo_tokens = set(repo_name.split("-"))
        candidate_tokens = set(candidate.name.split("-"))
        if repo_tokens and candidate_tokens:
            score += 0.10 * (len(repo_tokens & candidate_tokens) / len(repo_tokens | candidate_tokens))
        if score > best_score:
            best_score = score
            best_candidate = candidate

    if best_score >= 0.74:
        return best_candidate

    matches = difflib.get_close_matches(
        repo_name,
        [candidate.name for candidate in candidates],
        n=1,
        cutoff=0.74,
    )
    if matches:
        return next(candidate for candidate in candidates if candidate.name == matches[0])
    return fallback


def fetch_threads(
    db_path: Path,
    *,
    limit: int,
    archived: str,
    cwd_prefix: str | None = None,
    source_query: str | None = None,
    model_query: str | None = None,
    text_query: str | None = None,
    days: int | None = None,
    top_level_only: bool = False,
) -> list[ThreadRecord]:
    require_db(db_path)
    where = []
    params: list[Any] = []

    if archived == "active":
        where.append("archived = 0")
    elif archived == "archived":
        where.append("archived = 1")
    elif archived != "all":
        raise SystemExit("--archived must be one of active, archived, all")

    if cwd_prefix:
        where.append("cwd LIKE ?")
        params.append(f"{cwd_prefix}%")
    if source_query:
        where.append("source LIKE ?")
        params.append(f"%{source_query}%")
    if model_query:
        where.append("coalesce(model, '') LIKE ?")
        params.append(f"%{model_query}%")
    if text_query:
        lowered = f"%{text_query.lower()}%"
        where.append("(lower(title) LIKE ? OR lower(first_user_message) LIKE ?)")
        params.extend([lowered, lowered])
    if days:
        cutoff = int((datetime.now(tz=timezone.utc) - timedelta(days=days)).timestamp())
        where.append("updated_at >= ?")
        params.append(cutoff)
    if top_level_only:
        where.append("source IN ('vscode', 'cli', 'exec')")
        where.append("(agent_role IS NULL OR agent_role = '')")
        where.append("title NOT LIKE 'Automation:%'")

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""
    sql = f"""
        SELECT
            id,
            title,
            source,
            cwd,
            created_at,
            updated_at,
            archived,
            coalesce(model, ''),
            coalesce(reasoning_effort, ''),
            rollout_path,
            coalesce(agent_role, ''),
            coalesce(agent_nickname, '')
        FROM threads
        {where_sql}
        ORDER BY updated_at DESC, id DESC
        LIMIT ?
    """
    params.append(limit)

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(sql, params).fetchall()

    return [
        ThreadRecord(
            thread_id=row[0],
            title=row[1] or "",
            source=row[2] or "",
            cwd=row[3] or "",
            created_at=int(row[4]),
            updated_at=int(row[5]),
            archived=bool(row[6]),
            model=row[7] or "",
            reasoning_effort=row[8] or "",
            rollout_path=row[9] or "",
            agent_role=row[10] or "",
            agent_nickname=row[11] or "",
        )
        for row in rows
    ]


def fetch_thread_by_id(db_path: Path, thread_id: str) -> ThreadRecord | None:
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            """
            SELECT
                id, title, source, cwd, created_at, updated_at, archived,
                coalesce(model, ''), coalesce(reasoning_effort, ''),
                rollout_path, coalesce(agent_role, ''), coalesce(agent_nickname, '')
            FROM threads
            WHERE id = ?
            """,
            (thread_id,),
        ).fetchone()
    if not row:
        return None
    return ThreadRecord(
        thread_id=row[0],
        title=row[1] or "",
        source=row[2] or "",
        cwd=row[3] or "",
        created_at=int(row[4]),
        updated_at=int(row[5]),
        archived=bool(row[6]),
        model=row[7] or "",
        reasoning_effort=row[8] or "",
        rollout_path=row[9] or "",
        agent_role=row[10] or "",
        agent_nickname=row[11] or "",
    )


def find_orphan_rollout(thread_id: str) -> Path | None:
    for root in (CODEX_HOME / "sessions", CODEX_HOME / "archived_sessions"):
        for candidate in root.rglob(f"*{thread_id}.jsonl"):
            return candidate
    return None


def iter_rollout_events(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Bad JSON in {path}:{line_no}: {exc}") from exc


def collect_user_messages(thread: ThreadRecord) -> list[str]:
    path = Path(thread.rollout_path)
    if not path.exists():
        return []

    messages: list[str] = []
    for event in iter_rollout_events(path):
        if event.get("type") != "event_msg":
            continue
        payload = event.get("payload") or {}
        if payload.get("type") != "user_message":
            continue
        message = (payload.get("message") or "").strip()
        if message:
            messages.append(message)
    return messages


def query_matches_thread(thread: ThreadRecord, query: str | None) -> bool:
    if not query:
        return True
    needle = query.lower()
    if needle in (thread.title or "").lower():
        return True
    if needle in (thread.cwd or "").lower():
        return True
    for message in collect_user_messages(thread):
        if needle in message.lower():
            return True
    return False


def extract_message_text(payload: dict[str, Any]) -> str:
    content = payload.get("content") or []
    chunks: list[str] = []
    for item in content:
        if isinstance(item, dict):
            text = item.get("text")
            if text:
                chunks.append(str(text))
    return "\n".join(chunks).strip()


def print_threads_table(rows: list[ThreadRecord]) -> None:
    print("Updated UTC         St Source            Model           CWD                              Title                            Thread")
    print("------------------- -- ----------------- --------------- -------------------------------- -------------------------------- ------------------------------------")
    for row in rows:
        state = "AR" if row.archived else "AC"
        source = normalize_source(row.source)
        print(
            f"{to_utc(row.updated_at):<19} "
            f"{state:<2} "
            f"{shorten(source, 17):<17} "
            f"{shorten(row.model, 15):<15} "
            f"{shorten(row.cwd, 32):<32} "
            f"{shorten(row.title, 32):<32} "
            f"{row.thread_id}"
        )


def cmd_list(args: argparse.Namespace) -> None:
    rows = fetch_threads(
        STATE_DB,
        limit=args.limit,
        archived=args.archived,
        cwd_prefix=args.cwd,
        source_query=args.source,
        model_query=args.model,
        text_query=args.query,
        days=args.days,
        top_level_only=args.top_level_only,
    )
    print_threads_table(rows)


def render_transcript(thread: ThreadRecord, *, max_tool_chars: int, include_instructions: bool) -> None:
    rollout_path = Path(thread.rollout_path)
    if not rollout_path.exists():
        fallback = find_orphan_rollout(thread.thread_id)
        if fallback is not None:
            rollout_path = fallback

    print(f"# {thread.title or thread.thread_id}")
    print()
    print(f"- thread_id: `{thread.thread_id}`")
    print(f"- updated_at: `{to_utc(thread.updated_at)}`")
    print(f"- created_at: `{to_utc(thread.created_at)}`")
    print(f"- source: `{normalize_source(thread.source)}`")
    print(f"- model: `{thread.model}`")
    print(f"- reasoning_effort: `{thread.reasoning_effort}`")
    print(f"- archived: `{int(thread.archived)}`")
    print(f"- cwd: `{thread.cwd}`")
    print(f"- rollout_path: `{rollout_path}`")
    print()

    for event in iter_rollout_events(rollout_path):
        event_type = event.get("type")
        payload = event.get("payload") or {}

        if event_type == "event_msg":
            payload_type = payload.get("type")
            if payload_type == "user_message":
                message = (payload.get("message") or "").strip()
                if message:
                    print("## User")
                    print()
                    print(message)
                    print()
            elif payload_type == "agent_message":
                message = (payload.get("message") or "").strip()
                if message:
                    phase = payload.get("phase") or "assistant"
                    print(f"## Assistant ({phase})")
                    print()
                    print(message)
                    print()
            elif payload_type == "task_started":
                print("## Task Started")
                print()
            elif payload_type == "task_complete":
                print("## Task Complete")
                print()
            continue

        if event_type != "response_item":
            continue

        payload_type = payload.get("type")
        if payload_type == "message" and include_instructions:
            role = payload.get("role") or "unknown"
            if role not in {"developer", "system"}:
                continue
            text = extract_message_text(payload)
            if text:
                print(f"## {role.title()} Instructions")
                print()
                print(text)
                print()
        elif payload_type == "function_call":
            name = payload.get("name") or "unknown_tool"
            args = payload.get("arguments") or ""
            print(f"## Tool Call: {name}")
            print()
            print("```json")
            print(shorten(str(args), max_tool_chars))
            print("```")
            print()
        elif payload_type == "function_call_output":
            call_id = payload.get("call_id") or "unknown"
            output = payload.get("output") or ""
            print(f"## Tool Output: {call_id}")
            print()
            print("```text")
            print(shorten(str(output), max_tool_chars))
            print("```")
            print()


def cmd_show(args: argparse.Namespace) -> None:
    thread = fetch_thread_by_id(STATE_DB, args.thread_id)
    if thread is None:
        orphan = find_orphan_rollout(args.thread_id)
        if orphan is None:
            raise SystemExit(f"No thread found for {args.thread_id}")
        print(f"# Orphan Rollout {args.thread_id}")
        print()
        print(f"- rollout_path: `{orphan}`")
        print()
        for event in iter_rollout_events(orphan):
            if event.get("type") == "session_meta":
                print("```json")
                print(json.dumps(event.get("payload") or {}, indent=2, sort_keys=True))
                print("```")
                return
        return

    render_transcript(
        thread,
        max_tool_chars=args.max_tool_chars,
        include_instructions=args.include_instructions,
    )


def split_sentences(message: str) -> Iterable[str]:
    normalized = re.sub(r"\s+", " ", message).strip()
    for chunk in re.split(r"(?<=[.!?])\s+|;\s+|\s+\|\s+", normalized):
        chunk = chunk.strip(" \t\r\n\"'`")
        if chunk:
            yield chunk


def looks_like_preference(sentence: str) -> bool:
    lowered = sentence.lower()
    if NOISY_SNIPPET_RE.search(sentence):
        return False
    if any(token in lowered for token in TRANSIENT_ERROR_TOKENS):
        return False
    if "don't know" in lowered or "do not know" in lowered:
        return False
    if lowered in {"continue", "keep going", "just keep going", "sorry keep going"} or "don't stop" in lowered:
        return True
    if "come on" in lowered or "can't you just" in lowered:
        return True
    if lowered.startswith(QUESTION_PREFIXES):
        return False
    if sentence.endswith("?") and "make sure" not in lowered and "default to" not in lowered and "prefer" not in lowered:
        return False
    if lowered.startswith("can you") and "make sure" not in lowered:
        return False
    return any(marker in lowered for marker in PREFERENCE_MARKERS)


def normalize_suggestion(sentence: str) -> str:
    suggestion = sentence.strip()
    suggestion = re.sub(r"^(okay|ok|yeah|and then)[, ]+", "", suggestion, flags=re.IGNORECASE)
    suggestion = re.sub(r"^(can you|could you)\s+(please\s+)?", "", suggestion, flags=re.IGNORECASE)
    suggestion = re.sub(r"^make sure\s+(that\s+)?", "", suggestion, flags=re.IGNORECASE)
    suggestion = re.sub(r"^i want you to\s+", "", suggestion, flags=re.IGNORECASE)
    suggestion = re.sub(r"^i want the\s+", "Keep the ", suggestion, flags=re.IGNORECASE)
    suggestion = re.sub(r"^let'?s\s+", "Prefer to ", suggestion, flags=re.IGNORECASE)
    suggestion = re.sub(r"\b(relatively speaking|kind of|sort of|basically|actually|really|like)\b", "", suggestion, flags=re.IGNORECASE)
    suggestion = re.sub(
        r"\bto\s+not\s+have\s+any(?:\s+kind\s+of)?\s+incongruenc(?:y|ies)\b",
        "to avoid contradictions",
        suggestion,
        flags=re.IGNORECASE,
    )
    suggestion = re.sub(r"\bmake sure everything'?s aligned\b", "keep related docs aligned", suggestion, flags=re.IGNORECASE)
    suggestion = re.sub(r"\breads much more\s+a human documentation\b", "read like human-authored documentation", suggestion, flags=re.IGNORECASE)
    suggestion = re.sub(r"\breads much more\s+human documentation\b", "read like human-authored documentation", suggestion, flags=re.IGNORECASE)
    suggestion = re.sub(r"\bnothing is over-engineered\b", "avoid over-engineering", suggestion, flags=re.IGNORECASE)
    suggestion = re.sub(r"\s+", " ", suggestion)
    suggestion = suggestion.strip(" .!?")
    if not suggestion:
        return ""
    lowered = suggestion.lower()
    if "break up" in lowered and "agents.md" in lowered and "worktogether" in lowered:
        return "Split multi-file project packets into semantic notes and add a local AGENTS.md that explains file roles, source-of-truth boundaries, and routing."
    if "don't want the front ends to look ai generated" in lowered or "do not want the front ends to look ai generated" in lowered:
        return "Avoid AI-generated-looking frontend UI."
    if lowered in {"continue", "keep going", "just keep going", "sorry keep going"} or "don't stop" in lowered:
        return "When the user says `continue`, `keep going`, or `don't stop`, keep executing the current task without pausing unless there is a real blocker or destructive approval boundary."
    if "can't you just find it in my environment" in lowered or lowered == "come on":
        return "Treat “Come on” or “can't you just...” as frustration cues; inspect the local environment directly, reduce prose, and move forward with concrete actions instead of asking broad questions."
    if "keep telling the models to keep continuing" in lowered:
        return "Detect repeated `continue` / `keep going` nudges as a signal to persist autonomously and avoid stopping for unnecessary check-ins."
    if "human-authored documentation" in lowered and lowered.startswith(("that", "all of this")):
        return "Write docs and READMEs in human-authored, concrete prose."
    suggestion = re.sub(r"^(that|all of this)[, ]+", "", suggestion, flags=re.IGNORECASE)
    suggestion = suggestion[0].upper() + suggestion[1:]
    if not suggestion.endswith("."):
        suggestion += "."
    return suggestion


def known_skill_names() -> list[str]:
    names = []
    for root in SKILL_ROOTS:
        if not root.exists():
            continue
        for child in root.iterdir():
            if child.is_dir() and (child / "SKILL.md").exists():
                names.append(child.name)
    return sorted(names, key=len, reverse=True)


def infer_project_agents_path(cwd: str) -> str:
    path = Path(cwd).expanduser()
    home = Path.home()

    worktrees_root = CODEX_HOME / "worktrees"
    try:
        relative = path.relative_to(worktrees_root)
    except ValueError:
        relative = None
    if relative and len(relative.parts) >= 2:
        repo_name = relative.parts[1]
        fallback_repo = worktrees_root / relative.parts[0] / repo_name
        repo_root = resolve_repo_root_name(repo_name, fallback_repo)
        for filename in ("AGENTS.md", "AGENTS.MD"):
            candidate = repo_root / filename
            if candidate.exists():
                return str(candidate)
        return str(repo_root / "AGENTS.md")

    for search_root in (home / "dev", home / "code", home / "personal"):
        try:
            relative = path.relative_to(search_root)
        except ValueError:
            continue
        if not relative.parts:
            break
        repo_root = resolve_repo_root_name(relative.parts[0], search_root / relative.parts[0])
        for filename in ("AGENTS.md", "AGENTS.MD"):
            candidate = repo_root / filename
            if candidate.exists():
                return str(candidate)
        return str(repo_root / "AGENTS.md")

    for candidate_dir in [path, *path.parents]:
        if candidate_dir == home:
            break
        if candidate_dir == CODEX_HOME:
            break
        for filename in ("AGENTS.md", "AGENTS.MD"):
            candidate = candidate_dir / filename
            if candidate.exists():
                return str(candidate)
        if (candidate_dir / ".git").exists():
            return str(candidate_dir / "AGENTS.md")
    return str(path / "AGENTS.md")


def infer_skill_path(sentence: str, cwd: str, skills: list[str]) -> str:
    cwd_path = Path(cwd).expanduser()
    for root in SKILL_ROOTS:
        try:
            relative = cwd_path.relative_to(root)
            if relative.parts:
                candidate = root / relative.parts[0] / "SKILL.md"
                if candidate.exists():
                    return str(candidate)
        except ValueError:
            pass

    lowered = sentence.lower()
    for name in skills:
        if name not in lowered:
            continue
        for root in SKILL_ROOTS:
            candidate = root / name / "SKILL.md"
            if candidate.exists():
                return str(candidate)

    return str(SKILLS_ROOT / "<new-skill>" / "SKILL.md")


def classify_bucket(sentence: str, thread: ThreadRecord, skills: list[str]) -> tuple[str, str]:
    lowered = sentence.lower()
    cwd = thread.cwd or ""

    if (
        "skill" in lowered
        or "skill.md" in lowered
        or "/skills/" in lowered
        or any(cwd.startswith(str(root)) for root in SKILL_ROOTS)
    ):
        return "Skills", infer_skill_path(sentence, cwd, skills)

    if cwd == str(Path.home()) or cwd == str(CODEX_HOME):
        return "Global AGENTS.md", str(GLOBAL_AGENTS)

    if any(marker in lowered for marker in ("globally", "all repos", "all projects", "for any repo", "across repos")):
        return "Global AGENTS.md", str(GLOBAL_AGENTS)

    if cwd.startswith(str(Path.home() / "vault")) and any(
        token in lowered
        for token in ("pending slack replies", "resolved threads", "none right now", "fyi", "slack")
    ):
        return "Project AGENTS.md", infer_project_agents_path(cwd)

    if not any(token in lowered for token in PROJECT_CONTEXT_TOKENS):
        return "Global AGENTS.md", str(GLOBAL_AGENTS)

    return "Project AGENTS.md", infer_project_agents_path(cwd)


def extract_preference_signals(thread: ThreadRecord) -> list[tuple[str, str]]:
    signals: list[tuple[str, str]] = []
    for message in collect_user_messages(thread):
        if not message:
            continue
        if len(message) > 5000:
            continue
        if SKIP_USER_MESSAGE_RE.search(message):
            continue
        for sentence in split_sentences(message):
            if len(sentence) < 14 or len(sentence) > 600:
                continue
            if not looks_like_preference(sentence):
                continue
            suggestion = normalize_suggestion(sentence)
            if len(suggestion) >= 25:
                signals.append((sentence, suggestion))
    return signals


def collect_proposals(rows: list[ThreadRecord], min_support: int) -> list[Proposal]:
    skills = known_skill_names()
    grouped: dict[tuple[str, str, str], Proposal] = {}

    for thread in rows:
        for raw_sentence, suggestion in extract_preference_signals(thread):
            bucket, target = classify_bucket(raw_sentence, thread, skills)
            key = (bucket, target, suggestion.lower())
            proposal = grouped.setdefault(
                key,
                Proposal(bucket=bucket, target=target, suggestion=suggestion),
            )
            if not any(item.thread_id == thread.thread_id for item in proposal.evidence):
                proposal.evidence.append(
                    Evidence(
                        thread_id=thread.thread_id,
                        title=thread.title,
                        updated_at=thread.updated_at,
                        rollout_path=thread.rollout_path,
                        cwd=thread.cwd,
                        cluster_key=thread_cluster_key(thread, target),
                    )
                )

    proposals = [
        proposal
        for proposal in grouped.values()
        if proposal.support >= min_support
    ]
    return sorted(
        proposals,
        key=lambda item: (item.bucket, -item.confidence, -item.support, -item.last_seen, item.target),
    )


def skill_aliases(name: str, skill_path: Path) -> tuple[str, ...]:
    aliases = {
        name.lower(),
        f"${name.lower()}",
        name.lower().replace("-", " "),
        str(skill_path).lower(),
        skill_path.parent.name.lower(),
    }
    return tuple(sorted(alias for alias in aliases if alias))


def parse_skill_name(skill_text: str, fallback_name: str) -> str:
    match = re.search(r"^name:\s*['\"]?([^'\"\n]+)['\"]?\s*$", skill_text, re.MULTILINE)
    return match.group(1).strip() if match else fallback_name


@lru_cache(maxsize=1)
def load_skill_records() -> tuple[SkillRecord, ...]:
    records: list[SkillRecord] = []
    for root in SKILL_ROOTS:
        if not root.exists():
            continue
        for skill_file in sorted(root.glob("*/SKILL.md")):
            text = skill_file.read_text(encoding="utf-8")
            name = parse_skill_name(text, skill_file.parent.name)
            records.append(
                SkillRecord(
                    name=name,
                    path=skill_file,
                    text=text,
                    aliases=skill_aliases(name, skill_file),
                )
            )
    return tuple(sorted(records, key=lambda record: record.name))


def skill_matches_thread(skill: SkillRecord, thread: ThreadRecord, user_messages: list[str]) -> bool:
    haystack = " ".join(
        [
            thread.title or "",
            thread.cwd or "",
            *user_messages,
        ]
    ).lower()
    return any(alias and alias in haystack for alias in skill.aliases)


def suggestion_already_documented(skill: SkillRecord, suggestion: str) -> bool:
    suggestion_tokens = normalize_tokens(suggestion)
    if len(suggestion_tokens) < 3:
        return False

    skill_text = " ".join(skill.text.lower().split())
    suggestion_text = " ".join(suggestion.lower().split())
    if suggestion_text in skill_text:
        return True

    skill_tokens = normalize_tokens(skill.text)
    overlap = len(suggestion_tokens & skill_tokens) / max(len(suggestion_tokens), 1)
    if overlap >= 0.85:
        return True

    return difflib.SequenceMatcher(None, suggestion_text, skill_text).ratio() >= 0.9


def collect_skill_audit_proposals(
    rows: list[ThreadRecord],
    *,
    skill_name: str | None,
    min_support: int,
) -> tuple[list[Proposal], list[SkillRecord]]:
    all_skills = list(load_skill_records())
    if skill_name:
        needle = skill_name.lower()
        selected_skills = [
            skill
            for skill in all_skills
            if skill.name.lower() == needle or skill.path.parent.name.lower() == needle or needle in skill.aliases
        ]
        if not selected_skills:
            raise SystemExit(f"No installed skill matched {skill_name!r}")
    else:
        selected_skills = all_skills

    grouped: dict[tuple[str, str], Proposal] = {}

    for thread in rows:
        user_messages = collect_user_messages(thread)
        if not user_messages:
            continue
        suggestions = [suggestion for _, suggestion in extract_preference_signals(thread)]
        if not suggestions:
            continue

        for skill in selected_skills:
            if not skill_matches_thread(skill, thread, user_messages):
                continue
            for suggestion in suggestions:
                if suggestion_already_documented(skill, suggestion):
                    continue
                key = (str(skill.path), suggestion.lower())
                proposal = grouped.setdefault(
                    key,
                    Proposal(bucket="Skills", target=str(skill.path), suggestion=suggestion),
                )
                if not any(item.thread_id == thread.thread_id for item in proposal.evidence):
                    proposal.evidence.append(
                        Evidence(
                            thread_id=thread.thread_id,
                            title=thread.title,
                            updated_at=thread.updated_at,
                            rollout_path=thread.rollout_path,
                            cwd=thread.cwd,
                            cluster_key=thread_cluster_key(thread, str(skill.path)),
                        )
                    )

    proposals = [
        proposal
        for proposal in grouped.values()
        if proposal.support >= min_support
    ]
    return (
        sorted(proposals, key=lambda item: (-item.confidence, -item.support, -item.last_seen, item.target)),
        selected_skills,
    )


def emit_skill_audit_report(
    rows: list[ThreadRecord],
    proposals: list[Proposal],
    selected_skills: list[SkillRecord],
    *,
    max_per_skill: int,
    emit_patch: bool,
) -> None:
    if rows:
        newest = max(row.updated_at for row in rows)
        oldest = min(row.updated_at for row in rows)
    else:
        newest = oldest = 0

    print("# /self-improve skill-audit")
    print()
    print(
        f"Analyzed {len(rows)} top-level user threads from {to_utc(oldest) if oldest else 'n/a'} "
        f"to {to_utc(newest) if newest else 'n/a'} across {len(selected_skills)} installed skill(s)."
    )
    print("Default write policy: propose-first. Do not patch SKILL.md files until the user explicitly approves.")
    print()

    by_target: dict[str, list[Proposal]] = defaultdict(list)
    for proposal in proposals:
        by_target[proposal.target].append(proposal)

    if not proposals:
        print("- No uncovered skill proposals found in this sample.")
        print()
        return

    for target in sorted(by_target):
        print(f"## {target}")
        print()
        for proposal in by_target[target][:max_per_skill]:
            evidence_bits = []
            for item in proposal.evidence[:3]:
                evidence_bits.append(
                    f"{item.thread_id} | {shorten(item.title, 60)} | {to_utc(item.updated_at)} | {item.rollout_path}"
                )
            print(f"- Proposal: {proposal.suggestion}")
            print(f"  Support: {proposal.support} thread cluster(s)")
            print(f"  Confidence: {proposal.confidence:.2f}")
            print(f"  Evidence: {' || '.join(evidence_bits)}")
        print()

    if emit_patch:
        print("## Patch Preview")
        print()
        for target in sorted(by_target):
            print("```diff")
            print(f"--- {target}")
            print(f"+++ {target}")
            print("@@")
            for proposal in by_target[target][:max_per_skill]:
                print(f"+- {proposal.suggestion}")
            print("```")
            print()


def emit_patch_preview(proposals: list[Proposal], max_per_bucket: int) -> None:
    grouped: dict[str, dict[str, list[Proposal]]] = defaultdict(lambda: defaultdict(list))
    for proposal in proposals:
        grouped[proposal.bucket][proposal.target].append(proposal)

    print("## Patch Preview")
    print()
    for bucket in ("Skills", "Project AGENTS.md", "Global AGENTS.md"):
        if not grouped.get(bucket):
            continue
        print(f"### {bucket}")
        print()
        for target, target_items in grouped[bucket].items():
            print("```diff")
            print(f"--- {target}")
            print(f"+++ {target}")
            print("@@")
            for proposal in target_items[:max_per_bucket]:
                print(f"+- {proposal.suggestion}")
            print("```")
            print()


def emit_dream_report(
    rows: list[ThreadRecord],
    proposals: list[Proposal],
    *,
    max_per_bucket: int,
    emit_patch: bool,
) -> None:
    if rows:
        newest = max(row.updated_at for row in rows)
        oldest = min(row.updated_at for row in rows)
    else:
        newest = oldest = 0

    print("# /self-improve dream")
    print()
    print(f"Analyzed {len(rows)} top-level user threads from {to_utc(oldest) if oldest else 'n/a'} to {to_utc(newest) if newest else 'n/a'}.")
    print("Default write policy: propose-first. Do not patch files until the user explicitly approves.")
    print()

    buckets = ("Skills", "Project AGENTS.md", "Global AGENTS.md")
    by_bucket: dict[str, list[Proposal]] = defaultdict(list)
    for proposal in proposals:
        by_bucket[proposal.bucket].append(proposal)

    for bucket in buckets:
        print(f"## {bucket}")
        print()
        bucket_items = by_bucket.get(bucket, [])
        if not bucket_items:
            print("- No strong proposals found in this sample.")
            print()
            continue

        for proposal in bucket_items[:max_per_bucket]:
            evidence_bits = []
            for item in proposal.evidence[:3]:
                evidence_bits.append(
                    f"{item.thread_id} | {shorten(item.title, 60)} | {to_utc(item.updated_at)} | {item.rollout_path}"
                )
            print(f"- Target: `{proposal.target}`")
            print(f"  Proposal: {proposal.suggestion}")
            print(f"  Support: {proposal.support} thread cluster(s)")
            print(f"  Confidence: {proposal.confidence:.2f}")
            print(f"  Evidence: {' || '.join(evidence_bits)}")
        print()

    if emit_patch and proposals:
        emit_patch_preview(proposals, max_per_bucket=max_per_bucket)


def cmd_dream(args: argparse.Namespace) -> None:
    rows = fetch_threads(
        STATE_DB,
        limit=args.limit,
        archived=args.archived,
        cwd_prefix=args.cwd,
        source_query=None,
        model_query=None,
        text_query=None,
        days=args.days,
        top_level_only=True,
    )
    rows = [row for row in rows if query_matches_thread(row, args.query)]
    proposals = [
        proposal
        for proposal in collect_proposals(rows, min_support=args.min_support)
        if proposal.confidence >= args.min_confidence
    ]
    emit_dream_report(
        rows,
        proposals,
        max_per_bucket=args.max_per_bucket,
        emit_patch=args.emit_patch,
    )


def cmd_skill_audit(args: argparse.Namespace) -> None:
    rows = fetch_threads(
        STATE_DB,
        limit=args.limit,
        archived=args.archived,
        cwd_prefix=None,
        source_query=None,
        model_query=None,
        text_query=None,
        days=args.days,
        top_level_only=True,
    )
    rows = [row for row in rows if query_matches_thread(row, args.query)]
    proposals, selected_skills = collect_skill_audit_proposals(
        rows,
        skill_name=args.skill,
        min_support=args.min_support,
    )
    proposals = [
        proposal
        for proposal in proposals
        if proposal.confidence >= args.min_confidence
    ]
    emit_skill_audit_report(
        rows,
        proposals,
        selected_skills,
        max_per_skill=args.max_per_skill,
        emit_patch=args.emit_patch,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="self_improve.py",
        description="Browse Codex sessions and propose self-improvement edits.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List Codex sessions from state_5.sqlite.")
    list_parser.add_argument("--limit", type=int, default=25)
    list_parser.add_argument("--archived", choices=("active", "archived", "all"), default="active")
    list_parser.add_argument("--cwd")
    list_parser.add_argument("--source")
    list_parser.add_argument("--model")
    list_parser.add_argument("--query")
    list_parser.add_argument("--days", type=int)
    list_parser.add_argument("--top-level-only", action="store_true")
    list_parser.set_defaults(func=cmd_list)

    show_parser = subparsers.add_parser("show", help="Render one thread as a readable transcript.")
    show_parser.add_argument("thread_id")
    show_parser.add_argument("--max-tool-chars", type=int, default=1600)
    show_parser.add_argument("--include-instructions", action="store_true")
    show_parser.set_defaults(func=cmd_show)

    dream_parser = subparsers.add_parser(
        "dream",
        help="Mine user preference signals and emit improvement proposals.",
    )
    dream_parser.add_argument("--limit", type=int, default=250)
    dream_parser.add_argument("--days", type=int, default=365)
    dream_parser.add_argument("--archived", choices=("active", "archived", "all"), default="all")
    dream_parser.add_argument("--cwd")
    dream_parser.add_argument("--query")
    dream_parser.add_argument("--min-support", type=int, default=1)
    dream_parser.add_argument("--min-confidence", type=float, default=0.5)
    dream_parser.add_argument("--max-per-bucket", type=int, default=25)
    dream_parser.add_argument("--emit-patch", action="store_true")
    dream_parser.set_defaults(func=cmd_dream)

    skill_audit_parser = subparsers.add_parser(
        "skill-audit",
        help="Audit installed skills against prior sessions and emit uncovered SKILL.md proposals.",
    )
    skill_audit_parser.add_argument("--skill", help="Audit one skill by name or folder name.")
    skill_audit_parser.add_argument("--limit", type=int, default=500)
    skill_audit_parser.add_argument("--days", type=int, default=365)
    skill_audit_parser.add_argument("--archived", choices=("active", "archived", "all"), default="all")
    skill_audit_parser.add_argument("--query")
    skill_audit_parser.add_argument("--min-support", type=int, default=1)
    skill_audit_parser.add_argument("--min-confidence", type=float, default=0.6)
    skill_audit_parser.add_argument("--max-per-skill", type=int, default=8)
    skill_audit_parser.add_argument("--emit-patch", action="store_true")
    skill_audit_parser.set_defaults(func=cmd_skill_audit)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
