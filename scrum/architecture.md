# Architecture Memory

```yaml
section: architecture
title: Architecture Memory
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-09
type: architecture_memory
scope: smd_cli_architecture
tags: [architecture, cli, memory, smd]
```

This file records architecture notes for the `smd` CLI implementation.

[@ref: Technical specification](../specification.md#specification)
[@ref: Architecture principles](../specification.md#specification.principles)
[@ref: MVP roadmap](../specification.md#specification.mvp)

## Objective

```yaml
section: architecture.objective
title: Architecture Objective
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
tags: [objective, architecture]
```

Keep implementation-relevant architecture decisions and constraints discoverable without duplicating the full technical specification.

## Initial Constraints

```yaml
section: architecture.initial-constraints
title: Initial Constraints
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-09
tags: [constraints, cli]
```

* The CLI must operate on a configurable memory root, defaulting to `scrum/`.
* All commands must support `--json`, `--root <path>`, `--quiet`, and `--verbose`.
* JSON output must use the stable envelope defined by the specification.
* File mutations must preserve IDs, sections, and non-destructive history.
* Validation must be useful before full MDBind integration exists.
* MDBind behavior must be checked against `mdbind.md` when implementation details are unclear.
* MDBind is installed with `pip install mdbind` and should be integrated directly as a Python library for core validation.
* Jinja2 is the template renderer for generated Scrum memory files.

[@ref: Command reference](../specification.md#specification.commands)
[@ref: JSON output contract](../specification.md#specification.output-contract)
[@ref: MDBind reference](../mdbind.md#mdbind)

## MVP Components

```yaml
section: architecture.mvp-components
title: MVP Components
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-09
components:
  - cli_entrypoint
  - command_router
  - config_loader
  - template_renderer
  - jinja2_templates
  - memory_repository
  - markdown_metadata_parser
  - validators
  - json_envelope
  - test_fixtures
tags: [mvp, components]
```

The MVP architecture should separate command parsing from memory operations so behavior can be tested against temporary roots.

## Open Questions

```yaml
section: architecture.open-questions
title: Open Questions
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-09
questions:
  - What test command should become the default in .smd/config.yml for this repository?
tags: [questions, architecture]
```

These questions should be answered during sprint planning or early implementation.

## Implementation Baseline

```yaml
section: architecture.implementation-baseline
title: Implementation Baseline
status: active
owner: Guilherme
created_at: 2026-06-09
updated_at: 2026-06-09
language: Python
cli_framework: Typer
template_engine: Jinja2
mdbind_integration: direct_python_library
first_backlog_items:
  - B-002
  - B-003
  - B-004
tags: [architecture, implementation, foundation]
```

The first implementation foundation should deliver agent-operable Jinja2 templates, then memory/MDBind query primitives, then the Typer CLI shell.

[@ref: Architecture decision](decisions.md#decisions.DEC-005)
[@ref: Template foundation](backlog/B-002.md#backlog.item.B-002)
