# Slidev Polishing Guide

This guide covers adding polish and interactive elements to your slides. Use this **after** you've completed your first draft (see [SLIDEV_DRAFTING.md](./SLIDEV_DRAFTING.md)).

## Workflow: Incremental Enhancement

**Polish Mode Approach:**
- Add animations incrementally to specific slides
- Enhance code displays only when needed
- Add visual polish selectively
- Sync presenter notes with animations
- Test and validate click timing

**Key Principle:** Don't try to polish everything at once. Identify specific slides that would benefit from enhancement, then add polish incrementally.

**CRITICAL: Polish One Slide at a Time**

This is a very human process that requires a lot of intervention and iteration. When polishing:

1. **Work on one slide at a time** - Don't try to polish multiple slides in one pass
2. **Test each slide** - View the slide in the browser and verify animations work correctly
3. **Get feedback** - Show the polished slide to get input before moving to the next
4. **Iterate** - Make adjustments based on feedback before proceeding
5. **Validate click timing** - Ensure all click animations align properly with presenter notes

**Avoid:** Polishing the entire deck in one go. This leads to errors, misaligned animations, and makes it harder to catch issues. Take it step by step, one slide at a time.

## Click Animations

Click animations reveal content progressively as you advance through a slide.

### v-click

The basic click animation directive:

```html
<!-- Component -->
<v-click>Hello World!</v-click>

<!-- Directive -->
<div v-click class="text-xl">Hey!</div>
```

Each `v-click` appears on the next sequential click.

### v-after

Use `v-after` to show content on the same click as the previous element:

```html
<div v-click>Hello</div>
<div v-after>World</div>  <!-- Shows with previous click -->
```

`v-after` doesn't increment the click counter - it appears with the previous click.

### v-clicks

Use `v-clicks` to automatically animate list items:

```html
<v-clicks>
- Item 1
- Item 2
- Item 3
</v-clicks>
```

Each list item appears on successive clicks automatically.

**Advanced Options:**

```html
<v-clicks depth="2">
- Item 1
  - Item 1.1
  - Item 1.2
- Item 2
</v-clicks>

<v-clicks every="2">
- Item 1.1
- Item 1.2
- Item 2.1
- Item 2.2
</v-clicks>
```

### Hide After Clicking

Hide elements after clicking:

```html
<div v-click>Visible after 1 click</div>
<div v-click.hide>Hidden after 2 clicks</div>
<div v-after.hide>Hidden after 2 clicks</div>

<v-click>Visible after 1 click</v-click>
<v-click hide>Hidden after 2 clicks</v-click>
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

### v-click Alignment

**CORRECT - Sequential clicks:**

```html
<div v-click>Appears on click 1</div>
<div v-click>Appears on click 2</div>
<div v-click>Appears on click 3</div>
```

**CORRECT - v-after appears with previous:**

```html
<div v-click>Click 1</div>
<div v-after>Also click 1</div>
<div v-click>Click 2</div>
```

**INCORRECT - Don't mix v-click and v-after randomly:**

```html
<!-- WRONG - Unclear timing -->
<div v-click>1</div>
<div v-click>2</div>
<div v-after>Also 2?</div>
<div v-click>3 or 4?</div>
```

**Common Mistake - Wrapping everything in v-click:**

```html
<!-- WRONG - Creates nested click timing issues -->
<div v-click>
  <span v-mark.underline>Mark won't align properly</span>
</div>
```

### v-mark Click Alignment

**CRITICAL:** v-mark elements must have explicit click numbers that match when they become visible.

**CORRECT - Text always visible, marks appear on clicks:**

```html
<span v-mark.underline="1">Underline mark</span>
<span v-mark.circle="2">Circle mark</span>
<span v-mark.box="3">Box mark</span>
```

**INCORRECT - Wrapping v-mark in v-click:**

```html
<!-- WRONG - Creates double-click requirement -->
<div v-click>
  <span v-mark.underline>Mark appears on click 2, not click 1</span>
</div>
```

**CORRECT - If you need v-click wrapper, specify click number:**

```html
<div v-click>
  <span v-mark.underline="1">Mark appears on click 1</span>
