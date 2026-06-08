# Decisions - Memory and Governance

```yaml
section: decisions
title: Decision Memory
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
type: governance_memory
scope: memory_architecture_and_process_governance
tags: [decisions, governance, memory]
```

This file records the decision history about the memory architecture and governance process of this workspace.

[@include: Decision record format](decisions.md#decisions.record-format)
[@ref: Decision memory rule](CONSTITUTION.md#constitution.agent-memory-management.decisions)
[@ref: Memory policy](CONSTITUTION.md#constitution.memory-policy)
[@ref: MDBind notation policy](CONSTITUTION.md#constitution.agent-memory-management.mdbind-notation-policy)

## Objective

```yaml
section: decisions.objective
title: Decisions Objective
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
tags: [objective, decisions]
```

Maintain an auditable history of governance and memory architecture decisions so future agents can understand the context, choice, and impact of each decision.

## Record Format

```yaml
section: decisions.record-format
title: Decision Record Format
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
record_id_format: DEC-XXX
fields:
  - id
  - date
  - status
  - context
  - decision
  - impact
  - affected_files
  - future_review
allowed_statuses:
  - proposed
  - approved
  - superseded
  - obsolete
tags: [format, decisions, records]
```

Each decision record must use the documented fields and a unique `section`.

[@ref: History rule](CONSTITUTION.md#constitution.agent-memory-management.history)

## History

```yaml
section: decisions.history
title: Decision History
status: active
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
decisions:
  - DEC-001
  - DEC-002
  - DEC-003
  - DEC-004
tags: [decisions, history]
```

### DEC-001 - Bootstrap manual da memoria Scrum

```yaml
section: decisions.DEC-001
id: DEC-001
title: Bootstrap manual da memoria Scrum
date: 2026-06-08
status: approved
context: A CLI smd ainda nao existe, mas AGENTS.md exige que a memoria do projeto seja criada antes da implementacao.
decision: Criar manualmente a estrutura scrum/ seguindo specification.md e templates/default/.
impact: A proxima etapa de implementacao pode operar com backlog, constituicao, decisoes, experiencia e arquitetura oficiais.
affected_files:
  - scrum/CONSTITUTION.md
  - scrum/backlog.md
  - scrum/backlog/B-001.md
  - scrum/sprints.md
  - scrum/decisions.md
  - scrum/experience.md
  - scrum/architecture.md
future_review: Quando smd init existir, comparar a memoria manual com a saida gerada pela CLI.
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
```

The memory bootstrap is intentional and temporary. Future structural changes should be performed through `smd` once the relevant commands exist.

### DEC-002 - Adopt proven governance rules from reference project

```yaml
section: decisions.DEC-002
id: DEC-002
title: Adopt proven governance rules from reference project
date: 2026-06-08
status: approved
context: The Product Owner provided a constitution from another project that is operating well and asked to add missing rules to this project's constitution.
decision: Add the missing language, branch policy, delivery, sprint closure, risk calculation, memory management, and validity rules to scrum/CONSTITUTION.md.
impact: The scrum.md project now has stricter delivery gates, clearer governance, official English documentation policy, and more precise sprint planning rules.
affected_files:
  - scrum/CONSTITUTION.md
future_review: Review after the first sprint to confirm the governance rules are practical for the smd CLI workflow.
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
```

This change was explicitly requested by the Product Owner in conversation.

### DEC-003 - Register MDBind reference as operational documentation

```yaml
section: decisions.DEC-003
id: DEC-003
title: Register MDBind reference as operational documentation
date: 2026-06-08
status: approved
context: The Product Owner added mdbind.md and instructed agents to reference it when there are doubts about how MDBind works.
decision: Add MDBind metadata to mdbind.md and reference it from the constitution, architecture memory, and the MVP backlog item.
impact: Future implementation and validation work has an explicit local source for MDBind commands, invariants, and installation instructions.
affected_files:
  - mdbind.md
  - scrum/CONSTITUTION.md
  - scrum/architecture.md
  - scrum/backlog/B-001.md
  - scrum/decisions.md
future_review: When smd integrates MDBind, verify that command mappings still match mdbind.md.
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
```

MDBind installation for this project is `pip install mdbind`.

### DEC-004 - Require PO-approved specification before implementation

```yaml
section: decisions.DEC-004
id: DEC-004
title: Require PO-approved specification before implementation
date: 2026-06-08
status: approved
context: The PO clarified that implementation must not start before the scope is specified and approved.
decision: Add a constitutional rule requiring PO-approved specification before implementation and keep scrum records concise.
impact: B-001 now targets documentation gaps only, and SPR-2026-01 is obsolete.
affected_files:
  - scrum/CONSTITUTION.md
  - scrum/backlog.md
  - scrum/backlog/B-001.md
  - scrum/sprints.md
  - scrum/sprints/SPR-2026-01.md
future_review: Apply this rule before creating the first implementation sprint.
owner: Guilherme
created_at: 2026-06-08
updated_at: 2026-06-08
```
