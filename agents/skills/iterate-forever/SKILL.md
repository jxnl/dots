---
name: iterate-forever
description: Visual-reference-to-app implementation loop for building or restyling a web app screen to match a provided reference image. Use when Codex is asked to take a screenshot/reference/mockup/image and build an app or route that looks like it, especially when the task requires hosting the app, capturing Playwright screenshots, comparing against the reference, and repeatedly editing until the result is close.
---

# Iterate Forever

## Workflow

Use this skill for visual imitation work where the output is an app screen, not an image edit.

1. Establish the target.
   - Load the reference image with `view_image` when it is a local file or attached image.
   - Identify the intended app route, framework, viewport, and source files before editing.
   - If several reference screens belong to the same deliverable, prefer one hosted app with multiple routes over separate apps or dev servers. Let the shared dev server and HMR rebuild as route files change.
   - When multiple agents are working, keep shared scaffold edits local to the orchestrating agent first, then assign each worker a disjoint route/persona directory. Workers should not edit shared app files unless explicitly assigned.
   - If the repo has an `AGENTS.md`, update it when the workflow reveals a durable rule or routing convention future agents should inherit.
   - Preserve the existing product concept and copy unless the user asks for a redesign.
   - Treat third-party screenshots as references only; recreate the lookalike UI in code rather than embedding vendor screenshots, logos, or exact branded chrome.

2. Build the first pass.
   - Implement the smallest durable app changes that move the screen toward the reference.
   - Use Tailwind for layout and visual styling when the app is a Tailwind project or when adding Tailwind is part of the setup.
   - Use `$shadcn` when the app has a `components.json`, shadcn components, or the user requests shadcn/ui. Prefer existing shadcn components and compose them before writing custom component markup.
   - For Vite/React apps that are being set up from scratch for this workflow, make them Tailwind-ready and shadcn-aware unless the repo clearly uses a different design system.
   - It is OK to add focused design or visualization packages when they materially improve fidelity; inspect the package manager and existing dependencies first, keep additions purposeful, and avoid broad frameworks for one small effect.
   - Match composition first: viewport size, panel geometry, density, hierarchy, background, chrome, rails, toolbars, major content blocks.
   - Then match details: typography scale, spacing, borders, shadows, chart/canvas treatment, icons, data density, and selected/active states.
   - Make the screen responsive across the viewports relevant to the shoot or product surface. Text, panels, and controls must fit within their containers without clipping.
   - When the UI is built around desktop windows, make the windows movable and resizable unless the user explicitly asks for a static screenshot-style composition.
   - Prefer structured data and existing components over one-off hardcoded markup unless this is explicitly a shoot mockup.

3. Host and capture.
   - Use the repo's existing dev command. For Node projects with `pnpm`, prefer `corepack pnpm`.
   - Keep the server running in a terminal session until captures and validation are complete.
   - For one-app/multi-route work, start or reuse the single shared dev server. Workers should open their route and capture screenshots; they should not start separate servers unless the shared server is unreachable.
   - Tell route workers the exact shared URL when known so they only need to reload and capture their route while HMR rebuilds changes.
   - Use `$playwright-interactive` for fast iterative browser work when `js_repl` is available; keep the same browser handles alive across edit/reload/capture loops.
   - Use `$playwright` for CLI-first browser automation, snapshots, and screenshots from the terminal, especially for reproducible artifact capture under `output/playwright/`.
   - Use Playwright to open the target route at the intended viewport and save a screenshot under an existing output folder such as `output/playwright/`, or a clearly named new subfolder if none exists.
   - Capture the full browser/app area consistently across iterations; do not compare one pass at a different viewport unless the user asked for a responsive check.
   - Include at least one alternate viewport capture when responsive behavior is part of the request.

4. Compare like a reviewer.
   - Open the latest screenshot and the reference side by side, or generate a simple contact sheet when useful.
   - Name the largest visible deltas before editing: layout proportions, missing surfaces, wrong density, colors, text scale, chart/canvas fidelity, edge alignment, or fake-looking details.
   - Check interaction basics for movable/resizable windows: drag handles work, resize handles stay reachable, and content remains usable after resizing.
   - Fix the highest-impact deltas first. Do not churn small polish before the main structure matches.

5. Iterate.
   - Repeat: edit -> capture -> compare -> edit.
   - Continue until the screenshot is defensibly close, the remaining deltas are minor or explicitly accepted, or a real blocker appears.
   - If the user says "continue", "keep going", or similar, keep iterating instead of summarizing.

6. Run the stop check.
   - Before giving a final answer, ask yourself: "Are you ever really done?"
   - If there is still a clear visual delta and no blocker, do one more edit/capture/compare pass instead of stopping.
   - Stop only when the remaining issues are minor enough to state plainly, the user has accepted the result, or further progress is blocked by missing context, tooling, or assets.

## Practical Playwright Pattern

Prefer existing repo helpers. If none exist, use an inline Playwright script or the repo package runner:

```bash
corepack pnpm exec playwright screenshot --viewport-size=1440,900 http://localhost:5173/target-route output/playwright/iterate-forever/pass-01.png
```

If the project does not use `pnpm`, use the package manager already present in the repo. If Playwright is not installed, inspect `package.json` before adding dependencies; for a one-off capture, prefer an existing browser/capture tool already in the repo.

## Completion Notes

In the final response, report the route or files changed, the latest screenshot path, and any validation that ran. If captures could not be run, say exactly why.
