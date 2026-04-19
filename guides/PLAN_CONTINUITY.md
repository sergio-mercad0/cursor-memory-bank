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
    ├── e1-ws1.2-auth-system.plan.md
    ├── e2-ws2.1-database-migration.plan.md
    └── memory_bank_framework_sync.plan.md
```

Naming convention: `{epic}-{workstream}-{description}.plan.md` or descriptive name.

---

## Plan File Structure

```markdown
---
name: [Descriptive Plan Name]
overview: [One-sentence summary]
todos:
  - id: task-1
    content: "[Epic X > WS Y] First task"
    status: pending
  - id: task-2
    content: "[Epic X > WS Y] Second task"
    status: pending
---

# [Plan Title]

## Overview
[2-3 sentences explaining the goal and context]

## Architecture
[Mermaid diagram if multi-component]

## Phase 1: [Phase Name]
[Detailed breakdown]

## Phase 2: [Phase Name]
[Detailed breakdown]

## Rationale
[Why this approach was chosen]
```

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
I found an active plan: e2-ws2.1-database-migration.plan.md

## Remaining Todos
- [x] task-1: Create migration script
- [~] task-2: Update schema (IN PROGRESS)
- [ ] task-3: Run migration tests
- [ ] task-4: Update documentation

I'll continue from task-2 (Update schema). Should I proceed?
```

---

## Handoff Protocol

When a session ends with incomplete plan todos:

### 1. Update Todo Statuses

Mark completed tasks and note progress on in-progress tasks:

```yaml
todos:
  - id: task-1
    content: "Create migration script"
    status: completed
  - id: task-2
    content: "Update schema"
    status: in_progress  # Note: 3 of 5 tables done
  - id: task-3
    content: "Run migration tests"
    status: pending
```

### 2. Add Session Notes

Append to the plan file:

```markdown
## Session Notes

### Session 2024-01-15 14:30
- Completed task-1
- Started task-2, finished tables: users, orders, products
- Remaining for task-2: inventory, shipments
- No blockers
```

### 3. Update CURRENT_OBJECTIVE.md

```markdown
# Current Objective

**Plan:** e2-ws2.1-database-migration.plan.md
**Current Task:** task-2 (Update schema)
**Progress:** 3/5 tables migrated
**Next Step:** Continue with inventory table
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
mv .cursor/plans/e2-ws2.1-database-migration.plan.md \
   .cursor/plans/archive/e2-ws2.1-database-migration.plan.md
```

---

## Multiple Active Plans

If multiple plan files exist:

1. **Ask user which to prioritize** if unclear
2. **Work on one plan at a time** to maintain focus
3. **Document dependencies** between plans if they exist

```
I found multiple active plans:
1. e2-ws2.1-database-migration.plan.md (3 pending todos)
2. e3-ws3.2-api-refactor.plan.md (5 pending todos)

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
git commit -m "feat(e2-ws2.1): migrate users and orders tables

Plan: e2-ws2.1-database-migration.plan.md
Task: task-2 (Update schema)
Progress: 2/5 tables complete"
```

---

**Plan files are your memory across sessions. Use them.**
