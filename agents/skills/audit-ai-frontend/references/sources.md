# Source Basis

This skill treats "AI-looking" UI as a quality pattern, not a provenance claim. Use these sources as background for prompt refreshes; do not load them for every audit.

Web refreshed: 2026-06-15.

## AI-Shaped UI Risks

- CrowdGenUI on LLM UI generation producing generic solutions that miss task context and user preferences: `https://arxiv.org/abs/2411.03477`
- VISTA benchmark on visual spec-to-web-app agents; evaluates structural alignment, behavior, and visual fidelity together: `https://arxiv.org/abs/2605.26144`
- Wikipedia on AI slop terminology: `https://en.wikipedia.org/wiki/AI_slop`

## Component Structure And Tokens

- React "Thinking in React" for mapping UI to component hierarchy, data model, props, and minimal state: `https://react.dev/learn/thinking-in-react`
- React "Passing Props to a Component" for prop-driven component customization: `https://react.dev/learn/passing-props-to-a-component`
- Tailwind responsive design for mobile-first breakpoints and container-query variants: `https://tailwindcss.com/docs/responsive-design`
- Tailwind theme variables for tokens as the utility API: `https://tailwindcss.com/docs/theme`
- shadcn/ui theming for semantic CSS variables, token pairs, and radius scales: `https://ui.shadcn.com/docs/theming`
- Design Tokens Format Module for token vocabulary, aliases, and cross-tool exchange: `https://www.designtokens.org/tr/drafts/format/`

## Accessibility And Verification

- WCAG 2.2 for objective accessibility requirements: `https://www.w3.org/TR/WCAG22/`
- WAI-ARIA APG "Read Me First" for native semantics first and role contracts: `https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/`
- Playwright visual comparisons for screenshot baselines and environment sensitivity: `https://playwright.dev/docs/test-snapshots`
- Playwright accessibility testing with axe and the automated-plus-manual testing boundary: `https://playwright.dev/docs/accessibility-testing`
- Playwright ARIA snapshots for role/name/structure verification: `https://playwright.dev/docs/aria-snapshots`
- Storybook interaction, accessibility, and visual tests for component-level state coverage: `https://storybook.js.org/docs/writing-tests/interaction-testing`, `https://storybook.js.org/docs/writing-tests/accessibility-testing`, `https://storybook.js.org/docs/writing-tests/visual-testing`
