from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, fields as dataclass_fields
from enum import Enum
from pathlib import Path
from typing import TypeAlias

from migrate.agents import (
    AGENT_SOURCE_ROOTS,
    iter_agent_files,
)
from migrate.instructions import (
    INSTRUCTION_SOURCE_CANDIDATES,
    instruction_source_file,
    should_symlink_instructions,
)
from migrate.settings import (
    CLAUDE_SETTINGS_JSON_RELATIVE,
    OPENCODE_CONFIG_FILES,
    OPENCODE_CONFIG_KEYS,
    OPENCODE_MANUAL_PATHS,
    PI_CODE_MANUAL_PATHS,
    SOURCE_SCAN_ROOTS,
    SOURCE_SCOPE_MARKERS,
)
from migrate.skills import (
    COMMAND_FILE_SOURCES,
    SKILL_SOURCE_ROOTS,
    command_caveats,
    iter_skill_files,
)
from utils.scan import (
    render_scope_inventory,
    render_source_inventory,
)
from utils.util import (
    detected_json_keys,
    first_markdown_heading,
    format_backtick_list,
    load_jsonc_object,
    normalize_source_scope_root,
    read_json_mapping_file,
    resolve_source_root,
    slugify_name,
)


# Constants

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)
ENV_VAR_RE = re.compile(r"\A\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-[^}]*)?\}\Z")
BEARER_ENV_VAR_RE = re.compile(r"\ABearer\s+\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-[^}]*)?\}\Z")
DEFAULT_COMPONENTS = frozenset(("mcp", "skills", "subagents"))
MIGRATION_REPORT_PATH = Path(".codex") / "migrate-to-codex-report.txt"
CODEX_CONFIG_PATH = Path(".codex") / "config.toml"
CODEX_AGENTS_ROOT = Path(".codex") / "agents"
CODEX_SKILLS_ROOT = Path(".agents") / "skills"
SUMMARY_LABELS = {
    "mcp_servers": "mcp servers",
}
SCOPE_NAMES = ("global", "project")
SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_SUPPORT_DIRS = ("scripts", "references", "assets")
SUMMARY_OMIT_WHEN_ZERO = frozenset()
PERMISSION_MODE_MAPPINGS = {
    "acceptEdits": "workspace-write",
    "readOnly": "read-only",
}
YamlScalar: TypeAlias = str | bool
YamlValue: TypeAlias = YamlScalar | tuple[YamlScalar, ...]


# Core models

@dataclass(frozen=True)
class ScopePaths:
    source: Path
    is_global: bool


@dataclass(frozen=True)
class ModelMapping:
    source_prefix: str
    target_model: str
    effort_mapping: tuple[tuple[str, str], ...]

    def map_effort(self, effort: str) -> str:
        for source_effort, target_effort in self.effort_mapping:
            if effort == source_effort:
                return target_effort
        return effort


MODEL_PREFIX_MAPPINGS = (
    ModelMapping(
        "claude-opus",
        "gpt-5.4",
        (("low", "low"), ("medium", "medium"), ("high", "high"), ("max", "xhigh")),
    ),
    ModelMapping(
        "claude-sonnet",
        "gpt-5.4-mini",
        (("low", "medium"), ("medium", "high"), ("high", "xhigh"), ("max", "xhigh")),
    ),
    ModelMapping(
        "claude-haiku",
        "gpt-5.4-mini",
        (("low", "low"), ("medium", "medium"), ("high", "high"), ("max", "xhigh")),
    ),
)


class ArtifactKind(Enum):
    FILE = "file"
    SKILL = "skill"
    AGENT = "agent"


@dataclass(frozen=True)
class GeneratedText:
    content: str


@dataclass(frozen=True)
class SourceCopy:
    source_path: Path


@dataclass(frozen=True)
class SourceSymlink:
    source_path: Path


ArtifactPayload: TypeAlias = GeneratedText | SourceCopy | SourceSymlink


@dataclass(frozen=True)
class WriteTextAction:
    target_path: Path
    content: str


@dataclass(frozen=True)
class CopyFileAction:
    source_path: Path
    target_path: Path


@dataclass(frozen=True)
class CreateSymlinkAction:
    source_path: Path
    target_path: Path


@dataclass(frozen=True)
class DeletePathAction:
    path: Path
    recursive: bool = False


@dataclass(frozen=True)
class WarningAction:
    message: str


@dataclass(frozen=True)
class MigrationReportItem:
    status: str
    path: Path
    detail: str


@dataclass(frozen=True)
class SimpleYamlFrontmatter:
    values: dict[str, YamlValue]

    def required_string(self, key: str) -> str:
        return str(self.values[key])

    def optional_string(self, key: str) -> str | None:
        value = self.values.get(key)
        if value is None:
            return None
        return str(value)

    def string_tuple(self, key: str) -> tuple[str, ...]:
        value = self.values.get(key, ())
        if isinstance(value, tuple):
            items = value
        else:
            items = (value,)

        result: list[str] = []
        for item in items:
            result.extend(
                split_item
                for split_item in (part.strip() for part in str(item).split(","))
                if split_item
            )
        return tuple(result)

    def to_dict(self) -> dict[str, YamlValue]:
        return self.values


@dataclass(frozen=True)
class ParsedDocument:
    frontmatter: SimpleYamlFrontmatter
    body: str
    path: Path | None = None

    @classmethod
    def from_file(cls, source_file: Path) -> ParsedDocument:
        return parse_frontmatter(source_file.read_text(), source_file)


# JSON parsing

def json_object(value: object) -> Mapping[str, object]:
    if isinstance(value, Mapping):
        return value
    return {}


def json_string(value: object) -> str | None:
    if value is None:
        return None
    return str(value)


def json_string_tuple(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return tuple(str(item) for item in value)
    return (str(value),)


def load_scope_settings(scope_root: Path) -> Mapping[str, object]:
    settings: dict[str, object] = {}
    for rel in CLAUDE_SETTINGS_JSON_RELATIVE:
        outcome = read_json_mapping_file(scope_root / rel)
        if outcome.exists and outcome.ok:
            settings.update(json_object(outcome.data))
    return settings


def format_toml_array(values: Sequence[str]) -> str:
    return ", ".join(f'"{value}"' for value in values)


def append_toml_entries(
    lines: list[str],
    table_name: str,
    entries: tuple[tuple[str, str], ...],
) -> None:
    if not entries:
        return

    lines.append("")
    lines.append(table_name)
    for key, value in entries:
        lines.append(f'{key} = "{value}"')


def format_bullets(values: Sequence[str], prefix: str = "") -> str:
    return "\n".join(f"- {prefix}{value}" for value in values)


def format_manual_migration_block(notes: Sequence[str]) -> str:
    return (
        "## MANUAL MIGRATION REQUIRED\n\n"
        + "\n\n".join(note.rstrip() for note in notes if note.strip())
    )


def unsupported_frontmatter_fields(
    frontmatter_values: Mapping[str, YamlValue],
    supported_fields: Sequence[str],
) -> tuple[str, ...]:
    supported = frozenset(supported_fields)
    return tuple(
        sorted(
            field_name
            for field_name in frontmatter_values
            if field_name not in supported
        )
    )


def append_report_item(
    report_items: list[MigrationReportItem],
    requires_manual_fix: object,
    path: Path,
    manual_detail: str,
    rewritten_detail: str,
) -> None:
    if requires_manual_fix:
        report_items.append(manual_report_item(path, manual_detail))
        return
    report_items.append(MigrationReportItem("rewritten", path, rewritten_detail))


def manual_report_item(path: Path, detail: str) -> MigrationReportItem:
    return MigrationReportItem("manual_fix_required", path, detail)


@dataclass(frozen=True)
class McpHeaders:
    bearer_token_env_var: str | None = None
    static_headers: tuple[tuple[str, str], ...] = ()
    env_headers: tuple[tuple[str, str], ...] = ()

    @classmethod
    def from_mapping(cls, headers: Mapping[str, object]) -> McpHeaders:
        bearer_token_env_var: str | None = None
        static_headers: list[tuple[str, str]] = []
        env_headers: list[tuple[str, str]] = []

        for key, value in headers.items():
            header_value = str(value)
            bearer_match = BEARER_ENV_VAR_RE.match(header_value)
            if key.lower() == "authorization" and bearer_match:
                bearer_token_env_var = bearer_match.group(1)
                continue

            env_match = ENV_VAR_RE.match(header_value)
            if env_match:
                env_headers.append((key, env_match.group(1)))
                continue

            static_headers.append((key, header_value))

        return cls(
            bearer_token_env_var=bearer_token_env_var,
            static_headers=tuple(static_headers),
            env_headers=tuple(env_headers),
        )


@dataclass(frozen=True)
class McpEnv:
    static_env: tuple[tuple[str, str], ...] = ()
    env_vars: tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, env: Mapping[str, object]) -> McpEnv:
        static_env: list[tuple[str, str]] = []
        env_vars: list[str] = []

        for key, value in env.items():
            env_value = str(value)
            env_match = ENV_VAR_RE.match(env_value)
            if env_match and env_match.group(1) == key:
                env_vars.append(key)
                continue

            static_env.append((key, env_value))

        return cls(
            static_env=tuple(static_env),
            env_vars=tuple(env_vars),
        )


