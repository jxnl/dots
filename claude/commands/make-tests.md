# Make Tests

Collaborative test creation through coverage analysis and discussion.

## Workflow

### 1. Understand Context

**Read implementation:**
- Examine relevant files
- Identify key functions, edge cases, error paths

**Check existing tests:**
```bash
find . -path "*/tests/*" -name "*test*.py"
```
- Understand testing patterns (pytest/unittest)
- Note what's covered

**Analyze coverage:**
```bash
uv run coverage run -m pytest path/to/tests
uv run coverage report --show-missing
```

### 2. Analysis & Recommendations

```
📊 Coverage: X%
Uncovered: function_name() in file.py:42-58

💡 Test Categories:

Core Functionality:
  - Happy path for feature X
  - Typical input scenarios

Edge Cases:
  - Empty/null inputs
  - Boundary conditions
  - Type mismatches

Error Handling:
  - ValidationError paths
  - Exception handling
  - Error messages

Which are most important?
Any specific scenarios you're worried about?
```

### 3. Collaborative Planning

**Ask priorities:**
- Critical paths vs nice-to-have
- Real calls vs mocks (project prefers real)
- Many small tests vs fewer comprehensive

**For each test, explain first:**
```
📝 test_handles_empty_input
Purpose: Verify graceful empty array handling
Covers: Lines 42-48 in module.py
Scenario: [] input → default value
```

### 4. Create & Verify

**Follow project patterns:**
- Test file naming conventions
- Fixture usage from conftest.py
- Assertion style
- Arrange-Act-Assert structure

**Run & show results:**
```bash
uv run pytest tests/test_feature.py -v
uv run coverage run -m pytest tests/test_feature.py
uv run coverage report
```

**Iterate:**
```
Coverage: 75% → 87% (+12%)
Still missing lines 200-210
Should we cover those?
```

## Project Awareness

**Check conventions:**
```bash
cat tests/README.md CONTRIBUTING.md
cat tests/conftest.py  # fixtures
```

**Follow patterns:** test naming, imports, fixtures, assertions

**No mocking unless necessary** (per CLAUDE.md)

## Output Format

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

## Usage

```bash
/make-tests                    # Current changes
/make-tests path/to/module.py  # Specific module
/make-tests "feature desc"     # Described feature
```
