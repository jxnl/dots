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

## P1: Component And Implementation Slop

### 4. Hard-coded fixture screen

Tell:
- Sample arrays, copied cards, fake metrics, and perfect strings live inside the rendered page component.
- The screen cannot render realistic data, long labels, missing values, empty lists, permissions, or error states.
- Components accept only `className` or no props, even when repeated content clearly has a data shape.

Fix:
- Define the smallest useful data model and pass records through props.
- Move demo fixtures to stories/tests or a named fixture module when the app needs examples.
- Add states from the same data model: loading, empty, partial, error, long text, and unavailable values.

### 5. Broad component API or boolean-mode soup

Tell:
- Components expose many booleans such as `isHero`, `isCompact`, `showMeta`, `showActions`, `withGradient`, `hasBorder`.
- One component switches between unrelated layouts by conditionals instead of stable variants or composition.
- Props mirror implementation details instead of user-facing states or domain objects.

Fix:
- Replace clusters of booleans with a small variant enum, discriminated union, or separate components.
- Use slots/children for content regions that should remain flexible.
- Keep event handlers and state ownership explicit; lift state only to the closest useful owner.

### 6. Duplicated JSX and one-off CSS piles

Tell:
- Repeated `Icon + title + description` blocks differ only by literals.
- Long utility strings or arbitrary values are copied across components.
- Inline styles, local CSS modules, and global classes all set the same visual concepts.

Fix:
- Extract a local primitive only when it has a real reusable job.
- Promote repeated colors, radii, shadows, spacing, and motion into existing tokens or component variants.
- Keep Tailwind utility use idiomatic, but move recurring recipes into `cn`, `cva`, local variants, or project primitives when the repo already uses them.

### 7. Local design-system bypass

Tell:
- The page imports a new UI library or hand-rolls buttons, dialogs, menus, tabs, cards, or form controls when local primitives exist.
- shadcn/ui or Radix semantics are replaced with clickable `div`s or custom ARIA.
- Component states look different from adjacent app surfaces for no product reason.

Fix:
- Reuse existing primitives and semantic tokens first.
- If a primitive is too limited, extend it through its local variant/API pattern instead of styling around it at every call site.
- Preserve native semantics; add ARIA only when the role contract and keyboard behavior are complete.

## P1: Strong AI Aesthetic Tells

### 8. Default AI palette

Tell:
- Purple-to-blue gradients, indigo CTAs, cyan glows on dark backgrounds, gradient headline text, glass cards over blurred blobs.
- Many unrelated one-off accent colors with no palette logic.

Fix:
- Pick one aesthetic direction and encode it into tokens.
- Use one dominant neutral family, one supporting hue family, and one accent with a clear job.
- Replace decorative gradient text with composition, photography, texture, or shape if the content itself is the emphasis.

### 9. Default AI typography

Tell:
- Inter, Roboto, Arial, Open Sans, or system font stacks used as the entire visual personality.
- Monospace used as a lazy shorthand for "technical".
- Every heading and body block has the same weight, tracking, and rhythm.

Fix:
- Choose one distinctive display face plus one readable body face when the product brand allows it.
- If the codebase already has a typography system, tune the scale, line-height, and weight contrast instead of introducing a random new font.
- Keep body line length readable and use fluid type for hero/display text.

### 10. Cardocalypse

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

### 11. Icon-pill sameness

Tell:
- Large Lucide-style icon inside a rounded square/circle above every heading.
- Decorative icons that do not add information or action meaning.

Fix:
- Keep icons only where they improve scan or interaction clarity.
- Move iconography into one distinctive motif or structural treatment instead of repeating the same pill badge.
- Prefer domain-specific imagery, diagrams, or type-led hierarchy when icons are filler.

### 12. Template SaaS landing-page structure

Tell:
- Centered headline, subhead, two CTAs, hero mockup, then three feature cards, three metrics, testimonials, and a generic FAQ.
- "Everything centered" composition with no asymmetry or editorial rhythm.

Fix:
- Start from the job and audience, not a generic SaaS trope.
- Vary section geometry and alignment.
- Create one memorable section composition or interaction that feels specific to the product.
- If preserving structure, de-template one high-visibility section first: hero, primary feature block, or metrics.

### 13. Decorative motion and glow

Tell:
- Hover scale on every card, bouncy easing, endless float animations, glow borders, generic staggered fade-ins.
- Motion that signals "polish" but no state change or hierarchy.

Fix:
- Use one or two intentional motion moments tied to state, navigation, or reveal.
- Prefer transform/opacity, short durations, and smooth deceleration.
- Respect `prefers-reduced-motion`.

### 14. Generic AI marketing copy

