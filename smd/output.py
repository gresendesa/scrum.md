"""Stable command output helpers for the smd CLI."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


def json_safe(value: Any) -> Any:
    """Convert common Python values into JSON-serializable values."""

    if is_dataclass(value):
        return json_safe(asdict(value))
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [json_safe(item) for item in value]
    return value


def envelope(
    *,
    ok: bool,
    command: str,
    root: Path,
    data: Any,
    warnings: list[Any] | None = None,
    errors: list[Any] | None = None,
) -> dict[str, Any]:
    """Build the stable JSON envelope shared by CLI commands."""

    return {
        "ok": ok,
        "command": command,
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "root": str(root),
        "data": json_safe(data),
        "warnings": json_safe(warnings or []),
        "errors": json_safe(errors or []),
    }


def dumps(value: dict[str, Any]) -> str:
    """Serialize command output deterministically."""

    return json.dumps(value, ensure_ascii=False, sort_keys=True)
