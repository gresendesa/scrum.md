# Sprints Consolidator

```yaml
section: sprints
title: Sprints Consolidator
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
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
updated_at: 2026-06-08
sprints: []
tags: [sprints, registry]
```

No concrete sprints registered yet.

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