Tell:
- Vague claims like "Transform your workflow", "Unlock insights", "Build the future".
- Repeated intro paragraphs that restate the section heading.
- Labels like "Submit", "Learn more", "Get started" with no concrete object or outcome.

Fix:
- Rewrite around specific user jobs, product objects, and outcomes.
- Use concrete button labels with verb + object.
- Remove duplicate preambles and make empty/error states teach the next action.

## P2: Craft And Design-System Drift

### 15. Uniform spacing and radius everywhere

Tell:
- The same padding, gap, border radius, and shadow on every section.
- No clear rhythm between dense and airy areas.

Fix:
- Build spacing rhythm: tighter within groups, larger between sections.
- Use a small, deliberate radius/shadow scale and assign each token a role.

### 16. Token inconsistency

Tell:
- Arbitrary hex colors, inline style values, or one-off utility classes scattered across components.
- Mixed border colors, background shades, and shadow strengths with no system.

Fix:
- Consolidate into CSS variables or existing semantic tokens.
- Prefer changing the design-system layer over patching every component individually.

### 17. Safe but forgettable detail work

Tell:
- Rounded rectangles, soft shadow, low-contrast gray text, and no distinctive shape language.
- Surfaces look polished in isolation but the page has no point of view.

Fix:
- Choose one memorable visual rule: a specific border treatment, image crop language, section rhythm, type contrast, or material texture.
- Apply it consistently in one or two places, not everywhere.

## P1/P2: Dense App And Dashboard Tells

### 18. Equal-weight dashboard tiles

Tell:
- Every KPI, chart, activity feed, and table sits in an equally styled card with the same emphasis.
- The primary user job is buried among peer tiles instead of getting a dominant region, persistent controls, or a clear drilldown path.

Fix:
- Promote one primary surface and one supporting surface.
- Use lower-chrome rows, tables, split panes, or grouped sections for secondary content instead of repeating card shells.
- Make filters and sort controls persistent and visually obvious.

### 19. Generic admin/settings scaffolding

Tell:
- Settings pages are a stack of identical cards with duplicated "Manage..." descriptions and vague toggles.
- Forms rely on placeholder text, ambiguous labels, and no helper/error copy.
- Destructive actions are styled like ordinary actions or hidden inside a generic modal.

Fix:
- Group settings by user task, not by visual container.
- Use specific labels, helper text, and action copy.
- Add clear destructive states and confirmation copy tied to the exact object/action.

### 20. Table and list polish without real data behavior

Tell:
- Beautiful but brittle tables that assume short names, no missing values, no pagination stress, and no row actions.
- Dense lists where every row has the same icon, same badge, and same preview text rhythm.

Fix:
- Test long text, missing values, many rows, and mobile collapse.
- Add sorting/filtering affordances where they are needed for the task.
- Use hierarchy, alignment, and compact row structure before adding another layer of card styling.

### 21. Faux analytics decoration

Tell:
- Tiny sparklines, arbitrary percentages, or chart cards included for visual sophistication but not decision support.
- Metrics have no time range, comparison baseline, or explanation of why they matter.

Fix:
- Keep metrics only when they answer a concrete product question.
- Attach timeframe, denominator, and comparison context.
- Replace decorative charts with a useful table, trend panel, or status summary when the chart has no real analytical job.

## Code Smell Search Patterns

Search for these framework-agnostic patterns before patching:

- hard-coded arrays or fixture literals in pages: `const features = [`, `const cards = [`, `stats = [`, `testimonials = [`
- broad boolean props: `is[A-Z]`, `has[A-Z]`, `show[A-Z]`, `with[A-Z]`, especially many on one component
- repeated variant strings and ad hoc styling: `variant ===`, `className={`, `style={{`, arbitrary Tailwind values
- new custom controls where primitives exist: `role="button"`, `onClick` on non-buttons, custom dialog/menu/tab code
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
2. Replace hard-coded fixture rendering with props/data and realistic states.
3. Extract or reuse the smallest local primitive needed to remove duplication.
4. Move repeated visual constants into existing tokens or component variants.
5. Replace one overused font stack or retune type hierarchy.
6. Simplify the palette and remove one obvious gradient/glow trope.
7. Delete unnecessary cards and flatten nested surfaces.
8. De-template one prominent section with a more specific composition.
9. Cut vague copy and rewrite CTAs around concrete actions.
10. Keep one purposeful motion or visual motif and remove the rest.

## Prompt Hygiene For New UI Generation

If the user asks you to generate a new interface from scratch, gather these constraints before coding when they are not already available:

- target audience and usage context
- primary job/action the screen must support
- brand tone and one aesthetic direction
- one or two reference products or visual cues to borrow from
- accessibility, performance, and framework constraints

Avoid prompts that only say "modern SaaS", "beautiful dashboard", or "clean landing page". Those prompts push models toward the statistical average.
