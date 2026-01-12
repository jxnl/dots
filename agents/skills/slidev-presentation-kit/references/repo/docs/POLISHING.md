# Adding Animations & Polish

Add animations and enhancements to existing slides. Use this **after** content is complete.

## When to Polish

**Only polish after:**

- Content is complete and structure is solid
- Narrative flows well
- Speaker notes are written

**Never polish during first draft** - See [DRAFTING.md](./DRAFTING.md) for content creation workflow.

## Workflow: Incremental Enhancement

**Polish Mode Approach:**

- Add animations incrementally to specific slides
- Enhance code displays only when needed
- Add visual polish selectively
- Sync presenter notes with animations
- Test and validate click timing

**Key Principle:** Don't try to polish everything at once. Identify specific slides that would benefit from enhancement, then add polish incrementally.

## CRITICAL: Polish One Slide at a Time

This is a very human process that requires intervention and iteration:

1. **Work on one slide at a time** - Don't try to polish multiple slides in one pass
2. **Test each slide** - View the slide in the browser and verify animations work correctly
3. **Get feedback** - Show the polished slide to get input before moving to the next
4. **Iterate** - Make adjustments based on feedback before proceeding
5. **Validate click timing** - Ensure all click animations align properly with presenter notes

**Avoid:** Polishing the entire deck in one go. This leads to errors, misaligned animations, and makes it harder to catch issues.

## Click Animations

### v-click

Basic click animation directive:

```html
<div v-click>Appears on first click</div>
<div v-click>Appears on second click</div>
```

Each `v-click` appears on the next sequential click.

### v-after

Show content on the same click as the previous element:

```html
<div v-click>Hello</div>
<div v-after>World</div>  <!-- Shows with previous click -->
```

`v-after` doesn't increment the click counter.

### v-clicks

Automatically animate list items:

```html
<v-clicks>
- Item 1
- Item 2
- Item 3
</v-clicks>
```

Each list item appears on successive clicks automatically.

### Hide After Clicking

```html
<div v-click>Visible after 1 click</div>
<div v-click.hide>Hidden after 2 clicks</div>
```

## Click Animation Alignment - CRITICAL

**ALWAYS ensure click animations are properly aligned.** Misaligned clicks create a poor presentation experience.

### How Click Counting Works

Slidev counts clicks sequentially starting from 1. Each `v-click` directive increments the click counter.

**Basic Rules:**

- `v-click` - Appears on the next click (sequential)
- `v-after` - Appears on the same click as the previous element (doesn't increment counter)
- `v-clicks` - Automatically distributes clicks across children (N clicks for N children)
- `v-mark="N"` - Marks appear on click N (must match when element becomes visible)
- **Code highlighting** - First item shows initially (no click), then each `|` requires a click
  - Example: `{1|3-4|6-8|all}` = line 1 visible initially, then 3 clicks for remaining transitions

### Click Counting Comments Pattern

**RECOMMENDED:** Add explicit click number comments:

```html
<!-- Click 1 -->
<div v-click>First item</div>

<!-- Click 2 -->
<div v-click>Second item</div>

<!-- Click 3 (appears with Click 2) -->
<div v-after>Also appears on click 2</div>

<!-- Clicks 4-7 (v-clicks handles 4 items) -->
<v-clicks>
  <li>Item 1</li>
  <li>Item 2</li>
  <li>Item 3</li>
  <li>Item 4</li>
</v-clicks>
```

This makes it immediately obvious:

- How many clicks are on a slide
- What appears on each click
- Whether v-after is used correctly
- Whether presenter notes match

### Complete Example with Speaker Notes

```html
<!-- Click 1 -->
<div v-click>

**Header text**

</div>

<!-- Click 2-4 -->
<v-clicks>

- First item
- Second item
- Third item

</v-clicks>

<!-- Click 5 -->
<div v-click>

Conclusion text

</div>

<!--
Initial content is visible.

[click] Header appears.

[click] First item.

[click] Second item.

[click] Third item.

[click] Conclusion.
-->
```

**Tip:** More than 5-6 clicks per slide can overwhelm the audience. Group related items together instead of animating each one individually.

## Presenter Notes with [click] Markers

Presenter notes MUST align with click animations using `[click]` markers:

```html
<!--
Introduction text before first click

[click] This note highlights when first v-click appears

[click] This note highlights when second v-click appears

[click] This note highlights when third v-click appears
-->

<div v-click>First content</div>
<div v-click>Second content</div>
<div v-click>Third content</div>
```

**Key Points:**

- Use `[click]` markers to sync note highlighting with slide clicks
- Each `[click]` marker corresponds to one click animation
- Notes highlight progressively as you click through the slide
- Use `[click:N]` to skip clicks (e.g., `[click:3]` skips two clicks)

## Visual Enhancements

### v-mark (Rough Notation)

Mark and highlight elements:

```html
<span v-mark.underline="1">Underline mark</span>
<span v-mark.circle="2">Circle mark</span>
<span v-mark.highlight="{ at: 1, color: '#fef08a' }">Highlighted text</span>
```

**Best Practices:**

- Always use explicit click numbers for v-mark
- Use a single consistent highlight style per slide
- Use light yellow color with click timing: `v-mark.highlight="{ at: N, color: '#fef08a' }"`
- Keep it subtle

### Motion Animations

For motion animations, see [ADVANCED.md](./ADVANCED.md).

## Code Enhancements

### Dynamic Line Highlighting

Use `|` to separate stages for progressive highlighting:

```ts {2-3|5|all}
function add(
  a: number,
  b: number
) {
  return a + b
}
```

This highlights lines 2-3 first, then line 5, then all lines.

### Code Highlighting Best Practices

**CRITICAL:** Count lines carefully

1. Count lines from the start of the code block (starts at 1, not 0)
2. Include blank lines in your count
3. Verify your line numbers by manually counting
4. Group logically (imports together, class definitions together)
5. Test the highlighting in the browser

For advanced code features (Monaco editor, Magic Move), see [ADVANCED.md](./ADVANCED.md).

## Validation Checklist

Before finalizing slides, verify:

1. Count all v-click directives - Each increments the counter
2. v-after elements - Must appear with previous click (don't increment counter)
3. v-mark elements - Must have explicit click numbers matching visibility
4. v-clicks - Don't mix with individual v-click on children
5. Presenter notes - Must have `[click]` markers matching each v-click
6. Click comments - Add `<!-- Click N -->` comments for complex slides
7. Test the slide - Click through and verify timing matches expectations

## Summary

Polish mode is about incremental enhancement:

1. Start with content from your first draft
2. Identify specific slides that need emphasis
3. Add click animations selectively
4. Sync presenter notes with `[click]` markers
5. Validate and test timing
6. Add visual enhancements only where they add value

Remember: Don't polish everything at once. Enhance incrementally, test thoroughly, and keep your content clear and focused.
