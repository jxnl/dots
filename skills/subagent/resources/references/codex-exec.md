# Codex exec guide

Use `codex exec` (or `codex e`) for non-interactive runs.

## Codex CLI features (context)
Interactive mode:
- `codex` launches the full-screen UI for conversational workflows.
- `codex "Explain this codebase to me"` starts with an initial prompt.
- Use `/exit` or Ctrl+C to close.

Resume sessions:
- `codex resume` opens the picker for interactive sessions.
- `codex resume --all` shows sessions across directories.
- `codex resume --last` jumps to the most recent session.
- `codex resume <SESSION_ID>` targets a specific run.
- `codex exec resume --last "<prompt>"` resumes a non-interactive run.
- `codex exec resume <SESSION_ID> "<prompt>"` resumes by ID.
- Use `--cd` or `--add-dir` when resuming to adjust roots.

Models and reasoning:
- Default model is `gpt-5-codex` on macOS/Linux and `gpt-5` on Windows.
- Switch mid-session with `/model` or specify on launch: `codex --model <name>`.

Image inputs:
- `codex -i screenshot.png "Explain this error"`
- `codex --image img1.png,img2.jpg "Summarize these diagrams"`

## Common flags
- `--cd PATH` set workspace root for the run
- `--json` output newline-delimited JSON events
- `--model NAME` override model
- `--full-auto` use low-friction automation preset
- `--sandbox read-only|workspace-write|danger-full-access` set sandbox
- `--output-last-message PATH` write final message to a file
- `--skip-git-repo-check` allow running outside a Git repo
- `resume <SESSION_ID>` continue a prior exec session

Avoid `--yolo` unless running in an isolated runner.

## Model selection (gpt-5.2-codex family)
Available models:
- `gpt-5.2-codex-low`
- `gpt-5.2-codex-med`
- `gpt-5.2-codex-high`
- `gpt-5.2-codex-xhigh-fast`

Heuristics:
- Low: fast repo scanning, simple summaries, single-file lookup.
- Med: multi-file reading, straightforward edits, light refactors.
- High: complex reasoning, tricky bugs, broader changes.
- Xhigh-fast: highest difficulty or ambiguous work; use when others fail.

If the task is mostly IO (searching/listing), prefer low or med with a compact prompt.
If the task requires deep reasoning, prefer high or xhigh-fast and include more context.

## Code reading workflow
Start with discovery:
- `rg --files` to get a quick file list.
- `rg -n \"<keyword>\" -S` to find relevant locations.
- Read `AGENTS.md`/`CLAUDE.md`/`README.md` if present.

Minimize context bloat:
- Open only the files needed for the current step.
- Prefer small, targeted excerpts over whole files.
- Summarize long files instead of copying them wholesale.

When asked to change code:
- Locate the narrowest owning module.
- Trace call sites before editing.
- Note any tests or scripts affected.
