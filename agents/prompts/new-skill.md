# New Skill

Create a skill from conversation history or user description.

## Steps

1. **Detect context**
   - If history exists: auto-capture workflow into skill
   - If no history: parse user's description

2. **Ask 3 questions:**
   - "Codex or Claude skill?"
   - "What tools/scripts should this create?" (CLI, python script, shell script, none)
   - "What libraries/CLIs can it use?" (e.g., uv, bun, gh, jq, ffmpeg)

3. Check existing skills for patterns
```bash
ls ~/.codex/skills/
ls agents/skills/
```

4. Create skill structure:
```
{skill-name}/
  SKILL.md
  resources/         # references, samples, templates
  scripts/           # if tools requested
    run.py|ts|sh
```

5. Write SKILL.md:
```markdown
---
name: skill-name
description: one-line
allowed_tools: [list from question 3]
---

# Skill Name

## When to use
- trigger conditions

## Steps
1. ...
2. ...

## Tools created
- scripts/run.py: what it does
```

6. Report created files

## Flags

`--interview`: Ask detailed questions (purpose, triggers, inputs, outputs, edge cases)

## Script Templates

**Python (uv):**
```python
def main() -> int:
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

**TypeScript (bun):**
```typescript
console.log("ok");
```

**Shell:**
```bash
#!/usr/bin/env bash
set -euo pipefail
echo "ok"
```

## Rules

- Default to capturing conversation if history exists
- Ask 3 questions, infer everything else
- Only create scripts if requested
- Match existing skill patterns in repo
