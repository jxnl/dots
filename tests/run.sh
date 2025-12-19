#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

failures=0

while IFS= read -r -d '' test_file; do
  echo "==> $(basename "$test_file")"
  if ! (cd "$ROOT_DIR" && bash "$test_file"); then
    echo "FAILED: $test_file" >&2
    failures=$((failures + 1))
  fi
done < <(find "$ROOT_DIR/tests" -maxdepth 1 -type f -name 'test_*.sh' -print0 | sort -z)

if [ "$failures" -ne 0 ]; then
  echo ""
  echo "Tests failed: $failures" >&2
  exit 1
fi

echo ""
echo "All tests passed."