</div>
```

**Best Practice:** Keep v-mark elements unwrapped and use explicit click numbers:

```html
<div class="space-y-4">
  <div><span v-mark.underline="1">First mark</span></div>
  <div><span v-mark.circle="2">Second mark</span></div>
  <div><span v-mark.box="3">Third mark</span></div>
</div>
```

### v-clicks Alignment

`v-clicks` automatically handles click distribution. Don't mix with individual `v-click` on children.

**CORRECT:**

```html
<v-clicks>
  <li>Item 1 (click 1)</li>
  <li>Item 2 (click 2)</li>
  <li>Item 3 (click 3)</li>
</v-clicks>
```

**INCORRECT:**

```html
<v-clicks>
  <li v-click>Don't do this - breaks alignment</li>
  <li>Item 2</li>
</v-clicks>
```

### Click Counting Comments Pattern

**RECOMMENDED:** Add explicit click number comments to make auditing easier:

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

## Advanced Presenter Notes

### Using [click] Markers

Presenter notes MUST align with click animations using `[click]` markers. The last comment block of each slide is treated as presenter notes:

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

**INCORRECT - Notes don't match:**

```html
<!--
[click] Wrong - only one note for multiple clicks
-->

<div v-click>First</div>
<div v-click>Second</div>
<div v-click>Third</div>
```

Slidev divides content between click markers and highlights it in presenter notes, synchronized with slide progress.

## Visual Enhancements

### v-mark (Rough Notation)

Slidev integrates Rough Notation to mark or highlight elements. The `v-mark` directive works like `v-click` and triggers after a click.

**Type:**

```html
<span v-mark.underline>Underline mark (default)</span>
<span v-mark.circle>Circle mark</span>
<span v-mark.box>Box mark</span>
<span v-mark.highlight>Highlight mark</span>
```

**Color:**

```html
<span v-mark.red>Red notation</span>
<span v-mark.orange>Orange notation</span>
<span v-mark.circle.orange="4">Circle with orange color</span>
<span v-mark="{ color: '#234' }">Custom color</span>
```

**Clicks:**

```html
<span v-mark>Triggers after click</span>
<span v-mark="5">Triggers on click 5</span>
<span v-mark="'+1'">Triggers one click after previous</span>
```

**Combining Custom Color with Click Timing:**

When using custom colors, use the `at` property to specify click timing:

```html
<span v-mark.highlight="{ at: 1, color: '#fef08a' }">Highlighted on click 1</span>
<span v-mark.underline="{ at: 2, color: '#60a5fa' }">Underlined on click 2</span>
```

**Best Practices:**

- **Always use explicit click numbers** for v-mark to ensure proper alignment
- **Use a single consistent highlight style** per slide or section - don't mix underline, circle, box, and highlight on the same slide
- **Use light yellow color with click timing** - Always use `v-mark.highlight="{ at: N, color: '#fef08a' }"` where `N` is the click number. The `at` property specifies when the highlight appears, and `color` sets the light yellow color instead of default black
- **Keep it subtle** - highlighting should enhance, not distract

**Example with custom color and click timing:**

```html
<span v-mark.highlight="{ at: 1, color: '#fef08a' }">Highlighted text</span>
```

### Motion Animations

Motion animations are powered by @vueuse/motion. Use `v-motion` for smooth animations:

**Basic Usage:**

```html
<div
  v-motion
  :initial="{ x: -80, opacity: 0 }"
  :enter="{ x: 0, opacity: 1 }"
  :click-3="{ x: 80 }"
  :leave="{ x: 1000 }"
>
  Content
</div>
```

**Using Variables:**

```html
<script setup lang="ts">
const final = {
  x: 0,
  y: 0,
  rotate: 0,
  scale: 1,
  transition: {
    type: 'spring',
    damping: 10,
    stiffness: 20,
    mass: 2
  }
}
</script>

<img v-motion :initial="{ x: 800, y: -100, scale: 1.5 }" :enter="final" />
```

**Properties:** `:initial`, `:enter`, `:click-N`, `:leave`

**Transition:**

```html
:enter="{ 
  x: 0, 
  opacity: 1, 
  transition: { 
    delay: 2000, 
    duration: 1000,
    type: 'spring',
    damping: 10,
    stiffness: 20
  } 
}"
```

### Slide Transitions

Set slide transitions in frontmatter:

```markdown
---
transition: slide-left
---

---
transition: fade-out
---

