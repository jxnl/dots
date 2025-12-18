# New Skill

Create a new skill folder with `SKILL.md`, `resources/`, and `scripts/`.

## First: decide skill system + location (ask before writing files)

Use context clues (repo layout, `AGENTS.md`, existing `~/.codex/skills`, any Claude skills/plugin repo) to guess, then ask:

1. Skill system: **Codex** skill (`~/.codex/skills/**/SKILL.md`) or **Claude** skill (repo `skills/<name>/SKILL.md`)?
2. Location: **global** or **project-local**?
3. Skill name (kebab-case). If user gives spaces, sanitize.
4. Description (one line, <=500 chars).

## Then: scaffold

Create:
- `SKILL.md`
- `resources/` (for references, docs, samples)
- `scripts/` (for runnable helpers)

Ask what they want in `resources/` and `scripts/`:
1. `resources/` contents: `README.md` only, or also `references/` with starter `references/example.md`?
2. `scripts/` languages:
   - Shell (`scripts/run.sh`)
   - Python (uv) (`scripts/run.py`)
   - TypeScript (bun) (`scripts/run.ts` + `bun.lockb` ignored if present)

Make a concrete proposal (paths + files) and confirm once before writing.

## File templates

`SKILL.md`:
```md
---
name: <skill-name>
description: <one-line description>
---

# <Skill Name>

## When to use
- ...

## Inputs / outputs
- Inputs: ...
- Outputs: ...

## Steps
1. ...
2. ...

## Safety
- ...
```

`scripts/run.py` (uv):
```py
def main() -> int:
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

`scripts/run.ts` (bun):
```ts
console.log("ok");
```

`scripts/run.sh`:
```sh
#!/usr/bin/env bash
set -euo pipefail
echo "ok"
```

