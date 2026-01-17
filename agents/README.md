# Agents Configuration

General assistant setup (Claude Code, Codex CLI, and other tools) with shared prompts and global rules.

## Structure

```
agents/
├── AGENTS.md              # General instructions (Codex-style)
└── prompts/               # Reusable prompts / slash commands (tool-agnostic)
└── skills/                # Codex skills for ~/.codex/skills
```

## Installation

Run from the repo root (`dots/`) or inside `agents/`:

```bash
./agents/install.sh
```

### What `--agents` installs

`./agents/install.sh` (or `./install.sh --agents`) installs shared prompts into all supported tools (Claude Code + Codex CLI + Cursor) and installs Codex skills.

### Claude Code (Anthropic)

Installs:
- `~/.claude/CLAUDE.md` (copied from `agents/AGENTS.md`)
- `~/.claude/commands/*.md` (copied from `agents/prompts/`)

### OpenAI Developers (Codex CLI)

Installs:
- `~/.codex/prompts/*.md` (copied from `agents/prompts/`)
- `~/.codex/skills/*` (copied from `agents/skills/`)

Skills inventory:
- `agents/skills/README.md`

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
./agents/install.sh --openai
./agents/install.sh --cursor
./agents/install.sh --cursor-project
```

Install only Codex skills:
```bash
./agents/install.sh --skills
```

List what you can install:
```bash
./agents/install.sh --list-prompts
```

Install only specific prompts (works for `--claude`, `--openai`, `--cursor`, `--cursor-project`, and `--agents`):
```bash
./agents/install.sh --openai --only-prompts gh-commit,make-tests
./agents/install.sh --cursor --prompt gh-review-pr --prompt gh-fix-ci
./agents/install.sh --agents --prompt new-skill
```
