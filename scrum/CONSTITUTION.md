# Constitution - scrum.md

```yaml
section: constitution
title: Constitution
project_name: scrum.md
version: 1.1
status: active
owner: Guilherme
official_language: English
created_at: 2026-06-08
updated_at: 2026-06-08
tags: [governance, constitution, memory, scrum, mdbind]
```

This document defines the operating constitution for the `scrum.md` project.

## Official Language

```yaml
section: constitution.official-language
title: Official Language
status: active
owner: Guilherme
language: English
tags: [language, governance]
```

The official language of this project is **English**.

All documentation, specification, code comments, commit messages, and scrum files must be written in English.

Exceptions:

* Conversations with the PO may occur in any language.
* Legacy content predating this constitution version may be migrated progressively.

## Purpose

```yaml
section: constitution.purpose
title: Purpose
status: active
owner: Guilherme
tags: [purpose, governance]
```

Build the `smd` CLI as a deterministic Scrum memory orchestrator for AI-assisted development, following the technical specification in `specification.md`.

[@ref: Technical specification](../specification.md#specification)

## Non-Negotiable Rules

```yaml
section: constitution.non-negotiable-rules
title: Non-Negotiable Rules
status: active
owner: Guilherme
tags: [rules, governance]
```

* The official project memory lives under `scrum/`.
* Memory files must use MDBind-style `section` metadata and stable references.
* The `smd` CLI must follow the commands, lifecycle rules, and JSON contract described in `specification.md`.
* Until the CLI exists, memory may be bootstrapped manually by the agent, preserving the same structure the CLI will later enforce.
* Protected governance files require explicit Product Owner approval before meaningful policy changes.
* No backlog item or sprint may be marked `done` without validation evidence and explicit PO acceptance when required.
* No delivery is complete without documented manual testing.
* No delivery is complete without a regression checklist executed.
* Automated tests are mandatory in the development process.
* Sprint commits only occur after explicit PO acceptance.
* Technical closure must follow one commit per sprint per repository involved.

## Strategic Priorities

```yaml
section: constitution.strategic-priorities
title: Strategic Priorities
status: active
owner: Guilherme
tags: [strategy, priorities]
```

* Deliver a small but real MVP of `smd` first.
* Favor deterministic file operations and parseable output over interactive convenience.
* Keep memory structure auditable, non-destructive, and easy for agents to query.
* Use the default template as the baseline for generated project memory.
* Validate behavior with automated tests before expanding the command surface.
* Current priority order: implementation first, documentation alongside implementation.

## Branch and Change Policy

```yaml
section: constitution.branch-and-change-policy
title: Branch and Change Policy
status: active
owner: Guilherme
branch_model: Simplified Git Flow
accepted_release_risk: medium
tags: [git, branch, change, governance]
```

Branch model:

* Simplified Git Flow.

Change approval:

* Only the owner approves changes to the constitution and memory guidelines.

Accepted release risk:

* Medium. Post-release adjustments are accepted when necessary.

## Memory Policy

```yaml
section: constitution.memory-policy
title: Memory Policy
status: active
owner: Guilherme
protected: true
tags: [memory, governance]
```

* Only the owner approves changes to the constitution and memory policy.
* Consolidators keep concise summaries only.
* Detailed backlog items belong in `scrum/backlog/`.
* Detailed sprints belong in `scrum/sprints/`.
* Decisions are recorded in `scrum/decisions.md`.
* Process learnings and incidents are recorded in `scrum/experience.md`.
* Architecture notes are recorded in `scrum/architecture.md`.
* Historical records must be marked `obsolete` or `superseded` instead of being deleted.

## Naming Convention

```yaml
section: constitution.naming-convention
title: Naming Convention
status: active
owner: Guilherme
tags: [naming, ids, governance]
```

The project must use stable identifiers for backlog items, sprints, and sprint tasks.

### Backlog Items

```yaml
section: constitution.naming-convention.backlog-items
title: Backlog Item IDs
status: active
owner: Guilherme
id_format: B-XXX
example: B-001
tags: [backlog, ids]
```

* Official backlog item ID format: `B-XXX`.
* Example: `B-001`.

### Sprints

```yaml
section: constitution.naming-convention.sprints
title: Sprint IDs
status: active
owner: Guilherme
id_format: SPR-YYYY-NN
example: SPR-2026-01
tags: [sprints, ids]
```

* Official sprint ID format: `SPR-YYYY-NN`.
* Example: `SPR-2026-01`.

### Sprint Internal Tasks

```yaml
section: constitution.naming-convention.sprint-internal-tasks
title: Sprint Internal Task IDs
status: active
owner: Guilherme
id_format: S{N}-TXX
example: S1-T03
tags: [sprints, tasks, ids]
```

* Official sprint internal task ID format: `S{N}-TXX`.
* Example: `S1-T03`.

### ID Rules

```yaml
section: constitution.naming-convention.rules
title: ID Rules
status: active
owner: Guilherme
rules:
  ids_reusable: false
  discontinued_status: obsolete
  id_required_before_status: doing
tags: [ids, rules]
```

* IDs cannot be reused.
* Discontinued IDs must be marked as `obsolete`.
* Any new item must receive an ID before entering `doing`.

## Record Standard

```yaml
section: constitution.record-standard
title: Record Standard
status: active
owner: Guilherme
tags: [records, statuses, governance]
```

All records must have a unique `section`, an explicit status, ownership metadata, creation date, and update date when changed.

### Default Statuses

```yaml
section: constitution.record-standard.statuses
title: Default Statuses
status: active
owner: Guilherme
allowed_statuses:
  - todo
  - refined
  - planned
  - doing
  - blocked
  - review
  - done
  - cancelled
  - obsolete
tags: [records, statuses]
```

Statuses must follow the state models defined by the specification.

[@ref: Backlog state model](../specification.md#specification.state-model.backlog)
[@ref: Sprint state model](../specification.md#specification.state-model.sprint)

## Definition of Ready

```yaml
section: constitution.definition-of-ready
title: Definition of Ready
status: active
owner: Guilherme
required_fields:
  - id
  - title
  - problem_or_objective
  - acceptance_criteria
  - po_priority
  - risk
  - dependencies
  - detail_file
tags: [dor, quality, planning]
```

A backlog item can enter a sprint only when it has enough scope, criteria, priority, risk, dependencies, and traceability to be executed safely.

[@ref: Specification Definition of Ready](../specification.md#specification.definition-of-ready)

## Definition of Done

```yaml
section: constitution.definition-of-done
title: Definition of Done
status: active
owner: Guilherme
required_checks:
  - acceptance_criteria_met
  - automated_tests_successful
  - documented_manual_test
  - regression_checklist_executed
  - memory_files_updated
  - rebuilt_container_validation_at_sprint_close
  - impact_analyzed
  - relevant_decisions_registered
  - relevant_experiences_registered
  - explicit_po_acceptance_with_system_running_when_required
tags: [dod, quality, validation]
```

To mark any item as `done`, the mandatory checks above must be satisfied and recorded.

Minimum mandatory evidence:

1. Documented manual test.
2. Regression checklist executed.
3. Records updated in project memory files under `scrum/`.
4. Manual validation executed on rebuilt or reinstantiated containers at sprint close.
5. Final commit only after explicit PO acceptance with the system running.
6. Automated tests in `tests/` executed successfully with no failures.

[@ref: Sprint closing gate](CONSTITUTION.md#constitution.sprint-closing-gate)
[@ref: Specification Definition of Done](../specification.md#specification.definition-of-done)

## Sprint Planning

```yaml
section: constitution.sprint-planning
title: Sprint Planning
status: active
owner: Guilherme
required: true
tags: [sprint, planning, scrum]
```

Every sprint must go through formal planning with owner participation.

During planning, the following are mandatory:

1. Ask the PO for the priority of eligible backlog items.
2. Register or update the `PO Priority` field in the backlog.
3. Select backlog items for the sprint according to PO priority.
4. Decompose selected items into technical tasks.
5. Calculate risk per task and aggregated sprint risk.
6. Define execution order.
7. Register expected blockers and mitigations.

No item enters a sprint without a defined PO Priority.

[@ref: Backlog consolidator](backlog.md#backlog)
[@ref: Sprint consolidator](sprints.md#sprints)

### PO Priority Scale

```yaml
section: constitution.sprint-planning.po-priority-scale
title: PO Priority Scale
status: active
owner: Guilherme
scale:
  1: critical
  2: high
  3: medium
  4: low
tags: [priority, planning]
```

* `1` = critical
* `2` = high
* `3` = medium
* `4` = low

### PO Priority Rule

```yaml
section: constitution.sprint-planning.po-priority-rule
title: PO Priority Rule
status: active
owner: Guilherme
tags: [priority, planning, po]
```

Only the Product Owner defines or changes `po_priority`.

### Sprint Risk Calculation

```yaml
section: constitution.sprint-planning.sprint-risk-calculation
title: Sprint Risk Calculation
status: active
owner: Guilherme
tags: [risk, planning]
```

Sprint risk is derived from task complexity, uncertainty, dependency risk, and validation burden.

Task risk scale:

* `low` = 1
* `medium` = 2
* `high` = 3

Sprint risk calculation:

* Use a simple weighted average of selected task risks.
* Final classification is `low` when less than or equal to 1.4.
* Final classification is `medium` when greater than 1.4 and less than or equal to 2.3.
* Final classification is `high` when greater than 2.3.

## Sprint Closing Gate

```yaml
section: constitution.sprint-closing-gate
title: Sprint Closing Gate
status: active
owner: Guilherme
protected: true
tags: [sprint, gate, quality]
```

A sprint can close only after:

1. Sprint exists and is in `review`.
2. Linked backlog items are no longer pending.
3. Automated tests passed.
4. Build passed when configured.
5. `smd validate` passed.
6. MDBind graph validation passed when available.
7. Definition of Done is satisfied.
8. PO explicitly accepted the delivery when required.
9. Final commit exists or commit instruction was generated.
10. Local images were rebuilt with a stable tag when containers are in scope.
11. The previous instance was torn down and a new instance was brought up for validation when containers are in scope.
12. Exactly one commit per sprint per repository involved in the scope was created after PO acceptance.

## Agent Memory Management

```yaml
section: constitution.agent-memory-management
title: Agent Memory Management
status: active
owner: Guilherme
tags: [agent, memory, governance]
```

Agents must read project memory before implementation work, update memory as part of execution, and preserve traceability between backlog, sprint, decisions, experience, architecture, and code.

### MDBind Notation Policy

```yaml
section: constitution.agent-memory-management.mdbind-notation-policy
title: MDBind Notation Policy
status: active
owner: Guilherme
protected: true
tags: [mdbind, refs, includes]
```

* Every memory section must define a unique `section` value.
* Use `@ref` for contextual references and dependencies.
* Use `@include` only for structural composition.
* References must point to existing files and sections.
* Include cycles are forbidden.
* When there is uncertainty about MDBind behavior, agents must consult `mdbind.md` before inventing graph rules.
* MDBind can be installed with `pip install mdbind`.

[@ref: MDBind reference](../mdbind.md#mdbind)

### Backlog

```yaml
section: constitution.agent-memory-management.backlog
title: Backlog Memory Rule
status: active
owner: Guilherme
tags: [backlog, memory]
```

`scrum/backlog.md` is the synthetic backlog index and must stay consistent with detail files.

It must contain only ID, title, status, PO priority, risk, and pointer to the detailed file.

### Backlog Items

```yaml
section: constitution.agent-memory-management.backlog-items
title: Backlog Item Details Rule
status: active
owner: Guilherme
tags: [backlog, memory, details]
```

Each backlog item must have a detail file in `scrum/backlog/`.

The detailed file must contain scope, acceptance criteria, dependencies, owner, and update history.

### Sprints

```yaml
section: constitution.agent-memory-management.sprints
title: Sprint Memory Rule
status: active
owner: Guilherme
tags: [sprints, memory]
```

`scrum/sprints.md` is the synthetic sprint index and must stay consistent with detail files.

It must contain only summary status, focus, risk, and pointer to the detailed file.

### Sprint Details

```yaml
section: constitution.agent-memory-management.sprint-details
title: Sprint Detail Rule
status: active
owner: Guilherme
tags: [sprints, memory, details]
```

Each sprint must have a detail file in `scrum/sprints/`.

The detailed file must contain planning, tasks, risk, execution, blockers, and closure.

### Decisions

```yaml
section: constitution.agent-memory-management.decisions
title: Decision Memory Rule
status: active
owner: Guilherme
tags: [decisions, memory]
```

Governance and architecture decisions must be recorded in `scrum/decisions.md`.

Each decision must record context, choice, impact, and date.

### Experience

```yaml
section: constitution.agent-memory-management.experience
title: Experience Memory Rule
status: active
owner: Guilherme
tags: [experience, memory]
```

Incidents, retrospectives, and process learnings must be recorded in `scrum/experience.md`.

The file must be updated at every relevant retrospective or incident and must record problem, root cause, corrective action, and prevention.

### History

```yaml
section: constitution.agent-memory-management.history
title: History Rule
status: active
owner: Guilherme
tags: [history, audit]
```

Historical content must be preserved. Superseded or discontinued records must be marked with explicit status, date, and reason.

## Validity and Changes

```yaml
section: constitution.validity-and-changes
title: Validity and Changes
status: active
owner: Guilherme
protected: true
effective_date: 2026-06-08
tags: [validity, changes, governance]
```

This constitution takes effect immediately.

Any change requires explicit owner approval.
