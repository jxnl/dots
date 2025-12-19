#!/usr/bin/env bash
set -euo pipefail

die() {
  echo "ERROR: $*" >&2
  exit 1
}

mktempdir() {
  local d=""
  d="$(mktemp -d 2>/dev/null || mktemp -d -t dots-tests)"
  echo "$d"
}

make_fixture() {
  local fixture_dir="$1"
  mkdir -p "$fixture_dir"

  cp -p install.sh "$fixture_dir/install.sh"
  chmod +x "$fixture_dir/install.sh"

  cp -p vimrc "$fixture_dir/vimrc"
  cp -p bash_profile "$fixture_dir/bash_profile"
  cp -p tmux.conf "$fixture_dir/tmux.conf"
  cp -R colors "$fixture_dir/colors"
  cp -R agents "$fixture_dir/agents"
}

first_prompt() {
  local prompt_path=""
  prompt_path="$(find agents/prompts -maxdepth 1 -type f -name '*.md' | sort | head -n 1)"
  [ -n "$prompt_path" ] || die "No prompts found under agents/prompts"
  basename "$prompt_path" .md
}

two_prompts_or_one() {
  local -a paths=()
  local p1="" p2=""

  while IFS= read -r path; do
    [ -z "$path" ] && continue
    paths+=("$path")
  done < <(find agents/prompts -maxdepth 1 -type f -name '*.md' | sort)

  [ "${#paths[@]}" -ge 1 ] || die "No prompts found under agents/prompts"

  p1="$(basename "${paths[0]}" .md)"
  if [ "${#paths[@]}" -ge 2 ]; then
    p2="$(basename "${paths[1]}" .md)"
  fi

  if [ -z "$p2" ] || [ "$p1" = "$p2" ]; then
    echo "$p1"
    return 0
  fi

  echo "$p1,$p2"
}

assert_file_eq() {
  local a="$1"
  local b="$2"
  cmp -s "$a" "$b" || die "Files differ: $a vs $b"
}

assert_exists() {
  local p="$1"
  [ -e "$p" ] || die "Expected to exist: $p"
}

assert_not_exists() {
  local p="$1"
  [ ! -e "$p" ] || die "Expected not to exist: $p"
}
