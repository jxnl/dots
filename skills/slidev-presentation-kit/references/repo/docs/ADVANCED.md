# Advanced Features: Monaco, Magic Move & More

Advanced features for complex presentations. Use these when basic features aren't sufficient.

## Monaco Editor

### Basic Monaco Editor

Add `{monaco}` to make code editable:

```ts {monaco}
const message = 'Hello, Slidev!'
console.log(message)
```

### Monaco Diff Editor

Use `{monaco-diff}` with `~~~` separator:

```ts {monaco-diff}
const oldCode = 'original'
const result = oldCode + ' value'

~~~

const newCode = 'updated'
const result = newCode + ' value'
```

### Monaco Run

Execute code directly in slides:

```ts {monaco-run}
import { version } from 'vue'
import { emptyArray, sayHello } from './external'

sayHello()
console.log(`vue ${version}`)
```

## Shiki Magic Move

Animate code changes across multiple snippets. Wrap multiple code blocks with ````md magic-move`:

````md magic-move {lines: true}
```ts {*|2|*}
// Step 1: Reactive object
const author = reactive({
  name: 'John Doe',
  books: ['Vue 2 - Advanced Guide']
})
```

```ts {*|1-2|3-4}
// Step 2: Options API
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

## Motion Animations

Motion animations powered by @vueuse/motion:

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

## Slide Transitions

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

## Code Snippets

Import code from external files using regions:

**Create:**

```typescript
// #region snippet
export function reusableFunction() { /* code */ }
// #endregion snippet
```

**Import:** `<<< @/snippets/external.ts#snippet`

## MDC Syntax

Slidev supports optional MDC (Markdown Components) Syntax. Enable with `mdc: true` in frontmatter:

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

## Slide-Specific CSS

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
}
</style>

<div class="custom-box">
Styled content
</div>
```

