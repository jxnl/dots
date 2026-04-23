#!/usr/bin/env python3
"""Audit and optionally clean Codex-created Git worktrees."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import time
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def expand(path: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(path))).resolve()


def git_worktrees(repo: Path) -> list[dict[str, str]]:
    proc = run(["git", "-C", str(repo), "worktree", "list", "--porcelain"], check=True)
    rows: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        if line.startswith("worktree "):
            if current:
                rows.append(current)
            current = {"worktree": line[len("worktree ") :]}
        elif line.startswith("HEAD "):
            current["head"] = line[len("HEAD ") :]
        elif line.startswith("branch "):
            current["branch_ref"] = line[len("branch ") :]
    if current:
        rows.append(current)
    return rows


def short_branch(branch_ref: str | None) -> str:
    return (branch_ref or "").removeprefix("refs/heads/")


def du_kb(path: Path) -> int:
    proc = run(["du", "-sk", str(path)])
    if proc.returncode != 0 or not proc.stdout.strip():
        return 0
    return int(proc.stdout.split()[0])


def dirty_count(path: Path) -> int:
    proc = run(["git", "-C", str(path), "status", "--porcelain"])
    if proc.returncode != 0:
        return -1
    return len([line for line in proc.stdout.splitlines() if line])


def is_recent(path: Path, min_age_hours: float) -> bool:
    if min_age_hours <= 0:
        return False
    cutoff = time.time() - min_age_hours * 3600
    try:
        if path.stat().st_mtime >= cutoff:
            return True
    except OSError:
        return False
    # Check a bounded sample so active sessions are protected without making audits too slow.
    checked = 0
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "target", ".venv"}]
        for name in files[:20]:
            checked += 1
            try:
                if (Path(root) / name).stat().st_mtime >= cutoff:
                    return True
            except OSError:
                pass
            if checked >= 500:
                return False
    return False


def pr_lookup(repo: Path, branch: str) -> list[dict[str, object]]:
    if not branch or shutil.which("gh") is None:
        return []
    proc = run([
        "gh", "-C", str(repo), "pr", "list", "--head", branch,
        "--json", "number,title,url,state,headRefName,baseRefName",
    ])
    if proc.returncode != 0 or not proc.stdout.strip():
        return []
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def backup_dirty(worktree: Path, backup_dir: Path, label: str) -> None:
    backup_dir.mkdir(parents=True, exist_ok=True)
    (backup_dir / f"{label}.status.txt").write_text(run(["git", "-C", str(worktree), "status", "--porcelain"]).stdout)
    (backup_dir / f"{label}.diff").write_text(run(["git", "-C", str(worktree), "diff", "--binary"]).stdout)
    untracked = run(["git", "-C", str(worktree), "ls-files", "--others", "--exclude-standard", "-z"]).stdout
    names = [name for name in untracked.split("\0") if name]
    if names:
        with tarfile.open(backup_dir / f"{label}.untracked.tgz", "w:gz") as tar:
            for name in names:
                path = worktree / name
                if path.exists():
                    tar.add(path, arcname=name)


def move_leftovers(root: Path, audit_dir: Path, apply: bool) -> int:
    leftovers = [p for p in root.iterdir() if p.is_dir()] if root.exists() else []
    with (audit_dir / "leftover-directories.tsv").open("w") as out:
        for p in leftovers:
            out.write(f"{du_kb(p)}\t{p}\n")
    if not apply or not leftovers:
        return len(leftovers)
    trash = Path.home() / ".Trash" / "codex" / dt.datetime.now().strftime("%Y%m%d-%H%M%S-worktrees")
    trash.mkdir(parents=True, exist_ok=True)
    for p in leftovers:
        target = trash / p.name
        if target.exists():
            target = trash / f"{p.name}-{os.getpid()}"
        shutil.move(str(p), str(target))
    return len(leftovers)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="Source Git repository that owns registered worktrees.")
    parser.add_argument("--root", default="~/.codex/worktrees", help="Only consider worktrees under this root.")
    parser.add_argument("--audit-dir", default="~/.codex/worktree-cleanup-audit")
    parser.add_argument("--apply", action="store_true", help="Remove eligible registered worktrees and move leftovers to Trash.")
    parser.add_argument("--include-dirty", action="store_true", help="Remove dirty eligible worktrees after backing them up.")
    parser.add_argument("--force-pr-backed", action="store_true", help="Allow removal of named branch worktrees with open PRs.")
    parser.add_argument("--min-age-hours", type=float, default=24.0, help="Skip worktrees modified more recently than this many hours. Use 0 to disable.")
    args = parser.parse_args()

    repo = expand(args.repo)
    root = expand(args.root)
    audit_dir = expand(args.audit_dir) / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    audit_dir.mkdir(parents=True, exist_ok=True)
    backup_dir = audit_dir / "dirty-backups"

    rows = []
    removed = 0
    skipped = 0
    for meta in git_worktrees(repo):
        wt = expand(meta["worktree"])
        if wt == repo or root not in wt.parents:
            continue
        branch = short_branch(meta.get("branch_ref"))
        prs = pr_lookup(repo, branch) if branch else []
        dirty = dirty_count(wt) if wt.exists() else -1
        size = du_kb(wt) if wt.exists() else 0
        recent = is_recent(wt, args.min_age_hours) if wt.exists() else False
        eligible = (not prs or args.force_pr_backed) and (dirty == 0 or args.include_dirty) and not recent
        reason = "eligible"
        if recent:
            reason = "skip_recent"
        elif prs and not args.force_pr_backed:
            reason = "skip_pr_backed"
        elif dirty > 0 and not args.include_dirty:
            reason = "skip_dirty"
        elif dirty < 0:
            reason = "skip_unreadable"
        rows.append({
            "worktree": str(wt), "size_kb": size, "branch": branch or "detached",
            "dirty_count": dirty, "prs": prs,
            "action": "remove" if args.apply and eligible else "keep", "reason": reason,
        })
        if args.apply and eligible:
            if dirty > 0:
                backup_dirty(wt, backup_dir, wt.parent.name)
            proc = run(["git", "-C", str(repo), "worktree", "remove", "--force", str(wt)])
            if proc.returncode == 0:
                removed += 1
            else:
                skipped += 1
                rows[-1]["action"] = "failed"
                rows[-1]["reason"] = proc.stderr.strip()
        else:
            skipped += 1

    (audit_dir / "worktrees.json").write_text(json.dumps(rows, indent=2))
    with (audit_dir / "worktrees.tsv").open("w") as out:
        out.write("size_kb\tbranch\tdirty_count\tpr_count\taction\treason\tworktree\n")
        for row in sorted(rows, key=lambda r: int(r["size_kb"]), reverse=True):
            out.write(f"{row['size_kb']}\t{row['branch']}\t{row['dirty_count']}\t{len(row['prs'])}\t{row['action']}\t{row['reason']}\t{row['worktree']}\n")

    if args.apply:
        run(["git", "-C", str(repo), "worktree", "prune"])
    leftovers = move_leftovers(root, audit_dir, args.apply)
    total_gb = sum(int(row["size_kb"]) for row in rows) / 1024 / 1024
    print(f"audit_dir={audit_dir}")
    print(f"registered_under_root={len(rows)} size={total_gb:.1f}G removed={removed} skipped={skipped}")
    print(f"leftover_dirs={leftovers} {'moved_to_trash' if args.apply else 'audited_only'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
