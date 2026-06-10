"""Local zip template packages for smd memory creation."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from zipfile import BadZipFile, ZIP_DEFLATED, ZipFile, ZipInfo

from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateError
import yaml

from smd.templates import RenderedFile, TemplateRenderError, write_rendered_files


class TemplatePackageError(RuntimeError):
    """Raised when a local template package is invalid."""


class TemplatePackagePackError(RuntimeError):
    """Raised when a template package directory cannot be packed."""


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


@dataclass(frozen=True)
class PackedTemplatePackageResult:
    """Result produced by packing a local template package directory."""

    output: str
    manifest: dict[str, Any]
    signature: dict[str, Any]
    files: list[str]


MANDATORY_MANIFEST_FIELDS = (
    "name",
    "version",
    "description",
    "author",
    "template_engine",
    "smd_version",
    "files",
    "instructions",
)
SIGNATURE_FILE = "SIGNATURE.yaml"
MANIFEST_FILE = "manifest.yaml"
ZIP_EPOCH = (1980, 1, 1, 0, 0, 0)


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


def pack_template_package(
    source_dir: Path,
    output_path: Path,
    *,
    force: bool = False,
) -> PackedTemplatePackageResult:
    """Pack a local template directory into a deterministic checksum-signed zip."""

    source_dir = source_dir.resolve()
    output_path = output_path.resolve()
    manifest = _read_pack_manifest(source_dir)
    _validate_output_path(source_dir, output_path, force=force)

    source_files = _collect_source_files(source_dir)
    checksummed_files = [file for file in source_files if file.as_posix() != SIGNATURE_FILE]
    if not checksummed_files:
        raise TemplatePackagePackError("Template package directory does not contain packable files.")

    signature = _build_signature(source_dir, checksummed_files)
    zip_files = _build_zip_files(source_dir, source_files, signature)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _write_deterministic_zip(output_path, zip_files)

    return PackedTemplatePackageResult(
        output=output_path.as_posix(),
        manifest={
            "name": manifest["name"],
            "version": str(manifest["version"]),
            "template_engine": manifest["template_engine"],
            "smd_version": str(manifest["smd_version"]),
        },
        signature={
            "file": SIGNATURE_FILE,
            "policy": signature["policy"],
            "algorithm": signature["algorithm"],
            "scope": signature["scope"],
            "files": len(signature["files"]),
        },
        files=[path for path, _content in zip_files],
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


def _read_pack_manifest(root: Path) -> dict[str, Any]:
    if not root.exists():
        raise TemplatePackagePackError("Template package directory does not exist.")
    if not root.is_dir():
        raise TemplatePackagePackError("Template package source must be a directory.")

    manifest_path = root / MANIFEST_FILE
    if not manifest_path.exists():
        raise TemplatePackagePackError("Template package directory must include manifest.yaml.")

    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise TemplatePackagePackError("manifest.yaml must contain a YAML mapping.")

    for field in MANDATORY_MANIFEST_FIELDS:
        if field not in data:
            raise TemplatePackagePackError(f"manifest.yaml is missing required field '{field}'.")

    for field in ("name", "version", "description", "author", "template_engine", "smd_version"):
        if not isinstance(data[field], str) or not data[field].strip():
            raise TemplatePackagePackError(f"manifest.yaml field '{field}' must be a non-empty string.")
    if data["template_engine"] != "jinja2":
        raise TemplatePackagePackError("manifest.yaml field 'template_engine' must be 'jinja2'.")

    _validate_manifest_paths(root, data, "files", required_keys=("template", "target"))
    _validate_manifest_paths(root, data, "instructions")
    return data


def _validate_manifest_paths(
    root: Path,
    data: dict[str, Any],
    field: str,
    *,
    required_keys: tuple[str, ...] = (),
) -> None:
    value = data[field]
    if not isinstance(value, list) or not value:
        raise TemplatePackagePackError(f"manifest.yaml field '{field}' must be a non-empty list.")

    for item in value:
        if required_keys:
            if not isinstance(item, dict):
                raise TemplatePackagePackError(f"manifest.yaml field '{field}' entries must be mappings.")
            for key in required_keys:
                path = item.get(key)
                if not isinstance(path, str):
                    raise TemplatePackagePackError(f"manifest.yaml field '{field}' entries require '{key}'.")
                _assert_safe_relative(path, f"Manifest {field}.{key}")
                if key != "target" and not (root / path).exists():
                    raise TemplatePackagePackError(f"Manifest path '{path}' does not exist.")
        else:
            if not isinstance(item, str):
                raise TemplatePackagePackError(f"manifest.yaml field '{field}' entries must be strings.")
            _assert_safe_relative(item, f"Manifest {field}")
            if not (root / item).exists():
                raise TemplatePackagePackError(f"Manifest path '{item}' does not exist.")


def _validate_output_path(source_dir: Path, output_path: Path, *, force: bool) -> None:
    if output_path.suffix != ".zip":
        raise TemplatePackagePackError("Output path must end with .zip.")
    if _is_relative_to(output_path, source_dir):
        raise TemplatePackagePackError("Output zip must not be written inside the source directory.")
    if output_path.exists() and not force:
        raise TemplatePackagePackError("Refusing to overwrite existing output without --force.")
    if output_path.exists() and output_path.is_dir():
        raise TemplatePackagePackError("Output path must be a file, not a directory.")


def _collect_source_files(source_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(source_dir.rglob("*")):
        if path.is_symlink():
            raise TemplatePackagePackError("Template package directory must not contain symlinks.")
        if path.is_file():
            files.append(path.relative_to(source_dir))
    if Path(MANIFEST_FILE) not in files:
        raise TemplatePackagePackError("Template package directory must include manifest.yaml.")
    return files


def _build_signature(source_dir: Path, files: list[Path]) -> dict[str, Any]:
    signed_files = []
    for relative_path in sorted(files, key=lambda path: path.as_posix()):
        content = (source_dir / relative_path).read_bytes()
        signed_files.append(
            {
                "path": relative_path.as_posix(),
                "sha256": sha256(content).hexdigest(),
                "size": len(content),
            }
        )
    payload = "\n".join(f"{item['path']} {item['sha256']}" for item in signed_files).encode("utf-8")
    return {
        "version": "1",
        "policy": "checksum-only",
        "algorithm": "sha256",
        "scope": "file_contents_relative_paths_deterministic_order",
        "files": signed_files,
        "digest": sha256(payload).hexdigest(),
    }


def _build_zip_files(source_dir: Path, files: list[Path], signature: dict[str, Any]) -> list[tuple[str, bytes]]:
    output: list[tuple[str, bytes]] = []
    for relative_path in sorted(files, key=lambda path: path.as_posix()):
        if relative_path.as_posix() == SIGNATURE_FILE:
            continue
        output.append((relative_path.as_posix(), (source_dir / relative_path).read_bytes()))

    signature_content = yaml.safe_dump(signature, sort_keys=False, allow_unicode=False).encode("utf-8")
    output.append((SIGNATURE_FILE, signature_content))
    return sorted(output, key=lambda item: item[0])


def _write_deterministic_zip(output_path: Path, files: list[tuple[str, bytes]]) -> None:
    with ZipFile(output_path, "w", compression=ZIP_DEFLATED) as archive:
        for relative_path, content in files:
            info = ZipInfo(relative_path, ZIP_EPOCH)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, content)


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
