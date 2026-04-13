from __future__ import annotations

import glob
import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path


def detected_json_keys(content: str, keys: Sequence[str]) -> tuple[str, ...]:
    return tuple(
        key
        for key in keys
        if re.search(rf'"{re.escape(key)}"\s*:', content)
    )


def strip_jsonc_comments(content: str) -> str:
    lines: list[str] = []
    for line in content.splitlines():
        in_string = False
        escaped = False
        result: list[str] = []
        index = 0
        while index < len(line):
            char = line[index]
            if escaped:
                result.append(char)
                escaped = False
                index += 1
                continue
            if char == "\\" and in_string:
                result.append(char)
                escaped = True
                index += 1
                continue
            if char == '"':
                in_string = not in_string
                result.append(char)
                index += 1
                continue
            if not in_string and char == "/" and index + 1 < len(line) and line[index + 1] == "/":
                break
            result.append(char)
            index += 1
        lines.append("".join(result))
    return "\n".join(lines)


def load_jsonc_object(content: str, json_object: callable) -> Mapping[str, object]:
    without_comments = strip_jsonc_comments(content)
    without_trailing_commas = re.sub(r",\s*([}\]])", r"\1", without_comments)
    return json_object(json.loads(without_trailing_commas))


def parse_jsonc_mapping_text(text: str) -> Mapping[str, object] | None:
    """Return the top-level JSON object, or None if the text is not a JSON object."""
    try:
        without_comments = strip_jsonc_comments(text)
        without_trailing_commas = re.sub(r",\s*([}\]])", r"\1", without_comments)
        parsed = json.loads(without_trailing_commas)
    except (json.JSONDecodeError, TypeError, ValueError):
        return None
    if isinstance(parsed, Mapping):
        return parsed
    return None


@dataclass(frozen=True)
class JsonMappingFileRead:
    exists: bool
    ok: bool
    data: Mapping[str, object]


def read_json_mapping_file(path: Path) -> JsonMappingFileRead:
    """Read a JSON/JSONC file. ``ok`` is False when the file exists but could not be parsed."""
    if not path.is_file():
        return JsonMappingFileRead(exists=False, ok=True, data={})
    text = path.read_text()
    parsed = parse_jsonc_mapping_text(text)
    if parsed is None:
        return JsonMappingFileRead(exists=True, ok=False, data={})
    return JsonMappingFileRead(exists=True, ok=True, data=parsed)


def slugify_name(value: str) -> str:
    result = re.sub(r"[^A-Za-z0-9_-]+", "-", value.strip()).strip("-").lower()
    return result or "migrated-command"


def first_markdown_heading(content: str) -> str | None:
    for line in content.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return None


def format_backtick_list(values: Sequence[str]) -> str:
    if not values:
        return ""
    if len(values) == 1:
        return f"`{values[0]}`"
    return ", ".join(f"`{value}`" for value in values[:-1]) + f", and `{values[-1]}`"


def normalize_source_scope_root(path: Path, source_scope_markers: Sequence[Path]) -> Path:
    resolved = path
    for marker in source_scope_markers:
        if resolved.parts[-len(marker.parts) :] == marker.parts:
            return resolved.parents[len(marker.parts) - 1]
    return resolved


def resolve_source_root(source: str) -> Path:
    if not glob.has_magic(source):
        return Path(source)

    matches = [Path(match) for match in glob.glob(source, recursive=True)]
    if not matches:
        raise FileNotFoundError(f"No matches for source pattern: {source}")

    for match in matches:
        if match.is_dir() and (match / "global").exists() and (match / "project").exists():
            return match

    static_prefix = source.split("*", 1)[0].rstrip("/")
    return Path(static_prefix)
