from __future__ import annotations

from collections.abc import Callable
from pathlib import Path


INSTRUCTION_SOURCE_CANDIDATES = (
    Path(".claude") / "CLAUDE.md",
    Path("CLAUDE.md"),
    Path("claude.md"),
    Path("AGENTS.md"),
    Path("agents.md"),
    Path("AGENT.md"),
    Path("agent.md"),
    Path(".agents.md"),
    Path(".agents") / "AGENTS.md",
    Path(".agents") / "agents.md",
    Path("GEMINI.md"),
    Path("gemini.md"),
    Path(".config") / "opencode" / "AGENTS.md",
    Path(".pi") / "agent" / "AGENTS.md",
    Path("CURSOR.md"),
    Path(".cursorrules"),
    Path("AIDER.md"),
)

CLAUDE_ONLY_INSTRUCTION_MARKERS = (
    "/hooks",
    ".claude/agents/",
    ".claude/settings",
    "Subagent",
    "subagent",
    "permissionMode",
    "ExitPlanMode",
)


def instruction_source_file(
    source_root: Path,
    is_global: bool,
    path_exists_with_exact_case: Callable[[Path], bool],
) -> Path | None:
    candidates = INSTRUCTION_SOURCE_CANDIDATES
    if not is_global:
        candidates = tuple(
            candidate
            for candidate in candidates
            if candidate != Path(".claude") / "CLAUDE.md"
        )

    for candidate in candidates:
        source_file = source_root / candidate
        if path_exists_with_exact_case(source_file):
            return source_file
    return None


def should_symlink_instructions(content: str) -> bool:
    return not any(marker in content for marker in CLAUDE_ONLY_INSTRUCTION_MARKERS)
