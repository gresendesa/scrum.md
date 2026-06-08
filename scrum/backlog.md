# Backlog Consolidator

```yaml
section: backlog
title: Backlog Consolidator
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
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
updated_at: 2026-06-08
groups:
  - done
  - pending
  - refined
  - planned
  - doing
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
items: []
tags: [backlog, done]
```

No items registered.

### Pending

```yaml
section: backlog.synthetic-summary.pending
title: Pending Backlog Items
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
item_status: todo
items: []
tags: [backlog, pending]
```

No items registered.

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
  - B-001
tags: [backlog, planned]
```

#### B-001 - Close documentation gaps before implementation

```yaml
section: backlog.synthetic-summary.planned.B-001
id: B-001
title: Close documentation gaps before implementation
status: planned
po_priority: 1
risk: medium
linked_sprint:
detail_file: scrum/backlog/B-001.md
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
```

[@ref: Detailed backlog item](backlog/B-001.md#backlog.item.B-001)

### Doing

```yaml
section: backlog.synthetic-summary.doing
title: Backlog Items In Progress
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
item_status: doing
items: []
tags: [backlog, doing]
```

No items registered.

## Synthetic Template for New Items

```yaml
section: backlog.template.synthetic-item
title: Synthetic Template for New Backlog Items
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
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
  - done
  - obsolete
tags: [template, backlog]
```

Use this template when adding a new backlog item to the consolidator.

[@ref: Record standard](CONSTITUTION.md#constitution.record-standard)
[@ref: Default statuses](CONSTITUTION.md#constitution.record-standard.statuses)
