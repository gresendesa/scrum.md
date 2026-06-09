"""Jinja2 template rendering for Scrum memory files."""

from __future__ import annotations

from dataclasses import dataclass
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
    "created_at": "2026-06-09",
    "updated_at": "2026-06-09",
    "language": "en",
    "memory_root": "scrum",
    "template_profile": "standard",
    "timezone": "America/Sao_Paulo",
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

    data = {**DEFAULT_CONTEXT, **(context or {})}
    files: list[RenderedFile] = []
    for template_name, target in BASE_TEMPLATES:
        files.append(RenderedFile(Path(target), render_template(template_name, data)))
    return files


def write_rendered_files(project_root: Path, files: list[RenderedFile]) -> None:
    """Write rendered files under a project root using deterministic UTF-8 output."""

    for rendered in files:
        path = project_root / rendered.path
        path.parent.mkdir(parents=True, exist_ok=True)
        content = rendered.content
        if content and not content.endswith("\n"):
            content += "\n"
        path.write_text(content, encoding="utf-8")