@dataclass(frozen=True)
class ClaudeMcpServer:
    name: str
    url: str | None = None
    command: str | None = None
    args: tuple[str, ...] = ()
    headers: McpHeaders | None = None
    env: McpEnv | None = None

    @classmethod
    def from_mapping(cls, name: str, server_config: Mapping[str, object]) -> ClaudeMcpServer:
        headers = None
        if "headers" in server_config:
            headers = McpHeaders.from_mapping(json_object(server_config["headers"]))

        env = None
        if "env" in server_config:
            env = McpEnv.from_mapping(json_object(server_config["env"]))

        return cls(
            name=name,
            url=json_string(server_config.get("url")),
            command=json_string(server_config.get("command")),
            args=json_string_tuple(server_config.get("args")),
            headers=headers,
            env=env,
        )

    def render_toml_lines(
        self,
        enabled_servers: tuple[str, ...],
        disabled_servers: frozenset[str],
    ) -> list[str]:
        lines = [f"[mcp_servers.{self.name}]"]
        if enabled_servers and self.name not in enabled_servers:
            lines.append("enabled = false")
        elif self.name in disabled_servers:
            lines.append("enabled = false")
        if self.url:
            lines.append(f'url = "{self.url}"')
        if self.command:
            lines.append(f'command = "{self.command}"')
        if self.args:
            lines.append(f"args = [{format_toml_array(self.args)}]")
        if self.headers:
            if self.headers.bearer_token_env_var:
                lines.append(
                    f'bearer_token_env_var = "{self.headers.bearer_token_env_var}"'
                )
            append_toml_entries(
                lines,
                f"[mcp_servers.{self.name}.http_headers]",
                self.headers.static_headers,
            )
            append_toml_entries(
                lines,
                f"[mcp_servers.{self.name}.env_http_headers]",
                self.headers.env_headers,
            )
        if self.env:
            if self.env.env_vars:
                lines.append(f"env_vars = [{format_toml_array(self.env.env_vars)}]")
            append_toml_entries(
                lines,
                f"[mcp_servers.{self.name}.env]",
                self.env.static_env,
            )
        return lines


# Claude conversion models

@dataclass(frozen=True)
class ClaudeSettings:
    model: str | None = None
    permission_mode: str | None = None
    enabled_mcp_servers: tuple[str, ...] = ()
    disabled_mcp_servers: frozenset[str] = frozenset()
    mcp_servers: tuple[ClaudeMcpServer, ...] = ()

    @classmethod
    def from_scope(cls, scope: ScopePaths) -> ClaudeSettings | None:
        claude_mcp = scope.source / ".mcp.json"
        claude_global_mcp = scope.source / ".claude.json"

        settings = load_scope_settings(scope.source)

        mcp_config: Mapping[str, object] = {}
        if claude_mcp.exists():
            mcp_config = json_object(json.loads(claude_mcp.read_text()))
        elif claude_global_mcp.exists():
            mcp_config = json_object(json.loads(claude_global_mcp.read_text()))

        if not settings and not mcp_config:
            return None

        mcp_servers = json_object(mcp_config.get("mcpServers"))
        return cls(
            model=json_string(settings.get("model")),
            permission_mode=json_string(settings.get("permissionMode")),
            enabled_mcp_servers=json_string_tuple(settings.get("enabledMcpjsonServers")),
            disabled_mcp_servers=frozenset(
                json_string_tuple(settings.get("disabledMcpjsonServers"))
            ),
            mcp_servers=tuple(
                ClaudeMcpServer.from_mapping(server_name, json_object(server_config))
                for server_name, server_config in mcp_servers.items()
            ),
        )

    def render_codex_file(self) -> str:
        lines: list[str] = []
        if self.model:
            lines.append(f'model = "{map_model_name(self.model)}"')
        sandbox_mode = map_permission_mode(self.permission_mode)
        if sandbox_mode:
            lines.append(f'sandbox_mode = "{sandbox_mode}"')

        for server in self.mcp_servers:
            if lines:
                lines.append("")
            lines.extend(
                server.render_toml_lines(
                    self.enabled_mcp_servers,
                    self.disabled_mcp_servers,
                )
            )

        return "\n".join(lines) + "\n"

    def to_artifacts(self) -> list[PlannedArtifact]:
        return [
            PlannedArtifact(
                relative_path=CODEX_CONFIG_PATH,
                payload=GeneratedText(self.render_codex_file()),
            )
        ]


