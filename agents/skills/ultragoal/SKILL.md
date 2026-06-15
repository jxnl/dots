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

1. Read the canonical local source and applicable instructions.
2. Inspect the baseline, prior attempts, tests, benchmarks, reproductions, or acceptance criteria.
3. Refresh volatile facts from primary or live sources when they matter.
4. Stop once the finish line and verifier are grounded.

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

- **Outcome:** one observable result.
- **Baseline:** current state, failure, or starting metric.
- **Primary verifier:** strongest independent success check.
- **Supporting checks:** regression, quality, safety, or durability checks.
- **Iteration loop:** inspect, change one meaningful thing, run verifier, record evidence, choose next action.
- **Anti-cheating rules:** do not weaken tests, narrow scope, hide failures, swap in mocks, or change benchmarks without approval.
- **Approval gates:** irreversible, public, shared, or costly actions need separate user approval.
- **Blocker standard:** external blocker plus smallest next action; difficulty or uncertainty is not enough.
- **Completion proof:** exact commands, outputs, paths, screenshots, or readbacks required before `update_goal(status="complete")`.

For flaky or stateful checks, require clean-state reproduction and enough consecutive passes to rule out luck.

### 5. Keep State Durable

Keep the active goal objective compact. Put supporting context in the nearest durable file when it exceeds a few paragraphs.

Prefer project conventions. Otherwise propose:

```text
GOAL.md      outcome, baseline, constraints, success and blocker criteria
WORKLOG.md   attempts, evidence, current state, next action
RESULT.md    final change, verification, remaining risks
```

Do not create files in Design mode unless the user asked for a durable artifact or the repo convention makes it obvious. Preserve dirty work and read existing goal files before editing them.

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

If task work should continue after activation, create the goal first and then resume under Active Goal Discipline.

Use a compact objective:

```text
Complete and verify the objective defined in <absolute-path-to-GOAL.md>.
```

For a self-contained goal, put the observable outcome and strongest verifier directly in the objective. After `create_goal`, report the exact active objective and continue from that created goal.

## Goal Packet

Return:

1. **Fit:** Goal mode or better alternative, with one-sentence rationale.
2. **Grounding:** current state, assumptions, evidence gaps.
3. **Goal brief:** outcome, baseline, constraints, non-goals, verifier, loop, approval gates, blocker standard, completion proof.
4. **Delegation map:** only when useful and authorized.
5. **Exact objective:** concise text suitable for `create_goal`.
6. **Activation state:** `drafted`, `active`, or `not recommended`.

If activated, include the exact active objective. If not, say no goal was created.

## Active Goal Discipline

When operating an active goal:

- inspect goal state when resuming or after material steering;
- continue while a safe, relevant next step remains;
- mark complete only after the objective and completion proof are satisfied;
- mark blocked only after the required repeated external blocker threshold is met and no meaningful progress remains;
- preserve partial results and next action when stopping.
