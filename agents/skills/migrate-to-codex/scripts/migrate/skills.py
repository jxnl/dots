from __future__ import annotations

import re
from collections.abc import Sequence
from pathlib import Path


COMMAND_FILE_SOURCES = (
    (Path(".claude") / "commands", "source-command", "source command"),
    (Path(".opencode") / "commands", "opencode-command", "OpenCode command"),
    (
        Path(".config") / "opencode" / "commands",
        "opencode-command",
        "OpenCode global command",
    ),
    (Path(".pi") / "prompts", "pi-prompt", "PI-CODE prompt template"),
    (
        Path(".pi") / "agent" / "prompts",
        "pi-prompt",
        "PI-CODE global prompt template",
    ),
)

SKILL_SOURCE_ROOTS = (
    Path(".claude") / "skills",
    Path(".opencode") / "skills",
    Path(".config") / "opencode" / "skills",
    Path(".pi") / "skills",
    Path(".pi") / "agent" / "skills",
)


def iter_skill_files(source_root: Path) -> tuple[Path, ...]:
    if not source_root.exists():
        return ()
    return tuple(sorted(source_root.glob("*/SKILL.md")))


def command_caveats(
    template: str,
    unsupported_fields: Sequence[str],
) -> tuple[str, ...]:
    caveats: list[str] = []
    if re.search(r"\$(ARGUMENTS|\d+)\b", template):
        caveats.append(
            "Provider argument placeholders like `$ARGUMENTS` or `$1` were preserved as text; rewrite them into natural-language instructions for Codex."
        )
    if "{{" in template and "}}" in template:
        caveats.append(
            "Provider template variables like `{{name}}` were preserved as text; rewrite them into natural-language instructions for Codex."
        )
    if re.search(r"!\s*`", template):
        caveats.append(
            "Provider shell-output interpolation like ``!`command` `` was preserved as text; replace it with explicit Codex instructions to run the command when needed."
        )
    if re.search(r"(^|\s)@[\w./~:-]+", template):
        caveats.append(
            "Provider automatic file-reference expansion was preserved as text; verify Codex should read those files explicitly."
        )
    if unsupported_fields:
        caveats.append(
            "Review unsupported command metadata manually: "
            + ", ".join(f"`{field_name}`" for field_name in unsupported_fields)
            + "."
        )
    return tuple(caveats)