@dataclass(frozen=True)
class ClaudeSkill:
    name: str
    description: str
    body: str = ""
    source_path: Path | None = None
    allowed_tools: tuple[str, ...] = ()
    unsupported_fields: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: ParsedDocument) -> ClaudeSkill:
        return cls(
            name=document.frontmatter.required_string("name"),
            description=document.frontmatter.required_string("description"),
            body=document.body,
            source_path=document.path,
            allowed_tools=document.frontmatter.string_tuple("allowed-tools"),
            unsupported_fields=unsupported_frontmatter_fields(
                document.frontmatter.to_dict(),
                ("name", "description", "allowed-tools"),
            ),
        )

    def to_frontmatter(self) -> SimpleYamlFrontmatter:
        return SimpleYamlFrontmatter(
            {
                "name": self.name,
                "description": self.description,
            }
        )

    @classmethod
    def from_claude_file(cls, source_file: Path) -> ClaudeSkill:
        return cls.from_document(ParsedDocument.from_file(source_file))

    def to_artifacts(self) -> list[PlannedArtifact]:
        if not self.source_path:
            raise ValueError("Claude skill is missing source path.")

        artifacts = [
            PlannedArtifact.for_skill(self.source_path, self.render_codex_file()),
        ]
        artifacts.extend(self.support_artifacts())
        return artifacts

    def support_artifacts(self) -> list[PlannedArtifact]:
        if not self.source_path:
            raise ValueError("Claude skill is missing source path.")

        artifacts: list[PlannedArtifact] = []
        skill_root = self.source_path.parent
        target_root = CODEX_SKILLS_ROOT / skill_root.name
        source_files: list[Path] = []
        for dirname in SKILL_SUPPORT_DIRS:
            source_dir = skill_root / dirname
            if not source_dir.exists():
                continue
            source_files.extend(
                source_file
                for source_file in source_dir.rglob("*")
                if source_file.is_file() and is_path_within_root(source_file, skill_root)
            )
        for source_file in sorted(
            source_files,
            key=lambda path: path.relative_to(skill_root).as_posix(),
        ):
            artifacts.append(
                PlannedArtifact.from_source_file(
                    source_file,
                    target_root / source_file.relative_to(skill_root),
                )
            )
        return artifacts

    def render_codex_file(self) -> str:
        return format_frontmatter(self.to_frontmatter(), self.render_codex_body())

    def render_codex_body(self) -> str:
        manual_notes: list[str] = []
        if self.allowed_tools:
            manual_notes.append(
                "Claude `allowed-tools` was preserved as prompt guidance, not a Codex permission boundary.\n\n"
                "You're allowed to use these tools:\n\n"
                f"{format_bullets(self.allowed_tools)}"
            )
        if self.unsupported_fields:
            manual_notes.append(
                "Review unsupported Claude skill fields manually: "
                f"{', '.join(f'`{field_name}`' for field_name in self.unsupported_fields)}."
            )

        if not manual_notes:
            return self.body

        return (
            f"{self.body.rstrip()}\n\n"
            f"{format_manual_migration_block(manual_notes)}\n"
        )

    def report_detail(self) -> str:
        caveats: list[str] = []
        if self.allowed_tools:
            caveats.append("allowed-tools")
        caveats.extend(self.unsupported_fields)
        if not caveats:
            return "Converted Claude skill."
        return "Manual review required for Claude skill fields: " + ", ".join(
            f"`{field_name}`" for field_name in caveats
        ) + "."


@dataclass(frozen=True)
class MigratedCommandSkill:
    name: str
    description: str
    body: str
    provider: str
    source_name: str
    caveats: tuple[str, ...] = ()

    @classmethod
    def from_markdown_file(
        cls,
        source_root: Path,
        source_file: Path,
        name_prefix: str,
        provider: str,
    ) -> MigratedCommandSkill:
        document = ParsedDocument.from_file(source_file)
        command_name = "-".join(source_file.relative_to(source_root).with_suffix("").parts)
        frontmatter = document.frontmatter.to_dict()
        description = document.frontmatter.optional_string("description")
        if not description:
            description = f"Run the migrated {provider} `{command_name}`."
        unsupported_fields = unsupported_frontmatter_fields(
            frontmatter,
            ("description",),
        )
        return cls(
            name=slugify_name(f"{name_prefix}-{command_name}"),
            description=description,
            body=document.body,
            provider=provider,
            source_name=command_name,
            caveats=command_caveats(document.body, unsupported_fields),
        )

    @classmethod
    def from_opencode_config(
        cls,
        command_name: str,
        command_config: Mapping[str, object],
    ) -> MigratedCommandSkill | None:
        template = json_string(command_config.get("template"))
        if not template:
            return None
        description = json_string(command_config.get("description"))
        if not description:
            description = f"Run the migrated OpenCode command `{command_name}`."
        unsupported_fields = tuple(
            sorted(
                field_name
                for field_name in command_config
                if field_name not in ("template", "description")
            )
        )
        return cls(
            name=slugify_name(f"opencode-command-{command_name}"),
            description=description,
            body=template,
            provider="OpenCode command",
            source_name=command_name,
            caveats=command_caveats(template, unsupported_fields),
        )

    def to_artifact(self) -> PlannedArtifact:
        return PlannedArtifact(
            relative_path=CODEX_SKILLS_ROOT / self.name / "SKILL.md",
            payload=GeneratedText(self.render_codex_file()),
            kind=ArtifactKind.SKILL,
        )

    def render_codex_file(self) -> str:
        frontmatter = SimpleYamlFrontmatter(
            {
                "name": self.name,
                "description": self.description,
            }
        )
        return format_frontmatter(frontmatter, self.render_codex_body())

    def render_codex_body(self) -> str:
        manual_notes = [
            f"Migrated from {self.provider} `{self.source_name}` into a Codex skill. "
            f"Invoke it as `${self.name}` and manually rewrite any slash-command behavior that depended on provider-specific runtime expansion."
        ]
        manual_notes.extend(self.caveats)
        body = self.body.strip() or "No command template body was found."
        return (
            f"# {self.name}\n\n"
            f"Use this skill when the user asks to run the migrated {self.provider} `{self.source_name}`.\n\n"
            "## Command Template\n\n"
            f"{body}\n\n"
            f"{format_manual_migration_block(manual_notes)}\n"
        )

    def report_detail(self) -> str:
        return (
            f"Converted {self.provider} `{self.source_name}` to a single-file Codex skill; "
            "review invocation and template placeholder semantics."
        )


