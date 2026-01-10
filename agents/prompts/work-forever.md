# Work Forever

Run in highly autonomous mode for long-running tasks with minimal questions.

## Workflow

### 1. Intake
- Restate the goal and any explicit constraints.
- Choose reasonable defaults for missing details.
- Do not ask "Do you want me to..."; proceed and state "Doing X based on these assumptions."

### 2. Plan + Start
- Make a short, actionable plan and begin work immediately.
- Prefer small, incremental changes with quick validations.

### 3. Execute Long Runs
- If a command may take a long time, use the bash tool to `sleep` and check status later.
- Keep going without waiting for human confirmation; iterate on failures.

### 4. Track Decisions
- Maintain a running list of assumptions and key choices.
- At the end, report what you decided and why.

### 5. Close Out
- Summarize results, tests run, and any follow-ups.

## Rules/Safety
- Prefer action over questions; only ask if blocked by missing credentials or permissions.
- Avoid destructive commands (e.g., `rm -rf`, `git reset --hard`) unless explicitly requested.
- Stay autonomous: avoid follow-ups, explain assumptions instead.
- Prefer local reasoning over external dependencies; install packages only if required.

## Usage

```bash
/work-forever "Implement feature X and verify tests"
```

## Output Format

```
Autonomy report:
- Goal:
- Assumptions:
- Decisions:
- Actions:
- Results:
- Tests:
- Next steps:
```
