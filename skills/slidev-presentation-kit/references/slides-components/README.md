# Components

All components in this directory are automatically available in any Slidev deck without manual imports. They can be used directly in markdown slides using Vue syntax.

## Available Components

- [Callout](#callout) - Highlight information with styled callout boxes
- [Chart](#chart) - Data visualization with bar, line, and doughnut charts
- [FileExplorer](#fileexplorer) - Interactive file tree explorer with syntax highlighting
- [QRCode](#qrcode) - Generate QR codes dynamically
- [Terminal](#terminal) - Display terminal commands with syntax highlighting
- [AgentView](#agentview) - Visualize AI agent interactions and thought processes

---

## AgentView

Visualize the step-by-step thought process and actions of an AI agent in a Cursor-style interface. Perfect for explaining how agents work, from user queries to tool usage and final responses.

**File:** `AgentView.vue`

### Usage

```html
<AgentView 
  query="read some tiles and return"
  :events="[
    { type: 'status', content: 'Reading a few files and returning their contents.' },
    { type: 'files-explored', exploredCount: 4 },
    { type: 'files-edited', editedCount: 3 },
    { 
      type: 'files-read',
      content: 'Component documentation covering:',
      files: [
        { path: 'slides/components/README.md', lines: 503 }
      ]
    },
    { type: 'assistant', content: 'Summary of findings...' }
  ]"
  :height="400"
/>
```

### Props

- `events` (required) - Array of event objects
- `query` (optional) - User query to display in the input field at the top. If not provided, uses the first `user` event's content
- `stepByStep` (optional, default: `true`) - Whether to animate/reveal steps sequentially with clicks
- `height` (optional, default: 500) - Height of the component in pixels. Content area is scrollable

### Event Types

Each event object in the `events` array requires a `type` and `content`:

- `user` - User input/query (displayed in input field if `query` prop not provided)
- `status` - Status messages (e.g., "Reading files...")
- `files-explored` - File exploration status (e.g., "Explored 4 files >")
- `files-edited` - File editing status (e.g., "Edited 3 files >")
- `files-read` - List of files that were read with paths and line counts
- `tool-call` - Executing a tool (Blue text)
- `tool-result` - Output from a tool (Green text)
- `thought` - Internal reasoning (Italic, gray)
- `assistant` - Final response or summary

### Event Properties

- `content` (required for most types) - Text content to display (supports Markdown formatting)
- `title` (optional) - Custom title for tool calls
- `args` (optional) - Object to display structured arguments (for `tool-call`)
- `exploredCount` (optional) - Number of files explored (for `files-explored`)
- `editedCount` (optional) - Number of files edited (for `files-edited`)
- `files` (optional) - Array of file objects `{ path: string, lines?: number, description?: string }` (for `files-read`)

### Features

- Dark-themed console-style interface matching Cursor's agent view
- Scrollable content area for long event sequences
- Query input field at the top
- Supports file lists with highlighted paths
- Sequential reveal with `v-click` animations (when `stepByStep` is true)

---

## Callout

Highlight important information with styled callout boxes. Perfect for drawing attention to tips, warnings, success messages, errors, and notes.

**File:** `Callout.vue`

### Usage

```html
<Callout type="info">
This is an informational callout with helpful context.
</Callout>

<Callout type="warning" title="Important">
Make sure to save your work before proceeding.
</Callout>

<Callout type="success">
Operation completed successfully!
</Callout>

<Callout type="error" title="Error">
Something went wrong. Please try again.
</Callout>

<Callout type="tip" title="Pro Tip">
Use keyboard shortcuts to navigate faster.
</Callout>

<Callout type="note" title="Note">
This is a general note callout.
</Callout>
```

### Props

- `type` (optional, default: `'info'`) - One of: `info`, `warning`, `success`, `error`, `tip`, `note`
- `title` (optional) - Title text displayed above the content

### Available Types

- `info` - Blue, informational content
- `warning` - Yellow/amber, important warnings
- `success` - Green/emerald, success messages
- `error` - Red/rose, error messages
- `tip` - Purple/violet, helpful tips
- `note` - Gray, general notes

### Usage with Click Animations

Callouts work great with click animations to reveal information progressively:

```html
<!-- Click 1 -->
<Callout type="info" v-click>
This callout appears after the first click.
</Callout>

<!-- Click 2 -->
<Callout type="warning" v-click>
This warning appears after the second click.
</Callout>
```

---

## Chart

Visualize data with bar, line, and doughnut charts powered by Chart.js. Perfect for data-driven presentations.

**File:** `Chart.vue`

### Usage

```html
<!-- Bar Chart -->
<Chart 
  type="bar"
  title="Monthly Sales"
  :labels="['Jan', 'Feb', 'Mar', 'Apr', 'May']"
  :datasets="[{
    label: 'Sales',
    data: [12, 19, 3, 5, 2]
  }]"
/>

<!-- Line Chart -->
<Chart 
  type="line"
  title="User Growth"
  :labels="['Q1', 'Q2', 'Q3', 'Q4']"
  :datasets="[{
    label: 'Users',
    data: [100, 150, 200, 250]
  }]"
/>

<!-- Doughnut Chart -->
<Chart 
  type="doughnut"
  title="Device Distribution"
  :labels="['Mobile', 'Desktop', 'Tablet']"
  :datasets="[{
    data: [45, 30, 15],
    backgroundColor: ['#3B82F6', '#10B981', '#F59E0B']
  }]"
  :height="400"
/>
```

### Props

- `type` (required) - Chart type: `bar`, `line`, or `doughnut`
- `labels` (required) - Array of label strings for the x-axis (or categories for doughnut)
- `datasets` (required) - Array of dataset objects (see Chart.js documentation for full options)
- `title` (optional) - Chart title displayed above the chart
- `height` (optional, default 400) - Chart height in pixels

### Chart Types

- **Bar** - Vertical bar chart for comparing categories
- **Line** - Line chart for showing trends over time
- **Doughnut** - Circular chart for showing proportions

### Customization

You can override any Chart.js dataset options by passing them in the `datasets` array:

```html
<Chart 
  type="bar"
  :labels="['A', 'B', 'C']"
  :datasets="[{
    label: 'Custom',
    data: [10, 20, 30],
    backgroundColor: '#FF5733',
    borderColor: '#C0392B',
    borderWidth: 3
  }]"
/>
```

---

## FileExplorer

Display an interactive file tree explorer with syntax-highlighted code viewing. Perfect for code walkthroughs, showing project structures, or exploring configuration files.

**File:** `FileExplorer.vue`

### Usage

```html
<FileExplorer dir="components/example_fs/fastapi-app" />
```

### Props

- `dir` (required) - Directory path relative to `slides/decks/`. For example, `"components/example_fs/fastapi-app"` will display files from `slides/decks/components/example_fs/fastapi-app/`.

### Features

- Interactive file tree sidebar with expandable folders
- Click files to view their contents with syntax highlighting
- Automatically expands all folders and selects the first file on mount
- Supports syntax highlighting for many languages (Python, TypeScript, JavaScript, Markdown, JSON, YAML, Bash, Vue, HTML, CSS, Rust, Go, Java, C/C++, and more)
- Uses VS Code-style file icons
- Dark theme optimized for code display

### Example

```html
<FileExplorer dir="components/example_fs/fastapi-app" />
```

This will show all files and folders within the specified directory, allowing users to navigate and view file contents directly in the slide.

---

## QRCode

Generate QR codes dynamically in your slides. Useful for sharing links, resources, or follow-up materials.

**File:** `QRCode.vue`

### Usage

```html
<QRCode url="https://example.com" />

<QRCode url="https://example.com" size="250" caption="Scan to visit" />
```

### Props

- `url` (required) - URL to encode in QR code
- `size` (optional, default 200) - Size in pixels
- `caption` (optional) - Text to display below QR code

### Example

```html
<QRCode 
  url="https://sli.dev" 
  size="150" 
  caption="Scan to visit Slidev documentation" 
/>
```

---

## Terminal

Display terminal commands with syntax highlighting and optional output. Useful for showing installation instructions, command-line examples, API responses, or any terminal-based workflows.

**File:** `Terminal.vue`

### Usage

```html
<!-- Single command with output -->
<Terminal 
  command="npm install slidev"
  output="added 152 packages in 2m"
/>

<!-- Multiple commands -->
<Terminal 
  :lines="[
    { command: 'cd my-project', prompt: '$' },
    { command: 'npm install', output: 'added 152 packages' },
    { command: 'npm run dev', output: 'Server running on http://localhost:3030' }
  ]"
  :height="250"
/>

<!-- With JSON output -->
<Terminal 
  command="curl https://api.example.com/data"
  output='{
  "status": "success",
  "data": { "id": 123 }
}'
/>

<!-- Different shell types -->
<Terminal shell="bash" prompt="$" command="echo 'Hello'" />
<Terminal shell="powershell" prompt="PS>" command="Write-Host 'Hello'" />
```

### Props

- `command` (optional) - Single command to display
- `output` (optional) - Output text for the command
- `lines` (optional) - Array of command/output objects `{ command: string, output?: string, prompt?: string }`
- `prompt` (optional, default `'$'`) - Prompt symbol to display before commands
- `shell` (optional, default `'bash'`) - Shell type: `bash`, `zsh`, `powershell`, or `cmd`
- `title` (optional) - Custom title for the terminal header
- `height` (optional, default 300) - Height of the terminal in pixels
- `copyable` (optional, default true) - Show copy button on hover

### Features

- Syntax highlighting for commands using Shiki (same as FileExplorer)
- Automatic JSON detection and highlighting for output
- Copy-to-clipboard functionality for commands
- Supports multiple command/output pairs
- Consistent styling with FileExplorer component
- Dark theme optimized for code display

---

## Using Components

All components are automatically available in any deck without manual imports. They can be used directly in markdown slides:

```markdown
# My Slide

<Callout type="info">
This is a callout!
</Callout>

<Terminal command="echo 'Hello'" />
```

Components support all Vue directives like `v-click`, `v-motion`, and more:

```html
<Callout type="warning" v-click>
This appears after a click.
</Callout>
```

---

## Style Guide

This section documents the design system and styling conventions used across all components. Follow these guidelines when creating new components or modifying existing ones.

### Color Palette

**Primary Colors** (from `style.css`):
- Primary: `#3B82F6` (Blue-500)
- Primary Dark: `#2563EB` (Blue-600)
- Accent: `#8B5CF6` (Violet-500)
- Secondary: `#10B981` (Emerald-500)

**Text Colors**:
- Heading (light): `#111827` (Gray-900)
- Body (light): `#374151` (Gray-700)
- Heading (dark): `#F9FAFB` (Gray-50)
- Body (dark): `#D1D5DB` (Gray-300)

**Background Colors**:
- Light: `#ffffff`
- Dark: `#111827` (Gray-900)
- Soft (light): `#F3F4F6` (Gray-100)
- Soft (dark): `#1F2937` (Gray-800)

**Border Colors**:
- Light: `#E5E7EB` (Gray-200)
- Dark: `#374151` (Gray-700)

### Typography

**Fonts**:
- Body: `'Inter'` (weights 300-800)
- Code: `'JetBrains Mono'` (weights 400-600)

**Font Sizes**:
- Component text: `text-sm` (0.875rem)
- Headers: `text-xs` (0.75rem) for labels/headers
- Code: `text-sm` (0.875rem)

**Font Weights**:
- Headers: `font-bold` (700) or `font-semibold` (600)
- Body: `font-medium` (500) or default (400)

### Spacing

**Padding**:
- Standard: `p-4` (1rem)
- Compact: `p-2` (0.5rem)
- Header: `px-4 py-2` (horizontal 1rem, vertical 0.5rem)

**Gaps**:
- Standard: `gap-3` (0.75rem)
- Small: `gap-2` (0.5rem)

**Margins**:
- Between elements: `mb-4` or `mb-1`
- Top spacing: `mt-3` or `mt-1`

### Borders & Radius

**Border Radius**:
- Standard: `rounded-md` (0.375rem / 6px)
- Code blocks: `rounded-md`

**Borders**:
- Standard: `border border-gray-200 dark:border-gray-700`
- Dividers: `border-r`, `border-b` with same colors
- Width: `border` (1px)

### Shadows

**Shadow Levels**:
- Subtle: `shadow-sm` (most components)
- Standard: `shadow-sm` (most components)
- Code blocks: Custom shadow with `rgba(0, 0, 0, 0.1)`

### Dark Mode Pattern

Always include dark mode variants:

```vue
'bg-white dark:bg-[#1e1e1e]'
'border-gray-200 dark:border-gray-700'
'text-gray-800 dark:text-gray-300'
```

**Common Dark Mode Backgrounds**:
- Main: `dark:bg-[#1e1e1e]` (VS Code dark)
- Sidebar/Header: `dark:bg-[#252526]` or `dark:bg-[#2d2d2d]`
- Hover: `dark:hover:bg-[#2a2d2e]` or `dark:hover:bg-gray-700`

### Component Backgrounds

**Standard Pattern**:
```vue
bg-white dark:bg-[#1e1e1e]
```

**Header/Sidebar Pattern**:
```vue
bg-gray-50 dark:bg-[#252526]
```

**Hover States**:
```vue
hover:bg-gray-200 dark:hover:bg-[#2a2d2e]
```

### Icons

**Icon System**: Carbon icons via UnoCSS
- Format: `i-carbon:icon-name`
- Examples: `i-carbon:information-filled`, `i-carbon:chevron-right`
- Size: Usually `text-xs`, `text-sm`, or `text-base`

### Interactive States

**Hover**:
- Background: `hover:bg-gray-200 dark:hover:bg-[#2a2d2e]`
- Text: `hover:text-gray-300`
- Transitions: `transition-colors` or `transition-opacity`

**Selected/Active**:
- Background: `bg-blue-100 dark:bg-[#37373d]`
- Text: `text-blue-800 dark:text-white`

**Disabled/Inactive**:
- Opacity: `opacity-0 group-hover:opacity-100`

### Code Display

**Syntax Highlighting**:
- Theme: `github-dark` (Shiki)
- Background: `bg-[#0d1117]` (GitHub dark)
- Font: `font-mono` with `text-sm`

**Code Containers**:
- Background: `bg-white dark:bg-[#1e1e1e]`
- Border: `border border-gray-200 dark:border-gray-700`
- Padding: `p-4`

### Component-Specific Patterns

**Callout Colors**:
- Info: Blue (`blue-50`, `blue-200`, `blue-800`)
- Warning: Amber (`amber-50`, `amber-200`, `amber-800`)
- Success: Emerald (`emerald-50`, `emerald-200`, `emerald-800`)
- Error: Rose (`rose-50`, `rose-200`, `rose-800`)
- Tip: Violet (`violet-50`, `violet-200`, `violet-800`)
- Note: Gray (`gray-50`, `gray-200`, `gray-800`)

**Chart Colors**:
- Primary: `#3B82F6` (Blue)
- Secondary: `#10B981` (Emerald)
- Accent: `#8B5CF6` (Violet)
- Grid: `rgba(128, 128, 128, 0.1)`
- Text: `#9CA3AF` (Gray-400)

### Layout Patterns

**Flexbox**:
- Standard: `flex gap-3`
- Vertical: `flex flex-col`
- Spacing: `flex-1`, `flex-shrink-0`

**Container Heights**:
- Standard: `h-[400px]` or `height: 400px`
- Terminal: `height: 300px` (default)
- Configurable via props

### Text Alignment

- Headers: Left-aligned (`text-left`)
- Component labels: Left-aligned
- Code: Left-aligned (`text-left`)

### Component Creation Checklist

When creating new components, ensure:

- [ ] Dark mode variants for all colors
- [ ] `shadow-sm` for containers
- [ ] `rounded-md` for borders
- [ ] `border-gray-200 dark:border-gray-700` for borders
- [ ] `bg-white dark:bg-[#1e1e1e]` for main backgrounds
- [ ] `text-sm` for body text
- [ ] `font-mono` for code/terminal text
- [ ] Hover states with `transition-colors`
- [ ] Carbon icons via `i-carbon:` prefix
- [ ] Consistent padding (`p-4` standard, `p-2` compact)
- [ ] Proper spacing with `gap-3` or `gap-2`