@dataclass(frozen=True)
class ClaudeAgent:
    name: str
    description: str
    body: str = ""
    source_path: Path | None = None
    model: str | None = None
    permission_mode: str | None = None
    skills: tuple[str, ...] = ()
    tools: tuple[str, ...] = ()
    disallowed_tools: tuple[str, ...] = ()
    effort: str | None = None
    unsupported_fields: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: ParsedDocument) -> ClaudeAgent:
        return cls(
            name=document.frontmatter.required_string("name"),
            description=document.frontmatter.required_string("description"),
            body=document.body,
            source_path=document.path,
            model=document.frontmatter.optional_string("model"),
            permission_mode=document.frontmatter.optional_string("permissionMode"),
            skills=document.frontmatter.string_tuple("skills"),
            tools=document.frontmatter.string_tuple("tools"),
            disallowed_tools=document.frontmatter.string_tuple("disallowedTools"),
            effort=document.frontmatter.optional_string("effort"),
            unsupported_fields=unsupported_frontmatter_fields(
                document.frontmatter.to_dict(),
                (
                    "name",
                    "description",
                    "model",
                    "permissionMode",
                    "skills",
                    "tools",
                    "disallowedTools",
                    "effort",
                ),
            ),
        )

    @classmethod
    def from_claude_file(cls, source_file: Path) -> ClaudeAgent:
        document = ParsedDocument.from_file(source_file)
        inferred_fields: list[str] = []
        name = document.frontmatter.optional_string("name")
        if not name:
            name = slugify_name(source_file.stem)
            inferred_fields.append("name")

        description = document.frontmatter.optional_string("description")
        if not description:
            heading = first_markdown_heading(document.body)
            if heading:
                description = (
                    f"Migrated Claude subagent inferred from heading `{heading}`."
                )
            else:
                description = (
                    f"Migrated Claude subagent inferred from `{source_file.name}`."
                )
            inferred_fields.append("description")

        return cls(
            name=name,
            description=description,
            body=document.body,
            source_path=document.path,
            model=document.frontmatter.optional_string("model"),
            permission_mode=document.frontmatter.optional_string("permissionMode"),
            skills=document.frontmatter.string_tuple("skills"),
            tools=document.frontmatter.string_tuple("tools"),
            disallowed_tools=document.frontmatter.string_tuple("disallowedTools"),
            effort=document.frontmatter.optional_string("effort"),
            unsupported_fields=unsupported_frontmatter_fields(
                document.frontmatter.to_dict(),
                (
                    "name",
                    "description",
                    "model",
                    "permissionMode",
                    "skills",
                    "tools",
                    "disallowedTools",
                    "effort",
                ),
            )
            + tuple(inferred_fields),
        )

    def to_artifacts(self) -> list[PlannedArtifact]:
        if not self.source_path:
            raise ValueError("Claude agent is missing source path.")

        return [
            PlannedArtifact.for_agent(self.source_path, self.render_codex_file()),
        ]

    def render_codex_file(self) -> str:
        lines = [
            f'name = "{self.name}"',
            f'description = "{self.description}"',
        ]

        if self.model:
            lines.append(f'model = "{map_model_name(self.model)}"')
        if self.effort:
            lines.append(
                f'model_reasoning_effort = "{map_model_effort(self.model, self.effort)}"'
            )
        sandbox_mode = map_permission_mode(self.permission_mode)
        if sandbox_mode:
            lines.append(f'sandbox_mode = "{sandbox_mode}"')

        lines.extend(
            [
                'developer_instructions = """',
                self.render_codex_body().strip(),
                '"""',
            ]
        )

        return "\n".join(lines) + "\n"

    def render_codex_body(self) -> str:
        sections = []
        manual_notes: list[str] = []

        sandbox_mode = map_permission_mode(self.permission_mode)
        if self.permission_mode and not sandbox_mode:
            manual_notes.append(
                f"Claude `permissionMode: {self.permission_mode}` has no direct Codex mapping. "
                "Manually choose `sandbox_mode`, `[permissions]`, MCP tool filters, or app tool filters before relying on this agent."
            )

        if self.skills:
            sections.append(
                "## Skills\n\n"
                "You're allowed to use these skills when working on this task:\n\n"
                f"{format_bullets(self.skills, '$')}"
            )
            manual_notes.append(
                "Claude `skills` preload semantics were preserved as prompt guidance. Verify this agent still discovers the intended skills at runtime."
            )

        if self.tools or self.disallowed_tools:
            tool_section_lines = [
                "## Tools",
                "",
                "Claude tool allow/deny lists were preserved as prompt guidance, not Codex permissions.",
            ]
            if self.tools:
                tool_section_lines.extend(
                    [
                        "",
                        "You're allowed to use these tools:",
                        "",
                        format_bullets(self.tools),
                    ]
                )
            if self.disallowed_tools:
                tool_section_lines.extend(
                    [
                        "",
                        "Don't use these tools:",
                        "",
                        format_bullets(self.disallowed_tools),
                    ]
                )
            sections.append("\n".join(tool_section_lines))
            manual_notes.append(
                "Rebuild Claude `tools` / `disallowedTools` intent with Codex sandbox, MCP tool filters, or app tool filters if you need hard enforcement."
            )

        if self.unsupported_fields:
            manual_notes.append(
                "Review unsupported Claude subagent fields manually: "
                f"{', '.join(f'`{field_name}`' for field_name in self.unsupported_fields)}."
            )

        if manual_notes:
            sections.append(format_manual_migration_block(manual_notes))

        if not sections:
            return self.body

        joined_sections = "\n\n".join(sections)
        return f"{self.body.rstrip()}\n\n{joined_sections}\n"

    def report_detail(self) -> str:
        caveats: list[str] = []
        if self.skills:
            caveats.append("skills")
        if self.tools:
            caveats.append("tools")
        if self.disallowed_tools:
            caveats.append("disallowedTools")
        if self.permission_mode and not map_permission_mode(self.permission_mode):
            caveats.append("permissionMode")
        caveats.extend(self.unsupported_fields)
        if not caveats:
            return "Converted Claude subagent."
        return "Manual review required for Claude subagent fields: " + ", ".join(
            f"`{field_name}`" for field_name in caveats
        ) + "."


# Artifact and deployment planning

@dataclass(frozen=True)
class PlannedArtifact:
    relative_path: Path
    payload: ArtifactPayload
    kind: ArtifactKind = ArtifactKind.FILE

    @classmethod
    def for_skill(cls, source_file: Path, content: str) -> PlannedArtifact:
        return cls(
            relative_path=CODEX_SKILLS_ROOT / source_file.parent.name / "SKILL.md",
            payload=GeneratedText(content),
            kind=ArtifactKind.SKILL,
        )

    @classmethod
    def for_agent(cls, source_file: Path, content: str) -> PlannedArtifact:
        return cls(
            relative_path=CODEX_AGENTS_ROOT / f"{source_file.stem}.toml",
            payload=GeneratedText(content),
            kind=ArtifactKind.AGENT,
        )

    @classmethod
    def from_source_file(cls, source_file: Path, relative_path: Path) -> PlannedArtifact:
        return cls(
            relative_path=relative_path,
            payload=SourceCopy(source_file),
        )

    def prefixed(self, prefix: Path) -> PlannedArtifact:
        return PlannedArtifact(
            relative_path=prefix / self.relative_path,
            payload=self.payload,
            kind=self.kind,
        )

    def without_prefix(self) -> PlannedArtifact:
        return PlannedArtifact(
            relative_path=Path(*self.relative_path.parts[1:]),
            payload=self.payload,
            kind=self.kind,
        )

    def target_path(self, target_root: Path) -> Path:
        return target_root / self.relative_path

    def write_action(
        self,
        target_root: Path,
    ) -> WriteTextAction | CopyFileAction | CreateSymlinkAction:
        target_path = self.target_path(target_root)
        if isinstance(self.payload, GeneratedText):
            return WriteTextAction(target_path, self.payload.content)
        if isinstance(self.payload, SourceSymlink):
            return CreateSymlinkAction(self.payload.source_path, target_path)
        return CopyFileAction(self.payload.source_path, target_path)


@dataclass
class MigrationSummary:
    instructions: int = 0
    skills: int = 0
    subagents: int = 0
    mcp_servers: int = 0
    orphaned_skills: int = 0
    orphaned_subagents: int = 0

    def add(self, other: MigrationSummary) -> None:
        for summary_field in dataclass_fields(self):
            field_name = summary_field.name
            setattr(
                self,
                field_name,
                getattr(self, field_name) + getattr(other, field_name),
            )

    def render(self, deploy_mode: DeployMode, dry_run: bool) -> str:
        suffix = " (dry-run)" if dry_run else ""
        lines = [
            f"Migration summary{suffix}:",
            f"  deploy mode: {deploy_mode.value}",
        ]
        for summary_field in dataclass_fields(self):
            field_name = summary_field.name
            value = getattr(self, field_name)
            if field_name in SUMMARY_OMIT_WHEN_ZERO and value == 0:
                continue
            label = SUMMARY_LABELS.get(field_name, field_name.replace("_", " "))
            lines.append(f"  {label}: {value}")
        return "\n".join(lines)


@dataclass
class ConversionResult:
    summary: MigrationSummary = field(default_factory=MigrationSummary)
    artifacts: list[PlannedArtifact] = field(default_factory=list)
    report_items: list[MigrationReportItem] = field(default_factory=list)

    def add(self, other: ConversionResult) -> None:
        self.summary.add(other.summary)
        self.artifacts.extend(other.artifacts)
        self.report_items.extend(other.report_items)

    def prefixed(self, prefix: Path) -> ConversionResult:
        return ConversionResult(
            summary=self.summary,
            artifacts=[artifact.prefixed(prefix) for artifact in self.artifacts],
            report_items=[
                MigrationReportItem(
                    item.status,
                    prefix / item.path,
                    item.detail,
                )
                for item in self.report_items
            ],
        )


class DeployMode(Enum):
    MERGE = "merge"
    REPLACE = "replace"


