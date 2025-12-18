# New Command

Create new assistant commands/prompts following best practices.

## Interview Process

### 1. Understand Purpose
"Let's create a new command. Describe:"
- What problem does it solve?
- Who uses it and when?
- Expected output?
- Interactive or batch?

### 2. Research Similar Commands

**Check existing commands/prompts:**
```bash
ls -la .claude/commands/     # Project (Claude Code)
ls -la ~/.claude/commands/   # User (Claude Code)
ls -la ~/.codex/prompts/     # User (Codex CLI)
```

**Read similar ones for patterns:**
- Section structure
- Tool usage
- Argument handling
- Documentation references

### 3. Determine Location

**Project command** (.claude/commands/):
- Specific to this codebase
- Uses project conventions
- References project docs

**User command** (~/.claude/commands/):
- General-purpose
- Reusable across projects
- Personal productivity

**User prompt** (~/.codex/prompts/):
- General-purpose
- Reusable across projects
- Codex CLI custom prompts

### 4. Follow Patterns

**Common structures:**
```markdown
# Command Name

Brief description

## Workflow

### 1. Step One
bash commands, tool usage

### 2. Step Two
process, decisions

## Rules/Safety

Key constraints

## Usage

Examples
```

**Standard sections:**
- Clear workflow steps
- Bash examples for gh/git commands
- Safety/error handling
- Usage examples
- Output format

### 5. Generate & Test

**Create command file:**
- Follow naming (gh- prefix for GitHub)
- Include workflow steps
- Add safety checks
- Show examples

**Test it:**
- Run example scenarios
- Verify argument handling
- Check error cases

## Common Patterns

**GitHub commands:**
```bash
gh pr view {PR}
gh pr checkout {PR}
gh api repos/{owner}/{repo}/...
```

**Git operations:**
```bash
git branch --show-current
git diff main...HEAD
git status --short
```

**Safety checks:**
- Warn on main branch
- Check uncommitted changes
- Confirm destructive ops

## Command Categories

**gh-*** - GitHub workflows (PR, CI, commits)
**de-slop** - Code cleanup
**make-tests** - Test creation
**new-cmd** - Meta (this file)

## Output

```
✅ Command created: {location}/{name}.md

Usage: /{name} [args]
Example: /{name} 123

Next: Test it, refine based on usage
```

## Usage

```bash
/new-cmd
```
