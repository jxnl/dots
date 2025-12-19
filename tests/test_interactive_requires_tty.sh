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

set +e
out="$(
  cd "$fixture"
  HOME="$home" ./install.sh --interactive 2>&1
)"
code=$?
set -e

[ "$code" -ne 0 ] || die "Expected --interactive to fail without a TTY"
echo "$out" | grep -q "requires a TTY" || die "Expected error message about TTY, got: $out"