---
transition: slide-up
---
```

Common transitions: `slide-left`, `slide-right`, `slide-up`, `slide-down`, `fade`, `fade-out`, `zoom`, `none`.

## Advanced Code Features

### Line Highlighting

Add line numbers within brackets `{}` to highlight specific lines. Line numbers start counting from 1:

```ts {2,3}
function add(
  a: Ref<number> | number,
  b: Ref<number> | number
) {
  return computed(() => unref(a) + unref(b))
}
```

### Dynamic Line Highlighting

Use `|` to separate stages for progressive highlighting with multiple clicks:

```ts {2-3|5|all}
function add(
  a: Ref<number> | number,
  b: Ref<number> | number
) {
  return computed(() => unref(a) + unref(b))
}
```

This highlights lines 2-3 first, then line 5, then all lines.

### Code Highlighting Best Practices

**CRITICAL: Count lines carefully and thoughtfully**

When adding code highlighting, follow these steps:

1. **Count lines from the start of the code block** - Line numbers start at 1, not 0
2. **Include blank lines in your count** - Blank lines are still lines and affect line numbers
3. **Verify your line numbers** - Read through the code block and manually count to verify:
   - Start at line 1 (first line of code)
   - Count every line including blank lines
   - Double-check ranges (e.g., `{5-8}` means lines 5, 6, 7, and 8)
4. **Group logically** - Highlight related code together:
   - Imports together
   - Class definitions together
   - Related function calls together
   - Don't split logical units across highlights
5. **Test the highlighting** - View the slide in the browser to verify the correct lines are highlighted
6. **Common mistakes to avoid:**
   - Off-by-one errors (forgetting blank lines or starting at 0)
   - Highlighting unrelated code together
   - Highlighting too many lines at once (hard to follow)
   - Highlighting too few lines (missing context)

**Example - Correct counting:**

```python
1| import instructor          # Line 1
2| from pydantic import BaseModel  # Line 2
3|                            # Line 3 (blank)
4| class Person(BaseModel):   # Line 4
5|     name: str              # Line 5
6|     age: int               # Line 6
```

Correct highlighting: `{1-2|4-6}` (imports first, then class definition)
Incorrect: `{1-3|5-6}` (includes blank line in first group, misses class declaration line)

### Code Snippets

Import code from external files using regions:

**Create:**

```typescript
// #region snippet
export function reusableFunction() { /* code */ }
// #endregion snippet
```

**Import:** `<<< @/snippets/external.ts#snippet`

### Monaco Editor

Add `{monaco}` after the language id to turn a code block into a fully-featured Monaco editor:

```ts {monaco}
console.log('HelloWorld')
```

**Diff Editor:**

Use `{monaco-diff}` to create a diff editor. Use `~~~` to separate original and modified code:

```ts {monaco-diff}
console.log('Original text')

~~~

console.log('Modified text')
```

**Monaco Run:**

Use `{monaco-run}` to create an editor that can execute code directly in the slide:

```ts {monaco-run}
import { version } from 'vue'
import { emptyArray, sayHello } from './external'

sayHello()
console.log(`vue ${version}`)
console.log(emptyArray<number>(10).reduce(fib => [...fib, fib.at(-1)! + fib.at(-2)!], [1, 1]))
```

### Shiki Magic Move

