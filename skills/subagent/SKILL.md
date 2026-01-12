---
name: subagent
description: Delegate codebase exploration or scripted actions to a non-interactive Codex exec run (codex exec / codex e). Use when you want a subagent to read lots of code or take actions without human interaction, and you can accept CLI output and optional file changes as the result.
---

# Subagent

## When to use
- Delegate large codebase reading, searching, or multi-step actions to a non-interactive exec run.
- Offload scripted or CI-style tasks that should finish without questions.

## Inputs / outputs
- Inputs: a prompt string; optional flags such as `--cd`, `--model`, `--json`, or `--full-auto`.
- Outputs: CLI output from the exec run; possible file edits in the target repo.

## Prompt template
Use a structured prompt to keep exec runs focused:

```
Goal:
Scope/paths:
Constraints:
Deliverables:
Context:
```

## Steps
1. Decide the task and repo root; include constraints and expected deliverables in the prompt.
2. Choose a model using `resources/references/codex-exec.md` heuristics.
3. Prefer resuming when the follow-up builds on the same context (e.g., providers after a repo overview, reviewing verbose test output, or continuing a multi-step investigation). Use `codex exec resume <SESSION_ID> "<prompt>"`.
4. Start a new run when the task changes repos, needs a clean context, or should branch into a separate thread (e.g., exploring three unrelated areas in parallel).
5. Run `codex exec` directly with flags; attach images with `-i/--image` when needed. Use `--skip-git-repo-check` when running outside a Git repo.
6. Wait for completion; review output and any file changes.
7. If the task references a plan directory, update `learnings.md` in that plan directory with key findings and decisions.

## Result checklist
- Did it identify the right files and entry points?
- Are key decisions and rationale explicit?
- Are edits (if any) listed clearly?
- Are tests or verification steps noted?

## Session tracking
- Always copy the exec `session id` into the main thread for resuming.

## Safety
- Avoid `--yolo` unless inside an isolated runner.
- Prefer `--full-auto` or explicit sandbox settings when you need workspace changes.
- Keep prompts specific about allowed paths and operations.

## Resources
- `resources/references/codex-exec.md` includes flags, model selection, and code-reading guidance.
