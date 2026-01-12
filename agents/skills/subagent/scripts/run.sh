#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   run.sh "prompt text" [--cd PATH] [--model MODEL] [--json] [--full-auto]
#   run.sh -  (reads prompt from stdin)

prompt="${1:-}"
shift || true

if [[ -z "$prompt" ]]; then
  echo "error: missing prompt" >&2
  exit 2
fi

codex exec "$prompt" "$@"
