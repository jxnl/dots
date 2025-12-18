# De-Slop

Before a PR, remove obvious AI artifacts and cleanup noise.

## Checklist

- Delete pointless scratch markdown (NOTES/PLAN/IDEAS/TODO) unless it’s real docs
- Remove redundant comments and filler docstrings
- Replace mock-heavy tests with real assertions where possible
- Remove fake/uncited metrics

## Flow

1. Show a dry-run list of issues found (file + line).
2. Ask what to fix (`1 3 4`, `1-5`, `all`, `none`).
3. Apply selected edits and summarize.

Safety: do not delete `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, or `docs/**` without explicit confirmation.
