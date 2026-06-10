"""Configuration loading for the smd CLI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


DEFAULT_CONFIG: dict[str, Any] = {
    "memory_root": "scrum",
    "templates": {"profile": "standard"},
}


def load_config(root: Path) -> dict[str, Any]:
    """Load `.smd/config.yml` if present and merge it over safe defaults."""

    config_path = root / ".smd" / "config.yml"
    if not config_path.exists():
        return dict(DEFAULT_CONFIG)

    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(".smd/config.yml must contain a YAML mapping.")
    return _deep_merge(DEFAULT_CONFIG, data)


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged
