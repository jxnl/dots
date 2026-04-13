# AI Frontend Tells And Fixes

Use this reference to audit frontend code or screenshots for generic AI-generated patterns and to pick the smallest fix that makes the UI feel intentional.

## P0: Functional And Accessibility Failures

### 1. Happy-path-only UI

Tell:
- No loading, empty, disabled, offline, or error states.
- Forms accept ideal input only.
- Search/filter/list views render one perfect dataset shape.

Why it matters:
- AI-generated UI often looks complete while skipping real-world branches.

Fix:
- Add skeleton/loading, empty, error, and partial-success states.
- Include form validation copy and recovery paths.
- Stress-test with long names, missing values, zero results, and API failures.

### 2. Broken keyboard and screen-reader behavior

Tell:
- Clickable `div`/`span`, missing labels, missing dialog titles, invisible focus, incorrect or absent ARIA.
- Repeated icon-only buttons with no accessible name.

Fix:
- Use native elements first.
- Add visible focus states, labels, dialog titles, `aria-describedby`, and keyboard support.
- Verify tab order and focus trapping in overlays.

### 3. Weak mobile and responsive behavior

Tell:
- Desktop-only three-card grids collapse badly.
- Sticky sidebars, tables, and hero layouts overflow or hide critical actions.
- Text scales without layout adaptation.

Fix:
- Redesign the component behavior per breakpoint, not just width-shrink the desktop layout.
- Use fluid type/spacing, container-aware layouts, and explicit mobile navigation and table fallbacks.

## P1: Strong AI Aesthetic Tells

### 4. Default AI palette

Tell:
- Purple-to-blue gradients, indigo CTAs, cyan glows on dark backgrounds, gradient headline text, glass cards over blurred blobs.
- Many unrelated one-off accent colors with no palette logic.

Fix:
- Pick one aesthetic direction and encode it into tokens.
- Use one dominant neutral family, one supporting hue family, and one accent with a clear job.
- Replace decorative gradient text with composition, photography, texture, or shape if the content itself is the emphasis.

### 5. Default AI typography

Tell:
- Inter, Roboto, Arial, Open Sans, or system font stacks used as the entire visual personality.
- Monospace used as a lazy shorthand for "technical".
- Every heading and body block has the same weight, tracking, and rhythm.

Fix:
- Choose one distinctive display face plus one readable body face when the product brand allows it.
- If the codebase already has a typography system, tune the scale, line-height, and weight contrast instead of introducing a random new font.
- Keep body line length readable and use fluid type for hero/display text.

### 6. Cardocalypse

Tell:
- Every concept is inside a rounded card.
- Nested cards inside cards.
- Uniform `border-radius`, `border`, `box-shadow`, and `padding` treatments repeated across the page.
- Feature sections are just icon + heading + paragraph cards in identical grids.

Fix:
- Remove containers where the section can stand on spacing, dividers, or type alone.
- Flatten nested surfaces.
- Reserve cards for content that truly needs grouping, state, or affordance.
- Mix editorial blocks, split layouts, tables, timelines, or stacked rows instead of repeating one card grid.

### 7. Icon-pill sameness

Tell:
- Large Lucide-style icon inside a rounded square/circle above every heading.
- Decorative icons that do not add information or action meaning.

Fix:
- Keep icons only where they improve scan or interaction clarity.
- Move iconography into one distinctive motif or structural treatment instead of repeating the same pill badge.
- Prefer domain-specific imagery, diagrams, or type-led hierarchy when icons are filler.

### 8. Template SaaS landing-page structure

Tell:
- Centered headline, subhead, two CTAs, hero mockup, then three feature cards, three metrics, testimonials, and a generic FAQ.
- "Everything centered" composition with no asymmetry or editorial rhythm.

Fix:
- Start from the job and audience, not a generic SaaS trope.
- Vary section geometry and alignment.
- Create one memorable section composition or interaction that feels specific to the product.
- If preserving structure, de-template one high-visibility section first: hero, primary feature block, or metrics.

### 9. Decorative motion and glow

Tell:
- Hover scale on every card, bouncy easing, endless float animations, glow borders, generic staggered fade-ins.
- Motion that signals "polish" but no state change or hierarchy.

Fix:
- Use one or two intentional motion moments tied to state, navigation, or reveal.
- Prefer transform/opacity, short durations, and smooth deceleration.
- Respect `prefers-reduced-motion`.

### 10. Generic AI marketing copy

Tell:
- Vague claims like "Transform your workflow", "Unlock insights", "Build the future".
- Repeated intro paragraphs that restate the section heading.
- Labels like "Submit", "Learn more", "Get started" with no concrete object or outcome.

Fix:
- Rewrite around specific user jobs, product objects, and outcomes.
- Use concrete button labels with verb + object.
- Remove duplicate preambles and make empty/error states teach the next action.

## P2: Craft And Design-System Drift

### 11. Uniform spacing and radius everywhere

Tell:
- The same padding, gap, border radius, and shadow on every section.
- No clear rhythm between dense and airy areas.

