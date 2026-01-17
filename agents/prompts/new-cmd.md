# New Command

Create a command from conversation history or user description.

## Steps

1. **Detect context**
   - If history exists: auto-capture workflow into command
   - If no history: parse user's description
   - Use thread context clues to infer name, description, and usage

2. Determine host (Codex, Claude, Cursor) from current runtime
   - Say: "Since I am {host}, I will install it in {host}"

3. Check existing commands for style (host-specific)
```bash
ls ~/.codex/prompts/
ls ~/.claude/commands/
ls ~/.cursor/commands/
```

4. Propose the command name, description, usage, location, and key steps first
   - Proceed unless user rejects or corrects

5. Write command using concise format:
```markdown
# Name

One-line description.

## Steps
1. Step with `bash command`
2. Step with decisions

## Usage
/{name} [args]
```

6. Report created file and usage

## Flags

`--interview`: Ask detailed questions about purpose, triggers, inputs, outputs

## Rules

- Default to capturing conversation if history exists
- Default host to current runtime and install there
- Ask at most one question, only if ambiguity blocks execution
- Infer everything else from context
