---
name: ultragoal
description: Design, critique, set, create, activate, or run durable Codex goals for persistent or long-running objectives. Use when the user says "set a goal", "start a goal", "activate goal mode", "persistent goal", "long-running objective", "goal tree", or asks for a goal with verifiers, durable state, approval gates, completion proof, bounded delegation, or parent/child subagent goals.
---

# Ultragoal

Use this skill when a user wants a persistent Codex goal, not just a longer task. A good goal has an observable finish line, a verifier that can fail, and enough context for Codex to recover after interruptions.

Do not activate a goal from vague planning language. Activate only when the user explicitly asks to start, set, activate, create, or run a goal. Never set a token budget unless the user explicitly requests one.

## Modes

- **Design:** research and return a goal packet. Do not call `create_goal`.
- **Critique:** inspect an existing goal or draft and tighten it.
- **Activate:** design and critique the goal, then call `create_goal` as the final activation step.
- **Goal tree:** only when the user explicitly authorizes goal-backed subagents. Give each child one bounded objective and verifier.

## Default Activation Rule

When the user explicitly invokes this skill for a concrete work objective and asks Codex to build, complete, run, pursue, or "do it", treat the request as **Activate** by default.

Do not stop after writing durable goal files or reporting a goal packet. After grounding and, when useful, writing `GOAL.md` or equivalent durable state, call `create_goal` before continuing task work.

Only stay in **Design** mode when the user asks to draft, design, critique, or discuss a goal without starting it.

## Workflow

### 1. Ground the Outcome

Find the intended result, audience, destination, constraints, and why persistence helps. Inspect named files, repos, threads, artifacts, and live systems before drafting.

Ask only when the missing answer changes the finish line, grants consequential approval, or chooses between incompatible goals. Otherwise state the assumption and continue.

### 2. Research Enough

Gather the smallest useful evidence set:

k1. Read the canonical local source and its applicable instructions.
2. Inspect the current baseline, existing attempts, tests, benchmarks, reproductions, or acceptance criteria.
3. Inventory the capabilities needed to exercise the real outcome, including terminal access, Browser, authenticated Chrome, Computer Use, local apps, devices, accounts, permissions, and test environments.
4. Refresh volatile facts from primary or live sources when they determine the goal.
5. Search team discussion or public practitioner evidence when it can reveal a proven loop, known failure mode, or better verifier.
6. Stop when the finish line and verification path are supported; do not turn goal design into open-ended research.

Separate observed facts, user requirements, and inferred choices.

### 3. Check Goal Fit

Recommend Goal mode only when most are true:

- progress needs repeated attempts, waiting, recovery, or long feedback cycles;
- success can be measured by a test, benchmark, workflow, artifact inspection, screenshot, readback, or other external signal;
- Codex can respond to the next failure without another preference decision;
- completion evidence is stronger than Codex saying "done."

Prefer an ordinary task or plan when the work is one-shot, taste-dependent, blocked on repeated human choices, lacks a credible verifier, or risks unbounded external action.

### 4. Define the Loop

Specify:

- **Outcome:** one ambitious, observable result.
- **Baseline:** current state, exact failure, or starting metric.
- **Primary verifier:** the strongest independent check of success on the surface where the outcome actually matters.
- **Supporting checks:** regression, quality, safety, or durability checks.
- **Iteration loop:** inspect, change one meaningful thing, run verifier, record evidence, choose next action.
- **Anti-cheating rules:** do not weaken tests, narrow scope, hide failures, swap in mocks, or change benchmarks without approval.
- **Approval gates:** irreversible, public, shared, or costly actions need separate user approval.
- **Blocker standard:** external blocker plus smallest next action; difficulty or uncertainty is not enough.
- **Completion proof:** exact commands, outputs, paths, screenshots, or readbacks required before `update_goal(status="complete")`.

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

### 5. Keep State Durable

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

### 6. Delegate Carefully

When subagents are authorized, the parent keeps scope, integration, conflict resolution, and final completion. Delegate only separable lanes: environment discovery, source research, alternative approaches, or independent verification.

For each lane, name the objective, non-goals, ownership boundary, verifier, stop condition, and returned evidence. Use child goals only when the user explicitly asked for goal-backed subagents.

### 7. Activate Last

Before activation, red-team the draft:

- Can success be faked by weakening the verifier?
- Could the words be satisfied while missing the user's real outcome?
- Are approval gates explicit?
- Does the loop say what to do after a failed attempt or wait?
- Is completion observable outside the running agent?

If activation was requested, or the Default Activation Rule applies, call `create_goal` only after the goal packet is grounded and red-teamed. This call is the final action of activation; do not call it early, and do not merely say a goal should be set.

- Can success be faked by weakening or changing the verifier?
- Could Codex satisfy the words while missing the user's real outcome?
- Are irreversible, public, shared, or costly actions separately approval-gated?
- Does the goal explain what to do after a failed attempt or external wait?
- Is completion observable to someone other than the running agent?
- If the outcome is interactive, does the goal actually exercise it with Browser, authenticated Chrome, or Computer Use on the correct surface?
- Are all required verification capabilities available, or does the goal name the exact blocked handoff instead of weakening the verifier?

Use a compact objective:

```text
Complete and verify the objective in <workspace>/.codex/<request>/goal.md by executing and maintaining <workspace>/.codex/<request>/plan.md. Read and maintain both files throughout the work: update plan.md when the route, phase state, checks, or evidence changes, and update goal.md when steering or evidence changes the outcome, constraints, verifier, completion proof, or blocker criteria.
```

For a self-contained goal, put the observable outcome and strongest verifier directly in the objective. After `create_goal`, report the exact active objective and continue from that created goal.

## Goal Packet

Return:

1. **Fit:** use Goal mode or a better alternative, with one-sentence rationale.
2. **Grounding:** relevant current state, assumptions, and evidence gaps.
3. **Goal brief:** outcome, baseline, constraints, non-goals, verifier, verification surface and capabilities, iteration loop, review pressure, blocker standard, and completion proof.
4. **Durable artifacts:** the request slug, absolute paths, and complete proposed contents for `.codex/<request>/goal.md` and phased `.codex/<request>/plan.md`; write them before activation, but only when activation or durable artifacts were requested.
5. **Delegation map:** parent ownership and child lanes, only when useful and authorized.
6. **Exact objective:** the concise text suitable for goal activation.
7. **Activation state:** `drafted`, `active`, or `not recommended`.

If activated, include the exact active objective. If not, say no goal was created.

## Active Goal Discipline

When operating an active goal:

- inspect the active goal plus `.codex/<request>/goal.md` and `.codex/<request>/plan.md` when resuming;
- after user steering or material new evidence, update `plan.md` before continuing and update `goal.md` when its outcome, constraints, verifier, completion proof, or blocker criteria changed;
- keep phase statuses, implementation checklists, verification checklists, evidence, and next action current throughout execution;
- continue while a safe, relevant next step remains;
- run the primary verifier on the declared surface after material changes, using lower-level checks only as supporting evidence;
- mark phases complete only after their implementation and verification exit criteria pass;
- mark the goal complete only when the objective and completion proof are both satisfied, every required plan phase is complete, and no required work remains;
- mark blocked only after the same true external blocking condition persists for the required consecutive goal turns and meaningful progress is impossible;
- preserve partial results and the next action when stopping.
