<div align="center">

# Scrum.md

**Machine-first Scrum memory orchestration.**

Transform your Scrum memory into a deterministic, auditable document graph —  
without loose text, implicit decisions, or manual link checks.

[![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-23%20passing-brightgreen?logo=pytest&logoColor=white)](#development)
[![Version](https://img.shields.io/badge/version-0.1.0-informational)](#installation)
[![License](https://img.shields.io/badge/License-Apache_2.0-lightgreen.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI](https://img.shields.io/pypi/v/scrum-md?logo=pypi&logoColor=white&color=orange)](https://pypi.org/project/scrum-md/)

</div>

---

```bash
# Install
pip install scrum-md

# Validate your scrum folder
smd validate --root scrum/

# Get the active sprint
smd sprint active
```

---

## What is Scrum.md?

Scrum.md is a **Scrum memory orchestration engine** designed for development environments driven by AI agents. It acts as an operational track (*trilho operacional*) to prevent AI context degradation and guarantee methodological rigor.

By combining the **MdBind** notation with strict transition gates, it ensures:

- Stable document IDs (`B-XXX` for backlog, `SPR-YYYY-NN` for sprints)
- Automated verification of Definition of Done (DoD)
- Traceability between backlog items, active sprints, decisions, and code
- Structured context-composition for LLMs with bounded token consumption

---

## Why Scrum.md?

| Issue | Free-text Markdown | Vector DBs / Embeddings | **Scrum.md (smd)** |
|---|:---:|:---:|:---:|
| **ID Uniqueness** | Hallucinates IDs | N/A | ✓ Guaranteed by CLI |
| **Integrity Audit** | Manual check | ✗ Impossible | ✓ CLI Validate |
| **History Retention** | Deletes/modifies | ✗ Impossible | ✓ Logged events |
| **Quality Gates** | Ignored | ✗ N/A | ✓ Enforced gates |

Every status, every backlog item, and every sprint is fully structured and verifiable. AI routines stay auditable, and the Product Owner remains in control.

---

## Quick start

```bash
# 1. Clone and install
git clone <repo-url> && cd scrum.md
python3 -m venv .venv && source .venv/bin/activate
pip install -e .

# 2. Package your templates
smd pack templates/default --output default.zip

# 3. Initialize Scrum memory in a target project
smd init --template-package default.zip --project-name "MyProject" --owner "PO Name"
```

---

## See it in action

```bash
# Check if your Scrum memory has duplicate IDs or broken links
$ smd validate --root scrum/

# Retrieve the active sprint details
$ smd sprint active --root scrum/

# Query backlog items that are pending (todo/refined)
$ smd backlog list --pending --root scrum/

# Query backlog items filtered by status
$ smd backlog list --status todo --root scrum/ --json
```

---

## Syntax & Directory Structure

Scrum.md expects a standard memory layout under a designated `scrum/` folder:

```
scrum/
├── CONSTITUTION.md   # Project rules, DoD, and transition gates
├── backlog.md        # Synthetic consolidator for backlog items
├── sprints.md        # Synthetic consolidator for sprints
├── decisions.md      # Architecture Decision Records (ADRs)
├── experience.md     # Incident logs and lessons learned
├── backlog/          # Detailed backlog files (e.g. B-001.md)
└── sprints/          # Detailed sprint logs (e.g. SPR-2026-01.md)
```

### Declaring a Backlog Item

Detailed backlog files (e.g., `scrum/backlog/B-009.md`) use `mdbind` metadata to define their status, priorities, and relations:

````markdown
# B-009 - Create project README.md for PyPI publication

```yaml
section: backlog.item.B-009
id: B-009
title: Create project README.md for PyPI publication
status: doing
type: documentation
po_priority: 2
risk: low
linked_sprint: SPR-2026-08
owner: Guilherme
created_at: 2026-06-10
updated_at: 2026-06-10
tags: [backlog, documentation, readme, pypi, apache-2.0]
```

## Objective
...
````

---

## Commands

### Quick reference

| Command | Subcommand | Option/Argument | Description |
|---|---|---|---|
| `smd init` | — | `--template-package`, `--target` | Initializes Scrum memory directory from a signed template package |
| `smd validate` | — | `--root`, `--json` | Performs a full check of memory structure, IDs, and transitions |
| `smd pack` | — | `<dir>`, `--output`, `--force` | Creates a checksum-signed template package zip with signature validation |
| `smd backlog` | `list` | `--status`, `--pending` | Lists and filters backlog items from the consolidator |
| `smd sprint` | `active` | `--root` | Retrieves the active sprint in the repository |
| `smd template` | `render` | `--target`, `--project-name` | Renders template package files without creating full config |

All commands accept `--json` for programmatic consumption by LLM agents. All outputs are deterministic.

---

## Philosophy

Five principles behind Scrum.md memory management:

1. **Machine-First, Human-Approved** — AI operates the routine, but humans approve gates and prioritize the backlog.
2. **Determinism over Free Text** — CLI boundaries prevent structural hallucinations and ID collisions.
3. **No Destructive History** — Operational events, decisions, and status histories must be appended, not erased.
4. **Memory as a Graph** — All nodes (backlog, sprints, ADRs) are linked explicitly using MDBind directives.
5. **Quality is Non-Negotiable** — Quality gates and Definition of Ready/Done are system-enforced.

---

## Development

```bash
# Install in editable mode
pip install -e .

# Run the full test suite
python -m unittest discover -v
```

> 23 tests, 0 failures.

---

## License

[Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0)
