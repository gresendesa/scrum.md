# Sprints Consolidator

```yaml
section: sprints
title: Sprints Consolidator
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-10
type: consolidator
scope: sprints
detail_directory: scrum/sprints/
tags: [sprints, scrum, memory, consolidator]
```

This file is the synthetic consolidator for project sprints.

Full details for each sprint are stored in dedicated files under `scrum/sprints/`.

[@include: Sprint convention](sprints.md#sprints.convention)
[@ref: Sprint planning policy](CONSTITUTION.md#constitution.sprint-planning)
[@ref: Sprint closing gate](CONSTITUTION.md#constitution.sprint-closing-gate)
[@ref: Sprint memory rule](CONSTITUTION.md#constitution.agent-memory-management.sprints)
[@ref: Backlog consolidator](backlog.md#backlog)

## Objective

```yaml
section: sprints.objective
title: Sprints Objective
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
tags: [objective, sprints]
```

Maintain a concise index of project sprints, keeping only status, focus, PO priority summary, risk, and pointer to the detailed sprint file.

## Convention

```yaml
section: sprints.convention
title: Sprint Convention
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
sprint_id_format: SPR-YYYY-NN
detail_file_pattern: scrum/sprints/SPR-YYYY-NN.md
tags: [convention, sprints, ids]
```

* Sprint ID: `SPR-YYYY-NN`.
* Detailed file: `scrum/sprints/SPR-YYYY-NN.md`.

[@ref: Sprint ID convention](CONSTITUTION.md#constitution.naming-convention.sprints)
[@ref: Sprint detail rule](CONSTITUTION.md#constitution.agent-memory-management.sprint-details)

## Registered Sprints

```yaml
section: sprints.registered
title: Registered Sprints
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-10
sprints:
  - SPR-2026-01
  - SPR-2026-02
  - SPR-2026-03
  - SPR-2026-04
  - SPR-2026-05
  - SPR-2026-06
  - SPR-2026-07
  - SPR-2026-08
tags: [sprints, registry]
```

### SPR-2026-01 - Document smd CLI MVP Planning

```yaml
section: sprints.SPR-2026-01
sprint_id: SPR-2026-01
title: Document smd CLI MVP Planning
status: obsolete
focus: Obsoleted because the intended scope was documentation review, not implementation planning.
po_priority_summary: B-001 priority 1 critical.
sprint_risk: medium
detail_file: scrum/sprints/SPR-2026-01.md
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
obsolete_reason: PO clarified that Sprint 01 should not frame implementation work.
```

[@ref: Detailed sprint](sprints/SPR-2026-01.md#sprint.SPR-2026-01)

### SPR-2026-02 - Close documentation gaps

```yaml
section: sprints.SPR-2026-02
sprint_id: SPR-2026-02
title: Close documentation gaps
status: done
focus: Review and update essential project documentation before implementation.
po_priority_summary: B-001 priority 1 critical.
sprint_risk: medium
detail_file: scrum/sprints/SPR-2026-02.md
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-09
```

[@ref: Detailed sprint](sprints/SPR-2026-02.md#sprint.SPR-2026-02)

### SPR-2026-03 - Agent-operable foundation

```yaml
section: sprints.SPR-2026-03
sprint_id: SPR-2026-03
title: Agent-operable foundation
status: done
focus: Build Jinja2 templates and memory primitives that let agents operate Scrum memory deterministically.
po_priority_summary: B-002 priority 1 critical; B-003 priority 1 critical; B-004 priority 2 high deferred.
sprint_risk: medium
detail_file: scrum/sprints/SPR-2026-03.md
owner: Guilherme
created_at: 2026-06-09
updated_at: 2026-06-10
```

[@ref: Detailed sprint](sprints/SPR-2026-03.md#sprint.SPR-2026-03)

### SPR-2026-04 - Python CLI shell and JSON contract

```yaml
section: sprints.SPR-2026-04
sprint_id: SPR-2026-04
title: Python CLI shell and JSON contract
status: done
focus: Expose the memory foundation through the `smd` Typer CLI shell, stable JSON envelope, and local template zip package rendering.
po_priority_summary: B-004 priority 2 high; B-005 priority 4 low deferred.
sprint_risk: medium
detail_file: scrum/sprints/SPR-2026-04.md
owner: Guilherme
created_at: 2026-06-09
updated_at: 2026-06-09
```

[@ref: Detailed sprint](sprints/SPR-2026-04.md#sprint.SPR-2026-04)

### SPR-2026-05 - Signed template package packing

```yaml
section: sprints.SPR-2026-05
sprint_id: SPR-2026-05
title: Signed template package packing
status: done
focus: Implement `smd pack` for local checksum-signed template package creation with `manifest.yaml` declaration and `SIGNATURE.yaml` metadata.
po_priority_summary: B-006 priority 2 high; B-005 priority 4 low deferred; B-007 deferred until B-006 is complete.
sprint_risk: medium
detail_file: scrum/sprints/SPR-2026-05.md
owner: Guilherme
created_at: 2026-06-09
updated_at: 2026-06-09
```

[@ref: Detailed sprint](sprints/SPR-2026-05.md#sprint.SPR-2026-05)

### SPR-2026-06 - Initialize projects from signed template packages

```yaml
section: sprints.SPR-2026-06
sprint_id: SPR-2026-06
title: Initialize projects from signed template packages
status: done
focus: Implement `smd init` so a project can be initialized from a checksum-signed template package produced by `smd pack`.
po_priority_summary: B-007 priority 2 high; B-008 priority 2 high deferred; B-005 priority 4 low deferred.
sprint_risk: medium
detail_file: scrum/sprints/SPR-2026-06.md
owner: Guilherme
created_at: 2026-06-09
updated_at: 2026-06-09
```

[@ref: Detailed sprint](sprints/SPR-2026-06.md#sprint.SPR-2026-06)

### SPR-2026-07 - Move default template governance under scrum

```yaml
section: sprints.SPR-2026-07
sprint_id: SPR-2026-07
title: Move default template governance under scrum
status: done
focus: Move the default template governance files into `templates/default/scrum/` and keep package initialization, packing, and validation behavior intact.
po_priority_summary: B-008 priority 2 high; B-005 priority 4 low deferred.
sprint_risk: low
detail_file: scrum/sprints/SPR-2026-07.md
owner: Guilherme
created_at: 2026-06-10
updated_at: 2026-06-10
```

[@ref: Detailed sprint](sprints/SPR-2026-07.md#sprint.SPR-2026-07)

### SPR-2026-08 - PyPI publication readiness and README.md

```yaml
section: sprints.SPR-2026-08
sprint_id: SPR-2026-08
title: PyPI publication readiness and README.md
status: review
focus: Create a PyPI-compatible README.md in the project root with appropriate badges, command table, and licensing information.
po_priority_summary: B-009 priority 2 high; B-005 priority 4 low deferred.
sprint_risk: low
detail_file: scrum/sprints/SPR-2026-08.md
owner: Guilherme
created_at: 2026-06-10
updated_at: 2026-06-10
```

[@ref: Detailed sprint](sprints/SPR-2026-08.md#sprint.SPR-2026-08)

### SPR-YYYY-NN Template

```yaml
section: sprints.template.SPR-YYYY-NN
title: Sprint Template
status: template
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
sprint_id: SPR-YYYY-NN
sprint_status:
focus:
po_priority_summary:
sprint_risk:
detail_file: scrum/sprints/SPR-YYYY-NN.md
tags: [sprints, template]
```

Use this template when registering a new sprint.

[@ref: Risk calculation](CONSTITUTION.md#constitution.sprint-planning.sprint-risk-calculation)
[@ref: PO priority scale](CONSTITUTION.md#constitution.sprint-planning.po-priority-scale)
