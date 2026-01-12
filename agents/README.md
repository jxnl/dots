# Agents Configuration

General assistant setup (Claude Code, Codex CLI, and other tools) with shared prompts and global rules.

## Structure

```
agents/
├── AGENTS.md              # General instructions (Codex-style)
└── prompts/               # Reusable prompts / slash commands (tool-agnostic)
```

## Installation

Run from the repo root (`dots/`):

```bash
./install.sh --agents
```

### What `--agents` installs

`./install.sh --agents` installs the shared prompts into all supported tools (Claude Code + Codex CLI + Cursor).

### Claude Code (Anthropic)

Installs:
- `~/.claude/CLAUDE.md` (copied from `agents/AGENTS.md`)
- `~/.claude/commands/*.md` (copied from `agents/prompts/`)

### OpenAI Developers (Codex CLI)

Installs:
- `~/.codex/prompts/*.md` (copied from `agents/prompts/`)

### Cursor

Installs:
- `~/.cursor/commands/*.md` (copied from `agents/prompts/`)

Optional (project-local):
- `.cursor/commands/*.md` (copied from `agents/prompts/`)

---

## Common Install Recipes

Install everything (vim + bash + tmux + all agent config):
```bash
./install.sh
```

Install only prompts for a specific tool:
```bash
./install.sh --claude
./install.sh --openai
./install.sh --cursor
./install.sh --cursor-project
```

List what you can install:
```bash
./install.sh --list-prompts
```

Install only specific prompts (works for `--claude`, `--openai`, `--cursor`, `--cursor-project`, and `--agents`):
```bash
./install.sh --openai --only-prompts gh-commit,make-tests
./install.sh --cursor --prompt gh-review-pr --prompt gh-fix-ci
./install.sh --agents --prompt new-skill
```