@dataclass(frozen=True)
class DeploymentPlan:
    artifacts: tuple[PlannedArtifact, ...]
    orphaned_skill_dirs: tuple[Path, ...]
    orphaned_agent_files: tuple[Path, ...]
    colliding_skill_dirs: tuple[Path, ...]
    colliding_agent_files: tuple[Path, ...]
    summary: MigrationSummary

    def warning_actions(self) -> tuple[WarningAction, ...]:
        return tuple(
            [
                *(
                    WarningAction(
                        f"warning: overwriting existing Codex skill at {collision}"
                    )
                    for collision in self.colliding_skill_dirs
                ),
                *(
                    WarningAction(
                        f"warning: overwriting existing Codex subagent at {collision}"
                    )
                    for collision in self.colliding_agent_files
                ),
            ]
        )

    def write_actions(
        self,
        target_root: Path,
    ) -> tuple[WriteTextAction | CopyFileAction | CreateSymlinkAction, ...]:
        return tuple(artifact.write_action(target_root) for artifact in self.artifacts)

    def delete_actions(self) -> tuple[DeletePathAction, ...]:
        return tuple(
            [
                *(DeletePathAction(orphan, recursive=True) for orphan in self.orphaned_skill_dirs),
                *(DeletePathAction(orphan) for orphan in self.orphaned_agent_files),
            ]
        )


@dataclass(frozen=True)
class ScopeDeployment:
    artifacts: tuple[PlannedArtifact, ...]
    target_root: Path
    components: frozenset[str] = DEFAULT_COMPONENTS

    def planned_skill_dirs(self) -> frozenset[Path]:
        return frozenset(
            artifact.relative_path.parent
            for artifact in self.artifacts
            if artifact.kind == ArtifactKind.SKILL
        )

    def planned_agent_files(self) -> frozenset[Path]:
        return frozenset(
            artifact.relative_path
            for artifact in self.artifacts
            if artifact.kind == ArtifactKind.AGENT
        )

    def orphaned_skill_dirs(self) -> list[Path]:
        if "skills" not in self.components:
            return []

        target_skills_root = self.target_root / CODEX_SKILLS_ROOT
        if not target_skills_root.exists():
            return []

        planned_skill_dirs = self.planned_skill_dirs()
        orphans: list[Path] = []
        for target_skill_dir in target_skills_root.iterdir():
            if not target_skill_dir.is_dir():
                continue
            relative_path = CODEX_SKILLS_ROOT / target_skill_dir.name
            if relative_path not in planned_skill_dirs:
                orphans.append(target_skill_dir)
        return orphans

    def orphaned_agent_files(self) -> list[Path]:
        if "subagents" not in self.components:
            return []

        target_agents_root = self.target_root / CODEX_AGENTS_ROOT
        if not target_agents_root.exists():
            return []

        planned_agent_files = self.planned_agent_files()
        orphans: list[Path] = []
        for target_agent_file in target_agents_root.glob("*.toml"):
            relative_path = CODEX_AGENTS_ROOT / target_agent_file.name
            if relative_path not in planned_agent_files:
                orphans.append(target_agent_file)
        return orphans

    def colliding_skill_dirs(self) -> list[Path]:
        if "skills" not in self.components:
            return []

        target_skills_root = self.target_root / CODEX_SKILLS_ROOT
        if not target_skills_root.exists():
            return []

        collisions: list[Path] = []
        for relative_path in self.planned_skill_dirs():
            target_skill_dir = self.target_root / relative_path
            if target_skill_dir.exists():
                collisions.append(target_skill_dir)
        return collisions

    def colliding_agent_files(self) -> list[Path]:
        if "subagents" not in self.components:
            return []

        target_agents_root = self.target_root / CODEX_AGENTS_ROOT
        if not target_agents_root.exists():
            return []

        collisions: list[Path] = []
        for relative_path in self.planned_agent_files():
            target_agent_file = self.target_root / relative_path
            if target_agent_file.exists():
                collisions.append(target_agent_file)
        return collisions

    def plan(self) -> DeploymentPlan:
        orphaned_skill_dirs = tuple(self.orphaned_skill_dirs())
        orphaned_agent_files = tuple(self.orphaned_agent_files())
        colliding_skill_dirs = tuple(self.colliding_skill_dirs())
        colliding_agent_files = tuple(self.colliding_agent_files())
        return DeploymentPlan(
            artifacts=self.artifacts,
            orphaned_skill_dirs=orphaned_skill_dirs,
            orphaned_agent_files=orphaned_agent_files,
            colliding_skill_dirs=colliding_skill_dirs,
            colliding_agent_files=colliding_agent_files,
            summary=MigrationSummary(
                orphaned_skills=len(orphaned_skill_dirs),
                orphaned_subagents=len(orphaned_agent_files),
            ),
        )


# Conversion orchestration

def convert_tree(
    source_root: Path,
    components: frozenset[str] = DEFAULT_COMPONENTS,
) -> ConversionResult:
    """Convert a fixture tree containing global/ and project/ Claude scopes."""
    result = ConversionResult()
    scopes = [
        ScopePaths(source_root / "global", True),
        ScopePaths(source_root / "project", False),
    ]

    for scope_name, scope in zip(SCOPE_NAMES, scopes):
        if scope.source.exists():
            result.add(convert_scope(scope, components).prefixed(Path(scope_name)))

    if "skills" in components:
        result.artifacts.extend(migration_skill_artifacts(source_root))
    return result


def convert_scope(
    scope: ScopePaths,
    components: frozenset[str] = DEFAULT_COMPONENTS,
) -> ConversionResult:
    result = ConversionResult()

    result.add(convert_instructions(scope))
    result.add(report_other_agent_sources(scope))
    if "skills" in components:
        result.add(convert_skills(scope))
    if "mcp" in components:
        result.add(convert_settings(scope))
    if "subagents" in components:
        result.add(convert_agents(scope))
    return result


