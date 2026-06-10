# Backlog Consolidator

```yaml
section: backlog
title: Backlog Consolidator
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-09
type: consolidator
scope: backlog
detail_directory: scrum/backlog/
tags: [backlog, scrum, memory, consolidator]
```

This file is the synthetic consolidator for backlog items.

Full details for each backlog item are stored in dedicated files under `scrum/backlog/`.

[@include: Backlog convention](backlog.md#backlog.convention)
[@ref: Constitution backlog rules](CONSTITUTION.md#constitution.agent-memory-management.backlog)
[@ref: Backlog ID convention](CONSTITUTION.md#constitution.naming-convention.backlog-items)
[@ref: PO priority rule](CONSTITUTION.md#constitution.sprint-planning.po-priority-rule)

## Objective

```yaml
section: backlog.objective
title: Backlog Objective
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
tags: [objective, backlog]
```

Maintain a concise index of backlog items, keeping only the fields required for planning, tracking, and navigation.

Detailed scope, acceptance criteria, dependencies, owner, and history must remain in the corresponding item file.

## Convention

```yaml
section: backlog.convention
title: Backlog Convention
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
item_id_format: B-XXX
detail_file_pattern: scrum/backlog/B-XXX.md
tags: [convention, backlog, ids]
```

* Backlog item ID: `B-XXX`.
* Detailed file: `scrum/backlog/B-XXX.md`.

[@ref: Backlog item details rule](CONSTITUTION.md#constitution.agent-memory-management.backlog-items)

## Synthetic Item Summary

```yaml
section: backlog.synthetic-summary
title: Synthetic Item Summary
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-09
groups:
  - done
  - pending
  - refined
  - planned
  - doing
  - review
tags: [summary, backlog]
```

This section groups backlog items by operational status.

### Done

```yaml
section: backlog.synthetic-summary.done
title: Done Backlog Items
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
item_status: done
items:
  - B-001
  - B-002
  - B-003
tags: [backlog, done]
```

#### B-001 - Close documentation gaps before implementation

```yaml
section: backlog.synthetic-summary.done.B-001
id: B-001
title: Close documentation gaps before implementation
status: done
po_priority: 1
risk: medium
linked_sprint: SPR-2026-02
detail_file: scrum/backlog/B-001.md
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-09
```

[@ref: Detailed backlog item](backlog/B-001.md#backlog.item.B-001)
[@ref: Closed sprint](sprints/SPR-2026-02.md#sprint.SPR-2026-02)

#### B-002 - Build agent-operable Jinja2 templates

```yaml
section: backlog.synthetic-summary.done.B-002
id: B-002
title: Build agent-operable Jinja2 templates
status: done
po_priority: 1
risk: medium
linked_sprint: SPR-2026-03
detail_file: scrum/backlog/B-002.md
owner: Guilherme
created_at: 2026-06-09
updated_at: 2026-06-09
```

[@ref: Detailed backlog item](backlog/B-002.md#backlog.item.B-002)
[@ref: Closed sprint](sprints/SPR-2026-03.md#sprint.SPR-2026-03)

#### B-003 - Build memory repository and MDBind foundation

```yaml
section: backlog.synthetic-summary.done.B-003
id: B-003
title: Build memory repository and MDBind foundation
status: done
po_priority: 1
risk: medium
linked_sprint: SPR-2026-03
detail_file: scrum/backlog/B-003.md
owner: Guilherme
created_at: 2026-06-09
updated_at: 2026-06-09
```

[@ref: Detailed backlog item](backlog/B-003.md#backlog.item.B-003)
[@ref: Closed sprint](sprints/SPR-2026-03.md#sprint.SPR-2026-03)

### Pending

```yaml
section: backlog.synthetic-summary.pending
title: Pending Backlog Items
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-09
item_status: todo
items:
  - B-005
tags: [backlog, pending]
```

#### B-005 - Create LLM best practices manual for smd usage

```yaml
section: backlog.synthetic-summary.pending.B-005
id: B-005
title: Create LLM best practices manual for smd usage
status: todo
po_priority: 4
risk: low
linked_sprint:
detail_file: scrum/backlog/B-005.md
owner: Guilherme
created_at: 2026-06-09
updated_at: 2026-06-09
```

[@ref: Detailed backlog item](backlog/B-005.md#backlog.item.B-005)
[@ref: AI workflow](../specification.md#specification.ai-workflow)

### Refined

```yaml
section: backlog.synthetic-summary.refined
title: Refined Backlog Items
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
item_status: refined
items: []
tags: [backlog, refined]
```

No items registered.

### Planned

```yaml
section: backlog.synthetic-summary.planned
title: Planned Backlog Items
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
item_status: planned
items:
  - B-004
tags: [backlog, planned]
```

#### B-004 - Build Python CLI shell and JSON contract

```yaml
section: backlog.synthetic-summary.planned.B-004
id: B-004
title: Build Python CLI shell and JSON contract
status: planned
po_priority: 2
risk: medium
linked_sprint: SPR-2026-04
detail_file: scrum/backlog/B-004.md
owner: Guilherme
created_at: 2026-06-09
updated_at: 2026-06-09
```

[@ref: Detailed backlog item](backlog/B-004.md#backlog.item.B-004)
[@ref: Planned sprint](sprints/SPR-2026-04.md#sprint.SPR-2026-04)

### Doing

```yaml
section: backlog.synthetic-summary.doing
title: Backlog Items In Progress
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-09
item_status: doing
items: []
tags: [backlog, doing]
```

No items registered.

### Review

```yaml
section: backlog.synthetic-summary.review
title: Backlog Items In Review
status: active
owner: Guilherme
created_at: 2026-06-09
updated_at: 2026-06-09
item_status: review
items: []
tags: [backlog, review]
```

No items registered.

## Synthetic Template for New Items

```yaml
section: backlog.template.synthetic-item
title: Synthetic Template for New Backlog Items
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-09
template_fields:
  - id
  - title
  - status
  - po_priority
  - risk
  - detail_file
allowed_statuses:
  - todo
  - refined
  - planned
  - doing
  - blocked
  - review
  - done
  - obsolete
tags: [template, backlog]
```

Use this template when adding a new backlog item to the consolidator.

[@ref: Record standard](CONSTITUTION.md#constitution.record-standard)
[@ref: Default statuses](CONSTITUTION.md#constitution.record-standard.statuses)
