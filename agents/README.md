# Agents Configuration

General assistant setup (Claude Code, Codex CLI, and other tools) with shared prompts and global rules.

## Structure

```
agents/
├── AGENTS.md              # General instructions (Codex-style)
├── prompts/               # Reusable prompts / slash commands (tool-agnostic)
└── claude/
    ├── settings.json      # Claude Code settings
    └── agents/            # Claude background agents
```

## Installation

Run from the repo root (`dots/`):

```bash
./install.sh --agents
```

### What `--agents` installs

`./install.sh --agents` installs the shared prompts into all supported tools (Claude Code + Codex CLI + Cursor), plus Claude-only subagents.

### Claude Code (Anthropic)

Installs:
- `~/.claude/CLAUDE.md` (copied from `agents/AGENTS.md`)
- `~/.claude/settings.json`
- `~/.claude/commands/*.md` (copied from `agents/prompts/`)
- `~/.claude/agents/*.md` (Claude-only subagents)

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
./install.sh --list-claude-agents
```

Install only specific prompts (works for `--claude`, `--openai`, `--cursor`, `--cursor-project`, and `--agents`):
```bash
./install.sh --openai --only-prompts gh-commit,make-tests
./install.sh --cursor --prompt gh-review-pr --prompt gh-fix-ci
```

Install only specific Claude subagents (Claude-only):
```bash
./install.sh --claude --claude-agent test-runner
./install.sh --claude --claude-agent youtube --claude-agent test-runner
```
