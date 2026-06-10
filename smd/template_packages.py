"""Local zip template packages for smd memory creation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from zipfile import BadZipFile, ZipFile

from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateError
import yaml

from smd.templates import RenderedFile, TemplateRenderError, write_rendered_files


class TemplatePackageError(RuntimeError):
    """Raised when a local template package is invalid."""


@dataclass(frozen=True)
class TemplatePackageFile:
    """One template-to-target mapping from a package manifest."""

    template: str
    target: Path


@dataclass(frozen=True)
class TemplatePackage:
    """Loaded template package metadata."""

    name: str
    version: str | None
    files: list[TemplatePackageFile]
    instructions: list[str]


@dataclass(frozen=True)
class TemplatePackageRenderResult:
    """Result produced by rendering a template package."""

    package: dict[str, Any]
    files: list[str]
    instructions: list[str]


def render_template_package(
    package_path: Path,
    target_root: Path,
    context: dict[str, Any],
    *,
    force: bool = False,
) -> TemplatePackageRenderResult:
    """Render a local zip package into a target project root."""

    package_path = package_path.resolve()
    target_root = target_root.resolve()
    with TemporaryDirectory() as tmp:
        extracted = Path(tmp)
        package = _extract_package(package_path, extracted)
        rendered = _render_package_files(extracted, package, context)
        _prevent_unapproved_overwrites(target_root, rendered, force=force)
        write_rendered_files(target_root, rendered)
        return TemplatePackageRenderResult(
            package={"name": package.name, "version": package.version},
            files=[file.path.as_posix() for file in rendered],
            instructions=package.instructions,
        )


def _extract_package(package_path: Path, target: Path) -> TemplatePackage:
    if not package_path.exists():
        raise TemplatePackageError("Template package does not exist.")
    if package_path.suffix != ".zip":
        raise TemplatePackageError("Template package must be a .zip file.")

    try:
        with ZipFile(package_path) as archive:
            for member in archive.infolist():
                destination = (target / member.filename).resolve()
                if not _is_relative_to(destination, target):
                    raise TemplatePackageError("Template package contains an unsafe path.")
            archive.extractall(target)
    except BadZipFile as exc:
        raise TemplatePackageError("Template package is not a valid zip archive.") from exc

    return _read_manifest(target)


def _read_manifest(root: Path) -> TemplatePackage:
    manifest_path = root / "template.yml"
    if not manifest_path.exists():
        manifest_path = root / "template.yaml"
    if not manifest_path.exists():
        raise TemplatePackageError("Template package must include template.yml or template.yaml.")

    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise TemplatePackageError("Template manifest must contain a YAML mapping.")

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        raise TemplatePackageError("Template manifest must define a non-empty name.")

    raw_files = data.get("files")
    if not isinstance(raw_files, list) or not raw_files:
        raise TemplatePackageError("Template manifest must define at least one file mapping.")

    files: list[TemplatePackageFile] = []
    for raw_file in raw_files:
        if not isinstance(raw_file, dict):
            raise TemplatePackageError("Template file mappings must be YAML mappings.")
        template = raw_file.get("template")
        target = raw_file.get("target")
        if not isinstance(template, str) or not isinstance(target, str):
            raise TemplatePackageError("Template file mappings require template and target.")
        _assert_safe_relative(template, "Template path")
        _assert_safe_relative(target, "Target path")
        if not (root / template).exists():
            raise TemplatePackageError(f"Template file '{template}' does not exist in the package.")
        files.append(TemplatePackageFile(template=template, target=Path(target)))

    instructions = data.get("instructions", [])
    if not isinstance(instructions, list) or not instructions:
        raise TemplatePackageError("Template manifest must list at least one LLM instruction file.")
    for instruction in instructions:
        if not isinstance(instruction, str):
            raise TemplatePackageError("Instruction file paths must be strings.")
        _assert_safe_relative(instruction, "Instruction path")
        if not (root / instruction).exists():
            raise TemplatePackageError(f"Instruction file '{instruction}' does not exist in the package.")

    version = data.get("version")
    if version is not None:
        version = str(version)

    return TemplatePackage(name=name, version=version, files=files, instructions=instructions)


def _render_package_files(root: Path, package: TemplatePackage, context: dict[str, Any]) -> list[RenderedFile]:
    environment = Environment(
        loader=FileSystemLoader(root),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
    )
    rendered: list[RenderedFile] = []
    for file in package.files:
        try:
            content = environment.get_template(file.template).render(**context)
        except TemplateError as exc:
            raise TemplateRenderError(f"failed to render template '{file.template}': {exc}") from exc
        rendered.append(RenderedFile(file.target, content))
    return rendered


def _prevent_unapproved_overwrites(target_root: Path, files: list[RenderedFile], *, force: bool) -> None:
    if force:
        return
    conflicting: list[str] = []
    for rendered in files:
        path = target_root / rendered.path
        if path.exists():
            existing = path.read_text(encoding="utf-8")
            content = rendered.content
            if content and not content.endswith("\n"):
                content += "\n"
            if existing != content:
                conflicting.append(rendered.path.as_posix())
    if conflicting:
        joined = ", ".join(conflicting)
        raise TemplatePackageError(f"Refusing to overwrite existing files without --force: {joined}.")


def _assert_safe_relative(path: str, label: str) -> None:
    candidate = Path(path)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise TemplatePackageError(f"{label} must be a safe relative path.")


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False
