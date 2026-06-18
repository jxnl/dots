---
name: audit-ai-code
description: Audit, de-slop, parameterize, modularize, or safely clean up AI-generated or AI-shaped backend/general code. Use for Python, TypeScript, or other implementation diffs that may contain duplicate helpers, fixture hacks, hard-coded test data, over-defensive control flow, broad exception wrappers, config-bag or boolean-mode soup, speculative scaffolding, hallucinated APIs/dependencies, local-idiom drift, brittle tests, or maintainability/safety/performance gaps after a feature, bugfix, prototype, or agent pass.
---

# AI Code Audit

## Use

Audit or repair implementation code that reads generically AI-generated, overfit, or hard to maintain. Preserve behavior, public APIs, and tests unless the user explicitly asks for a refactor.

Review in this order:

1. Find the target scope.
   - Prefer `git diff --check` and `git diff --stat` first.
   - Inspect the current diff for touched files; if there is no git diff, fall back to recently modified files.
   - Ask one narrow question if scope is genuinely ambiguous.

2. Establish the local idiom.
   - Read adjacent handwritten code before judging style.
   - Identify existing patterns for module boundaries, configuration, validation, errors, logging, tests, naming, and helper placement.
   - Prefer the repo's established utilities, dependency injection style, and data shapes over new local conventions.
   - Treat local consistency as evidence; do not impose generic "clean code" rules that fight the codebase.

3. Collapse duplicate helpers and shadow APIs.
   - Find helpers or wrappers that do the same job with slightly different names, signatures, or one-off branches.
   - Prefer one canonical helper with a narrow, intention-revealing API.
   - Replace hand-rolled parsing, path, date/time, and string logic with existing project utilities when they already exist.
   - Verify any newly introduced helper, method, import, or package is real and canonical in this repo or dependency graph.

4. Improve parameterization and modularity.
   - Parameterize repeated literals, fixture-specific values, environment assumptions, and duplicated branches only when doing so clarifies a real variation point.
   - Keep cohesion high: move behavior to the module or type that already owns the concept; avoid shared utility bins.
   - Keep coupling low: pass the smallest stable domain object or explicit value needed, not unrelated context, global state, or sprawling option maps.
   - Replace boolean mode arguments with explicit methods, named strategies, or derived decisions when callers need different behaviors.
   - Use parameter objects only for cohesive data that changes together; do not turn them into config bags.
   - Preserve typed, explicit interfaces; do not make code more dynamic or generic just to reduce lines.

5. Flatten defensive control flow and exception boundaries.
   - Replace nested condition ladders with guard clauses and early exits.
   - Consolidate checks that lead to the same result and hoist duplicate branch bodies.
   - Remove stateful control flags when direct control flow is clearer.
   - Delete broad exception wrappers that hide uncertainty, keep one clear handler around real boundary failures, and replace expected non-exceptional cases with explicit precondition checks.

6. Remove generated-code residue.
   - Delete speculative abstractions, factories, generic hooks, pass-through wrappers, broad options objects, dead branches, and placeholder fallbacks that have no concrete caller or product need.
   - Remove comments/docstrings that restate obvious code; keep only non-obvious intent, invariants, and tradeoffs.
   - Normalize naming, module boundaries, error style, and helper shape to match adjacent hand-written code.
   - Treat fixture-shaped branches, magic constants, and deleted or weakened tests as a smell; encode the actual behavior or invariant instead.

7. Check tests for behavior focus.
   - Prefer tests named and structured around behavior, not a 1:1 mirror of implementation methods.
   - Remove branches that special-case fixture names, timestamps, ids, or canned responses in production code.
   - Replace snapshot-only or mock-call-only assertions with observable behavior when practical.
   - Keep test helpers parameterized around meaningful scenarios, not hidden setup that makes failures hard to read.

8. Check safety and runtime basics.
   - Look for secrets in code/config, string-built queries or shell commands, path traversal, unsafe deserialization, SSRF-shaped fetches, missing server-side authorization, sensitive data in logs, swallowed exceptions, unchecked return values, missing outbound timeouts, and check-then-act races.
   - Verify generated imports, packages, APIs, permissions, and defaults against project docs, lockfiles, or official sources before trusting them.
   - Patch only high-confidence local fixes; report broader security, dependency, or architecture changes as follow-up.

9. Verify.
   - Run the narrowest relevant tests, typechecks, and linters for touched files.
   - Re-open the diff and confirm cleanup did not change intended behavior.

For larger diffs, parallelize read-only review into up to four passes: local idiom/reuse, cohesion/API shape, control-flow/exception boundaries, and behavior tests/safety/performance. Prefer a stronger model for ambiguous tradeoffs and a smaller model for narrow, easy-to-verify scans.

## Output

For each finding, include:

- `Issue`
- `Evidence`
- `Class` (`P0`, `P1`, `P2`)
- `Why it matters`
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
- Prefer parameterized, modular, locally idiomatic code when it reduces real duplication or clarifies ownership.
- Do not widen APIs into mega-helpers, config bags, boolean-flag modes, or generic parameter soup just to reduce line count.
- Do not add speculative abstraction layers, broad framework wrappers, or one-off utility namespaces.
- Do not reformat unrelated files or chase broad style churn.

## Resource

- `references/sources.md`: source basis for code-smell, AI-generated-code, API-shape, test-focus, and security-review checks.
