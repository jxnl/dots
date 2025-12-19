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

echo "OLD" > "$home/.vimrc"

cd "$fixture"
HOME="$home" ./install.sh --vim --backup

assert_exists "$home/.vimrc"
assert_file_eq "$fixture/vimrc" "$home/.vimrc"

bak_count="$(ls -1 "$home/.vimrc.bak."* 2>/dev/null | wc -l | tr -d ' ')"
[ "$bak_count" -ge 1 ] || die "Expected at least one backup file for .vimrc"

