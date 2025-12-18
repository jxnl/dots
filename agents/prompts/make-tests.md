# Make Tests

Add tests for the change you’re working on.

## Steps

1. Identify the code under test
```bash
git diff --name-only
```

2. Propose 3–6 tests (happy path + edge + error/regression). Confirm priorities.

3. Write tests following existing patterns (no excessive mocking).

4. Run the smallest relevant test command (then the full suite if needed).

5. Summarize what’s covered and what’s not.
