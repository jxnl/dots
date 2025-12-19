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
p="$(first_prompt)"
HOME="$home" ./install.sh --cursor-project --prompt "$p"

assert_exists "$fixture/.cursor/commands/$p.md"
assert_file_eq "$fixture/agents/prompts/$p.md" "$fixture/.cursor/commands/$p.md"

