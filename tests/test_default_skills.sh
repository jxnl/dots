#!/usr/bin/env bash
set -euo pipefail
source tests/testlib.sh
tmp="$(mktempdir)"
trap 'rm -rf "$tmp"' EXIT
legacy="$tmp/.codex/skills/dotfiles-check"
target="$tmp/.agents/skills/dotfiles-check"
mkdir -p "$legacy"
echo custom > "$legacy/SKILL.md"
HOME="$tmp" ./install.sh --dry-run >/dev/null
assert_not_exists "$tmp/.agents"
HOME="$tmp" ./install.sh --backup >/dev/null
[ -L "$target" ] || die "Expected the existing skill to be linked"
assert_file_eq agents/skills/dotfiles-check/SKILL.md "$target/SKILL.md"
backups=("$legacy"/SKILL.md.bak.*)
[ "$(cat "${backups[0]}")" = custom ] || die "Expected original skill backup"
HOME="$tmp" ./install.sh --backup >/dev/null
again=("$legacy"/SKILL.md.bak.*)
[ "${#again[@]}" = 1 ] || die "Unexpected backup on repeat install"
assert_file_eq agents/skills/gh-fix-ci/SKILL.md "$tmp/.agents/skills/gh-fix-ci/SKILL.md"
