"""Jinja2 template rendering for Scrum memory files."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader, StrictUndefined, TemplateError


class TemplateRenderError(RuntimeError):
    """Raised when a Scrum memory template cannot be rendered."""


@dataclass(frozen=True)
class RenderedFile:
    """A rendered template and its target path relative to the project root."""

    path: Path
    content: str


DEFAULT_CONTEXT: dict[str, Any] = {
    "project_name": "scrum.md",
    "owner": "Guilherme",
    "language": "en",
    "memory_root": "scrum",
    "template_profile": "standard",
    "timezone": "America/Sao_Paulo",
    "purpose": "Build and maintain an auditable Scrum memory for AI-assisted development.",
    "nnr": [
        "The official project memory lives under `scrum/`.",
        "Memory files must use stable section metadata and references.",
        "No backlog item or sprint may be marked `done` without validation evidence.",
        "Protected governance changes require explicit Product Owner approval.",
    ],
    "strategic_priority": [
        "Deliver a small, real MVP first.",
        "Favor deterministic file operations and parseable output.",
        "Validate behavior with automated tests before expanding scope.",
    ],
    "memory_policy": [
        "Consolidators keep concise summaries only.",
        "Detailed backlog items belong in `scrum/backlog/`.",
        "Detailed sprints belong in `scrum/sprints/`.",
        "Historical records must be marked obsolete or superseded instead of deleted.",
    ],
}


BASE_TEMPLATES: tuple[tuple[str, str], ...] = (
    ("default/CONSTITUTION.md.j2", "scrum/CONSTITUTION.md"),
    ("default/scrum/backlog.md.j2", "scrum/backlog.md"),
    ("default/scrum/sprints.md.j2", "scrum/sprints.md"),
    ("default/scrum/decisions.md.j2", "scrum/decisions.md"),
    ("default/scrum/experience.md.j2", "scrum/experience.md"),
    ("default/scrum/architecture.md.j2", "scrum/architecture.md"),
)


def environment() -> Environment:
    """Create the strict Jinja environment used by smd templates."""

    return Environment(
        loader=PackageLoader("smd", "templates"),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
        trim_blocks=False,
        lstrip_blocks=False,
    )


def render_template(name: str, context: dict[str, Any]) -> str:
    """Render one package template with strict variable checking."""

    try:
        return environment().get_template(name).render(**context)
    except TemplateError as exc:
        raise TemplateRenderError(f"failed to render template '{name}': {exc}") from exc


def render_project_memory(context: dict[str, Any] | None = None) -> list[RenderedFile]:
    """Render the base Scrum memory files for a project."""

    data = {**default_context(), **(context or {})}
    files: list[RenderedFile] = []
    for template_name, target in BASE_TEMPLATES:
        files.append(RenderedFile(Path(target), render_template(template_name, data)))
    return files


def default_context() -> dict[str, Any]:
    """Build default template values that depend on render time."""

    today = date.today().isoformat()
    return {**DEFAULT_CONTEXT, "created_at": today, "updated_at": today}


def write_rendered_files(project_root: Path, files: list[RenderedFile]) -> None:
    """Write rendered files under a project root using deterministic UTF-8 output."""

    for rendered in files:
        path = project_root / rendered.path
        path.parent.mkdir(parents=True, exist_ok=True)
        content = rendered.content
        if content and not content.endswith("\n"):
            content += "\n"
        path.write_text(content, encoding="utf-8")
