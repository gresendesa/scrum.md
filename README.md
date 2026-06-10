# Scrum.md (smd CLI)

[![PyPI version](https://img.shields.io/pypi/v/scrum-md.svg)](https://pypi.org/project/scrum-md/)
[![Python Support](https://img.shields.io/pypi/pyversions/scrum-md.svg)](https://pypi.org/project/scrum-md/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![MDBind](https://img.shields.io/badge/MDBind-compliant-success.svg)](https://github.com/gresendesa/mdbind)

**Scrum.md** is a machine-first, human-approved Scrum memory orchestration engine and CLI (`smd`) designed to streamline AI-assisted software development. By modeling project memory as a deterministic document graph, it prevents AI context degradation and ensures strict methodological rigor.

---

## 💡 The Problem It Resolves

AI software developers and agents (like Claude, Gemini, or GPTs) are highly capable but face significant challenges as codebases scale:

1. **Context Amnesia & Fragmentation:** In long sessions, LLMs lose track of business requirements, previous design decisions, task states, acceptance criteria, and historical pivots when context windows get saturated or when they must reconcile disjointed markdown files.
2. **Structural Hallucination:** When editing free-form markdown logs, AI agents frequently duplicate IDs, invent task states, break link anchors, delete audit histories, or close tasks without meeting quality requirements.
3. **Methodological Drift & Quality Decay:** AI agents tend to bypass standard development stages (implementing features without a plan, skipping test execution, ignoring the Definition of Done, or forgetting to log decisions) unless restricted by system-level constraints.
4. **Developer/PO Fatigue:** Without automated governance, human developers must continuously babysit AI agents—manually verifying documentation integrity, fixing broken links, and policing workflow compliance.

**Scrum.md** resolves these issues by acting as an **operational track (trilho operacional)** for AI agents. Instead of allowing agents to write arbitrary documentation, it forces them to interact with Scrum memory via the deterministic `smd` CLI.

---

## 🛠️ Installation

You can install `scrum-md` via pip:

```bash
pip install scrum-md
```

To install it locally for development or customization:

```bash
git clone https://github.com/gresendesa/scrum.md.git
cd scrum.md
pip install -e .
```

---

## 🚀 How to Use

`scrum-md` operates on a `scrum/` directory containing the project's living memory (backlog, sprints, decisions, architecture, and experiences) structured using the `mdbind` format.

### 1. Initialize a Project
Initialize a clean Scrum memory directory and configuration:
```bash
smd init --template-package templates/default.zip --project-name "MyAwesomeProject" --owner "PO Name"
```

### 2. Validate Project Memory
Verify the entire Scrum memory graph, asserting that all IDs are unique, references/includes are intact, statuses are valid, and there are no cycles:
```bash
smd validate
```

### 3. Query the Active Sprint
Retrieve details about the current sprint:
```bash
smd sprint active
```

### 4. Query the Backlog
List pending or refine backlog items:
```bash
smd backlog list --pending
```

---

## 📋 Commands Reference Table

The `smd` CLI provides the following command suite:

| Command | Subcommand | Key Options | Description |
| :--- | :--- | :--- | :--- |
| **`init`** | — | `--template-package`, `--target`, `--force` | Initializes project Scrum memory (`scrum/`) from a signed template package. |
| **`validate`** | — | `--root`, `--json` | Validates the entire Scrum memory graph for structural integrity, unique IDs, and valid state transitions. |
| **`pack`** | — | `--output`, `--force` | Bundles templates from a directory into a secure, checksum-signed zip package. |
| **`backlog`** | `list` | `--status`, `--pending` | Lists and filters backlog items (e.g., pending tasks, refined items) using structured queries. |
| **`sprint`** | `active` | `--root` | Returns details of the currently active sprint. |
| **`template`** | `render` | `--target`, `--project-name`, `--owner` | Renders boilerplate template files into a target directory. |

*Global Options:* You can pass `--json` to any command to receive a structured, stable JSON envelope optimized for programmatic consumption by LLM agents.

---

## 🧠 Philosophy: Machine-First, Human-Approved

Scrum.md is built around a unique collaboration model:

* **Machine-First (AI Routine):** The AI agent (acting as Scrum Master and Developer) executes the operational routine. It queries the backlog, plans tasks, updates status, generates detail logs, registers design choices, writes code, runs tests, and validates the memory graph. It is banned from mutating state without validation.
* **Human-Approved (PO Control):** The human Product Owner remains the supreme governor. The AI cannot close sprints, change core constitutional policies, or modify high-priority features without explicit, logged PO consent.
* **Determinism over Free Text:** By utilizing `mdbind` annotations, documents become a verifiable graph database. Links and structural integrity are checked on every step.

---

## 📄 License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
