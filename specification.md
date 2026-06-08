# Scrum.md: Especificação Técnica da CLI `smd`

```yaml
section: specification
title: Technical Specification for smd CLI
status: active
version: 2.0.0
language: pt-BR
scope: machine_first_scrum_orchestration
tags: [smd, scrum, cli, ai, mdbind, memory, governance]
```

## 1. Visão Geral

```yaml
section: specification.overview
title: Overview
status: active
tags: [overview, purpose]
```

A CLI `smd` é uma ferramenta de orquestração Scrum projetada para ambientes de desenvolvimento conduzidos por agentes de IA.

Seu objetivo é transformar a memória operacional do projeto em um sistema determinístico, auditável e validável, reduzindo a dependência de documentação solta, decisões implícitas e manutenção manual de contexto.

A ferramenta assume que:

1. O humano atua como **Product Owner**.
2. A IA atua como **Scrum Master** e **Developer**.
3. A CLI atua como **trilho operacional**, impedindo corrupção estrutural, inconsistência de IDs, perda de rastreabilidade e fechamento indevido de ciclos.
4. O diretório `scrum/` é a memória oficial do projeto.
5. Todos os arquivos Markdown de memória seguem a notação `mdbind`.

[@ref: Constitution](scrum/CONSTITUTION.md#constitution)
[@ref: MDBind notation policy](scrum/CONSTITUTION.md#constitution.agent-memory-management.mdbind-notation-policy)

## 2. Problema a Resolver

```yaml
section: specification.problem
title: Problem Statement
status: active
tags: [problem, ai, context, memory]
```

Ferramentas de IA integradas ao desenvolvimento sofrem degradação operacional conforme o projeto cresce.

Os principais problemas são:

### 2.1 Amnésia e Fragmentação de Contexto

```yaml
section: specification.problem.context-amnesia
title: Context Amnesia
status: active
tags: [problem, context, memory]
```

A IA perde requisitos, decisões, estado de execução, critérios de aceite e histórico de mudanças quando a sessão fica longa, quando o contexto é truncado ou quando múltiplos arquivos precisam ser reconciliados manualmente.

### 2.2 Alucinação Estrutural

```yaml
section: specification.problem.structural-hallucination
title: Structural Hallucination
status: active
tags: [problem, hallucination, ids]
```

Ao editar Markdown livremente, a IA pode:

* inventar IDs;
* duplicar identificadores;
* quebrar links;
* criar referências para seções inexistentes;
* alterar convenções;
* apagar histórico relevante;
* marcar itens como concluídos sem cumprir critérios de qualidade.

### 2.3 Fadiga do Desenvolvedor

```yaml
section: specification.problem.developer-fatigue
title: Developer Fatigue
status: active
tags: [problem, cognitive-load]
```

Sem um trilho determinístico, o humano precisa supervisionar constantemente a IA, corrigindo documentação, reconstruindo contexto e validando tarefas que deveriam ser controladas pela própria metodologia.

### 2.4 Falta de Rigor Metodológico

```yaml
section: specification.problem.methodological-drift
title: Methodological Drift
status: active
tags: [problem, scrum, quality]
```

A IA tende a pular etapas quando não existe enforcement sistêmico.

Exemplos:

* iniciar implementação sem planejamento;
* mover item para `doing` sem prioridade do PO;
* fechar sprint sem validação;
* esquecer testes;
* não atualizar memória;
* não registrar decisões;
* não documentar incidentes;
* misturar planejamento, execução e retrospectiva em texto solto.

## 3. Finalidade da Solução

```yaml
section: specification.solution
title: Solution
status: active
tags: [solution, machine-first, scrum]
```

A CLI `smd` implementa um fluxo **Machine-First Scrum**, no qual a IA é a operadora principal do sistema metodológico.

O humano não precisa memorizar comandos nem manipular arquivos de processo no dia a dia. Ele conversa em linguagem natural com a IA, define prioridades, responde dúvidas e aprova entregas.

A IA, por sua vez, usa a CLI para:

* criar artefatos com IDs corretos;
* consultar estado do projeto;
* montar contexto;
* validar integridade;
* executar gates;
* registrar decisões;
* controlar sprints;
* impedir fechamento indevido de ciclos.

## 4. Princípios Arquiteturais

```yaml
section: specification.principles
title: Architectural Principles
status: active
tags: [principles, architecture]
```

### 4.1 Machine-First, Human-Approved

```yaml
section: specification.principles.machine-first
title: Machine-First, Human-Approved
status: active
tags: [principle, machine-first]
```

A IA executa a rotina operacional. O humano aprova decisões de produto e mudanças protegidas.

O humano deve ser poupado de:

* calcular IDs;
* abrir arquivos de memória;
* validar links;
* consolidar backlog;
* lembrar formato de sprint;
* verificar manualmente grafo documental.

Mas o humano nunca deve ser removido de:

* priorização;
* aceitação final;
* mudanças constitucionais;
* alterações de política de memória;
* decisões de produto com impacto relevante.

### 4.2 Determinismo sobre Texto Livre

```yaml
section: specification.principles.determinism
title: Determinism Over Free Text
status: active
tags: [principle, determinism]
```

Sempre que houver risco de erro estrutural, a IA deve usar comando da CLI em vez de improvisar texto.

Exemplos:

* criar backlog item;
* criar sprint;
* descobrir sprint ativa;
* listar pendências;
* validar grafo;
* fechar sprint;
* calcular próximo ID;
* verificar Definition of Done.

### 4.3 Memória como Grafo

```yaml
section: specification.principles.memory-graph
title: Memory as Graph
status: active
tags: [principle, mdbind, graph]
```

A memória do projeto é formada por seções Markdown endereçáveis, cada uma com metadados YAML e identificador `section` único.

Relações entre seções devem usar:

* `@ref` para referência contextual ou dependência;
* `@include` para composição estrutural.

[@ref: MDBind notation policy](scrum/CONSTITUTION.md#constitution.agent-memory-management.mdbind-notation-policy)

### 4.4 Histórico Não Destrutivo

```yaml
section: specification.principles.non-destructive-history
title: Non-Destructive History
status: active
tags: [principle, history, audit]
```

A ferramenta não deve apagar histórico metodológico.

Conteúdo antigo deve ser:

* preservado;
* marcado como `obsolete` quando necessário;
* acompanhado de motivo e data;
* mantido rastreável para auditoria futura.

[@ref: History rule](scrum/CONSTITUTION.md#constitution.agent-memory-management.history)

### 4.5 Gates Inegociáveis

```yaml
section: specification.principles.gates
title: Non-Negotiable Gates
status: active
tags: [principle, gates, quality]
```

Nenhuma sprint ou backlog item pode ser marcado como `done` sem passar pelos gates definidos.

O fechamento de sprint deve exigir:

* testes automatizados;
* validação da memória;
* validação de grafo MDBind;
* verificação de Definition of Done;
* aprovação explícita do PO;
* registro da entrega;
* commit final após aprovação.

[@ref: Definition of Done](scrum/CONSTITUTION.md#constitution.definition-of-done)
[@ref: Sprint closing gate](scrum/CONSTITUTION.md#constitution.sprint-closing-gate)

## 5. Papéis

```yaml
section: specification.roles
title: Roles
status: active
tags: [roles, scrum, ai]
```

### 5.1 Product Owner Humano

```yaml
section: specification.roles.product-owner
title: Human Product Owner
status: active
tags: [role, po, human]
```

Responsabilidades:

* definir propósito do projeto;
* aprovar Constituição;
* priorizar backlog;
* responder dúvidas de negócio;
* aceitar ou rejeitar entregas;
* aprovar mudanças protegidas;
* decidir trade-offs relevantes.

O PO não deve ser responsável por manter a memória operacional manualmente.

### 5.2 IA Scrum Master

```yaml
section: specification.roles.ai-scrum-master
title: AI Scrum Master
status: active
tags: [role, scrum-master, ai]
```

Responsabilidades:

* conduzir planning;
* proteger o processo;
* exigir prioridade do PO;
* decompor backlog em sprint;
* registrar riscos;
* cobrar Definition of Done;
* conduzir fechamento;
* registrar retrospectivas;
* impedir avanço indevido de estado.

### 5.3 IA Developer

```yaml
section: specification.roles.ai-developer
title: AI Developer
status: active
tags: [role, developer, ai]
```

Responsabilidades:

* implementar tarefas da sprint;
* executar testes;
* atualizar memória técnica;
* registrar decisões e incidentes;
* manter rastreabilidade entre código, backlog e sprint;
* validar alterações antes de pedir aprovação.

### 5.4 CLI `smd`

```yaml
section: specification.roles.smd-cli
title: smd CLI Role
status: active
tags: [role, cli, guardrail]
```

Responsabilidades:

* controlar IDs;
* criar artefatos;
* validar estrutura;
* consultar estado;
* compor contexto;
* bloquear transições inválidas;
* executar gates;
* produzir saída determinística para consumo por IA.

## 6. Diretório Oficial de Memória

```yaml
section: specification.memory-layout
title: Memory Directory Layout
status: active
root: scrum/
tags: [memory, layout, files]
```

A estrutura padrão é:

```text
scrum/
  CONSTITUTION.md
  backlog.md
  sprints.md
  decisions.md
  experience.md
  architecture.md
  backlog/
    B-001.md
    B-002.md
  sprints/
    SPR-2026-01.md
    SPR-2026-02.md
```

### 6.1 Arquivos Consolidadores

```yaml
section: specification.memory-layout.consolidators
title: Consolidator Files
status: active
tags: [memory, consolidators]
```

Arquivos consolidadores são índices sintéticos.

Eles devem conter apenas informações suficientes para navegação, filtragem e planejamento.

São consolidadores oficiais:

* `scrum/backlog.md`
* `scrum/sprints.md`

Eles não devem conter detalhes extensos que pertencem aos arquivos individuais.

[@ref: Backlog consolidator](scrum/backlog.md#backlog)
[@ref: Sprints consolidator](scrum/sprints.md#sprints)

### 6.2 Arquivos Detalhados

```yaml
section: specification.memory-layout.detail-files
title: Detail Files
status: active
tags: [memory, details]
```

Cada backlog item e cada sprint deve ter arquivo próprio.

Exemplos:

```text
scrum/backlog/B-004.md
scrum/sprints/SPR-2026-03.md
```

Arquivos detalhados contêm:

* escopo;
* contexto;
* critérios de aceite;
* dependências;
* tarefas;
* riscos;
* histórico;
* links MDBind;
* evidências de validação.

## 7. Modelo de Estados

```yaml
section: specification.state-model
title: State Model
status: active
tags: [states, lifecycle]
```

### 7.1 Estados de Backlog Item

```yaml
section: specification.state-model.backlog
title: Backlog Item States
status: active
allowed_statuses:
  - todo
  - refined
  - planned
  - doing
  - blocked
  - done
  - obsolete
tags: [states, backlog]
```

Estados:

* `todo`: item registrado, ainda não refinado.
* `refined`: item possui descrição, critérios e dependências suficientes.
* `planned`: item foi selecionado para uma sprint.
* `doing`: item está em execução.
* `blocked`: item não pode avançar sem desbloqueio.
* `done`: item entregue e aceito conforme DoD.
* `obsolete`: item preservado no histórico, mas não será executado.

### 7.2 Transições de Backlog Item

```yaml
section: specification.state-model.backlog-transitions
title: Backlog Item Transitions
status: active
tags: [states, backlog, transitions]
```

Transições permitidas:

```text
todo -> refined
refined -> planned
planned -> doing
doing -> blocked
blocked -> doing
doing -> done
todo/refined/planned/doing/blocked -> obsolete
```

Transições proibidas:

```text
todo -> doing
todo -> done
refined -> done
planned -> done
obsolete -> doing
done -> doing
done -> obsolete sem justificativa explícita
```

### 7.3 Estados de Sprint

```yaml
section: specification.state-model.sprint
title: Sprint States
status: active
allowed_statuses:
  - planned
  - doing
  - blocked
  - review
  - done
  - cancelled
tags: [states, sprint]
```

Estados:

* `planned`: sprint criada e planejada, ainda não iniciada.
* `doing`: sprint em execução.
* `blocked`: sprint não pode avançar.
* `review`: implementação concluída, aguardando validação e aceite.
* `done`: sprint aceita e fechada.
* `cancelled`: sprint cancelada sem apagar histórico.

### 7.4 Transições de Sprint

```yaml
section: specification.state-model.sprint-transitions
title: Sprint Transitions
status: active
tags: [states, sprint, transitions]
```

Transições permitidas:

```text
planned -> doing
doing -> blocked
blocked -> doing
doing -> review
review -> done
planned/doing/blocked/review -> cancelled
```

Transições proibidas:

```text
planned -> done
doing -> done
blocked -> done
cancelled -> doing
done -> doing
```

## 8. Regras de Identificação

```yaml
section: specification.identifiers
title: Identifier Rules
status: active
tags: [ids, naming]
```

### 8.1 Backlog Items

```yaml
section: specification.identifiers.backlog
title: Backlog Identifier Rules
status: active
format: B-XXX
example: B-001
tags: [ids, backlog]
```

Formato oficial:

```text
B-XXX
```

Exemplos:

```text
B-001
B-002
B-029
```

A CLI deve calcular o próximo ID com base no maior ID existente em:

* `scrum/backlog.md`;
* arquivos em `scrum/backlog/`.

IDs nunca podem ser reutilizados.

### 8.2 Sprints

```yaml
section: specification.identifiers.sprints
title: Sprint Identifier Rules
status: active
format: SPR-YYYY-NN
example: SPR-2026-01
tags: [ids, sprints]
```

Formato oficial:

```text
SPR-YYYY-NN
```

Exemplos:

```text
SPR-2026-01
SPR-2026-02
SPR-2027-01
```

O contador `NN` reinicia por ano.

### 8.3 Tarefas Internas de Sprint

```yaml
section: specification.identifiers.sprint-tasks
title: Sprint Task Identifier Rules
status: active
format: S{N}-TXX
example: S1-T03
tags: [ids, sprint-tasks]
```

Formato oficial:

```text
S{N}-TXX
```

Exemplo:

```text
S1-T01
S1-T02
S2-T01
```

## 9. Comandos

```yaml
section: specification.commands
title: Command Reference
status: active
tags: [cli, commands]
```

Todos os comandos devem aceitar:

```bash
--json
--root <path>
--quiet
--verbose
```

Regras gerais:

* `--json` deve produzir saída estável e parseável por IA.
* comandos com falha devem retornar exit code diferente de zero.
* validações devem retornar lista de erros com código, severidade, arquivo e sugestão.
* comandos que alteram arquivos devem ser idempotentes quando possível.
* comandos destrutivos devem exigir flag explícita.

## 10. Comandos de Inicialização

```yaml
section: specification.commands.init
title: Init Commands
status: active
tags: [cli, init]
```

### 10.1 `smd init`

```yaml
section: specification.commands.init.smd-init
title: smd init
status: active
command: smd init
tags: [cli, init]
```

Inicializa a memória Scrum do projeto.

Exemplo:

```bash
smd init
```

Entradas coletadas:

* nome do projeto;
* owner;
* propósito;
* template;
* idioma;
* diretório raiz de memória;
* entrypoint da IA;
* stack de teste;
* comando de build;
* comando de teste;
* política de commit;
* nível de rigidez dos gates.

Saídas criadas:

```text
scrum/CONSTITUTION.md
scrum/backlog.md
scrum/sprints.md
scrum/decisions.md
scrum/experience.md
scrum/architecture.md
scrum/backlog/B-001.md
```

Também deve injetar no entrypoint da IA uma instrução apontando para a Constituição e para o backlog inicial.

### 10.2 `smd init --template`

```yaml
section: specification.commands.init.template
title: smd init template
status: active
command: smd init --template
tags: [cli, init, templates]
```

Templates oficiais:

* `lean`;
* `standard`;
* `verbose`;
* `enterprise`;
* `custom`.

Exemplo:

```bash
smd init --template standard
```

## 11. Comandos de Backlog

```yaml
section: specification.commands.backlog
title: Backlog Commands
status: active
tags: [cli, backlog]
```

### 11.1 `smd backlog create`

```yaml
section: specification.commands.backlog.create
title: smd backlog create
status: active
command: smd backlog create
tags: [cli, backlog, create]
```

Cria novo item de backlog com ID sequencial.

Exemplo:

```bash
smd backlog create --title "Implement authentication flow" --json
```

A CLI deve:

1. descobrir próximo ID;
2. criar arquivo `scrum/backlog/B-XXX.md`;
3. inserir registro sintético em `scrum/backlog.md`;
4. criar metadados MDBind;
5. retornar caminho e ID.

Saída JSON esperada:

```json
{
  "ok": true,
  "type": "backlog_item",
  "id": "B-029",
  "status": "todo",
  "detail_file": "scrum/backlog/B-029.md",
  "consolidator": "scrum/backlog.md",
  "created": true
}
```

### 11.2 `smd backlog list`

```yaml
section: specification.commands.backlog.list
title: smd backlog list
status: active
command: smd backlog list
tags: [cli, backlog, query]
```

Lista itens de backlog.

Exemplos:

```bash
smd backlog list
smd backlog list --status todo
smd backlog list --pending
smd backlog list --priority 1 --json
```

Campos mínimos:

* ID;
* título;
* status;
* PO priority;
* risco;
* sprint vinculada;
* arquivo detalhado.

### 11.3 `smd backlog get`

```yaml
section: specification.commands.backlog.get
title: smd backlog get
status: active
command: smd backlog get
tags: [cli, backlog, query]
```

Recupera item específico.

Exemplo:

```bash
smd backlog get B-004 --json
```

### 11.4 `smd backlog update`

```yaml
section: specification.commands.backlog.update
title: smd backlog update
status: active
command: smd backlog update
tags: [cli, backlog, update]
```

Atualiza metadados controlados de um item.

Exemplo:

```bash
smd backlog update B-004 --status refined --priority 1 --json
```

A CLI deve recusar:

* status inválido;
* prioridade fora da escala;
* transição proibida;
* alteração de ID;
* marcação como `done` sem gate.

### 11.5 `smd backlog obsolete`

```yaml
section: specification.commands.backlog.obsolete
title: smd backlog obsolete
status: active
command: smd backlog obsolete
tags: [cli, backlog, obsolete]
```

Marca item como obsoleto sem apagar histórico.

Exemplo:

```bash
smd backlog obsolete B-010 --reason "Substituído por B-014" --json
```

## 12. Comandos de Sprint

```yaml
section: specification.commands.sprint
title: Sprint Commands
status: active
tags: [cli, sprint]
```

### 12.1 `smd sprint create`

```yaml
section: specification.commands.sprint.create
title: smd sprint create
status: active
command: smd sprint create
tags: [cli, sprint, create]
```

Cria nova sprint.

Exemplo:

```bash
smd sprint create --title "Authentication foundation" --json
```

A CLI deve:

1. calcular próximo ID `SPR-YYYY-NN`;
2. criar arquivo detalhado em `scrum/sprints/`;
3. registrar a sprint em `scrum/sprints.md`;
4. iniciar status como `planned`;
5. impedir criação se já houver sprint ativa, salvo com `--allow-parallel`.

Saída JSON esperada:

```json
{
  "ok": true,
  "type": "sprint",
  "id": "SPR-2026-05",
  "status": "planned",
  "detail_file": "scrum/sprints/SPR-2026-05.md",
  "created": true
}
```

### 12.2 `smd sprint active`

```yaml
section: specification.commands.sprint.active
title: smd sprint active
status: active
command: smd sprint active
tags: [cli, sprint, query]
```

Retorna a sprint ativa.

Estados considerados ativos:

* `planned`;
* `doing`;
* `blocked`;
* `review`.

Exemplo:

```bash
smd sprint active --json
```

Se não houver sprint ativa:

```json
{
  "ok": true,
  "active": null
}
```

### 12.3 `smd sprint plan`

```yaml
section: specification.commands.sprint.plan
title: smd sprint plan
status: active
command: smd sprint plan
tags: [cli, sprint, planning]
```

Associa backlog items a uma sprint planejada.

Exemplo:

```bash
smd sprint plan SPR-2026-05 --items B-003,B-004,B-008 --json
```

A CLI deve validar:

* itens existem;
* itens não estão `done` ou `obsolete`;
* todos possuem PO priority;
* todos possuem critérios de aceite mínimos;
* não há sprint conflitante;
* dependências estão mapeadas.

### 12.4 `smd sprint start`

```yaml
section: specification.commands.sprint.start
title: smd sprint start
status: active
command: smd sprint start
tags: [cli, sprint, start]
```

Inicia sprint planejada.

Exemplo:

```bash
smd sprint start SPR-2026-05 --json
```

A CLI deve recusar início se:

* sprint não tiver backlog items;
* houver item sem prioridade PO;
* houver item sem critérios de aceite;
* risco não tiver sido calculado;
* houver dependência bloqueante sem mitigação.

### 12.5 `smd sprint review`

```yaml
section: specification.commands.sprint.review
title: smd sprint review
status: active
command: smd sprint review
tags: [cli, sprint, review]
```

Move sprint para revisão.

Exemplo:

```bash
smd sprint review SPR-2026-05 --json
```

A CLI deve exigir:

* todas as tarefas técnicas concluídas ou justificadas;
* evidências de teste registradas;
* memória atualizada;
* validação estrutural sem erro crítico.

### 12.6 `smd sprint close`

```yaml
section: specification.commands.sprint.close
title: smd sprint close
status: active
command: smd sprint close
tags: [cli, sprint, close]
```

Fecha sprint após gate.

Exemplo:

```bash
smd sprint close SPR-2026-05 --po-accepted --json
```

Esse comando deve chamar ou equivaler a:

```bash
smd gate close-sprint SPR-2026-05
```

A CLI deve recusar fechamento sem aprovação explícita do PO.

## 13. Comandos de Gate

```yaml
section: specification.commands.gate
title: Gate Commands
status: active
tags: [cli, gate, quality]
```

### 13.1 `smd gate close-sprint`

```yaml
section: specification.commands.gate.close-sprint
title: smd gate close-sprint
status: active
command: smd gate close-sprint
tags: [cli, gate, sprint]
```

Executa gate completo de fechamento de sprint.

Exemplo:

```bash
smd gate close-sprint SPR-2026-05 --json
```

Checklist obrigatório:

1. sprint existe;
2. sprint está em `review`;
3. backlog items vinculados não estão pendentes;
4. testes automatizados passaram;
5. build passou;
6. `smd validate` passou;
7. `mdb validate --root scrum/` passou;
8. Definition of Done cumprida;
9. PO aceitou explicitamente;
10. commit final foi realizado ou instrução de commit foi gerada.

Saída JSON esperada:

```json
{
  "ok": false,
  "gate": "close-sprint",
  "sprint_id": "SPR-2026-05",
  "status": "failed",
  "errors": [
    {
      "code": "PO_ACCEPTANCE_MISSING",
      "severity": "blocking",
      "message": "Sprint cannot be closed without explicit Product Owner acceptance."
    }
  ]
}
```

### 13.2 `smd gate item-done`

```yaml
section: specification.commands.gate.item-done
title: smd gate item-done
status: active
command: smd gate item-done
tags: [cli, gate, backlog]
```

Valida se um backlog item pode ser marcado como `done`.

Exemplo:

```bash
smd gate item-done B-004 --json
```

Critérios mínimos:

* critérios de aceite cumpridos;
* evidência de teste registrada;
* vínculos com sprint atual;
* memória atualizada;
* dependências resolvidas;
* impacto documentado.

## 14. Comandos de Validação

```yaml
section: specification.commands.validate
title: Validation Commands
status: active
tags: [cli, validation]
```

### 14.1 `smd validate`

```yaml
section: specification.commands.validate.smd-validate
title: smd validate
status: active
command: smd validate
tags: [cli, validation]
```

Executa validação completa da memória Scrum.

Exemplo:

```bash
smd validate --json
```

Deve verificar:

* existência dos arquivos obrigatórios;
* conformidade dos nomes;
* unicidade de IDs;
* unicidade de `section`;
* consistência entre consolidadores e arquivos detalhados;
* status válidos;
* transições válidas;
* links `@ref` e `@include`;
* ausência de ciclos de include;
* presença de campos obrigatórios;
* ausência de sprint ativa duplicada;
* backlog items planejados vinculados a sprint existente;
* backlog items `done` com evidências de DoD;
* decisões e experiências com formato válido.

### 14.2 Severidades

```yaml
section: specification.commands.validate.severity
title: Validation Severity
status: active
tags: [validation, severity]
```

Severidades:

* `info`: observação não bloqueante.
* `warning`: problema não bloqueante, mas recomendado corrigir.
* `error`: problema que deve ser corrigido.
* `blocking`: impede mudança de estado ou fechamento de gate.

### 14.3 Códigos de Erro

```yaml
section: specification.commands.validate.error-codes
title: Validation Error Codes
status: active
tags: [validation, errors]
```

Códigos mínimos:

```text
MISSING_REQUIRED_FILE
DUPLICATE_ID
DUPLICATE_SECTION
BROKEN_REF
BROKEN_INCLUDE
INCLUDE_CYCLE
INVALID_STATUS
INVALID_TRANSITION
MISSING_PO_PRIORITY
MISSING_ACCEPTANCE_CRITERIA
MISSING_DOD_EVIDENCE
ACTIVE_SPRINT_CONFLICT
CONSOLIDATOR_OUT_OF_SYNC
DETAIL_FILE_MISSING
DETAIL_FILE_ORPHAN
PROTECTED_FILE_CHANGED_WITHOUT_APPROVAL
PO_ACCEPTANCE_MISSING
TEST_COMMAND_FAILED
BUILD_COMMAND_FAILED
```

## 15. Comandos de Contexto

```yaml
section: specification.commands.context
title: Context Commands
status: active
tags: [cli, context, mdbind]
```

### 15.1 `smd context sprint`

```yaml
section: specification.commands.context.sprint
title: smd context sprint
status: active
command: smd context sprint
tags: [cli, context, sprint]
```

Monta contexto relevante da sprint para a IA.

Exemplo:

```bash
smd context sprint SPR-2026-05 --depth 2 --token-limit 4000 --json
```

Deve usar `mdb context-compose` internamente quando disponível.

### 15.2 `smd context item`

```yaml
section: specification.commands.context.item
title: smd context item
status: active
command: smd context item
tags: [cli, context, backlog]
```

Monta contexto de um backlog item.

Exemplo:

```bash
smd context item B-004 --json
```

Deve incluir:

* item detalhado;
* sprint vinculada;
* decisões relacionadas;
* experiências relacionadas;
* arquitetura relacionada;
* dependências;
* backlinks relevantes.

### 15.3 `smd impact`

```yaml
section: specification.commands.context.impact
title: smd impact
status: active
command: smd impact
tags: [cli, context, impact]
```

Retorna impacto de uma seção ou item.

Exemplo:

```bash
smd impact backlog/B-004.md#backlog.item.B-004 --json
```

Deve delegar a `mdb impact` quando possível.

## 16. Comandos de Decisões e Experiências

```yaml
section: specification.commands.records
title: Decision and Experience Commands
status: active
tags: [cli, decisions, experience]
```

### 16.1 `smd decision create`

```yaml
section: specification.commands.records.decision-create
title: smd decision create
status: active
command: smd decision create
tags: [cli, decision]
```

Cria registro de decisão.

Exemplo:

```bash
smd decision create --title "Use PostgreSQL for persistence" --json
```

Formato de ID:

```text
DEC-XXX
```

### 16.2 `smd experience create`

```yaml
section: specification.commands.records.experience-create
title: smd experience create
status: active
command: smd experience create
tags: [cli, experience]
```

Cria registro de experiência, incidente ou aprendizado.

Exemplo:

```bash
smd experience create --title "Regression caused by missing validation" --json
```

Formato de ID:

```text
EXP-XXX
```

## 17. Proteção de Arquivos

```yaml
section: specification.protected-files
title: Protected Files
status: active
tags: [governance, protection]
```

Arquivos protegidos:

* `scrum/CONSTITUTION.md`;
* política de memória;
* regras de Definition of Done;
* convenções de ID;
* comandos de gate;
* entrypoint da IA.

Mudanças nesses arquivos exigem aprovação explícita do PO.

A CLI deve detectar alterações em arquivos protegidos por diff estrutural e bloquear fechamento de sprint se não houver aprovação registrada.

## 18. Contrato de Saída JSON

```yaml
section: specification.output-contract
title: JSON Output Contract
status: active
tags: [cli, json, contract]
```

Todo comando com `--json` deve retornar o mesmo envelope:

```json
{
  "ok": true,
  "command": "smd backlog create",
  "timestamp": "2026-06-08T22:00:00-03:00",
  "root": ".",
  "data": {},
  "warnings": [],
  "errors": []
}
```

Em caso de erro:

```json
{
  "ok": false,
  "command": "smd validate",
  "timestamp": "2026-06-08T22:00:00-03:00",
  "root": ".",
  "data": null,
  "warnings": [],
  "errors": [
    {
      "code": "BROKEN_REF",
      "severity": "blocking",
      "file": "scrum/backlog.md",
      "section": "backlog.synthetic-summary.pending",
      "message": "Reference target does not exist.",
      "target": "backlog/B-999.md#backlog.item.B-999",
      "suggestion": "Create the missing detail file or remove the reference."
    }
  ]
}
```

## 19. Workflow Operacional da IA

```yaml
section: specification.ai-workflow
title: AI Operational Workflow
status: active
tags: [workflow, ai]
```

### 19.1 Ao Iniciar Sessão

```yaml
section: specification.ai-workflow.session-start
title: Session Start Workflow
status: active
tags: [workflow, startup]
```

A IA deve:

1. ler o entrypoint;
2. localizar `scrum/CONSTITUTION.md`;
3. executar `smd validate --json`;
4. executar `smd sprint active --json`;
5. executar `smd backlog list --pending --json`;
6. verificar se `B-001` está pendente;
7. se não houver sprint ativa, conduzir planning com o PO.

### 19.2 Ao Receber Nova Demanda do PO

```yaml
section: specification.ai-workflow.new-request
title: New PO Request Workflow
status: active
tags: [workflow, backlog]
```

A IA deve:

1. classificar se a demanda é bug, feature, melhoria, dívida técnica ou decisão;
2. verificar se já existe item relacionado;
3. criar backlog item se necessário;
4. pedir prioridade ao PO se o item for candidato a sprint;
5. registrar contexto e critérios de aceite;
6. validar memória;
7. apresentar resumo ao PO.

### 19.3 Ao Implementar

```yaml
section: specification.ai-workflow.implementation
title: Implementation Workflow
status: active
tags: [workflow, implementation]
```

A IA deve:

1. obter sprint ativa;
2. obter contexto da sprint;
3. selecionar tarefa em ordem planejada;
4. implementar;
5. executar testes relevantes;
6. atualizar arquivos de memória;
7. registrar decisão se houver escolha arquitetural;
8. registrar experiência se houver incidente;
9. executar `smd validate`.

### 19.4 Ao Fechar Sprint

```yaml
section: specification.ai-workflow.sprint-closing
title: Sprint Closing Workflow
status: active
tags: [workflow, sprint, closing]
```

A IA deve:

1. mover sprint para `review`;
2. executar `smd gate close-sprint`;
3. corrigir erros bloqueantes;
4. demonstrar entrega ao PO;
5. solicitar aceite explícito;
6. registrar aceite;
7. executar fechamento;
8. fazer commit final;
9. atualizar retrospectiva.

## 20. Definition of Ready

```yaml
section: specification.definition-of-ready
title: Definition of Ready
status: active
tags: [scrum, quality, ready]
```

Um backlog item só pode entrar em sprint se possuir:

* ID válido;
* título claro;
* problema ou objetivo;
* critérios de aceite;
* prioridade PO;
* status permitido;
* risco inicial;
* dependências conhecidas;
* arquivo detalhado;
* referência no consolidador;
* links MDBind relevantes.

## 21. Definition of Done

```yaml
section: specification.definition-of-done
title: Definition of Done
status: active
tags: [scrum, quality, done]
```

Um item só pode ser `done` se:

* critérios de aceite foram cumpridos;
* testes automatizados passaram;
* teste manual foi documentado quando aplicável;
* regressão foi verificada;
* memória foi atualizada;
* impacto foi analisado;
* decisão relevante foi registrada;
* experiência relevante foi registrada;
* PO aceitou quando o item for parte de entrega visível.

[@ref: Constitution Definition of Done](scrum/CONSTITUTION.md#constitution.definition-of-done)

## 22. Integração com MDBind

```yaml
section: specification.mdbind-integration
title: MDBind Integration
status: active
tags: [mdbind, integration]
```

A CLI `smd` deve usar `mdbind` como motor de grafo documental.

Mapeamento sugerido:

```text
smd validate              -> mdb validate --root scrum/
smd context item          -> mdb context-compose <item-uri> --root scrum/
smd impact                -> mdb impact <uri> --root scrum/
smd graph tree            -> mdb tree <uri> --root scrum/
smd graph backlinks       -> mdb backlinks <uri> --root scrum/
smd graph query           -> mdb query <expression> --root scrum/
```

A integração deve respeitar:

* `section` único;
* URI válida;
* `@ref` para dependência;
* `@include` para composição;
* falha em links quebrados;
* falha em ciclos de include.

[@ref: MDBind notation policy](scrum/CONSTITUTION.md#constitution.agent-memory-management.mdbind-notation-policy)

## 23. Templates

```yaml
section: specification.templates
title: Templates
status: active
tags: [templates, jinja]
```

A CLI deve usar templates renderizados por Jinja2.

Templates mínimos:

```text
templates/
  constitution.md.j2
  backlog.md.j2
  sprints.md.j2
  decisions.md.j2
  experience.md.j2
  architecture.md.j2
  backlog_item.md.j2
  sprint.md.j2
  decision.md.j2
  experience.md.j2
```

Variáveis globais:

```yaml
project_name:
owner:
created_at:
language:
memory_root:
template_profile:
test_command:
build_command:
default_branch:
timezone:
```

## 24. Configuração do Projeto

```yaml
section: specification.config
title: Project Configuration
status: active
tags: [config]
```

Arquivo recomendado:

```text
.smd/config.yml
```

Exemplo:

```yaml
project_name: "{{ project_name }}"
owner: "{{ owner }}"
language: pt-BR
timezone: America/Sao_Paulo
memory_root: scrum
entrypoint: AGENTS.md

commands:
  test: "pytest"
  build: "docker compose build"
  lint: "ruff check ."

gates:
  require_po_acceptance: true
  require_tests: true
  require_build: true
  require_mdbind_validate: true
  require_memory_update: true

git:
  commit_policy: one_commit_per_sprint
  default_branch: main

templates:
  profile: standard
```

## 25. Git e Auditoria

```yaml
section: specification.git-audit
title: Git and Audit
status: active
tags: [git, audit]
```

A CLI deve apoiar auditoria por Git.

Regras:

* uma sprint deve gerar pelo menos um commit final;
* commits devem referenciar ID da sprint;
* commits relevantes devem referenciar backlog items;
* fechamento de sprint deve registrar hash do commit;
* mudança em arquivo protegido deve registrar aprovação do PO.

Formato sugerido de commit:

```text
SPR-2026-05: deliver authentication foundation

Backlog:
- B-004
- B-005

PO-Accepted: yes
```

## 26. Segurança Metodológica

```yaml
section: specification.methodological-safety
title: Methodological Safety
status: active
tags: [safety, governance]
```

A CLI deve proteger contra:

* alteração não aprovada da Constituição;
* fechamento sem aceite;
* falso `done`;
* IDs duplicados;
* sprint paralela acidental;
* item sem prioridade;
* referência quebrada;
* consolidador divergente;
* histórico apagado;
* include cíclico;
* alteração manual incompatível.

## 27. MVP Recomendado

```yaml
section: specification.mvp
title: Recommended MVP
status: active
tags: [mvp, roadmap]
```

O MVP deve implementar primeiro:

1. `smd init`;
2. templates base;
3. `smd backlog create`;
4. `smd sprint create`;
5. `smd sprint active`;
6. `smd backlog list --pending`;
7. `smd validate`;
8. integração básica com `mdb validate`;
9. `smd gate close-sprint`;
10. saída `--json`.

Fora do MVP inicial:

* UI interativa;
* dashboards;
* multi-repo avançado;
* integração direta com GitHub;
* métricas complexas;
* plugin de IDE.

## 28. Roadmap

```yaml
section: specification.roadmap
title: Roadmap
status: active
tags: [roadmap]
```

### 28.1 Fase 1 — Núcleo Determinístico

```yaml
section: specification.roadmap.phase-1
title: Phase 1 - Deterministic Core
status: active
tags: [roadmap, phase-1]
```

Entregas:

* init;
* templates;
* ID sequencial;
* criação de backlog;
* criação de sprint;
* validação estrutural;
* JSON estável.

### 28.2 Fase 2 — Gates Scrum

```yaml
section: specification.roadmap.phase-2
title: Phase 2 - Scrum Gates
status: active
tags: [roadmap, phase-2]
```

Entregas:

* Definition of Ready;
* Definition of Done;
* sprint planning;
* sprint review;
* close-sprint gate;
* teste/build configurável.

### 28.3 Fase 3 — Grafo e Contexto

```yaml
section: specification.roadmap.phase-3
title: Phase 3 - Graph and Context
status: active
tags: [roadmap, phase-3]
```

Entregas:

* context compose;
* impact analysis;
* backlinks;
* graph query;
* token budget;
* integração profunda com MDBind.

### 28.4 Fase 4 — Auditoria e Multi-Repositório

```yaml
section: specification.roadmap.phase-4
title: Phase 4 - Audit and Multi-Repository
status: active
tags: [roadmap, phase-4]
```

Entregas:

* suporte multi-repo;
* hash de commit por sprint;
* diff estrutural;
* changelog automático;
* integração com GitHub Issues;
* exportação de relatório.

## 29. Critérios de Aceite da Própria CLI

```yaml
section: specification.acceptance-criteria
title: CLI Acceptance Criteria
status: active
tags: [acceptance, cli]
```

A CLI `smd` será considerada funcional quando:

1. inicializar um projeto do zero;
2. criar memória Scrum válida;
3. criar backlog items sem duplicar IDs;
4. criar sprints sem conflito;
5. impedir transições inválidas;
6. validar MDBind;
7. detectar links quebrados;
8. detectar inconsistência entre consolidador e detalhe;
9. impedir fechamento sem DoD;
10. emitir JSON determinístico;
11. operar de modo útil para uma IA no terminal;
12. permitir que o humano atue apenas como PO no chat.

## 30. Síntese

```yaml
section: specification.summary
title: Summary
status: active
tags: [summary]
```

A `smd` não é apenas uma CLI de Scrum.

Ela é uma camada de controle metodológico para agentes de IA.

Sua função central é impedir que a IA trate a memória do projeto como texto descartável. O projeto passa a ter uma estrutura operacional auditável, navegável, validável e resistente à degradação de contexto.

O resultado esperado é um fluxo em que:

* o humano decide;
* a IA opera;
* a CLI valida;
* o grafo preserva memória;
* os gates protegem a qualidade;
* o histórico permanece auditável.

[@ref: Constitution](scrum/CONSTITUTION.md#constitution)
[@ref: Backlog consolidator](scrum/backlog.md#backlog)
[@ref: Sprints consolidator](scrum/sprints.md#sprints)
[@ref: Decision memory](scrum/decisions.md#decisions)
[@ref: Experience memory](scrum/experience.md#experience)
