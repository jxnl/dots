---
name: clean-worktrees
description: Audit and clean Codex-created Git worktrees and leftover worktree directories safely. Use when disk usage appears inflated by ~/.codex/worktrees, Git worktree metadata, detached Codex worktrees, stale branch worktrees, or when the user asks to map worktrees to pull requests before deletion.
---

# Clean Worktrees

Use this skill when `~/.codex/worktrees` or repository `.git/worktrees` directories are large, or when the user asks which worktrees are safe to remove.

## Workflow

1. Measure disk first:
   ```bash
   df -h / /System/Volumes/Data
   du -sh ~/.codex ~/.codex/worktrees 2>/dev/null
   ```

2. Audit before cleanup. Prefer the bundled script:
   ```bash
   python3 ~/.codex/skills/clean-worktrees/scripts/clean_worktrees.py \
     --repo ~/path/to/repo \
     --root ~/.codex/worktrees \
     --audit-dir ~/.codex/worktree-cleanup-audit \
     --min-age-hours 24
   ```

3. Interpret risk:
   - **Clean detached Codex worktrees**: safest to remove.
   - **Dirty detached Codex worktrees**: back up status, diff, and untracked files before removal.
   - **Named branch worktrees without an open PR**: usually safe after checking dirty status.
   - **Named branch worktrees with an open PR**: keep unless the user explicitly asks to remove them.
   - **Main checkout or non-Codex path**: never remove as part of automatic cleanup.

4. Apply cleanup only after the audit result is clear:
   ```bash
   python3 ~/.codex/skills/clean-worktrees/scripts/clean_worktrees.py \
     --repo ~/path/to/repo \
     --root ~/.codex/worktrees \
     --audit-dir ~/.codex/worktree-cleanup-audit \
     --apply \
     --include-dirty \
     --min-age-hours 24
   ```

5. Prune repository metadata after removals:
   ```bash
   git -C ~/path/to/repo worktree prune
   ```

6. Verify:
   ```bash
   git -C ~/path/to/repo worktree list --porcelain
   du -sh ~/.codex ~/.codex/worktrees 2>/dev/null
   df -h / /System/Volumes/Data
   ```

## Pull Request Mapping

For named branch worktrees, map branches to PRs before deletion:

```bash
gh -C <repo> pr list --head <branch> --json number,title,url,state,headRefName,baseRefName
```

Detached worktrees do not map cleanly to PRs by branch. Treat them as not PR-backed unless the worktree has a named branch or a remote branch can be inferred from local metadata.

## Safety Rules

- Default to audit-only.
- Do not delete by raw `rm` or `rm -rf`.
- Save audit artifacts under a dedicated audit directory, such as `~/.codex/worktree-cleanup-audit`.
- For dirty worktrees, save:
  - `git status --porcelain`
  - `git diff --binary`
  - an archive of untracked files
- Skip worktrees modified within the configured age window, default `24` hours, to avoid deleting active sessions.
- Skip PR-backed branches unless the user explicitly says to delete them.
- Use Git's own `worktree remove --force` for registered worktrees.
- Move unregistered leftover directories to `~/.Trash/codex/<timestamp>/` instead of deleting them directly.
