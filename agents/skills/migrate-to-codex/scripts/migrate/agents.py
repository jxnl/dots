from __future__ import annotations

from pathlib import Path


AGENT_SOURCE_ROOTS = (
    Path(".claude") / "agents",
    Path(".opencode") / "agents",
    Path(".config") / "opencode" / "agents",
)


def iter_agent_files(source_root: Path) -> tuple[Path, ...]:
    if not source_root.exists():
        return ()
    return tuple(
        source_file
        for source_file in sorted(source_root.glob("*.md"))
        if source_file.stem != "README"
    )
