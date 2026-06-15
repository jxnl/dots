---
name: ultragoal
description: Research, design, critique, or activate a Codex goal for long-running work, including verifiers, durable goal files, review pressure, and bounded parent/child goal delegation.
---

# Ultragoal

Turn a promising but underspecified ambition into a standing job Codex can actually finish. Research before committing. Prefer a compact objective backed by durable context, a trustworthy feedback loop, explicit constraints, and independent review.

Do not use Goal mode merely to make an ordinary task run longer. A good goal lets Codex tell whether it is getting warmer without redefining success.

## Modes

- **Design** (default): research and return a goal packet, but do not activate a goal.
- **Critique**: diagnose an existing goal and rewrite weak parts.
- **Activate**: design the goal, then create it only when the user explicitly asks to start, set, activate, or run the goal.
- **Goal tree**: when the user explicitly authorizes subagents or parallel agent work, design a parent goal plus bounded research, execution, or verification lanes. Create child goals only when the user explicitly asks for goal-backed subagents.

Never infer activation from a request to research, plan, improve, or draft a goal. Never set a token budget unless the user explicitly requests one.

## Workflow

### 1. Establish the real outcome

Recover the intended result, audience, destination, constraints, and why the work benefits from persistence. Inspect named files, repositories, artifacts, threads, and live systems before writing the goal.

Ask a question only when the missing answer would materially change the finish line, authorize a consequential action, or choose between incompatible goals. Otherwise proceed with a stated assumption.

### 2. Research the starting state

Gather the smallest body of evidence that can ground the objective:

1. Read the canonical local source and its applicable instructions.
2. Inspect the current baseline, existing attempts, tests, benchmarks, reproductions, or acceptance criteria.
3. Refresh volatile facts from primary or live sources when they determine the goal.
4. Search team discussion or public practitioner evidence when it can reveal a proven loop, known failure mode, or better verifier.
5. Stop when the finish line and verification path are supported; do not turn goal design into open-ended research.

Separate observed facts, user requirements, and inferred choices in the goal packet.

### 3. Decide whether Goal mode fits

Recommend Goal mode when the work has most of these properties:

- it needs repeated attempts, waiting, recovery, or a long feedback cycle;
- progress can be measured by a test, benchmark, reproduction, workflow, threshold, artifact inspection, or other external signal;
- Codex can act on the next failure without needing a fresh preference decision;
- the environment can remain available long enough to make progress;
- the completion evidence is stronger than the agent's own assertion.

Prefer an ordinary task, a plan, or a short interactive session when the work is one-shot, taste-dependent, blocked on repeated human choices, lacks a credible verifier, or could cause unbounded external actions.

### 4. Design the feedback loop

Define:

- **Outcome:** one ambitious, observable result.
- **Baseline:** current state, exact failure, or starting metric.
- **Primary verifier:** the strongest independent check of success.
- **Supporting checks:** regression, quality, safety, or durability checks.
- **Iteration loop:** inspect, change one meaningful thing, run the verifier, record evidence, and choose the next action.
- **Anti-cheating constraints:** forbid weakening tests, changing the benchmark, hiding failures, substituting mocks, or narrowing scope unless explicitly approved.
- **Review pressure:** side chat, skeptical review, fresh-context audit, or an independent verifier lane at meaningful checkpoints and before completion.
- **Blocker standard:** concrete evidence of an external blocker plus the smallest actionable next step; difficulty, uncertainty, or slow progress is not a blocker.
- **Completion proof:** exact commands, outputs, artifact paths, screenshots, or readbacks that must exist before the goal can be marked complete.

For flaky or stateful checks, require clean-state reproduction and enough consecutive successes to distinguish a fix from luck.

### 5. Keep state durable

Keep the active goal objective short. When the supporting specification is more than a few compact paragraphs, write or update the nearest appropriate durable file instead of cramming it into the goal text.

Use the project's established files when they exist. Otherwise propose:

```text
GOAL.md      outcome, baseline, constraints, success and blocker criteria
WORKLOG.md   hypotheses, attempts, evidence, current state, next action
RESULT.md    final change, verification, remaining risks
```

Do not create files in Design mode unless the user asked for a durable artifact or local conventions make that the obvious destination. Preserve dirty state and do not rewrite an existing goal packet without reading it first.

### 6. Design delegation without losing ownership

When subagents are authorized, the parent thread remains responsible for scope, integration, conflicts, and final completion. Delegate only cleanly separable lanes such as environment discovery, alternative approaches, source research, or independent verification.

For every child lane, specify:

- a bounded objective and non-goals;
- source or mutation ownership with no overlap;
- a verifier and stop condition;
- the artifact or evidence returned to the parent;
- whether it is a research task or an explicitly authorized child goal.

Subagents can manage their own active goals when the user explicitly requests a goal tree. Give each child one local finish line; do not clone the parent goal. The parent must reconcile child results and must not mark itself complete merely because every child stopped.

When spawning a goal-backed child, carry the user's authorization into the delegation prompt and instruct the child to create its own bounded goal, inspect that goal while working, and update its status only after its local completion proof is satisfied. Keep the parent's active goal separate from every child's goal.

Prefer ordinary delegated tasks over child goals when a lane can finish in one turn. Avoid nested goals when agents would edit the same files, wait on one another circularly, or multiply costly work without independent evidence value.

### 7. Draft, critique, then activate

Before activation, run a red-team pass:

- Can success be faked by weakening or changing the verifier?
- Could Codex satisfy the words while missing the user's real outcome?
- Are irreversible, public, shared, or costly actions separately approval-gated?
- Does the goal explain what to do after a failed attempt or external wait?
- Is completion observable to someone other than the running agent?

If the user explicitly requested activation, create the goal only after this pass. Use a compact objective such as:

```text
Complete and verify the objective defined in <absolute-path-to-GOAL.md>.
```

For a self-contained goal, state the observable outcome and strongest verifier directly. Do not activate a goal while still in a planning-only mode; finish the plan first, then switch to an execution-capable mode.

## Goal Packet

Return:

1. **Fit:** use Goal mode or a better alternative, with one-sentence rationale.
2. **Grounding:** relevant current state, assumptions, and evidence gaps.
3. **Goal brief:** outcome, baseline, constraints, non-goals, verifier, iteration loop, review pressure, blocker standard, and completion proof.
4. **Delegation map:** parent ownership and child lanes, only when useful and authorized.
5. **Exact objective:** the concise text suitable for goal activation.
6. **Activation state:** `drafted`, `active`, or `not recommended`.

If activated, report the exact active objective. If only drafted, say plainly that no goal was created.

## Completion Discipline

While operating an active goal:

- inspect current goal state when resuming or after material steering;
- continue while a safe, relevant next step remains;
- mark complete only when the objective and completion proof are both satisfied and no required work remains;
- mark blocked only after the same true external blocking condition persists for the required consecutive goal turns and meaningful progress is impossible;
- preserve partial results and the next action when stopping.
