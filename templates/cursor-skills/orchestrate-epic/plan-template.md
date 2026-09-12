# Orchestratable Plan Template

Copy this into `.cursor/plans/<slug>.plan.md` during Plan mode. It extends the `.cursorrules` §1.3 plan
format with per-workstream orchestration metadata (`phase`, `run_as`, `model_role`, `exit_gates`) so
`orchestrate-epic` can dispatch it without manual triage.

## Metadata contract

Every todo adds four required fields beyond the standard `id` / `content` / `status`, plus two optional fields:

| Field | Values | Meaning |
| --- | --- | --- |
| `phase` | integer | Execution batch. Human reviews at each phase boundary. |
| `run_as` | `subagent` \| `parent` | Assigns the human-gate router: `subagent` = no parent-held gate; `parent` = orchestrator stops, presents the gate to the user, and routes the approved context. A fresh Task agent always performs the work. |
| `model_role` | role name | Which **role** executes this workstream. The orchestrator resolves it to a live slug at dispatch time. Omit to let the orchestrator infer from task type. |
| `exit_gates` | list | Gates that must pass before the workstream is marked complete. |
| `heavy` | `true` (optional) | Marks a workstream whose sub-steps produce large tool output (builds, CI logs, screenshots, long test runs). Signals the orchestrator to dispatch those sub-steps to a fresh subagent that returns only a verdict, while the parent retains the user gate. |
| `model` | exact slug (optional) | Escape hatch to pin one specific model, overriding `model_role`. Use only with a stated reason; a pin goes stale the moment that version is retired. |

`run_as` answers _who routes the human gate_; `heavy` answers _who absorbs the tokens_. A
`run_as: parent, heavy: true` workstream (e.g. "rebuild the client, then open the PR") means: the parent
gets the user's PR approval, then a subagent performs the build and PR open while returning a
`BUILD OK/FAIL` verdict and the PR URL.

**Never write a model version into a plan.** Valid roles: `BUILDER`, `ARCHITECT`, `SCRIBE`, `DEEP`,
`OPERATOR`, `BULK`. Definitions, family ladders, and the resolution procedure live in
`docs/MODEL_ROUTING.md` — this file does not restate them.

## Frontmatter template

```markdown
---
name: Epic N — <Title>
overview: <one-sentence summary>
todos:
  - id: eN-ws1.1-<shortname>
    content: '[Epic N > WS 1.1] (Phase 1) <task description>'
    status: pending
    phase: 1
    run_as: subagent
    model_role: BUILDER
    exit_gates: [typecheck, test, lint]
  - id: eN-ws1.2-<shortname>
    content: '[Epic N > WS 1.2] (Phase 1) <schema-cascade task>'
    status: pending
    phase: 1
    run_as: parent # parent routes the protected-file / ADR user gate
    model_role: DEEP
    exit_gates: [typecheck, test, lint]
  - id: eN-ws3.1-build-verify
    content: '[Epic N > WS 3.1] (Phase 3) Build release artifact, verify on target, open PR'
    status: pending
    phase: 3
    run_as: parent # parent routes the PR-open user gate
    heavy: true # build log stays in the subagent that performs the work
    model_role: OPERATOR
    exit_gates: [build]
  - id: eN-ws4.1-closeout
    content: '[Epic N > WS 4.1] (Phase 4) Roadmap + memory + closeout PR'
    status: pending
    phase: 4
    run_as: parent # parent routes the PRODUCT_ROADMAP.md + PR user gates
    model_role: SCRIBE
    exit_gates: [typecheck, test, lint, format:check]
---
```

## Phases summary table (recommended)

Keep the `.cursorrules` §1.3 table, with a Role column added:

| Phase | Workstreams | Run as | Role | Exit gates |
| --- | --- | --- | --- | --- |
| 1 — Foundations | WS 1.1, 1.2 | subagent (1.2 parent-gate) | BUILDER / DEEP | typecheck + test + lint |
| 2 — UI shell | WS 2.1, 2.2 | subagent | BUILDER | typecheck + test + lint |
| 3 — Build & verify | WS 3.1 | parent-gate, heavy | OPERATOR | build + manual smoke |
| 4 — Closeout | WS 4.1 | parent-gate | SCRIBE | + format:check |

## Per-workstream body

Under each `### WS P.O — <name>` section, include what the subagent must read (it has no chat context):

```markdown
### WS 1.2 — <Workstream name>

**Run as:** parent (routes the schema-cascade user gate; a subagent performs the work)
**Role:** DEEP
**Inputs:** .cursorrules §2.4 (schema cascade), <source files>, <design doc>
**Exit:** typecheck + test + lint; <any workstream-specific gate, e.g. visual-parity check>

<Acceptance criteria, approach, code examples>
```

## Default routing cheat sheet

- Stores / hooks / queries / components / tests / wiring → `BUILDER`
- Epic planning / architecture / ADR draft / code review → `ARCHITECT`
- Schema cascade → `DEEP`, `run_as: parent` for the user gate
- Subtle timing / persistence / transaction bug → `DEEP`
- Terminal / native build / device / CI debugging → `OPERATOR`
- Docs / roadmap / PR body / memory-bank updates → `SCRIBE`
- High-volume mechanical passes → `BULK`

Anything editing a protected file (`.cursorrules` §1.5), accepting an ADR, or opening a PR is
`run_as: parent` so the orchestrator routes the user gate; the dispatch prompt must explicitly relay
any protected-file approval, and a subagent performs the work.
