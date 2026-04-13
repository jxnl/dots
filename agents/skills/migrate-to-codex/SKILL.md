---
name: migrate_to_codex
description: Migrate supported instruction files, skills, agents, and MCP config into Codex project and global files.
---

# Migrate to Codex

## Autonomy

Keep going until the selected migration is completely done: run the migrator, inspect the report, fix migrated Codex instructions/skills/agents/MCP config, and re-run checks without stopping to ask for confirmation of the next step. If the user has selected a target, do not ask before creating, editing, replacing, or deleting generated Codex artifacts in that target (`AGENTS.md`, `.codex/`, `.agents/`, or `~/.codex/`). Still ask before changing source provider files (`.claude/`, `~/.claude/`, `.opencode/`, and similar), unrelated project code, secrets, or another repository.

## Steps

1. Read `references/differences.md` (and refresh Codex docs if its `Docs last checked` date is old).

2. Dry-run, then run without `--dry-run`, for global and project. Use `--replace` to drop orphan generated skills or agents.

   ```bash
   python3 .codex/skills/migrate-to-codex/scripts/migrate-to-codex.py --source ~/.claude/ --target ~/.codex/ --dry-run
   python3 .codex/skills/migrate-to-codex/scripts/migrate-to-codex.py --source ~/.claude/ --target ~/.codex/
   python3 .codex/skills/migrate-to-codex/scripts/migrate-to-codex.py --source ./.claude/ --target ./.codex/ --dry-run
   python3 .codex/skills/migrate-to-codex/scripts/migrate-to-codex.py --source ./.claude/ --target ./.codex/
   ```

3. Read the terminal output and `.codex/migrate-to-codex-report.txt` (on real runs). Fix every `manual_fix_required` and `skipped` row; start with `## MANUAL MIGRATION REQUIRED` in files.

4. Review in order: `AGENTS.md`, skills, MCP, subagents.

5. Re-run checks and `--dry-run` after edits. Ask the user about other repos that still need migration.

Run `python3 .codex/skills/migrate-to-codex/scripts/migrate-to-codex.py --help` for flags (`--scan-only`, defaults, and so on). Deep tables and more links are in `references/differences.md`.
