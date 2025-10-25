# Claude Configuration

Personal Claude Code setup with custom commands, agents, and global preferences.

## Structure

```
claude/
├── CLAUDE.md              # Global instructions for all projects
├── settings.json          # Claude Code settings
├── commands/              # Slash commands for workflows
│   ├── gh-*.md           # GitHub workflow automation
│   ├── make-tests.md     # Test creation assistant
│   ├── de-slop.md        # AI artifact cleanup
│   └── new-cmd.md        # Command creation helper
└── agents/               # Background task agents
    ├── test-runner.md    # Test execution & diagnostics
    └── youtube.md        # YouTube transcript processing
```

## Global Instructions (CLAUDE.md)

Core rules applied to all projects:

- **Use `uv run` not `python`** - Always prefer uv for Python execution
- **No mocking in tests** - Real calls over mocks, tests must verify actual behavior
- **YouTube transcripts** - Use `uv run youtube_transcript_api VIDEO_ID`
- **No emojis in PRs** - Keep pull requests professional
- **No fake data** - Never fabricate case studies or metrics
- **Git hygiene** - Never `git add .`, select files individually
- **Plan mode** - Always include writing tests
- **Commit discipline** - Commit in logical groups, never work on main without permission
- **Concise writing** - Sacrifice grammar for concision
- **Unresolved questions** - List any unclear items at the end

## Commands

Slash commands available via `/command-name`.

### GitHub Workflows

#### `/gh-commit` - Smart Commit Manager

Creates well-organized commits following conventional commit standards.

**Features:**
- Branch safety (never commit to main, auto-creates feature branches)
- Smart batching (groups related changes: feat/test/docs/refactor/chore)
- Conventional commits (type(scope): description format)
- Follows existing patterns from `git log`

**Usage:**
```bash
/gh-commit                    # Analyze and commit changes
/gh-commit "description"      # Use description to inform messages
```

**Batching strategy:**
1. Core implementation (feat/fix)
2. Tests (test)
3. Documentation (docs)
4. Refactoring (refactor)
5. Chores (chore)

**Output:**
```
✅ Created 3 commits:
  • feat(yaml): add MD_YAML mode for extraction
  • test(yaml): add tests for MD_YAML mode
  • docs(yaml): document MD_YAML usage

Next: git push -u origin feat/add-yaml-support
```

---

#### `/gh-review-pr` - Comprehensive PR Review

Thorough PR analysis including code, discussions, and CI status.

**Features:**
- Fetches PR metadata, comments, reviews, CI checks
- Checks out PR branch locally
- Compares against base branch
- Analyzes commit history
- Reviews all changed files
- Provides structured feedback

**Usage:**
```bash
/gh-review-pr 123                                    # Review PR #123
/gh-review-pr https://github.com/owner/repo/pull/456 # Review by URL
/gh-review-pr owner/repo#789                         # Review with repo context
```

**Review structure:**
1. Executive Summary (purpose, scope, risk, recommendation)
2. Code Quality Analysis (architecture, style, testing, docs)
3. File-by-File Review (detailed feedback per file)
4. Discussion & CI Review (unresolved threads, check status)
5. Testing Verification (run tests if appropriate)
6. Recommendations & Action Items (must/should/consider fixes)

---

#### `/gh-address-pr-comments` - Interactive Comment Resolution

Addresses reviewer feedback from PR comments.

**Features:**
- Fetches all PR comments and reviews
- Filters actionable items (file/line references)
- Categorizes by type (CODE, STYLE, DOCS, TEST, QUESTIONS)
- Interactive selection of items to address
- Shows context before making changes

**Usage:**
```bash
/gh-address-pr-comments 18
/gh-address-pr-comments https://github.com/owner/repo/pull/123
```

**Workflow:**
1. Checkout PR branch
2. Fetch and analyze comments
3. Present actionable items
4. User selects which to address ("1,3,4" or "all")
5. Apply changes with Edit tool
6. Show summary and suggest next steps

**Prioritizes:**
- File/line references over general feedback
- Directive language ("change this" vs "consider")
- Maintainer feedback over contributor suggestions
- Unresolved discussions

---

