"""CLI entrypoint for Scrum memory orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Any

import typer

from smd.config import load_config
from smd.memory import MemoryRepository, ScrumRecord
from smd.output import dumps, envelope
from smd.template_packages import (
    TemplatePackageError,
    TemplatePackagePackError,
    TemplatePackageVariable,
    inspect_template_package,
    init_from_template_package,
    pack_template_package,
    render_template_package,
)
from smd.templates import DEFAULT_CONTEXT, TemplateRenderError, default_context


app = typer.Typer(
    name="smd",
    help="Scrum memory orchestration for AI-assisted development.",
    add_completion=False,
    no_args_is_help=True,
)
backlog_app = typer.Typer(help="Backlog foundation queries.", no_args_is_help=True)
sprint_app = typer.Typer(help="Sprint foundation queries.", no_args_is_help=True)
template_app = typer.Typer(help="Local template package commands.", no_args_is_help=True)

app.add_typer(backlog_app, name="backlog")
app.add_typer(sprint_app, name="sprint")
app.add_typer(template_app, name="template")


class CliError(RuntimeError):
    """Structured CLI error."""

    def __init__(self, code: str, message: str, *, suggestion: str | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.suggestion = suggestion

    def as_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": "blocking",
            "file": None,
            "section": None,
            "message": self.message,
            "target": None,
            "suggestion": self.suggestion,
        }


@app.callback()
def main(
    ctx: typer.Context,
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit a stable JSON envelope."),
    ] = False,
    root: Annotated[
        Path,
        typer.Option("--root", file_okay=False, resolve_path=True, help="Project root."),
    ] = Path("."),
    quiet: Annotated[
        bool,
        typer.Option("--quiet", help="Suppress non-JSON informational output."),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", help="Emit additional human-readable details."),
    ] = False,
) -> None:
    """Run smd commands."""

    resolved_root = root.resolve()
    ctx.obj = {
        "json": json_output,
        "root": resolved_root,
        "quiet": quiet,
        "verbose": verbose,
    }
    try:
        ctx.obj["config"] = load_config(resolved_root)
    except ValueError as exc:
        _fail(ctx, "INVALID_CONFIG", str(exc), suggestion="Fix .smd/config.yml.")


@app.command()
def init(
    ctx: typer.Context,
    template_package: Annotated[
        Path | None,
        typer.Option(
            "--template-package",
            dir_okay=False,
            resolve_path=True,
            help="Local signed template package .zip.",
        ),
    ] = None,
    target: Annotated[
        Path | None,
        typer.Option("--target", file_okay=False, resolve_path=True, help="Root to initialize."),
    ] = None,
    force: Annotated[bool, typer.Option("--force", help="Overwrite existing Scrum memory and config.")] = False,
    project_name: Annotated[str | None, typer.Option("--project-name", help="Template project_name value.")] = None,
    owner: Annotated[str | None, typer.Option("--owner", help="Template owner value.")] = None,
    language: Annotated[str | None, typer.Option("--language", help="Template language value.")] = None,
    purpose: Annotated[str | None, typer.Option("--purpose", help="Template purpose value.")] = None,
    memory_root: Annotated[str | None, typer.Option("--memory-root", help="Scrum memory root directory.")] = None,
    template_profile: Annotated[str | None, typer.Option("--template", help="Template profile name for config.")] = None,
) -> None:
    """Initialize Scrum memory from a signed local template package."""

    root = _root(ctx)
    target_root = (target or root).resolve()
    context = _template_context(ctx)
    json_output = _json_output(ctx)

    if template_package is None:
        if json_output:
            _fail(
                ctx,
                "INVALID_INIT_INPUT",
                "--template-package is required when --json is used.",
                command="smd init",
                root=target_root,
                suggestion="Pass --template-package <file.zip> for deterministic JSON execution.",
            )
        template_package = Path(typer.prompt("Template package")).expanduser().resolve()
    if not template_package.exists():
        _fail(
            ctx,
            "INVALID_INIT_INPUT",
            f"Template package does not exist: {template_package}.",
            command="smd init",
            root=target_root,
            suggestion="Pass a local signed .zip package created by smd pack.",
        )

    try:
        package = inspect_template_package(template_package, verify_signature=True)
    except TemplatePackageError as exc:
        _fail(
            ctx,
            "INIT_FAILED",
            str(exc),
            command="smd init",
            root=target_root,
            suggestion="Use a valid signed template package created by smd pack.",
        )

    option_values = {
        "project_name": project_name,
        "owner": owner,
        "language": language,
        "purpose": purpose,
        "memory_root": memory_root,
        "template_profile": template_profile,
    }
    context.update(_collect_init_variables(ctx, package.variables, context, option_values))
    memory_root = str(context["memory_root"])
    template_profile = str(context["template_profile"])

    if not memory_root.strip() or Path(memory_root).is_absolute() or ".." in Path(memory_root).parts:
        _fail(
            ctx,
            "INVALID_INIT_INPUT",
            "--memory-root must be a safe relative path.",
            command="smd init",
            root=target_root,
            suggestion="Use a relative memory root such as 'scrum'.",
        )

    try:
        result = init_from_template_package(
            template_package,
            target_root,
            context,
            force=force,
            memory_root=memory_root,
            template_profile=template_profile,
        )
    except (TemplatePackageError, TemplateRenderError) as exc:
        _fail(
            ctx,
            "INIT_FAILED",
            str(exc),
            command="smd init",
            root=target_root,
            suggestion="Use a valid signed template package and an empty target root, or pass --force explicitly.",
        )

    _emit(
        ctx,
        ok=True,
        command="smd init",
        root=target_root,
        data=result,
        human=f"Initialized Scrum memory in {target_root}.",
    )


@app.command()
def validate(ctx: typer.Context) -> None:
    """Validate the Scrum memory graph."""

    repo = _repo(ctx)
    result = repo.validate()
    data = {"total_sections": result.total_sections, "total_edges": result.total_edges} if result.ok else None
    _emit(
        ctx,
        ok=result.ok,
        command="smd validate",
        data=data,
        warnings=result.warnings,
        errors=result.errors,
        human="Memory validation passed." if result.ok else "Memory validation failed.",
        exit_code=0 if result.ok else 1,
    )


@app.command()
def pack(
    ctx: typer.Context,
    directory: Annotated[Path, typer.Argument(help="Local template package directory.")],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", dir_okay=False, resolve_path=True, help="Output .zip path."),
    ] = None,
    force: Annotated[bool, typer.Option("--force", help="Overwrite an existing output zip.")] = False,
) -> None:
    """Create a checksum-signed template package zip from a directory."""

    root = _root(ctx)
    source_dir = directory.resolve()
    output_path = (output or (root / f"{source_dir.name}.zip")).resolve()
    try:
        result = pack_template_package(source_dir, output_path, force=force)
    except TemplatePackagePackError as exc:
        _fail(
            ctx,
            "PACK_FAILED",
            str(exc),
            command="smd pack",
            suggestion="Fix the package directory, manifest.yaml, or output path.",
        )

    _emit(
        ctx,
        ok=True,
        command="smd pack",
        data=result,
        human=f"Packed template package to {result.output}.",
    )


@sprint_app.command("active")
def sprint_active(ctx: typer.Context) -> None:
    """Return active sprints."""

    sprints = [_record_dict(record) for record in _repo(ctx).active_sprints()]
    _emit(
        ctx,
        ok=True,
        command="smd sprint active",
        data={"sprints": sprints},
        human=_format_records(sprints, "No active sprint."),
    )


@backlog_app.command("list")
def backlog_list(
    ctx: typer.Context,
    status: Annotated[str | None, typer.Option("--status", help="Filter by status.")] = None,
    pending: Annotated[bool, typer.Option("--pending", help="Only list pending todo/refined items.")] = False,
) -> None:
    """List backlog records using foundation queries."""

    repo = _repo(ctx)
    if pending:
        records = repo.pending_backlog_items()
    elif status is not None:
        records = [
            record
            for record in repo.by_status(status, under="scrum/backlog")
            if record.section.startswith("backlog.item.")
        ]
    else:
        records = [record for record in repo.sections() if record.section.startswith("backlog.item.")]

    items = [_record_dict(record) for record in records]
    _emit(
        ctx,
        ok=True,
        command="smd backlog list",
        data={"items": items},
        human=_format_records(items, "No backlog items found."),
    )


@template_app.command("render")
def template_render(
    ctx: typer.Context,
    package: Annotated[Path, typer.Argument(exists=True, dir_okay=False, help="Local .zip template package.")],
    target: Annotated[
        Path | None,
        typer.Option("--target", file_okay=False, resolve_path=True, help="Root where files are rendered."),
    ] = None,
    force: Annotated[bool, typer.Option("--force", help="Overwrite files that differ from rendered output.")] = False,
    project_name: Annotated[str | None, typer.Option("--project-name", help="Template project_name value.")] = None,
    owner: Annotated[str | None, typer.Option("--owner", help="Template owner value.")] = None,
) -> None:
    """Render Scrum memory files from a local template zip package."""

    root = _root(ctx)
    target_root = (target or root).resolve()
    context = _template_context(ctx)
    if project_name is not None:
        context["project_name"] = project_name
    if owner is not None:
        context["owner"] = owner

    try:
        result = render_template_package(package, target_root, context, force=force)
    except (TemplatePackageError, TemplateRenderError) as exc:
        _fail(
            ctx,
            "INVALID_TEMPLATE_PACKAGE",
            str(exc),
            command="smd template render",
            root=target_root,
            suggestion="Fix the local template package manifest, files, or variables.",
        )

    _emit(
        ctx,
        ok=True,
        command="smd template render",
        root=target_root,
        data=result,
        human=f"Rendered {len(result.files)} file(s) from template package '{result.package['name']}'.",
    )


def _repo(ctx: typer.Context) -> MemoryRepository:
    return MemoryRepository.from_config(_root(ctx), _config(ctx))


def _root(ctx: typer.Context) -> Path:
    return ctx.find_root().obj["root"]


def _config(ctx: typer.Context) -> dict[str, Any]:
    return ctx.find_root().obj["config"]


def _json_output(ctx: typer.Context) -> bool:
    return bool(ctx.find_root().obj["json"])


def _template_context(ctx: typer.Context) -> dict[str, Any]:
    config = _config(ctx)
    return {
        **default_context(),
        **{key: value for key, value in config.items() if not isinstance(value, dict)},
        "template_profile": config.get("templates", {}).get("profile", DEFAULT_CONTEXT["template_profile"]),
    }


def _collect_init_variables(
    ctx: typer.Context,
    variables: list[TemplatePackageVariable],
    context: dict[str, Any],
    option_values: dict[str, Any],
) -> dict[str, Any]:
    json_output = _json_output(ctx)
    values: dict[str, Any] = {}
    declared_names = {variable.name for variable in variables}

    for name, value in option_values.items():
        if value is not None:
            values[name] = _validate_init_value(ctx, name, value)

    for variable in variables:
        if variable.name in values:
            continue
        default = variable.default if variable.default is not None else context.get(variable.name)
        if json_output:
            if default is None and variable.required:
                _fail(
                    ctx,
                    "INVALID_INIT_INPUT",
                    f"Missing required template variable '{variable.name}'.",
                    command="smd init",
                    suggestion="Pass the variable through an init option or use a package default.",
                )
            if default is not None:
                values[variable.name] = _validate_init_value(ctx, variable.name, default)
            continue

        prompt_kwargs: dict[str, Any] = {}
        if default is not None:
            prompt_kwargs["default"] = str(default)
        value = typer.prompt(variable.prompt, **prompt_kwargs)
        if not value and not variable.required:
            values[variable.name] = ""
        else:
            values[variable.name] = _validate_init_value(ctx, variable.name, value)

    for name in ("memory_root", "template_profile"):
        if name not in values:
            values[name] = _validate_init_value(ctx, name, context[name])

    for name, value in option_values.items():
        if value is not None and name not in declared_names:
            values[name] = _validate_init_value(ctx, name, value)

    return values


def _validate_init_value(ctx: typer.Context, name: str, value: Any) -> Any:
    if isinstance(value, str) and not value.strip():
        _fail(
            ctx,
            "INVALID_INIT_INPUT",
            f"Template variable '{name}' must not be blank.",
            command="smd init",
        )
    return value


def _record_dict(record: ScrumRecord) -> dict[str, Any]:
    return {
        "uri": record.uri,
        "section": record.section,
        "title": record.title,
        "status": record.status,
        "metadata": record.metadata,
    }


def _format_records(records: list[dict[str, Any]], empty: str) -> str:
    if not records:
        return empty
    return "\n".join(f"{record['section']} [{record['status']}] {record['title'] or ''}".rstrip() for record in records)


def _emit(
    ctx: typer.Context,
    *,
    ok: bool,
    command: str,
    data: Any,
    warnings: list[Any] | None = None,
    errors: list[Any] | None = None,
    human: str,
    exit_code: int = 0,
    root: Path | None = None,
) -> None:
    output = envelope(
        ok=ok,
        command=command,
        root=root or _root(ctx),
        data=data,
        warnings=warnings,
        errors=errors,
    )
    if ctx.find_root().obj["json"]:
        typer.echo(dumps(output))
    elif not ctx.find_root().obj["quiet"]:
        typer.echo(human)
    raise typer.Exit(exit_code)


def _fail(
    ctx: typer.Context,
    code: str,
    message: str,
    *,
    command: str | None = None,
    root: Path | None = None,
    suggestion: str | None = None,
) -> None:
    error = CliError(code, message, suggestion=suggestion)
    _emit(
        ctx,
        ok=False,
        command=command or ctx.info_name or "smd",
        root=root,
        data=None,
        errors=[error.as_dict()],
        human=message,
        exit_code=1,
    )


if __name__ == "__main__":
    app()
