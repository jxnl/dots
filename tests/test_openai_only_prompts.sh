#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=tests/testlib.sh
source "$ROOT_DIR/tests/testlib.sh"

tmp="$(mktempdir)"
trap 'rm -rf "$tmp"' EXIT

fixture="$tmp/fixture"
home="$tmp/home"
mkdir -p "$home"
make_fixture "$fixture"

cd "$fixture"
prompts_csv="$(two_prompts_or_one)"
HOME="$home" ./install.sh --openai --only-prompts "$prompts_csv"

assert_exists "$home/.codex/prompts"

expected_count="$(echo "$prompts_csv" | awk -F',' '{print NF}')"
actual_count="$(find "$home/.codex/prompts" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"
[ "$actual_count" -eq "$expected_count" ] || die "Expected $expected_count prompt(s), got $actual_count"

IFS=',' read -r -a prompts <<< "$prompts_csv"
for p in "${prompts[@]}"; do
  assert_exists "$home/.codex/prompts/$p.md"
  assert_file_eq "$fixture/agents/prompts/$p.md" "$home/.codex/prompts/$p.md"
done

