from __future__ import annotations

"""Shared path constants for migration.

Paths in CLAUDE_* are relative to ScopePaths.source (the directory that contains
``.claude``, ``.mcp.json``, etc.).
"""

from pathlib import Path

CLAUDE_SETTINGS_JSON_RELATIVE = (
    Path(".claude") / "settings.json",
    Path(".claude") / "settings.local.json",
)

OPENCODE_CONFIG_FILES = (
    Path("opencode.json"),
    Path("opencode.jsonc"),
    Path(".config") / "opencode" / "opencode.json",
    Path(".config") / "opencode" / "opencode.jsonc",
)

OPENCODE_CONFIG_KEYS = (
    "instructions",
    "mcp",
    "agent",
    "plugin",
    "permission",
)

_OPENCODE_MANUAL_SEGMENTS: tuple[tuple[str, ...], str] = (
    (("agents",), "markdown agents"),
    (("plugins",), "plugins and plugin hooks"),
    (("skills",), "skills"),
    (("tools",), "custom tools"),
)


def _build_opencode_manual_paths() -> tuple[tuple[Path, str], ...]:
    rows: list[tuple[Path, str]] = []
    for base, prefix in (
        (Path(".opencode"), "OpenCode "),
        (Path(".config") / "opencode", "OpenCode global "),
    ):
        for segments, tail in _OPENCODE_MANUAL_SEGMENTS:
            rows.append((base.joinpath(*segments), f"{prefix}{tail}"))
    return tuple(rows)


OPENCODE_MANUAL_PATHS = _build_opencode_manual_paths()

_PI_CODE_MANUAL_SEGMENTS: tuple[tuple[str, ...], str] = (
    (("settings.json",), "settings"),
    (("SYSTEM.md",), "replacement system prompt"),
    (("APPEND_SYSTEM.md",), "appended system prompt"),
    (("extensions",), "extensions, tools, commands, and hooks"),
    (("skills",), "skills"),
    (("git",), "git package cache"),
    (("npm",), "npm package cache"),
)


def _build_pi_code_manual_paths() -> tuple[tuple[Path, str], ...]:
    rows: list[tuple[Path, str]] = []
    pi = Path(".pi")
    agent = pi / "agent"
    for segments, tail in _PI_CODE_MANUAL_SEGMENTS:
        rows.append((pi.joinpath(*segments), f"PI-CODE {tail}"))
    for segments, tail in _PI_CODE_MANUAL_SEGMENTS:
        rows.append((agent.joinpath(*segments), f"PI-CODE global {tail}"))
    return tuple(rows)


PI_CODE_MANUAL_PATHS = _build_pi_code_manual_paths()

SOURCE_SCAN_ROOTS = (
    (Path(".claude"), "primary source"),
    (Path(".opencode"), "OpenCode"),
    (Path(".config") / "opencode", "OpenCode global"),
    (Path(".pi"), "PI-CODE"),
    (Path(".pi") / "agent", "PI-CODE global"),
)

SOURCE_SCOPE_MARKERS = (
    Path(".claude"),
    Path(".opencode"),
    Path(".pi"),
    Path(".config") / "opencode",
)
