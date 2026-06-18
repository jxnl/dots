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
3. Inventory the capabilities needed to exercise the real outcome, including terminal access, Browser, authenticated Chrome, Computer Use, local apps, devices, accounts, permissions, and test environments.
4. Refresh volatile facts from primary or live sources when they determine the goal.
5. Search team discussion or public practitioner evidence when it can reveal a proven loop, known failure mode, or better verifier.
6. Stop when the finish line and verification path are supported; do not turn goal design into open-ended research.

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
- **Primary verifier:** the strongest independent check of success on the surface where the outcome actually matters.
- **Supporting checks:** regression, quality, safety, or durability checks.
- **Iteration loop:** inspect, change one meaningful thing, run the verifier, record evidence, and choose the next action.
- **Anti-cheating constraints:** forbid weakening tests, changing the benchmark, hiding failures, substituting mocks, or narrowing scope unless explicitly approved.
- **Review pressure:** side chat, skeptical review, fresh-context audit, or an independent verifier lane at meaningful checkpoints and before completion.
- **Blocker standard:** concrete evidence of an external blocker plus the smallest actionable next step; difficulty, uncertainty, or slow progress is not a blocker.
- **Completion proof:** exact commands, outputs, artifact paths, screenshots, or readbacks that must exist before the goal can be marked complete.

The primary verifier must do two jobs: reliably distinguish success from failure and return enough evidence to choose the next repair. Prefer the strongest feasible verifier closest to the user's actual experience. Static analysis, unit tests, mocks, builds, and code inspection are supporting evidence; they are not substitutes for exercising an interactive workflow when the outcome depends on one.

#### Test on the real interaction surface

Require Browser, authenticated Chrome, or Computer Use verification when success depends on rendered UI, browser or app state, authentication, permissions, native dialogs, files, clipboard, keyboard or pointer input, window focus, notifications, media, accessibility, installation, restart behavior, OS integration, or a multi-app workflow. Use the actual app or browser and representative state rather than inferring success from source code or a mocked environment.

For real-surface verification, put these in the goal brief:

- the exact surface, build, URL, account type, machine or device, and starting state;
- a short reproducible workflow with observable pass and fail criteria;
- evidence to capture, such as screenshots, video, console or network output, logs, resulting files, or a final state readback;
- clean-state, reload or restart, failure-recovery, and important negative-path checks proportional to risk;
- the required capability and fallback owner if Codex cannot access the surface.

Before activation, verify that the required browser, computer-use tool, app, device, credentials, and environment are actually available. If the real-surface verifier is unavailable, do not silently replace it with a weaker check. Name the capability gap and either choose a user-approved equivalent or define a blocked handoff with the exact manual test and evidence required. Keep sends, purchases, publication, access changes, and other consequential actions approval-gated even when they appear inside a test workflow.

For flaky or stateful checks, require clean-state reproduction and enough consecutive successes to distinguish a fix from luck.

### 5. Keep state durable

Keep the active goal objective short and put the durable operating state under the current workspace or project root:

- **`.codex/<request>/goal.md`:** the stable finish line: outcome, baseline, constraints, non-goals, primary verifier, completion proof, blocker criteria, and the path to the companion plan.
- **`.codex/<request>/plan.md`:** the living route: a link back to the goal, ordered phases, implementation checklists, phase-level testing criteria, evidence, status, and next action.

Derive `<request>` once as a short, descriptive, kebab-case slug. Reuse that directory when resuming or steering the same goal; create a different directory only for a genuinely distinct goal. When activating a goal, create or update both files before starting implementation and make them cross-reference one another. Read and preserve an existing request directory rather than replacing it blindly, and record both absolute paths in the goal packet.

Structure `plan.md` so every phase has:

```text
## Phase N: Observable milestone
Status: pending | in progress | blocked | complete

Implementation
- [ ] Concrete change or investigation

Verification
- [ ] Exact test, browser/computer-use workflow, or artifact inspection
- [ ] Observable pass criteria and required evidence

Exit criteria
- [ ] Conditions that must be true before the next phase starts
```

Keep at most one phase `in progress`. Check off work only after it is done, and check off verification only after the declared test passes. Record failed checks and resulting plan changes without erasing useful evidence. Optional `.codex/<request>/worklog.md` or `.codex/<request>/result.md` files may hold detailed attempts or the final handoff, but they do not replace `goal.md` or `plan.md`.

Treat user steering, new evidence, changed constraints, failed verification, and completed phases as plan-update events. Before continuing implementation after any such event:

1. re-read `.codex/<request>/goal.md` and `.codex/<request>/plan.md`;
2. decide whether the finish line changed or only the route changed;
3. update affected phases, checklists, verification criteria, dependencies, and next action in `plan.md`;
4. update `goal.md` when steering or evidence changes the outcome, constraints, verifier, completion proof, or blocker criteria;
5. preserve completed evidence, explicitly mark invalidated work, and then resume from the revised plan.

Do not let chat become the only source of current plan state. Do not create these files in Design mode unless the user asked for durable artifacts; include complete draft contents in the goal packet instead.

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
- If the outcome is interactive, does the goal actually exercise it with Browser, authenticated Chrome, or Computer Use on the correct surface?
- Are all required verification capabilities available, or does the goal name the exact blocked handoff instead of weakening the verifier?

If the user explicitly requested activation, create the goal only after this pass. Use a compact objective such as:

```text
Complete and verify the objective in <workspace>/.codex/<request>/goal.md by executing and maintaining <workspace>/.codex/<request>/plan.md. Read and maintain both files throughout the work: update plan.md when the route, phase state, checks, or evidence changes, and update goal.md when steering or evidence changes the outcome, constraints, verifier, completion proof, or blocker criteria.
```

For a self-contained goal, state the observable outcome and strongest verifier directly. Do not activate a goal while still in a planning-only mode; finish the plan first, then switch to an execution-capable mode.

## Goal Packet

Return:

1. **Fit:** use Goal mode or a better alternative, with one-sentence rationale.
2. **Grounding:** relevant current state, assumptions, and evidence gaps.
3. **Goal brief:** outcome, baseline, constraints, non-goals, verifier, verification surface and capabilities, iteration loop, review pressure, blocker standard, and completion proof.
4. **Durable artifacts:** the request slug, absolute paths, and complete proposed contents for `.codex/<request>/goal.md` and phased `.codex/<request>/plan.md`; write them before activation, but only when activation or durable artifacts were requested.
5. **Delegation map:** parent ownership and child lanes, only when useful and authorized.
6. **Exact objective:** the concise text suitable for goal activation.
7. **Activation state:** `drafted`, `active`, or `not recommended`.

If activated, report the exact active objective. If only drafted, say plainly that no goal was created.

## Completion Discipline

While operating an active goal:

- inspect the active goal plus `.codex/<request>/goal.md` and `.codex/<request>/plan.md` when resuming;
- after user steering or material new evidence, update `plan.md` before continuing and update `goal.md` when its outcome, constraints, verifier, completion proof, or blocker criteria changed;
- keep phase statuses, implementation checklists, verification checklists, evidence, and next action current throughout execution;
- continue while a safe, relevant next step remains;
- run the primary verifier on the declared surface after material changes, using lower-level checks only as supporting evidence;
- mark phases complete only after their implementation and verification exit criteria pass;
- mark the goal complete only when the objective and completion proof are both satisfied, every required plan phase is complete, and no required work remains;
- mark blocked only after the same true external blocking condition persists for the required consecutive goal turns and meaningful progress is impossible;
- preserve partial results and the next action when stopping.
