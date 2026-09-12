# Memory Bank System

**Purpose:** Persistent context structure for seamless AI agent handoffs without hallucinations.
**Framework:** [cursor-memory-bank](https://github.com/sergio-mercad0/cursor-memory-bank) v3.0.
The enforceable protocol lives in `.cursorrules`; this file is the map.

---

## Directory Structure

```
.cursor/
├── README.md                    # This file - system documentation
├── plans/                       # Active planning documents (the job queue)
│   └── *.plan.md                # One per Epic or sizeable task, with orchestration metadata
├── rules/                       # Cursor rule files (.mdc)
│   ├── environment.mdc          # Shell / tooling conventions — always applied
│   ├── orchestrator-ready-plans.mdc   # Plan metadata contract — applied when planning
│   └── pr-artifact-verify.mdc   # Build / attach / verify ritual — only if the project ships an artifact
├── skills/
│   └── orchestrate-epic/        # Executes an approved plan: one fresh subagent per workstream
│       ├── SKILL.md
│       └── plan-template.md
├── prompts/
│   ├── orchestrate.md           # Bootstrap prompt for an orchestrator chat
│   └── handoff.md               # Phase-boundary handoff prompt
├── memory/                      # Long-term context
│   ├── PROJECT_BRIEF.md         # ReadOnly — mission, scope, future capabilities
│   ├── TECH_STACK.md            # ReadOnly — technologies, versions, capability tier
│   ├── ARCHITECTURE.md          # ReadOnly — system design and data flow
│   ├── PRODUCT_ROADMAP.md       # Approval required — epics, phases, workstreams
│   ├── LESSONS_LEARNED.md       # Read/Write — patterns, gotchas, workflow failures
│   └── DECISION_LOG.md          # Read/Write — ADRs, including process decisions
└── active_sprint/               # Short-term state (high-frequency updates)
    ├── CURRENT_OBJECTIVE.md     # Current session goal, plan, phase, branch
    └── TASK_LOG.md              # Progress; one line per workstream with the resolved model
```

Also part of the protocol but outside `.cursor/`: `docs/MODEL_ROUTING.md` (model roles — single source of truth)
and `.github/workflows/ci.yml` (the authoritative quality gate).

---

## File Purposes

### Long-Term Context (`memory/`)

| File | Update Frequency | Approval | Purpose |
|------|-----------------|:--------:|---------|
| `PROJECT_BRIEF.md` | Rarely | Yes | Mission, scope, future capabilities |
| `TECH_STACK.md` | On dependency/tier changes | Yes | Technologies, versions, capability tier |
| `ARCHITECTURE.md` | On structural changes | Yes | System design, data flow, modules |
| `PRODUCT_ROADMAP.md` | Per workstream | Scope changes only | Epics → phases → workstreams; status ✅ 🔄 ⏳ |
| `LESSONS_LEARNED.md` | After issues | No | Patterns, gotchas, workflow failures |
| `DECISION_LOG.md` | On decisions | No | ADRs — architecture and process |

### Short-Term Context (`active_sprint/`)

| File | Update Frequency | Purpose |
|------|-----------------|---------|
| `CURRENT_OBJECTIVE.md` | Per session | Plan, phase, branch, blockers, next action |
| `TASK_LOG.md` | Per workstream | `[WS <id>] <role> → <resolved model> — <outcome>` |

### Execution (`plans/`, `rules/`, `skills/`, `prompts/`)

| File | Purpose |
|------|---------|
| `plans/*.plan.md` | Authoritative while it has pending todos. Each todo carries `phase`, `run_as`, `model_role`, `exit_gates`, optional `heavy` |
| `rules/environment.mdc` | The machine's shell quirks, loaded every turn so they stop recurring |
| `rules/orchestrator-ready-plans.mdc` | Makes Plan mode emit the metadata the orchestrator needs |
| `skills/orchestrate-epic/` | Dispatches one fresh subagent per workstream; the parent only routes human gates |
| `prompts/orchestrate.md`, `prompts/handoff.md` | Start an orchestrator; hand off at every phase boundary |

---

## Agent Startup Protocol

When a new agent session begins (`.cursorrules` §1.2):

1. **Check for active plans** in `plans/` — a plan with pending todos is authoritative; print remaining todos by phase.
2. **Verify branch state** — warn on `main`; list uncommitted changes (confirm with `git diff --stat`, line-ending noise is common).
3. **Read context** — `PRODUCT_ROADMAP.md`, `CURRENT_OBJECTIVE.md`, skim `LESSONS_LEARNED.md`.
4. **Print a numbered plan** referencing `[Epic X > WS P.O]`.
5. **Await approval** ("approved", "yes", "go").
6. **Execute** — for a multi-workstream plan, via the `orchestrate-epic` skill in a fresh chat started from `prompts/orchestrate.md`.

---

## Recording Guidelines

### When to Add a DECISION (DECISION_LOG.md)

- Choosing a technology, library, or architecture pattern
- Designing a schema
- Changing **process**: testing policy, capability tier, branch strategy, orchestration contract

### When to Add a LESSON (LESSONS_LEARNED.md)

- A bug and its root cause; an operational constraint; a performance insight
- A **workflow failure**: a closeout that was not really done, a stale artifact under test, an agent that ran out of context

### Heuristic

> **DECISION:** "We chose X because..."
> **LESSON:** "We learned that X causes Y when..."

---

## Todo Format

Plan todos are hierarchical and phase-numbered:

```
id:      e{epic}-ws{phase}.{ordinal}-{shortname}
content: [Epic X > WS P.O] (Phase P) Task description
```

The ordinal resets in each phase (`WS 1.1, 1.2 | 2.1, 2.2, 2.3 | 3.1`). Examples:
- `e0-ws1.2-tech-stack` → `[Epic 0 > WS 1.2] (Phase 1) Write TECH_STACK.md from dependency files`
- `e2-ws2.1-status-table` → `[Epic 2 > WS 2.1] (Phase 2) Create system_status table`

---

## Maintenance

### Regular Updates

| Trigger | Action |
|---------|--------|
| Workstream completed (gates green) | Flip plan todo; append `TASK_LOG.md` line with role → resolved model |
| Phase boundary reached | Write `prompts/handoff.md`; start a fresh orchestrator chat |
| Last workstream of an Epic ✅ | Push, then open the Epic closeout PR (`.cursorrules` §1.4.1) |
| Bug fixed / workflow failure | Add to `LESSONS_LEARNED.md` |
| Architecture or process choice | Add ADR to `DECISION_LOG.md` |
| Session end | Update `CURRENT_OBJECTIVE.md`; commit **and push** |

### Periodic Review

- **Every Epic closeout:** run a transcript retrospective (`guides/RETROSPECTIVE.md` in the framework) and turn recurring friction into rules.
- **Monthly:** consolidate `LESSONS_LEARNED.md`; check `docs/MODEL_ROUTING.md` prefix patterns against the live model list.
- **Quarterly:** validate `DECISION_LOG.md` decisions still hold.

---

**END OF README**
