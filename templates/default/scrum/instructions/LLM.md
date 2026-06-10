# LLM Instructions - smd-default

```yaml
section: template.smd-default.instructions
title: LLM Instructions
status: active
template: smd-default
tags: [template, llm, scrum, smd]
```

Use this package as the default Scrum memory foundation for an AI-operated project.

## Operating Rules

```yaml
section: template.smd-default.instructions.operating-rules
title: Operating Rules
status: active
tags: [rules, llm]
```

* Use `smd` commands for routine memory operations.
* Do not use `mdb` directly in normal workflows; `smd` encapsulates graph operations.
* Validate memory before changing Scrum state.
* Ask the Product Owner before changing priorities, closing sprints, or altering governance policy.
* Keep backlog, sprint, decisions, experience, and architecture memory aligned.

## Scrum Flow

```yaml
section: template.smd-default.instructions.scrum-flow
title: Scrum Flow
status: active
tags: [scrum, workflow]
```

1. Start by checking validation, active sprint, and pending backlog.
2. During planning, select only PO-prioritized items.
3. During execution, update memory when meaningful state changes happen.
4. During review, record test and validation evidence.
5. Close a sprint only after PO acceptance and Definition of Done evidence.

## Package Notes

```yaml
section: template.smd-default.instructions.package-notes
title: Package Notes
status: active
tags: [package, templates]
```

This package uses Jinja2 templates and must be packed with `smd pack`, which generates checksum-only `SIGNATURE.yaml` metadata.
