# New Skill

Create a new skill folder with `SKILL.md`, `resources/`, and `scripts/`.

## Start by interviewing the user (ask before writing files)

This command is an interview. Optimize for clarity and reusability.

First, determine whether the user wants:
- **(A) New skill from scratch**, or
- **(B) “Capture what we just did”**: summarize the current thread/work into a reusable skill.

Ask:
1. “What are you trying to accomplish with this skill?” (1–2 sentences)
2. “Who is it for and when should it be used?” (trigger conditions)
3. “What are the inputs and outputs?” (files, URLs, CLI args, artifacts)
4. “What should the skill do step-by-step?” (happy path)
5. “What can go wrong?” (constraints, safety, edge cases)

If the user says (B), ask:
- “Which part of our work should become the skill?” (link to repo area / recap)
- “What should be standardized vs left flexible?”
- “What are the exact commands/scripts you want to keep?”

## Decide skill system + location (make an educated guess, then confirm)

Use context clues (repo layout, `AGENTS.md`, existing `~/.codex/skills`, any Claude skills/plugin repo) to guess, then ask for confirmation:

1. Skill system: **Codex** skill (`~/.codex/skills/**/SKILL.md`) or **Claude** skill (repo `skills/<name>/SKILL.md`)?
2. Location: **global** or **project-local**?
3. Skill name (kebab-case). If user gives spaces, sanitize.
4. Description (one line, <=500 chars).

## Propose scripts + resources (make suggestions, then confirm)

Based on the interview, your job is to make a concrete recommendation for:
- tool/runtime choices (shell vs uv Python vs bun TypeScript)
- what to put in `scripts/`
- what to put in `resources/` + `resources/references/`

First, present a short recommendation (then confirm). Keep it specific and tied to the user’s goal.

**Good candidates for `scripts/`:**
- Shell: glue + reproducible CLI sequences, git/gh workflows, simple automation
- Python (uv): data transforms, scraping/parsing, small utilities, reproducible runs
- TypeScript (bun): API calls, JSON manipulation, quick CLIs, web tooling

Ask targeted questions:
1. “Do you want runnable scripts, or just instructions?”
2. “Which runtime(s) should we assume?” (uv Python / bun TS / shell)
3. “Should scripts be single-file entrypoints (`run.py`, `run.ts`, `run.sh`) or multiple modules?”
4. “Do scripts need external deps?” If yes, ask where to document them (e.g. `resources/README.md`).

**Good candidates for `resources/`:**
- `references/` (APIs, docs links, conventions, style/brand guides)
- `samples/` (example inputs/outputs)
- `templates/` (boilerplate docs, PR templates, message templates)
- `checklists.md` (QA steps, release steps)

Make a concrete proposal (paths + files + 1-line purpose each) and confirm once.

## Recommendation format (use this structure)

Before writing files, output a recommendation like:

```
Recommendation
- Skill system: Codex | Claude
- Location: global | project-local
- Name: ...
- Scripts: shell | uv python | bun ts (why)
- Files to create:
  - SKILL.md (purpose)
  - resources/README.md (what’s in here)
  - resources/references/README.md (links + conventions)
  - resources/samples/... (optional)
  - scripts/run.(sh|py|ts) (what it does)
```

Then ask: “Confirm this plan? (yes/no)”. Only write files after yes.

## Scaffold (after confirmation)

Create:
- `SKILL.md`
- `resources/` (for references, docs, samples)
- `scripts/` (for runnable helpers)

Default layout (adjust based on answers):
```
<skill-root>/
  SKILL.md
  resources/
    README.md
    references/
      README.md
  scripts/
    run.sh
    run.py
    run.ts
```

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