Fix:
- Build spacing rhythm: tighter within groups, larger between sections.
- Use a small, deliberate radius/shadow scale and assign each token a role.

### 12. Token inconsistency

Tell:
- Arbitrary hex colors, inline style values, or one-off utility classes scattered across components.
- Mixed border colors, background shades, and shadow strengths with no system.

Fix:
- Consolidate into CSS variables or existing semantic tokens.
- Prefer changing the design-system layer over patching every component individually.

### 13. Safe but forgettable detail work

Tell:
- Rounded rectangles, soft shadow, low-contrast gray text, and no distinctive shape language.
- Surfaces look polished in isolation but the page has no point of view.

Fix:
- Choose one memorable visual rule: a specific border treatment, image crop language, section rhythm, type contrast, or material texture.
- Apply it consistently in one or two places, not everywhere.

## P1/P2: Dense App And Dashboard Tells

### 14. Equal-weight dashboard tiles

Tell:
- Every KPI, chart, activity feed, and table sits in an equally styled card with the same emphasis.
- The primary user job is buried among peer tiles instead of getting a dominant region, persistent controls, or a clear drilldown path.

Fix:
- Promote one primary surface and one supporting surface.
- Use lower-chrome rows, tables, split panes, or grouped sections for secondary content instead of repeating card shells.
- Make filters and sort controls persistent and visually obvious.

### 15. Generic admin/settings scaffolding

Tell:
- Settings pages are a stack of identical cards with duplicated "Manage..." descriptions and vague toggles.
- Forms rely on placeholder text, ambiguous labels, and no helper/error copy.
- Destructive actions are styled like ordinary actions or hidden inside a generic modal.

Fix:
- Group settings by user task, not by visual container.
- Use specific labels, helper text, and action copy.
- Add clear destructive states and confirmation copy tied to the exact object/action.

### 16. Table and list polish without real data behavior

Tell:
- Beautiful but brittle tables that assume short names, no missing values, no pagination stress, and no row actions.
- Dense lists where every row has the same icon, same badge, and same preview text rhythm.

Fix:
- Test long text, missing values, many rows, and mobile collapse.
- Add sorting/filtering affordances where they are needed for the task.
- Use hierarchy, alignment, and compact row structure before adding another layer of card styling.

### 17. Faux analytics decoration

Tell:
- Tiny sparklines, arbitrary percentages, or chart cards included for visual sophistication but not decision support.
- Metrics have no time range, comparison baseline, or explanation of why they matter.

Fix:
- Keep metrics only when they answer a concrete product question.
- Attach timeframe, denominator, and comparison context.
- Replace decorative charts with a useful table, trend panel, or status summary when the chart has no real analytical job.

## Code Smell Search Patterns

Search for these framework-agnostic patterns before patching:

- `Inter`, `Roboto`, `Arial`, `Open Sans`, `system-ui`, `ui-sans-serif`
- purple/indigo/cyan gradients, gradient-clipped headline text, blurred glow layers, and glass surfaces
- repeated large radii such as `16px`, `24px`, or `9999px` used everywhere without a clear role
- repeated soft shadows and frosted-glass effects such as `box-shadow`, `backdrop-filter: blur(...)`, or `filter: blur(...)`
- repeated hover scale transforms on every card or tile
- repeated `Card` maps with the same `Icon + title + description` structure
- repeated outline-icon imports used only as section decoration
- `outline: none`, `tabIndex={-1}`, clickable `div`/`span`
- missing `aria-label`, `aria-describedby`, `alt`, or dialog titles
- fixed desktop widths, fixed card grids, sticky sidebars, or wide tables with no mobile fallback
- repeated copy prefixes such as "Manage", "Seamlessly", "Powerful", "AI-powered", or section intros that restate the heading
- tables/lists with hard-coded short sample content and no long-text, empty, or error states

If the project uses Tailwind, also search for these optional utility-class equivalents:

- `font-sans`, `from-purple-*`, `to-indigo-*`, `bg-indigo-*`, `text-transparent bg-clip-text`
- `rounded-2xl`, `rounded-3xl`, `shadow-xl`, `backdrop-blur-*`, `hover:scale-105`

## Minimal Repair Playbook

Use this order when making a page feel less AI-generated without a redesign:

1. Fix accessibility, responsive behavior, and missing states.
2. Replace one overused font stack or retune type hierarchy.
3. Simplify the palette and remove one obvious gradient/glow trope.
4. Delete unnecessary cards and flatten nested surfaces.
5. De-template one prominent section with a more specific composition.
6. Cut vague copy and rewrite CTAs around concrete actions.
7. Keep one purposeful motion or visual motif and remove the rest.

## Prompt Hygiene For New UI Generation

If the user asks you to generate a new interface from scratch, gather these constraints before coding when they are not already available:

- target audience and usage context
- primary job/action the screen must support
- brand tone and one aesthetic direction
- one or two reference products or visual cues to borrow from
- accessibility, performance, and framework constraints

Avoid prompts that only say "modern SaaS", "beautiful dashboard", or "clean landing page". Those prompts push models toward the statistical average.
