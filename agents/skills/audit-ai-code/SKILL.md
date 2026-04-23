---
name: audit-ai-code
description: Audit AI-generated or AI-shaped backend/general code diffs for duplicate helpers, over-defensive control flow, broad exception wrappers, speculative scaffolding, comment/docstring boilerplate, local style drift, hallucinated APIs/dependencies, fixture-shaped test hacks, and obvious safety/performance gaps. Use when reviewing or safely cleaning up Python, TypeScript, or other implementation code after a feature, bugfix, or prototype pass.
---

# AI Code Audit

## Use

Audit or repair implementation code that reads generically AI-generated, while preserving behavior, public APIs, and tests unless the user explicitly asks for a refactor.

Review in this order:

1. Find the target scope.
   - Prefer `git diff --check` and `git diff --stat` first.
   - Inspect the current diff for touched files; if there is no git diff, fall back to recently modified files.
   - Ask one narrow question if scope is genuinely ambiguous.

2. Collapse duplicate helpers and shadow APIs.
   - Find helpers or wrappers that do the same job with slightly different names, signatures, or one-off branches.
   - Prefer one canonical helper with a narrow, clear API.
   - Replace hand-rolled parsing, path, date/time, and string logic with existing project utilities when they already exist.
   - Verify any newly introduced helper, method, import, or package is real and canonical in this repo or dependency graph.

3. Flatten defensive control flow and exception boundaries.
   - Replace nested condition ladders with guard clauses and early exits.
   - Consolidate checks that lead to the same result and hoist duplicate branch bodies.
   - Remove stateful control flags when direct control flow is clearer.
   - Delete broad exception wrappers that hide uncertainty, keep one clear handler around real boundary failures, and replace expected non-exceptional cases with explicit precondition checks.

4. Remove generated-code residue.
   - Delete speculative abstractions, factories, generic hooks, pass-through wrappers, broad options objects, dead branches, and placeholder fallbacks that have no concrete caller or product need.
   - Remove comments/docstrings that restate obvious code; keep only non-obvious intent, invariants, and tradeoffs.
   - Normalize naming, module boundaries, error style, and helper shape to match adjacent hand-written code.
   - Treat fixture-shaped branches, magic constants, and deleted or weakened tests as a smell; encode the actual invariant instead.

5. Check safety and runtime basics.
   - Look for secrets in code/config, string-built queries or shell commands, path traversal, unsafe deserialization, SSRF-shaped fetches, missing server-side authorization, sensitive data in logs, swallowed exceptions, unchecked return values, missing outbound timeouts, and check-then-act races.
   - Patch only high-confidence local fixes; report broader security or architecture changes as follow-up.

6. Verify.
   - Run the narrowest relevant tests, typechecks, and linters for touched files.
   - Re-open the diff and confirm cleanup did not change intended behavior.

For larger diffs, parallelize read-only review into up to four passes: reuse/shadow APIs, control-flow/exception boundaries, generated-code residue, and quality/safety/performance. Prefer a stronger model for ambiguous tradeoffs and a smaller model for narrow, easy-to-verify scans.

## Output

For each finding, include:

- `Issue`
- `Evidence`
- `Class` (`P0`, `P1`, `P2`)
- `Why it matters / why it reads as generated`
- `Possible non-AI explanation`
- `Smallest fix`
- `Acceptance check`
- `Confidence` (`High`, `Medium`, `Low`)
- `File/line`

Return only the top 5-8 findings for review-only asks and merge repeated symptoms under one root cause.

For implementation asks, patch the code directly, then summarize what was simplified, what was intentionally left alone, what validation ran, and any follow-up risks.

## Guardrails

- Treat "AI-looking" as a quality smell, not a provenance claim.
- Prefer objective maintainability, correctness, and safety defects over style-only opinions.
- Do not widen APIs into mega-helpers, config bags, or boolean-flag mode switches just to reduce line count.
- Do not add speculative abstraction layers, broad framework wrappers, or one-off utility namespaces.
- Do not reformat unrelated files or chase broad style churn.

## Resource

- `references/sources.md`: source basis for code-smell, AI-generated-code, and security-review checks.
