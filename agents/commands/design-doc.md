# Design Doc Command

Format implementation plans as structured design documents for technical review and discussion.

## Usage

```bash
/design-doc                    # Start a new design doc
/design-doc "feature name"     # Start with a specific feature
```

## Workflow

### 1. Gather Context

Ask the user:
- What problem are you solving?
- What's the current state/pain points?
- Any constraints or requirements?

Research the codebase if needed to understand existing patterns.

### 2. Generate Design Doc

Output the design doc using this exact structure:

---

# {Project Name} Design Doc

## Problem Context

Brief description of the problem or opportunity. Overview of the domain and pain points. What is the current solution? What are its shortcomings?

## Proposed Solution

High-level summary of the proposed solution:
- What it will do
- How it will be built
- What's different from current state
- Key advantages

## Goals and Non-Goals

### Goals

- Goal 1: expected impact
- Goal 2: expected impact
- Goal 3: expected impact

### Non-Goals

- Non-goal 1 (explain why out of scope)
- Non-goal 2

## Design

Overall summary of the design and major components.

```
[Include diagram if helpful - ASCII or mermaid]
```

### Key Components

Describe major request paths, data models, and architectural decisions.

Add subsections for each major component as needed:
- Component A
- Component B

## Alternatives Considered

| Alternative | Pros | Cons | Why Not Chosen |
|-------------|------|------|----------------|
| Option A | ... | ... | ... |
| Option B | ... | ... | ... |

## Open Questions

- [ ] Question 1
- [ ] Question 2

## Implementation Plan

### Phase 1: Foundation
- Task 1
- Task 2

### Phase 2: Core Implementation
- Task 3
- Task 4

### Phase 3: Polish & Testing
- Write tests
- Documentation

## Appendix

Relevant links, detailed figures, or additional context.

---

### 3. Iterate

After generating:
- Ask if any sections need expansion
- Clarify open questions
- Refine based on feedback

## Rules

- Keep language concise, sacrifice grammar for brevity
- No fake case studies or made-up numbers
- Include realistic implementation phases
- Always include a testing phase
- List unresolved questions at the end
- Use tables for comparisons
- Include code snippets or diagrams where helpful

## Output Format

```
# {Project Name} Design Doc

[Full document as specified above]

---

Open questions to discuss:
1. ...
2. ...

Ready to refine any section or proceed to implementation?
```
