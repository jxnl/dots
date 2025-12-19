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

out="$(
  cd "$fixture"
  HOME="$home" ./install.sh --vim --dry-run
)"

echo "$out" | grep -Fq '[dry-run] cp "vimrc"' || die "Expected dry-run output to include cp vimrc"
assert_not_exists "$home/.vimrc"
assert_not_exists "$home/.vim/colors"
