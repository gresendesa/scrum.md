# Sprints Consolidator

```yaml
section: sprints
title: Sprints Consolidator
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-09
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
updated_at: 2026-06-09
sprints:
  - SPR-2026-01
  - SPR-2026-02
  - SPR-2026-03
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
updated_at: 2026-06-09
```

[@ref: Detailed sprint](sprints/SPR-2026-03.md#sprint.SPR-2026-03)

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
