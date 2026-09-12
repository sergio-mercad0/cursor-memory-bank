# Plan Continuity Guide

How to use `.plan.md` files for seamless multi-session work.

---

## Overview

Plan files (`.plan.md`) serve as the **authoritative source of truth** during multi-session work. When a plan file exists with pending todos, it takes precedence over the general roadmap.

This enables:
- Seamless handoffs between agent sessions
- Clear progress tracking across context window limits
- Consistent execution of complex multi-step tasks

---

## When to Create a Plan File

Create a `.plan.md` file when:

| Trigger | Example |
|---------|---------|
| Task touches >2 files | Refactoring a module across multiple files |
| Architectural changes | Adding a new service or data flow |
| Multiple valid approaches | Need to document trade-offs before choosing |
| Multi-session work | Task too large for single context window |
| User requests planning | "Let's plan this out before coding" |

---

## Plan File Location

Plan files live in `.cursor/plans/`:

```
.cursor/
└── plans/
    ├── epic_1_auth_system.plan.md
    ├── epic_2_database_migration.plan.md
    └── fix_login_timeout.plan.md
```

Naming convention: `epic_{N}_{description}.plan.md` for Epics, or a descriptive slug for smaller work.

> **Cursor Plan mode gotcha (v3.0):** Plan mode may write the plan file **outside the repository**
> (under the user's `.cursor/plans/`) and may **strip frontmatter fields it does not recognise**. Before
> executing, copy the plan into the repo's `.cursor/plans/` and re-check that every todo still carries
> the orchestration metadata below. The `orchestrate-epic` skill does this as its first preflight step.

---

## Plan File Structure

The plan is the **job queue** that execution consumes, so every workstream carries machine-readable
metadata (full contract: `templates/cursor-skills/orchestrate-epic/plan-template.md`).

```markdown
---
name: Epic 2 — Database Migration
overview: [One-sentence summary]
todos:
  - id: e2-ws1.1-migration-script
    content: "[Epic 2 > WS 1.1] (Phase 1) Create migration script"
    status: pending
    phase: 1
    run_as: subagent
    model_role: BUILDER
    exit_gates: [typecheck, test, lint]
  - id: e2-ws1.2-schema
    content: "[Epic 2 > WS 1.2] (Phase 1) Update schema (protected — parent routes the gate)"
    status: pending
    phase: 1
    run_as: parent
    model_role: DEEP
    exit_gates: [typecheck, test, lint]
  - id: e2-ws2.1-closeout
    content: "[Epic 2 > WS 2.1] (Phase 2) Roadmap + memory + closeout PR"
    status: pending
    phase: 2
    run_as: parent
    model_role: SCRIBE
    exit_gates: [typecheck, test, lint, format:check]
---

# [Plan Title]

## Overview
[2-3 sentences explaining the goal and context]

## Architecture
[Mermaid diagram if multi-component]

## Phases (execution batching)
| Phase | Workstreams | Run as | Role | Exit gates |
|---|---|---|---|---|
| 1 — Migration | WS 1.1, 1.2 | subagent (1.2 parent-gate) | BUILDER / DEEP | typecheck + test + lint |
| 2 — Closeout | WS 2.1 | parent-gate | SCRIBE | + format:check |

## Phase 1 — [Phase Name]
**Run as:** subagent
**Inputs:** [exact files the executing agent must read — it has no chat context]
**Exit:** [gates]

### WS 1.1 — [Workstream Name]
[Acceptance criteria, approach, code examples]

### WS 1.2 — [Workstream Name]
...

## Phase 2 — [Phase Name]
...

## Rationale
[Why this approach was chosen]
```

### Todo ID convention

`e{epic}-ws{phase}.{ordinal}-{shortname}` — the ordinal **resets to 1 in every phase**, so `WS 3.2`
means "phase 3, second workstream" within this Epic. Content strings read
`[Epic X > WS P.O] (Phase P) description`. This is the one format used across `.cursorrules`, the
README, and this guide.

### Metadata fields

| Field | Meaning |
|---|---|
| `phase` | Execution batch; a human reviews at every phase boundary |
| `run_as` | `subagent` = no human gate; `parent` = the orchestrator stops, gets approval, relays it — a subagent still does the work |
| `model_role` | `BUILDER` / `ARCHITECT` / `SCRIBE` / `DEEP` / `OPERATOR` / `BULK` — never a model name |
| `exit_gates` | What must pass before the todo flips to `completed` |
| `heavy` | Optional; sub-steps produce large output (builds, logs, screenshots) — a throwaway subagent absorbs it |

See `guides/ORCHESTRATION.md` for how these are consumed.

---

## Todo Status Markers

| Marker | Meaning | When to Use |
|--------|---------|-------------|
| `pending` | Not started | Initial state |
| `in_progress` | Currently working | Active task |
| `completed` | Done | Task finished |
| `cancelled` | Skipped | With documented reason |

In markdown task lists:
- `[ ]` - Pending
- `[~]` - In Progress
- `[x]` - Completed
- `[-]` - Cancelled/Skipped

---

## Session Startup with Plan Files

At session start, the agent MUST check for active plans:

```
1. List files in .cursor/plans/
2. IF *.plan.md exists with pending todos:
   → Read the plan file
   → This plan is now AUTHORITATIVE
   → Print remaining todos
   → Propose next steps from the plan
3. ELSE:
   → Follow normal startup (read PRODUCT_ROADMAP.md)
```

### Example Startup Message

```
I found an active plan: epic_2_database_migration.plan.md

## Remaining Todos
Phase 1 — Migration
- [x] e2-ws1.1-migration-script  (BUILDER → <resolved slug>)
- [~] e2-ws1.2-schema            (DEEP, parent-gate — IN PROGRESS, 3/5 tables)
Phase 2 — Closeout
- [ ] e2-ws2.1-closeout          (SCRIBE, parent-gate)

I'll continue from WS 1.2 (Update schema). It is a parent-gated protected-file edit — do you approve
the schema change described in the plan section?
```

---

## Handoff Protocol

When a session ends with incomplete plan todos — and **always at a phase boundary** during
orchestrated execution:

### 1. Update Todo Statuses

Flip statuses **after** the exit gates pass, never before. A todo marked `completed` while the work
sits half-finished in the working tree is the most expensive lie a plan can tell the next agent.

```yaml
todos:
  - id: e2-ws1.1-migration-script
    status: completed
  - id: e2-ws1.2-schema
    status: in_progress  # 3 of 5 tables done; partial work uncommitted — do not wipe
  - id: e2-ws2.1-closeout
    status: pending
```

### 2. Log the workstream

Append one line per workstream to `.cursor/active_sprint/TASK_LOG.md`, including the model that
actually ran:

```
[WS 1.1] BUILDER → <resolved slug> — migration script + tests (12 passing)
```

### 3. Write the handoff prompt

Fill `.cursor/prompts/handoff.md` (Completed / branch + gate state / partial work / remaining phases
with `run_as` + `model_role` / pending gates / stop conditions / single next action) and print it.
The next session starts in a **fresh chat** from `.cursor/prompts/orchestrate.md` with this pasted in.

### 4. Update CURRENT_OBJECTIVE.md

```markdown
# Current Objective

**Plan:** epic_2_database_migration.plan.md
**Phase:** 1 of 2 — WS 1.2 in progress (3/5 tables)
**Branch:** feat/epic-2-database-migration (pushed: yes, last gates green)
**Next Step:** Approve schema gate, dispatch WS 1.2 as DEEP
```

---

## Plan Completion

When all todos are complete:

1. **Verify all tasks marked complete** in the plan file
2. **Update PRODUCT_ROADMAP.md** with completion status
3. **Archive or delete the plan file** (optional)
4. **Record any decisions** made during execution in DECISION_LOG.md
5. **Record any lessons** learned in LESSONS_LEARNED.md

### Archive Pattern

```bash
# Move completed plan to archive
mv .cursor/plans/epic_2_database_migration.plan.md \
   .cursor/plans/archive/epic_2_database_migration.plan.md
```

Plan completion at an Epic boundary also triggers the **Epic closeout PR** (`.cursorrules` §1.4.1).

---

## Multiple Active Plans

If multiple plan files exist:

1. **Ask user which to prioritize** if unclear
2. **Work on one plan at a time** to maintain focus — and run **one orchestrator per repository**
3. **Document dependencies** between plans if they exist; if two plans must run in parallel, each
   declares the files it owns so their agents do not collide

```
I found multiple active plans:
1. epic_2_database_migration.plan.md (3 pending todos)
2. epic_3_api_refactor.plan.md (5 pending todos)

Which should I continue? Or should I prioritize based on the roadmap?
```

---

## Plan vs Roadmap Priority

| Situation | Authority |
|-----------|-----------|
| Active plan exists | Plan file is authoritative |
| No active plan | PRODUCT_ROADMAP.md is authoritative |
| User redirects during plan | Update plan OR create new plan |
| Plan conflicts with roadmap | Ask user to reconcile |

---

## Best Practices

### DO

- ✅ Check for active plans at every session start
- ✅ Update todo statuses as you complete work
- ✅ Add session notes for context
- ✅ Reference plan ID in commit messages
- ✅ Archive completed plans for history

### DON'T

- ❌ Ignore active plans and start from roadmap
- ❌ Leave todos in ambiguous states
- ❌ Create multiple plans for the same work
- ❌ Delete plans without archiving (loses history)

---

## Integration with Git

Reference plan IDs in commit messages:

```bash
git commit -m "feat(e2-ws1.2): migrate users and orders tables

Plan: epic_2_database_migration.plan.md
Workstream: e2-ws1.2-schema
Progress: 2/5 tables complete"
```

(On PowerShell, write multi-line messages to a file and use `git commit -F <file>`; heredocs do not exist there.)

---

**Plan files are your memory across sessions. Use them.**