#### `/gh-fix-ci` - CI Failure Auto-Fix

Auto-detects, analyzes, and fixes CI/CD failures from logs.

**Features:**
- Works on any branch (main, feature, with/without PR)
- Downloads CI logs via GitHub API
- Parses common error patterns
- Applies targeted fixes
- Shows diff and summary

**Usage:**
```bash
/gh-fix-ci              # Current branch
/gh-fix-ci 123          # PR number
/gh-fix-ci https://...  # PR URL
```

**Detects and fixes:**
- **Ruff formatting**: `Would reformat: file.py` → `uv run ruff format file.py`
- **Test failures**: AssertionError, ModuleNotFoundError, import errors
- **Type errors**: Missing type hints, incompatible types
- **Build errors**: SyntaxError, ImportError

**Safety:**
- Warns on main/master branch
- Checks for uncommitted changes
- Flags unclear fixes for manual review
- Asks which failures to prioritize if multiple

**Output:**
```
✅ Fixed 3 issues:
  • Lint: app/api.py - Removed unused import
  • Test: tests/test_auth.py - Fixed assertion
  • Type: models/user.py - Added type hint

Next: /commit then git push
```

---

### Development Tools

#### `/make-tests` - Collaborative Test Creation

Creates tests through coverage analysis and discussion.

**Features:**
- Analyzes implementation for test opportunities
- Runs coverage reports to find gaps
- Suggests test categories (core, edge cases, errors)
- Explains each test before writing
- Verifies coverage improvements

**Usage:**
```bash
/make-tests                    # Current changes
/make-tests path/to/module.py  # Specific module
/make-tests "feature desc"     # Described feature
```

**Workflow:**
1. Read implementation and existing tests
2. Analyze coverage gaps
3. Suggest test categories (core/edge/error handling)
4. Ask priorities and preferences
5. Create tests iteratively with explanations
6. Run tests and show coverage improvements

**Test categories:**
- Core functionality (happy paths)
- Edge cases (empty/null inputs, boundaries)
- Error handling (exceptions, validation)
- Integration tests (if applicable)

**Follows project rules:**
- No mocking unless necessary (per CLAUDE.md)
- Uses project fixtures and patterns
- Runs tests with `uv run pytest`

**Output:**
```
✅ Tests Created: 5
Coverage: 75% → 87% (+12%)

Files:
  tests/test_validation.py (3 tests)
  tests/test_edge_cases.py (2 tests)

Run: uv run pytest tests/

Remaining gaps:
  - Lines 200-210: Async timeout
  Cover these too?
```

---

#### `/de-slop` - AI Artifact Cleanup

Removes AI-generated artifacts before PR submission.

**Features:**
- Scans for unnecessary markdown files
- Detects redundant comments
- Flags AI TODOs
- Identifies excessive docstrings
- Catches mock-heavy tests
- Spots fake data/metrics

**Usage:**
```bash
/de-slop              # Compare against base branch
/de-slop 123          # Compare against PR #123
```

**Detects:**

**Unnecessary markdown:**
- NOTES.md, PLAN.md, ARCHITECTURE.md, THOUGHTS.md, etc.
- Ignores: README.md, CONTRIBUTING.md, CHANGELOG.md, docs/

**Redundant comments:**
```python
# Create user  ← Just restates next line
user = User()
```

**AI TODOs:**
```python
# TODO: Add error handling
# TODO: Consider edge cases
```

**Mock-heavy tests:**
```python
@patch @patch @patch  # >3 mocks, tests nothing real
```

**Fake data:**
- Metrics without citations
- Made-up case studies

**Workflow:**
1. Dry run scan and categorize
2. Present findings with numbers
3. User selects items to fix ("1,3,4" or "all")
4. Execute deletions/edits
5. Show summary

**Safety:**
- Always dry run first
- Never removes: README, CONTRIBUTING, CHANGELOG, docs/
- Confirms if deleting >5 files or >50 lines

---

#### `/new-cmd` - Command Creation Helper

Helps create new Claude commands following best practices.

**Features:**
- Interviews to understand command purpose
- Researches similar existing commands
- Determines project vs user location
- Generates structured command files
- Follows established patterns

