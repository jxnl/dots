#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=tests/testlib.sh
source "$ROOT_DIR/tests/testlib.sh"

tmp="$(mktempdir)"
trap 'rm -rf "$tmp"' EXIT

fixture="$tmp/fixture"
home="$tmp/home"
outside="$tmp/outside"
mkdir -p "$home/.codex" "$outside"
make_fixture "$fixture"

ln -s "$outside" "$home/.codex/skills"

set +e
out="$(
  cd "$fixture"
  HOME="$home" ./install.sh --skills 2>&1
)"
code=$?
set -e

[ "$code" -ne 0 ] || die "Expected install through a symlinked skills directory to fail"
echo "$out" | grep -qi "symbolic link" || die "Expected a symbolic-link error, got: $out"
assert_not_exists "$outside/audit-ai-code/SKILL.md"

rm "$home/.codex/skills"
mkdir -p "$home/.codex/prompts"
prompt="$(
  cd "$fixture"
  first_prompt
)"
target="$outside/prompt.md"
echo "OLD" > "$target"
ln -s "$target" "$home/.codex/prompts/$prompt.md"

set +e
out="$(
  cd "$fixture"
  HOME="$home" ./install.sh --openai --prompt "$prompt" 2>&1
)"
code=$?
set -e

[ "$code" -ne 0 ] || die "Expected install through a symlinked prompt file to fail"
echo "$out" | grep -qi "symbolic link" || die "Expected a symbolic-link error, got: $out"
echo "OLD" | cmp -s - "$target" || die "Expected prompt symlink target to remain unchanged"
