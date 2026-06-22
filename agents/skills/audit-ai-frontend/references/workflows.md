# Improvement Workflows

Use this reference when a UI needs concrete anti-generic repair work, not just a style critique.

## Code-Structure Audit Loop

Use this loop before visual restyling when source code is available.

1. Map the UI to local architecture:
   - page/route owner
   - layout shell
   - existing design-system primitives
   - state/data source
   - repeated component shapes
2. Trace the data path from source to render:
   - props and loaders/API responses
   - derived state versus stored state
   - loading, empty, error, disabled, and permission states
   - realistic fixture/story data when no backend is wired
3. Inspect component APIs:
   - prefer one domain object or a small prop set over many implementation props
   - prefer stable variants over boolean clusters
   - use slots/children for flexible content regions
   - keep callbacks explicit and state ownership near the common parent that needs it
4. Inspect styling reuse:
   - use local primitives and semantic tokens before new CSS
   - promote repeated utility recipes into variants/helpers only when the repo has that pattern
   - remove arbitrary values and one-off CSS when they duplicate token roles
5. Patch one coherent cluster:
   - data model/props first
   - primitive or variant extraction second
   - visual token/style cleanup third
   - responsive/a11y state verification last

Do not abstract only to look clever. Extract when it reduces current duplication, supports real states, or matches an existing local pattern.

## Browser-Grounded QA Loop

Use this loop whenever the page can be rendered locally.

Use whatever browser tooling is available in the current Codex environment.
Keep this workflow focused on what to inspect for AI-frontend quality, not how
to operate browser primitives.

1. Open the page in a real browser.
2. Capture at least one desktop screenshot and one mobile screenshot; use extra breakpoints when the layout has tablet/sidebar/table behavior.
3. After each meaningful state change, run three checks in order: visual inspection, accessibility scan, and semantic/ARIA inspection.
4. Inspect the DOM/accessibility tree and manually tab through the main flow.
5. Exercise non-happy-path states: empty data, long content, missing values, validation errors, loading, disabled actions, and reduced-motion when relevant.
6. Patch one coherent issue cluster at a time.
7. Re-open the page and compare screenshots, accessibility tree, keyboard behavior, and responsive behavior before calling the work done.

If the repo already has Playwright Test, prefer adding or updating visual and accessibility checks instead of relying only on manual inspection. Use the repo's own test conventions and the Playwright docs surfaced by `playwright` / `playwright-interactive`; these are the audit-specific checks to encode:

- Add screenshot baselines with `await expect(page).toHaveScreenshot()`.
- Mask or hide volatile UI regions so snapshot diffs stay deterministic.
- Run baselines in the same OS/browser environment where they were generated.
- Add automated a11y scans with `@axe-core/playwright`, but do not treat those scans as complete WCAG coverage.
- Scope axe scans to the changed component/region when possible, and wait for the UI to settle before calling `analyze()`.
- Include at least one mobile/tablet emulation profile and one desktop profile for layout regressions.
- Add ARIA snapshots for stable role/name/heading/menu/dialog structures when those semantics are the point of the fix.
- If the repo uses Storybook, prefer `play` functions for stateful interaction coverage and Chromatic for browser/viewport visual review.

Manual checks still required:

- tab order and visible focus
- keyboard operation for menus, dialogs, custom controls, and focus traps (`Tab`, `Shift+Tab`, `Enter`, `Space`, `Esc`, arrows)
- semantic heading/landmark structure
- color contrast and non-color state cues
- scroll/overflow behavior on narrow screens

## Reference-Packet Workflow

Use this loop when the UI looks generic and needs a stronger visual point of view.

Build a reference packet before editing:

- 1 structure reference that shows the section layout or interaction model you want
- 1-3 style references for tone, density, color, imagery, or typography
- 1 token contract that defines palette, type, spacing rhythm, radii, elevation, iconography, motion, and theme modes
- 1 or more realistic data/copy samples that force the UI to handle actual content
- 1 short note describing what to borrow from each reference and what must not be copied literally

Interpretation rules:

- Use screenshots and component crops for layout and component shape.
- Prefer Figma links/frames over screenshots when available; use one frame per UI slice for complex screens.
- Use moodboards or style references for palette, texture, image treatment, and density.
- Use product copy, data samples, and API examples to force realistic content constraints.
- Specify whether a reference should be rebuilt 1:1 or used only as style inspiration.
- If no external references exist, infer an initial direction from the product's domain, existing primitives, and user job, then write that as a concrete design contract. Do not fabricate named reference sites.

Implementation rules:

- Generate or patch one page section/component at a time instead of one full-page rewrite.
- Compare the rendered result to the reference packet and iterate only on the mismatched deltas.
- Promote repeated visual decisions into theme tokens, CSS variables, component props, or reusable primitives.
- Split token work into primitives, semantic tokens, and component-level tokens when the design system is large enough to need that separation.
- Keep token references alias-driven and reject circular or unresolved references.
- If the stack defaults to a common component library look, override the visual layer at the token/component level rather than sprinkling one-off styles.

## Brief-Lock And Critique Loop

Use this loop when the incoming request is under-specified and likely to produce "modern SaaS" defaults.

1. Extract or ask for the minimum missing brief:
   - audience
   - primary action or job-to-be-done
   - brand tone
   - hard constraints
   - 1-2 reference products or screenshots
2. Propose 2-3 meaningfully different directions.
   - Vary layout strategy, section rhythm, density, typography, and interaction model.
   - Do not offer only cosmetic palette swaps.
3. Lock one direction and write a short design contract.
4. Implement in slices.
5. Run a critique pass before finalizing:
   - Component/data shape: is repeated UI parameterized through real props/data instead of hard-coded fixture markup?
   - User-task fit: does the screen make the primary job and primary action obvious?
   - Visual hierarchy and clutter: does one thing clearly win, and has unnecessary chrome/copy been removed?
   - Consistency: does the screen respect local patterns and tokens rather than inventing one-off styles?
   - Operability: can keyboard users reach and operate every critical control with visible focus and no traps?
   - Responsive resilience: does the layout survive narrow screens, long text, and larger zoom/text?
   - Feedback and recovery: are loading, empty, error, disabled, and success states visible and useful?
   - Copy quality: is the language specific, action-oriented, and free of generic filler?
   - AI-default check: are cards, gradients, and icon pills being used because they help, or because they are defaults?
   - Extensibility: can the style be carried to the next screen without inventing new one-off tokens?
6. If this prompt/workflow will be reused, create a tiny regression suite:
   - 3-5 representative UI tasks or screens
   - one rubric for accessibility, responsiveness, design specificity, and copy quality
   - a changelog of prompt edits and observed regressions

Prompt hygiene when generating new UI:

- Prefer concrete examples and compact structured sections over vague adjectives.
- If the model supports structured prompt tags, isolate references, constraints, and instructions in separate sections.
- Include 3-5 diverse examples when output format or aesthetic behavior needs to stay stable.
- Keep anti-pattern bans paired with a positive replacement, for example "avoid generic centered card grids; use an editorial split layout with one dominant visual block."