Shiki Magic Move enables animations across multiple code snippets. Wrap multiple code blocks with ````md magic-move` (four backticks) to enable magic move:

````md magic-move {lines: true}
```ts {*|2|*}
// step 1
const author = reactive({
  name: 'John Doe',
  books: ['Vue 2 - Advanced Guide']
})
```

```ts {*|1-2|3-4}
// step 2
export default {
  data() {
    return {
      author: {
        name: 'John Doe',
        books: ['Vue 2 - Advanced Guide']
      }
    }
  }
}
```
````

Non-code blocks are ignored. Use line highlighting syntax `{*|2|*}` to control which lines animate.

## Styling & Polish

### Slide-Specific CSS

Use `<style>` tags for slide-specific CSS:

```html
<style>
h1 {
  background-color: #2B90B6;
  background-image: linear-gradient(45deg, #4EC5D4 10%, #146b8c 20%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.custom-box {
  padding: 20px;
  border: 2px solid #2B90B6;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}
</style>

<div class="custom-box">
Styled content with custom CSS
</div>
```

### MDC Syntax

Slidev supports optional MDC (Markdown Components) Syntax powered by markdown-it-mdc.

Enable it by adding `mdc: true` to the slide's frontmatter:

```markdown
---
mdc: true
---

This is [red text]{style="color:red"} :inline-component{prop="value"}

![](/image.png){width=500px lazy}

::block-component{prop="value"}

The **default** slot

::
```

## Validation & Alignment

### Click Alignment Checklist

Before finalizing slides, verify:

1. **Count all v-click directives** - Each increments the counter
2. **v-after elements** - Must appear with previous click (don't increment counter)
3. **v-mark elements** - Must have explicit click numbers matching visibility
4. **v-clicks** - Don't mix with individual v-click on children
5. **Presenter notes** - Must have `[click]` markers matching each v-click
6. **Click comments** - Add `<!-- Click N -->` comments for complex slides
7. **Test the slide** - Click through and verify timing matches expectations

### Manual Audit Process

When auditing clicks, follow this process:

1. **Scan for all click directives:**
   ```bash
   grep -n "v-click\|v-after\|v-clicks\|v-mark" slides.md
   ```

2. **Count clicks sequentially:**
   - Each `v-click` = +1 click
   - Each `v-after` = same click as previous
   - Each `v-clicks` = +N clicks (where N = number of children)
   - Each `v-mark="N"` = mark appears on click N

3. **Verify presenter notes:**
   ```bash
   grep -n "\[click" slides.md
   ```
   - Count `[click]` markers
   - Should match total number of clicks

4. **Check v-mark alignment:**
   - All v-mark should have explicit click numbers
   - Click numbers should match when text becomes visible
   - If text is always visible, marks should be sequential (1, 2, 3...)

### Constraints to Prevent Mistakes

**ENFORCE THESE RULES:**

1. **Always use explicit click numbers for v-mark** - Never rely on default behavior
2. **Never wrap v-mark in v-click** - Keep marks unwrapped with explicit numbers
3. **Always add click comments for slides with 3+ clicks** - Makes auditing trivial
4. **Presenter notes must have [click] markers** - One per v-click/v-clicks item
5. **Test every slide manually** - Click through and verify timing

### Common Alignment Mistakes

**Mistake 1: v-mark without click numbers**

```html
<!-- WRONG -->
<span v-mark.underline>Mark</span>
<span v-mark.circle>Mark</span>
<!-- Marks appear randomly, not aligned -->
```

**Correct example:**

```html
<!-- CORRECT -->
<span v-mark.underline="1">Mark appears on click 1</span>
<span v-mark.circle="2">Mark appears on click 2</span>
```

**Mistake 2: Nested v-click with v-mark**

```html
<!-- WRONG -->
<div v-click>
  <span v-mark>Mark appears on click 2, not click 1</span>
</div>
```

**Correct example:**

```html
<!-- CORRECT -->
<div v-click>
  <span v-mark.underline="1">Mark appears on click 1</span>
</div>
<span v-mark.circle="2">Second mark on click 2</span>
```

**Mistake 3: Presenter notes missing [click] markers**

```html
<!-- WRONG -->
<!--
All notes highlight at once
-->

<div v-click>First</div>
<div v-click>Second</div>
```

**Correct example:**

```html
<!-- CORRECT -->
<!--
[click] Note for first click
[click] Note for second click
-->

<div v-click>First</div>
<div v-click>Second</div>
```

**Mistake 4: Mixing v-click and v-after inconsistently**

```html
<!-- WRONG - Unclear timing -->
<div v-click>1</div>
<div v-click>2</div>
<div v-after>Also 2?</div>
<div v-click>3 or 4?</div>
```

**Correct example:**

```html
<!-- CORRECT -->
<div v-click>1</div>
<div v-after>Also 1</div>
<div v-click>2</div>
```

## Summary

Polish mode is about incremental enhancement:

1. Start with content from your first draft
2. Identify specific slides that need emphasis
3. Add click animations selectively
4. Sync presenter notes with `[click]` markers
5. Validate and test timing
6. Add visual enhancements only where they add value

Remember: Don't polish everything at once. Enhance incrementally, test thoroughly, and keep your content clear and focused.

