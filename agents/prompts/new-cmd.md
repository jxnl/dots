# New Command

Create a command from conversation history or user description.

## Steps

1. **Detect context**
   - If history exists: auto-capture workflow into command
   - If no history: parse user's description

2. Check existing commands for style
```bash
ls ~/.claude/commands/
ls ~/.codex/prompts/
```

3. Ask: "Claude, Codex, or both?"

4. Write command using concise format:
```markdown
# Name

One-line description.

## Steps
1. Step with `bash command`
2. Step with decisions

## Usage
/{name} [args]
```

5. Report created file and usage

## Flags

`--interview`: Ask detailed questions about purpose, triggers, inputs, outputs

## Rules

- Default to capturing conversation if history exists
- Ask one question: "Claude, Codex, or both?"
- Infer everything else from context
