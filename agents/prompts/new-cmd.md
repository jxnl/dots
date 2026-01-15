# New Command

Create a new command from user's description. No interview - just build it.

## Steps

1. Parse request - extract name (kebab-case, gh- prefix for GitHub), purpose, args
2. Check existing commands for style
```bash
ls ~/.claude/commands/
ls ~/.codex/prompts/
```
3. Write to `~/.claude/commands/{name}.md` using concise format:
```markdown
# Name

One-line description.

## Steps
1. Step with `bash command`
2. Step with decisions

## Usage
/{name} [args]
```
4. Ask: "Claude, Codex, or both?" then install to chosen location(s)
5. Report created files and usage

## Rules

- Ask once: "Claude, Codex, or both?"
- No other questions unless truly ambiguous
- Infer intent from context
- Start minimal, iterate later
