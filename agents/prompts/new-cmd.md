# New Command

Create a new reusable command/prompt (keep it short and action-oriented).

## Questions

1. Name (file name, kebab-case)?
2. What problem does it solve?
3. Inputs (args)? Output (what should the assistant return/do)?
4. Where should it live?
   - Cursor: `.cursor/commands/` or `~/.cursor/commands/`
   - Codex: `~/.codex/prompts/`
   - Claude: `~/.claude/commands/`

## Template

```md
# Title

One-line description.

## Steps
1. ...
2. ...

## Safety
- ...
```

Finish by testing the command once on a small example and tightening wording.