def path_exists_with_exact_case(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        return path.name in {child.name for child in path.parent.iterdir()}
    except FileNotFoundError:
        return False


def convert_instructions(scope: ScopePaths) -> ConversionResult:
    source_file = instruction_source_file(
        scope.source,
        scope.is_global,
        path_exists_with_exact_case,
    )
    if not source_file:
        return ConversionResult()

    content = source_file.read_text()
    payload: ArtifactPayload
    if source_file == scope.source / "AGENTS.md":
        report_item = MigrationReportItem(
            "rewritten",
            Path("AGENTS.md"),
            f"Existing Codex instructions already present at {source_file}.",
        )
        return ConversionResult(
            summary=MigrationSummary(instructions=1),
            report_items=[report_item],
        )
    if should_symlink_instructions(content):
        payload = SourceSymlink(source_file)
        report_item = MigrationReportItem(
            "symlinked",
            Path("AGENTS.md"),
            f"Linked to {source_file}.",
        )
    else:
        manual_block = format_manual_migration_block(
            (
                "Claude-only instructions were copied into `AGENTS.md`. Remove Claude hooks, slash commands, and subagent assumptions before relying on this file in Codex.",
            )
        )
        payload = GeneratedText(
            f"{content.rstrip()}\n\n"
            f"{manual_block}\n"
        )
        report_item = MigrationReportItem(
            "manual_fix_required",
            Path("AGENTS.md"),
            "Generated copy contains Claude-only instruction semantics.",
        )
    return ConversionResult(
        summary=MigrationSummary(instructions=1),
        artifacts=[
            PlannedArtifact(
                relative_path=Path("AGENTS.md"),
                payload=payload,
            )
        ],
        report_items=[report_item],
    )


def report_other_agent_sources(scope: ScopePaths) -> ConversionResult:
    result = ConversionResult()
    result.add(report_opencode_sources(scope))
    result.add(report_pi_code_sources(scope))
    return result


def report_opencode_sources(scope: ScopePaths) -> ConversionResult:
    result = ConversionResult()

    for config_path in OPENCODE_CONFIG_FILES:
        source_file = scope.source / config_path
        if not path_exists_with_exact_case(source_file):
            continue
        detected_keys = detected_json_keys(source_file.read_text(), OPENCODE_CONFIG_KEYS)
        if detected_keys:
            detail = (
                "Manual review required for OpenCode config fields: "
                f"{format_backtick_list(detected_keys)}. "
                "This converter does not translate the OpenCode config schema."
            )
        else:
            detail = (
                "Manual review required for OpenCode config. "
                "This converter does not translate the OpenCode config schema."
            )
        result.report_items.append(manual_report_item(config_path, detail))

    result.add(report_manual_paths(scope, OPENCODE_MANUAL_PATHS))

    return result


def report_pi_code_sources(scope: ScopePaths) -> ConversionResult:
    return report_manual_paths(scope, PI_CODE_MANUAL_PATHS)


def report_manual_paths(
    scope: ScopePaths,
    path_labels: Sequence[tuple[Path, str]],
) -> ConversionResult:
    result = ConversionResult()

    for relative_path, label in path_labels:
        if path_exists_with_exact_case(scope.source / relative_path):
            result.report_items.append(
                manual_report_item(
                    relative_path,
                    f"Manual review required for {label}; not converted by this tool.",
                )
            )

    return result


def symlink_target(source_path: Path, target_path: Path) -> str:
    return os.path.relpath(source_path, target_path.parent)

def is_path_within_root(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def convert_settings(scope: ScopePaths) -> ConversionResult:
    claude_settings = ClaudeSettings.from_scope(scope)
    if not claude_settings:
        return ConversionResult()
    if not claude_settings.render_codex_file().strip():
        return ConversionResult()
    return ConversionResult(
        summary=MigrationSummary(mcp_servers=len(claude_settings.mcp_servers)),
        artifacts=claude_settings.to_artifacts(),
        report_items=[
            MigrationReportItem(
                "rewritten",
                CODEX_CONFIG_PATH,
                f"Converted {len(claude_settings.mcp_servers)} MCP server entries.",
            )
        ],
    )


def convert_skills(scope: ScopePaths) -> ConversionResult:
    result = convert_skill_files(scope.source / ".claude" / "skills")
    result.add(convert_command_skills(scope))
    return result


def convert_agents(scope: ScopePaths) -> ConversionResult:
    return convert_agent_files(scope.source / ".claude" / "agents")


def convert_skill_files(source_root: Path) -> ConversionResult:
    result = ConversionResult()
    for source_file in iter_skill_files(source_root):
        claude_skill = ClaudeSkill.from_claude_file(source_file)
        result.artifacts.extend(claude_skill.to_artifacts())
        result.summary.skills += 1
        skill_path = CODEX_SKILLS_ROOT / source_file.parent.name / "SKILL.md"
        append_report_item(
            result.report_items,
            claude_skill.allowed_tools or claude_skill.unsupported_fields,
            skill_path,
            claude_skill.report_detail(),
            claude_skill.report_detail(),
        )
    return result


def convert_command_skills(scope: ScopePaths) -> ConversionResult:
    result = ConversionResult()
    for source_root, name_prefix, provider in COMMAND_FILE_SOURCES:
        result.add(
            convert_markdown_command_files(
                scope.source / source_root,
                name_prefix,
                provider,
            )
        )
    result.add(convert_opencode_config_commands(scope))
    return result


def command_skill_path(command_skill: MigratedCommandSkill) -> Path:
    return CODEX_SKILLS_ROOT / command_skill.name / "SKILL.md"


def append_command_skill(
    result: ConversionResult,
    command_skill: MigratedCommandSkill,
) -> None:
    result.artifacts.append(command_skill.to_artifact())
    result.summary.skills += 1
    result.report_items.append(
        manual_report_item(
            command_skill_path(command_skill),
            command_skill.report_detail(),
        )
    )


def convert_markdown_command_files(
    source_root: Path,
    name_prefix: str,
    provider: str,
) -> ConversionResult:
    result = ConversionResult()
    if not source_root.exists():
        return result
    for source_file in sorted(source_root.rglob("*.md")):
        append_command_skill(
            result,
            MigratedCommandSkill.from_markdown_file(
                source_root,
                source_file,
                name_prefix,
                provider,
            )
        )
    return result


def convert_opencode_config_commands(scope: ScopePaths) -> ConversionResult:
    result = ConversionResult()
    for config_path in OPENCODE_CONFIG_FILES:
        config_file = scope.source / config_path
        if not path_exists_with_exact_case(config_file):
            continue
        try:
            config = load_jsonc_object(config_file.read_text(), json_object)
        except json.JSONDecodeError:
            if detected_json_keys(config_file.read_text(), ("command",)):
                result.report_items.append(
                    manual_report_item(
                        config_path,
                        "OpenCode `command` config was detected but could not be parsed; commands were not converted.",
                    )
                )
            continue
        command_entries = json_object(config.get("command"))
        for command_name, command_config in command_entries.items():
            command_skill = MigratedCommandSkill.from_opencode_config(
                command_name,
                json_object(command_config),
            )
            if not command_skill:
                result.report_items.append(
                    manual_report_item(
                        config_path,
                        f"OpenCode command `{command_name}` has no string `template`; it was not converted.",
                    )
                )
                continue
            append_command_skill(result, command_skill)
    return result


def convert_agent_files(source_root: Path) -> ConversionResult:
    result = ConversionResult()
    for source_file in iter_agent_files(source_root):
        claude_agent = ClaudeAgent.from_claude_file(source_file)
        result.artifacts.extend(claude_agent.to_artifacts())
        result.summary.subagents += 1
        agent_path = CODEX_AGENTS_ROOT / f"{source_file.stem}.toml"
        append_report_item(
            result.report_items,
            claude_agent.skills
            or claude_agent.tools
            or claude_agent.disallowed_tools
            or (
                claude_agent.permission_mode
                and not map_permission_mode(claude_agent.permission_mode)
            )
            or claude_agent.unsupported_fields,
            agent_path,
            claude_agent.report_detail(),
            claude_agent.report_detail(),
        )
    return result


def has_artifact_path(
    conversion_result: ConversionResult,
    suffix: str,
) -> bool:
    return any(
        artifact.relative_path.as_posix().endswith(suffix)
        for artifact in conversion_result.artifacts
    )


def surface_line(status: str, surface: str, detail: str) -> str:
    return f"  {status}: {surface} - {detail}"


def render_migration_surfaces(
    conversion_result: ConversionResult,
    components: frozenset[str],
) -> str:
    summary = conversion_result.summary
    lines = ["", "Migration surfaces:"]

    if summary.instructions:
        lines.append(
            surface_line(
                "active",
                "AGENTS.md",
                f"{summary.instructions} instruction file(s) found.",
            )
        )
    else:
        lines.append(
            surface_line(
                "inactive",
                "AGENTS.md",
                "No supported instruction file found.",
            )
        )

    if "skills" not in components:
        lines.append(surface_line("inactive", "skills", "Not selected by CLI flags."))
    elif summary.skills:
        lines.append(
            surface_line(
                "active",
                "skills",
                f"{summary.skills} skill(s) converted.",
            )
        )
    else:
        lines.append(surface_line("inactive", "skills", "No skills found."))

    if "mcp" not in components:
        lines.append(surface_line("inactive", "MCP config", "Not selected by CLI flags."))
    elif has_artifact_path(conversion_result, ".codex/config.toml"):
        lines.append(
            surface_line(
                "active",
                "MCP config",
                f"{summary.mcp_servers} MCP server(s) converted into config.toml.",
            )
        )
    else:
        lines.append(
            surface_line(
                "inactive",
                "MCP config",
                "No settings or MCP config found.",
            )
        )

    if "subagents" not in components:
        lines.append(surface_line("inactive", "subagents", "Not selected by CLI flags."))
    elif summary.subagents:
        lines.append(
            surface_line(
                "active",
                "subagents",
                f"{summary.subagents} subagent(s) converted.",
            )
        )
    else:
        lines.append(surface_line("inactive", "subagents", "No subagents found."))

    return "\n".join(lines)


def render_migration_report(
    report_items: Sequence[MigrationReportItem],
    deployment_plan: DeploymentPlan,
    deploy_mode: DeployMode,
    dry_run: bool,
) -> str:
    lines = ["", "Migration report:"]
    for item in report_items:
        lines.append(f"  {item.status}: {item.path.as_posix()} - {item.detail}")
    for collision in deployment_plan.colliding_skill_dirs:
        lines.append(
            f"  overwritten: {collision.as_posix()} - Existing Codex skill will be replaced."
        )
    for collision in deployment_plan.colliding_agent_files:
        lines.append(
            f"  overwritten: {collision.as_posix()} - Existing Codex subagent will be replaced."
        )
    if deploy_mode == DeployMode.REPLACE:
        orphan_status = "would_delete" if dry_run else "deleted"
        for orphan in deployment_plan.orphaned_skill_dirs:
            lines.append(
                f"  {orphan_status}: {orphan.as_posix()} - Orphaned generated skill."
            )
        for orphan in deployment_plan.orphaned_agent_files:
            lines.append(
                f"  {orphan_status}: {orphan.as_posix()} - Orphaned generated subagent."
            )
    return "\n".join(lines)


def write_migration_report(target_root: Path, report_text: str) -> None:
    report_path = target_root / MIGRATION_REPORT_PATH
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(f"{report_text.lstrip()}\n")


# Parsing and rendering helpers

def parse_frontmatter(content: str, path: Path | None = None) -> ParsedDocument:
    match = FRONTMATTER_RE.match(content)
    if not match:
        return ParsedDocument(SimpleYamlFrontmatter({}), content, path)

    raw_frontmatter, body = match.groups()
    return ParsedDocument(parse_simple_yaml(raw_frontmatter), body, path)


def parse_simple_yaml(content: str) -> SimpleYamlFrontmatter:
    result: dict[str, YamlValue] = {}
    current_key: str | None = None

    for line in content.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            current_value = result.get(current_key, ())
            if not isinstance(current_value, tuple):
                current_value = (current_value,)
            result[current_key] = (*current_value, parse_scalar(line[4:]))
            continue
        key, _, value = line.partition(":")
        current_key = key.strip()
        value = value.strip()
        if value:
            result[current_key] = parse_scalar(value)
        else:
            result[current_key] = ()

    return SimpleYamlFrontmatter(result)


def parse_scalar(value: str) -> YamlScalar:
    if value == "true":
        return True
    if value == "false":
        return False
    return value.strip('"')


def format_frontmatter(frontmatter: SimpleYamlFrontmatter, body: str) -> str:
    lines = ["---"]
    for key, value in frontmatter.to_dict().items():
        lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append("")
    lines.append(body.lstrip())
    return "\n".join(lines)


def map_model_name(model: str) -> str:
    for mapping in MODEL_PREFIX_MAPPINGS:
        if model.startswith(mapping.source_prefix):
            return mapping.target_model
    return model


def map_model_effort(model: str | None, effort: str) -> str:
    if not model:
        return effort
    for mapping in MODEL_PREFIX_MAPPINGS:
        if model.startswith(mapping.source_prefix):
            return mapping.map_effort(effort)
    return effort


def map_permission_mode(permission_mode: str | None) -> str | None:
    if not permission_mode:
        return None
    return PERMISSION_MODE_MAPPINGS.get(permission_mode)


# Deployment orchestration

def deploy_tree(
    conversion_result: ConversionResult,
    target_root: Path,
    components: frozenset[str] = DEFAULT_COMPONENTS,
) -> DeploymentPlan:
    summary = MigrationSummary()
    artifacts: list[PlannedArtifact] = []
    orphaned_skill_dirs: list[Path] = []
    orphaned_agent_files: list[Path] = []
    colliding_skill_dirs: list[Path] = []
    colliding_agent_files: list[Path] = []
    for scope_name in SCOPE_NAMES:
        prefixed_scope_artifacts = tuple(
            artifact
            for artifact in conversion_result.artifacts
            if artifact.relative_path.parts and artifact.relative_path.parts[0] == scope_name
        )
        scope_artifacts = tuple(
            artifact.without_prefix()
            for artifact in prefixed_scope_artifacts
        )
        if not scope_artifacts:
            continue
        scope_plan = ScopeDeployment(
            scope_artifacts,
            target_root / scope_name,
            components,
        ).plan()
        summary.add(scope_plan.summary)
        artifacts.extend(prefixed_scope_artifacts)
        orphaned_skill_dirs.extend(scope_plan.orphaned_skill_dirs)
        orphaned_agent_files.extend(scope_plan.orphaned_agent_files)
        colliding_skill_dirs.extend(scope_plan.colliding_skill_dirs)
        colliding_agent_files.extend(scope_plan.colliding_agent_files)
    return DeploymentPlan(
        artifacts=tuple(artifacts),
        orphaned_skill_dirs=tuple(orphaned_skill_dirs),
        orphaned_agent_files=tuple(orphaned_agent_files),
        colliding_skill_dirs=tuple(colliding_skill_dirs),
        colliding_agent_files=tuple(colliding_agent_files),
        summary=summary,
    )


def migration_skill_artifacts(source_root: Path) -> list[PlannedArtifact]:
    artifacts: list[PlannedArtifact] = []
    for scope_name in SCOPE_NAMES:
        if not (source_root / scope_name).exists():
            continue
        artifacts.append(
            PlannedArtifact(
                relative_path=Path(scope_name)
                / ".agents"
                / "skills"
                / "migrate-to-codex"
                / "SKILL.md",
                payload=SourceCopy(SKILL_ROOT / "SKILL.md"),
                kind=ArtifactKind.SKILL,
            )
        )
        artifacts.append(
            PlannedArtifact.from_source_file(
                SKILL_ROOT / "references" / "differences.md",
                Path(scope_name)
                / ".agents"
                / "skills"
                / "migrate-to-codex"
                / "references"
                / "differences.md",
            )
        )
    return artifacts


def normalize_scope_root(path: Path, marker: str) -> Path:
    if path.name == marker:
        return path.parent
    return path


def selected_components(args: argparse.Namespace) -> frozenset[str]:
    components = {
        component
        for component in ("mcp", "skills", "subagents")
        if getattr(args, component, False)
    }
    if not components:
        return DEFAULT_COMPONENTS
    return frozenset(components)


# CLI

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Claude-style source tree to Codex (--target). "
            "Omit --mcp/--skills/--subagents to run all three. "
            "See migrate-to-codex SKILL.md."
        ),
    )
    parser.add_argument("--source", required=True, help="Source root (optional global/ + project/ subdirs).")
    parser.add_argument("--target", help="Codex root (required unless --scan-only).")
    parser.add_argument("--mcp", action="store_true", help="Write MCP/settings to config.toml.")
    parser.add_argument("--skills", action="store_true", help="Write skills under .agents/skills.")
    parser.add_argument("--subagents", action="store_true", help="Write agents under .codex/agents.")
    parser.add_argument("--scan-sources", action="store_true", help="Print source inventory before migrate.")
    parser.add_argument("--scan-only", action="store_true", help="Inventory only; omit --target.")
    deploy_group = parser.add_mutually_exclusive_group()
    deploy_group.add_argument(
        "--merge",
        action="store_true",
        help="Keep orphan generated skills/agents (default).",
    )
    deploy_group.add_argument(
        "--replace",
        action="store_true",
        help="Remove orphan generated skills/agents for selected surfaces.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print report; do not write files.")
    args = parser.parse_args()

    source_root = resolve_source_root(args.source)
    if not source_root.exists():
        normalized_candidate = normalize_source_scope_root(
            source_root,
            SOURCE_SCOPE_MARKERS,
        )
        if normalized_candidate.exists():
            source_root = normalized_candidate
        else:
            raise SystemExit(f"Missing source root: {source_root}")

    if args.scan_only and args.target:
        parser.error("--scan-only does not use --target.")
    if not args.scan_only and not args.target:
        parser.error("--target is required unless --scan-only is set.")

    if args.scan_only:
        if (source_root / "global").exists() and (source_root / "project").exists():
            print(
                render_source_inventory(
                    source_root / "global",
                    SOURCE_SCAN_ROOTS,
                    path_exists_with_exact_case,
                )
            )
            print(
                render_scope_inventory(
                    source_root / "global",
                    INSTRUCTION_SOURCE_CANDIDATES,
                    COMMAND_FILE_SOURCES,
                    SKILL_SOURCE_ROOTS,
                    AGENT_SOURCE_ROOTS,
                    iter_skill_files,
                    iter_agent_files,
                    path_exists_with_exact_case,
                )
            )
            print(
                render_source_inventory(
                    source_root / "project",
                    SOURCE_SCAN_ROOTS,
                    path_exists_with_exact_case,
                )
            )
            print(
                render_scope_inventory(
                    source_root / "project",
                    INSTRUCTION_SOURCE_CANDIDATES,
                    COMMAND_FILE_SOURCES,
                    SKILL_SOURCE_ROOTS,
                    AGENT_SOURCE_ROOTS,
                    iter_skill_files,
                    iter_agent_files,
                    path_exists_with_exact_case,
                )
            )
        else:
            normalized_source_root = normalize_source_scope_root(
                source_root,
                SOURCE_SCOPE_MARKERS,
            )
            print(render_source_inventory(normalized_source_root, SOURCE_SCAN_ROOTS, path_exists_with_exact_case))
            print(
                render_scope_inventory(
                    normalized_source_root,
                    INSTRUCTION_SOURCE_CANDIDATES,
                    COMMAND_FILE_SOURCES,
                    SKILL_SOURCE_ROOTS,
                    AGENT_SOURCE_ROOTS,
                    iter_skill_files,
                    iter_agent_files,
                    path_exists_with_exact_case,
                )
            )
        return

    target_root = Path(args.target)
    components = selected_components(args)
    deploy_mode = DeployMode.REPLACE if args.replace else DeployMode.MERGE

    if (source_root / "global").exists() and (source_root / "project").exists():
        conversion_result = convert_tree(source_root, components)
        deployment_target_root = target_root
        deployment_plan = deploy_tree(
            conversion_result,
            deployment_target_root,
            components,
        )
    else:
        source_scope_root = normalize_scope_root(source_root, ".claude")
        deployment_target_root = normalize_scope_root(target_root, ".codex")
        scope = ScopePaths(
            source_scope_root,
            source_scope_root == Path.home(),
        )
        conversion_result = convert_scope(scope, components)
        deployment_plan = ScopeDeployment(
            tuple(conversion_result.artifacts),
            deployment_target_root,
            components,
        ).plan()

    conversion_result.summary.add(deployment_plan.summary)
    source_inventory = ""
    migration_inventory = ""
    if args.scan_sources:
        if (source_root / "global").exists() and (source_root / "project").exists():
            source_inventory = (
                render_source_inventory(
                    source_root / "global",
                    SOURCE_SCAN_ROOTS,
                    path_exists_with_exact_case,
                )
                + "\n"
                + render_source_inventory(
                    source_root / "project",
                    SOURCE_SCAN_ROOTS,
                    path_exists_with_exact_case,
                )
            )
        else:
            source_inventory = render_source_inventory(
                normalize_source_scope_root(source_root, SOURCE_SCOPE_MARKERS),
                SOURCE_SCAN_ROOTS,
                path_exists_with_exact_case,
            )
    if (source_root / "global").exists() and (source_root / "project").exists():
        migration_inventory = (
            render_scope_inventory(
                source_root / "global",
                INSTRUCTION_SOURCE_CANDIDATES,
                COMMAND_FILE_SOURCES,
                SKILL_SOURCE_ROOTS,
                AGENT_SOURCE_ROOTS,
                iter_skill_files,
                iter_agent_files,
                path_exists_with_exact_case,
            )
            + "\n"
            + render_scope_inventory(
                source_root / "project",
                INSTRUCTION_SOURCE_CANDIDATES,
                COMMAND_FILE_SOURCES,
                SKILL_SOURCE_ROOTS,
                AGENT_SOURCE_ROOTS,
                iter_skill_files,
                iter_agent_files,
                path_exists_with_exact_case,
            )
        )
    else:
        migration_inventory = render_scope_inventory(
            normalize_source_scope_root(source_root, SOURCE_SCOPE_MARKERS),
            INSTRUCTION_SOURCE_CANDIDATES,
            COMMAND_FILE_SOURCES,
            SKILL_SOURCE_ROOTS,
            AGENT_SOURCE_ROOTS,
            iter_skill_files,
            iter_agent_files,
            path_exists_with_exact_case,
        )
    migration_surfaces = render_migration_surfaces(conversion_result, components)
    migration_report = render_migration_report(
        conversion_result.report_items,
        deployment_plan,
        deploy_mode,
        args.dry_run,
    )
    for action in deployment_plan.warning_actions():
        print(action.message, file=sys.stderr)
    if not args.dry_run:
        for action in deployment_plan.write_actions(deployment_target_root):
            action.target_path.parent.mkdir(parents=True, exist_ok=True)
            if action.target_path.is_symlink():
                action.target_path.unlink()
            if isinstance(action, WriteTextAction):
                action.target_path.write_text(action.content)
                continue
            if isinstance(action, CreateSymlinkAction):
                if action.target_path.exists():
                    action.target_path.unlink()
                action.target_path.symlink_to(
                    symlink_target(action.source_path, action.target_path)
                )
                continue
            shutil.copy2(action.source_path, action.target_path)
        if deploy_mode == DeployMode.REPLACE:
            for action in deployment_plan.delete_actions():
                if action.recursive:
                    shutil.rmtree(action.path)
                    continue
                action.path.unlink()
        write_migration_report(
            deployment_target_root,
            f"{source_inventory}{migration_inventory}{migration_surfaces}{migration_report}",
        )
    print(conversion_result.summary.render(deploy_mode, args.dry_run))
    if source_inventory:
        print(source_inventory)
    if migration_inventory:
        print(migration_inventory)
    print(migration_surfaces)
    print(migration_report)


if __name__ == "__main__":
    main()
