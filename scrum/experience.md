# Experience - Retrospective and Process Memory

```yaml
section: experience
title: Experience Memory
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
type: process_memory
scope: retrospectives_and_incidents
tags: [experience, retrospective, incident, process, memory]
```

This file records problems observed in the development process, their causes, and how recurrence should be prevented.

[@include: Experience record format](experience.md#experience.record-format)
[@ref: Experience memory rule](CONSTITUTION.md#constitution.agent-memory-management.experience)
[@ref: Decision memory](decisions.md#decisions)
[@ref: Definition of Done](CONSTITUTION.md#constitution.definition-of-done)

## Objective

```yaml
section: experience.objective
title: Experience Objective
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
tags: [objective, experience]
```

Register process learning in a form that can be reused by agents during planning, execution, retrospectives, and incident analysis.

## Record Format

```yaml
section: experience.record-format
title: Experience Record Format
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
record_id_format: EXP-XXX
fields:
  - id
  - date
  - context
  - problem
  - impact
  - root_cause
  - corrective_action
  - preventive_action
  - status
  - owner
allowed_statuses:
  - open
  - mitigated
  - resolved
  - obsolete
tags: [format, experience, records]
```

Each experience record must use the documented fields and a unique `section`.

[@ref: History rule](CONSTITUTION.md#constitution.agent-memory-management.history)

## Records

```yaml
section: experience.records
title: Experience Records
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
records: []
tags: [experience, records]
```

### EXP-001 - Keep sprint execution inside approved scope

```yaml
section: experience.EXP-001
id: EXP-001
date: 2026-06-09
context: During SPR-2026-02 closure, the PO corrected the agent after it interpreted approval as permission to start CLI source code implementation.
problem: The agent almost crossed from documentation-only sprint execution into implementation work.
impact: Without the correction, the sprint scope and constitutional implementation gate could have been violated.
root_cause: The approval phrase was interpreted too broadly instead of being reconciled against the active sprint scope.
corrective_action: Keep SPR-2026-02 documentation-only, update B-001 and sprint closure records, and defer all CLI source code implementation to a future approved implementation sprint.
preventive_action: Before implementation work, always inspect the active sprint scope and backlog item out-of-scope fields, even when the PO gives a short approval.
status: resolved
owner: Guilherme
created_at: 2026-06-09
updated_at: 2026-06-09
tags: [experience, scope, sprint, prevention]
```

This process learning applies to future implementation approvals.
