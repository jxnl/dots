#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

for arg in "$@"; do
  case "$arg" in
    --vim|--bash|--tmux|--interactive)
      echo "Error: ${arg} is not supported by agents/install.sh" >&2
      exit 1
      ;;
  esac
done

has_target=false
for arg in "$@"; do
  case "$arg" in
    --agents|--claude|--openai|--codex|--cursor|--cursor-project|--skills)
      has_target=true
      ;;
  esac
done

if [ $# -eq 0 ]; then
  exec "${REPO_ROOT}/install.sh" --agents
fi

for arg in "$@"; do
  case "$arg" in
    --help|--list-prompts)
      exec "${REPO_ROOT}/install.sh" "$@"
      ;;
  esac
done

if [ "$has_target" = false ]; then
  exec "${REPO_ROOT}/install.sh" --agents "$@"
fi

exec "${REPO_ROOT}/install.sh" "$@"
