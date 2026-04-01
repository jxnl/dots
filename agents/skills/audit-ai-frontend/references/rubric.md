# Review Rubric

Use this rubric when the user asks for a broader audit and you need more structure than the pattern checklist alone.

Score each dimension as `P0`, `P1`, `P2`, or `OK`, then only report the highest-leverage findings.

## Core Dimensions

### User-task fit

Check:
- Is the primary user job obvious within the first screen?
- Is there one primary action or decision path, or are all actions equal weight?
- Does the screen solve a product-specific problem, or could the same layout belong to any SaaS app?

### Visual hierarchy and clutter

Check:
- Does one region, CTA, or data surface clearly win?
- Are cards, borders, badges, and icons doing grouping/scan work, or just adding chrome?
- Can you remove 20-30% of visible decoration/copy without losing meaning?

### AI-default distinctiveness

Check:
- Is there one memorable visual rule or composition that is specific to the product?
- Are fonts, gradients, icon pills, and rounded cards being used because they fit the concept, or because they are defaults?
- If you replaced the logo and headline, would the page still feel tied to this product?

### Design-system consistency

Check:
- Do spacing, radius, color, elevation, and component states follow a small set of reusable rules?
- Are there one-off values that should be promoted into tokens or component variants?
- If the current "generic" look is already a documented brand/system choice, is the review preserving that instead of overcorrecting?

### Copy specificity

Check:
- Does the copy name the audience, the object, and the action outcome?
- Are CTAs concrete (`Verb + Object`) instead of vague (`Get started`, `Learn more`)?
- Do empty, loading, and error states explain what happened and what to do next?

### Interaction feedback and recovery

Check:
- Are hover, pressed, focus, disabled, loading, success, empty, and error states present where needed?
- Do state changes communicate what changed, not just animate?
- Can users recover from mistakes or retry after failure?

### Keyboard and screen-reader operability

Check:
- Every interactive element has native semantics or correct role/name/value wiring.
- Focus is visible, logical, and not trapped or lost.
- Dialogs, menus, tabs, and custom controls can be operated with keyboard only.

### Responsive resilience

Check:
- Does the layout adapt at mobile/tablet widths, or just shrink the desktop composition?
- Do long text, large zoom/text, and narrow viewports avoid overlap, clipping, or horizontal scroll?
- For data-heavy UIs, is there a clear mobile prioritization or collapse strategy?

### Trust and proof quality

Check:
- Are metrics, testimonials, logos, and social proof specific, verifiable, and relevant to the audience?
- Do charts or KPIs include the timeframe, comparison baseline, and why the metric matters?
- Is visual polish being used to compensate for missing product evidence?

### Help and discoverability

Check:
- Can a new user infer what to do next without reading a wall of text?
- Are advanced options progressively revealed instead of hidden or dumped into one panel?
- If the task is complex, is there in-flow guidance, documentation, or a clear next-step affordance?

## Evidence Standard

For each reported finding include:

- `Issue`
- `Evidence`
- `Class`
- `Why it matters / why it reads as generic`
- `Possible non-AI explanation`
- `Smallest fix`
- `Acceptance check`
- `Confidence`
- `File/line`

Use this rule for screenshots-only reviews:

- Visible defect = state as fact.
- Implementation defect not directly visible = mark as `Inferred`.
- Do not claim missing ARIA, missing keyboard support, or broken semantics unless code, DOM, or browser behavior confirms it.
