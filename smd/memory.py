"""Structured access to Scrum memory through MDBind."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re
from typing import Any, Iterable

from mdbind.index import index_repository
from mdbind.parser import ParseError


ACTIVE_SPRINT_STATUSES = {"planned", "doing", "blocked", "review"}
SPRINT_STATUSES = {"planned", "doing", "blocked", "review", "done", "cancelled", "obsolete"}
BACKLOG_STATUSES = {"todo", "refined", "planned", "doing", "blocked", "review", "done", "obsolete"}
REQUIRED_MEMORY_FILES = (
    "CONSTITUTION.md",
    "backlog.md",
    "sprints.md",
    "decisions.md",
    "experience.md",
    "architecture.md",
)


@dataclass(frozen=True)
class MemoryErrorItem:
    """A structured memory validation error."""

    code: str
    severity: str
    file: str | None
    section: str | None
    message: str
    target: str | None = None
    suggestion: str | None = None


@dataclass(frozen=True)
class ValidationResult:
    """Validation output produced by memory primitives."""

    ok: bool
    errors: list[MemoryErrorItem]
    warnings: list[MemoryErrorItem]
    total_sections: int = 0
    total_edges: int = 0


@dataclass(frozen=True)
class ScrumRecord:
    """A section record relevant to Scrum operations."""

    uri: str
    section: str
    title: str | None
    status: str | None
    metadata: dict[str, Any]

    @property
    def path(self) -> Path:
        return Path(self.uri.split("#", 1)[0])


class MemoryRepository:
    """Query and validate a Scrum memory repository."""

    def __init__(self, project_root: str | Path, memory_root: str | Path = "scrum") -> None:
        self.project_root = Path(project_root).resolve()
        self.memory_root = (self.project_root / memory_root).resolve()
        self._graph = None

    @classmethod
    def from_config(cls, project_root: str | Path, config: dict[str, Any] | None = None) -> "MemoryRepository":
        memory_root = (config or {}).get("memory_root", "scrum")
        return cls(project_root, memory_root)

    @property
    def graph(self):
        if self._graph is None:
            self._graph = index_repository(self.project_root)
        return self._graph

    def required_files(self) -> list[Path]:
        return [self.memory_root / name for name in REQUIRED_MEMORY_FILES]

    def missing_required_files(self) -> list[Path]:
        return [path for path in self.required_files() if not path.exists()]

    def sections(self) -> list[ScrumRecord]:
        records: list[ScrumRecord] = []
        for uri, section in sorted(self.graph.index.sections.items()):
            metadata = _json_safe(section.metadata)
            records.append(
                ScrumRecord(
                    uri=uri,
                    section=str(metadata.get("id", uri.rsplit("#", 1)[-1])),
                    title=_optional_str(metadata.get("title")),
                    status=_optional_str(metadata.get("status")),
                    metadata=metadata,
                )
            )
        return records

    def by_status(self, status: str, *, under: str | None = None) -> list[ScrumRecord]:
        return [
            record
            for record in self.sections()
            if record.status == status and (under is None or f"/{under.strip('/')}/" in record.uri)
        ]

    def active_sprints(self) -> list[ScrumRecord]:
        return [
            record
            for record in self.sections()
            if record.section.startswith("sprint.") and record.status in ACTIVE_SPRINT_STATUSES
        ]

    def pending_backlog_items(self) -> list[ScrumRecord]:
        return [
            record
            for record in self.sections()
            if record.section.startswith("backlog.item.") and record.status in {"todo", "refined"}
        ]

    def next_backlog_id(self) -> str:
        return _next_id(self._scan_ids(r"\bB-(\d{3})\b"), "B")

    def next_decision_id(self) -> str:
        return _next_id(self._scan_ids(r"\bDEC-(\d{3})\b"), "DEC")

    def next_experience_id(self) -> str:
        return _next_id(self._scan_ids(r"\bEXP-(\d{3})\b"), "EXP")

    def next_sprint_id(self, year: int | None = None) -> str:
        sprint_year = year or date.today().year
        values = self._scan_ids(rf"\bSPR-{sprint_year}-(\d{{2}})\b")
        next_number = max(values, default=0) + 1
        return f"SPR-{sprint_year}-{next_number:02d}"

    def validate(self) -> ValidationResult:
        errors: list[MemoryErrorItem] = []
        for path in self.missing_required_files():
            errors.append(
                MemoryErrorItem(
                    code="MISSING_REQUIRED_FILE",
                    severity="blocking",
                    file=str(path.relative_to(self.project_root)),
                    section=None,
                    message="Required Scrum memory file is missing.",
                    suggestion="Create the file from the default templates.",
                )
            )

        try:
            graph = self.graph
        except ParseError as exc:
            errors.append(
                MemoryErrorItem(
                    code="MDBIND_PARSE_ERROR",
                    severity="blocking",
                    file=None,
                    section=None,
                    message=str(exc),
                )
            )
            return ValidationResult(ok=False, errors=errors, warnings=[])

        all_uris = set(graph.index.sections)
        seen_sections: dict[str, str] = {}
        for record in self.sections():
            if not self._is_memory_record(record):
                continue
            if record.section in seen_sections:
                errors.append(
                    MemoryErrorItem(
                        code="DUPLICATE_SECTION",
                        severity="blocking",
                        file=_relative_file(record.uri, self.project_root),
                        section=record.section,
                        message="Section identifier appears more than once.",
                        target=seen_sections[record.section],
                        suggestion="Rename one section to a globally unique identifier.",
                    )
                )
            else:
                seen_sections[record.section] = record.uri

            if re.fullmatch(r"backlog\.item\.B-\d{3}", record.section) and record.status not in BACKLOG_STATUSES:
                errors.append(_invalid_status(record, self.project_root, sorted(BACKLOG_STATUSES)))
            if re.fullmatch(r"sprint\.SPR-\d{4}-\d{2}", record.section) and record.status not in SPRINT_STATUSES:
                errors.append(_invalid_status(record, self.project_root, sorted(SPRINT_STATUSES)))

        for src_uri, section in graph.index.sections.items():
            for directive in section.directives:
                if directive.type in {"ref", "include"} and directive.target_uri not in all_uris:
                    errors.append(
                        MemoryErrorItem(
                            code="BROKEN_INCLUDE" if directive.type == "include" else "BROKEN_REF",
                            severity="blocking",
                            file=_relative_file(src_uri, self.project_root),
                            section=src_uri.rsplit("#", 1)[-1],
                            message="Reference target does not exist.",
                            target=directive.target_uri,
                            suggestion="Create the missing section or update the directive target.",
                        )
                    )

        total_edges = sum(len(targets) for targets in graph.outgoing_edges.values())
        return ValidationResult(
            ok=not errors,
            errors=errors,
            warnings=[],
            total_sections=len(all_uris),
            total_edges=total_edges,
        )

    def _scan_ids(self, pattern: str) -> list[int]:
        regex = re.compile(pattern)
        values: list[int] = []
        for record in self.sections():
            if not self._is_memory_record(record):
                continue
            values.extend(int(match.group(1)) for match in regex.finditer(record.uri))
            values.extend(int(match.group(1)) for match in regex.finditer(str(record.metadata)))
        return values

    def _is_memory_record(self, record: ScrumRecord) -> bool:
        try:
            record.path.relative_to(self.memory_root)
            return True
        except ValueError:
            return False


def _next_id(values: Iterable[int], prefix: str) -> str:
    return f"{prefix}-{max(values, default=0) + 1:03d}"


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, (date,)):
        return value.isoformat()
    return value


def _relative_file(uri: str, root: Path) -> str:
    file_part = uri.split("#", 1)[0]
    try:
        return str(Path(file_part).relative_to(root))
    except ValueError:
        return file_part


def _invalid_status(record: ScrumRecord, root: Path, allowed: list[str]) -> MemoryErrorItem:
    return MemoryErrorItem(
        code="INVALID_STATUS",
        severity="blocking",
        file=_relative_file(record.uri, root),
        section=record.section,
        message=f"Invalid status '{record.status}'.",
        suggestion=f"Use one of: {', '.join(allowed)}.",
    )