**Usage:**
```bash
/new-cmd
```

**Interview process:**
1. Understand purpose (problem, users, output, interactive/batch)
2. Research similar commands for patterns
3. Determine location (project `.claude/` vs user `~/.claude/`)
4. Follow patterns (sections, tools, safety, examples)
5. Generate and test

**Common patterns:**
```markdown
# Command Name
Brief description

## Workflow
### 1. Step One
bash commands, tool usage

## Rules/Safety
Key constraints

## Usage
Examples
```

**Command categories:**
- `gh-*` - GitHub workflows
- Development tools
- Meta commands

---

## Agents

Background task agents for specialized operations.

### test-runner

Runs tests on specific files with comprehensive diagnostics.

**Capabilities:**
- Execute tests systematically with `uv run`
- Analyze results (passed/failed/skipped/coverage)
- Diagnose root causes
- Generate structured reports
- Provide actionable fixes

**Model:** Haiku (fast, efficient for test execution)

**When to use:**
- Testing new authentication module
- Debugging failing payment tests
- Comprehensive test analysis needed

**Output:**
- Executive summary
- Detailed failure breakdown
- Root cause analysis
- Recommended fixes
- Coverage gaps

---

### youtube

YouTube video processing workflow automation.

**Capabilities:**
- Extract transcripts with `youtube_transcript_api`
- Download videos
- Extract frames at timestamps
- Organize files for study notes

**Usage:**
```bash
# Full processing with auto-detected frames
uv run python yt_processor.py "https://www.youtube.com/watch?v=VIDEO_ID" --auto-frames

# Specific timestamps
uv run python yt_processor.py "VIDEO_ID" --frames "90,400,560,780"

# Transcript only (no video)
uv run python yt_processor.py "VIDEO_ID" --skip-video --auto-frames

# Video info
uv run python yt_processor.py info "VIDEO_ID"
```

**Features:**
- Auto-detects interesting frames
- Custom output directories
- Skip video/frames options
- Organizes for note creation

---

## Settings (settings.json)

```json
{
  "alwaysThinkingEnabled": true,
  "feedbackSurveyState": {
    "lastShownTime": 1754014063729
  }
}
```

**Configuration:**
- Always-on thinking mode for better reasoning
- Feedback survey tracking

---

## Installation

Copy configuration to Claude directory:

```bash
# From dots repo
./install.sh --claude

# Or manually
cp -r claude/ ~/.claude/
```

**Files installed:**
- `~/.claude/CLAUDE.md` - Global instructions
- `~/.claude/settings.json` - Settings
- `~/.claude/commands/*.md` - Slash commands
- `~/.claude/agents/*.md` - Background agents

---

## Usage Patterns

### Typical PR Workflow

```bash
# 1. Review PR
/gh-review-pr 123

# 2. Address comments
/gh-address-pr-comments 123

# 3. Fix CI failures
/gh-fix-ci 123

# 4. Clean up AI artifacts
/de-slop 123

# 5. Commit changes
/gh-commit
```

### Test-Driven Development

```bash
# 1. Create tests
/make-tests path/to/new_feature.py

# 2. Run tests with agent (if needed)
# Use test-runner agent for diagnostics

# 3. Commit tests
/gh-commit "add tests for new feature"
```

### Command Development

```bash
# Create new command
/new-cmd

# Test and refine based on usage
```

---

## Best Practices

**Commands:**
- Use `gh-` prefix for GitHub workflows
- Keep under 200 lines
- Include usage examples
- Show expected output
- Add safety checks

**Agents:**
- Use Haiku for fast operations
- Structured reports
- Actionable recommendations

**Global rules:**
- Always `uv run`, never `python`
- No mocking in tests
- Commit often in logical groups
- Never work directly on main
- List unresolved questions

---

## Customization

**Adding commands:**
1. Use `/new-cmd` for guidance
2. Study similar commands in `commands/`
3. Follow naming conventions
4. Test thoroughly

**Modifying global rules:**
Edit `CLAUDE.md` to update instructions for all projects.

**Agent configuration:**
Edit agent frontmatter (name, description, tools, model, color) in `agents/*.md`.
