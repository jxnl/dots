# New Command

Create a new reusable command/prompt by interviewing the user first, then writing the smallest useful version.

## Interview (ask before writing files)

Start by asking:
1. “What are you trying to accomplish with this command?” (1–2 sentences)
2. “When should someone use it?” (trigger + success criteria)
3. “What inputs does it take?” (positional args? named args? files?)
4. “What should the output look like?” (format + what to include/omit)
5. “Any safety rules?” (no destructive ops, confirm before write, etc.)

If this command is meant to codify the current thread, ask:
- “Which workflow should we capture from what we just did?”
- “What should be standardized vs left flexible?”

## Decide where it lives (guess, then confirm)

Use context clues (repo type, existing directories, user mentions) to guess, then ask:
1. Cursor: `.cursor/commands/` (project) or `~/.cursor/commands/` (global)
2. Codex prompts: `~/.codex/prompts/`
3. Claude: `~/.claude/commands/`

Also confirm:
- File name (kebab-case, no spaces)
- One-line description

## Propose a minimal command outline (confirm once)

Suggest the smallest set of steps that solve the problem, plus safety. Confirm before writing the file.

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
