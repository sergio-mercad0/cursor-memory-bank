# File Boundaries Cheatsheet

Quick reference for Memory Bank file access permissions, tool permissions, and update triggers.

---

## Access Control Matrix

| File | Read | Write | Approval Required | When to Modify |
|------|:----:|:-----:|:-----------------:|----------------|
| **PROJECT_BRIEF.md** | ✅ Always | ⚠️ Rarely | **YES** | Only if project scope changes |
| **TECH_STACK.md** | ✅ Always | ⚠️ Rarely | **YES** | Only when adding new technology |
| **ARCHITECTURE.md** | ✅ Always | ⚠️ Rarely | **YES** | Only for significant design changes |
| **PRODUCT_ROADMAP.md** | ✅ Always | ⚠️ Scope changes | **YES** | When adding/removing epics or changing scope |
| **.cursor/README.md** | ✅ Always | ⚠️ Rarely | **YES** | Only when protocol changes |
| **LESSONS_LEARNED.md** | ✅ Always | ✅ Often | No | After debugging sessions |
| **DECISION_LOG.md** | ✅ Always | ✅ Often | No | After architectural choices |
| **CURRENT_OBJECTIVE.md** | ✅ Always | ✅ Every session | No | At session start and when pivoting |
| **TASK_LOG.md** | ✅ Always | ✅ Frequently | No | Throughout session |

> **Note (v2.0):** PRODUCT_ROADMAP.md now requires approval for scope changes (adding/removing epics, changing priorities). Updating task statuses (`[ ]` → `[x]`) does NOT require approval.

---

## Tool Permissions Matrix

| Tool/Action | Allowed | Requires Approval | Notes |
|-------------|:-------:|:-----------------:|-------|
| **Read any file** | ✅ | No | Always allowed |
| **Write to `.cursor/active_sprint/`** | ✅ | No | Session state files |
| **Write to LESSONS_LEARNED.md** | ✅ | No | After debugging |
| **Write to DECISION_LOG.md** | ✅ | No | After decisions |
| **Update task statuses in ROADMAP** | ✅ | No | `[ ]` → `[x]` transitions |
| **Write to protected files** | ⚠️ | **YES** | See protected files list |
| **Add/remove epics from ROADMAP** | ⚠️ | **YES** | Scope changes |
| **Git commit to feature branch** | ✅ | No | Normal workflow |
| **Git commit to main/master** | ❌ | **YES** | Protected branches |
| **Create new files in project** | ✅ | No | Normal workflow |
| **Delete files** | ⚠️ | **YES** | Destructive action |
| **Run shell commands** | ✅ | No | Normal workflow |
| **Run destructive commands** | ❌ | **YES** | rm -rf, drop table, etc. |

---

## Protected Files (Require Approval)

These files define the project's foundation. Changes require explicit user approval.

### 1. PROJECT_BRIEF.md
**Contains:** Mission, scope, future capabilities, user personas

**Modify When:**
- Project scope changes significantly
- New major capability is planned
- User personas are refined

**Approval Process:**
1. Explain what change is needed and why
2. Show the proposed change
3. Wait for user approval
4. Add ADR to DECISION_LOG.md

---

### 2. TECH_STACK.md
**Contains:** Technologies, versions, dependencies

**Modify When:**
- New technology is added
- Major version upgrades
- Dependencies change significantly

**Approval Process:**
1. Propose the technology change
2. Explain rationale and alternatives
3. Wait for user approval
4. Update file and add ADR

---

### 3. ARCHITECTURE.md
**Contains:** System design, data flow, module structure

**Modify When:**
- New service/component is added
- Data flow changes
- Design patterns evolve

**Approval Process:**
1. Describe architectural change
2. Show updated diagrams
3. Wait for user approval
4. Update file and add ADR

---

### 4. PRODUCT_ROADMAP.md
**Contains:** Epics, workstreams, tasks, priorities

**Modify When (Approval Required):**
- Adding or removing epics
- Changing workstream scope
- Reprioritizing work
- Scope changes to project direction

**Modify When (No Approval Needed):**
- Marking tasks complete `[x]`
- Adding detailed subtasks within approved workstreams
- Updating status markers

**Approval Process:**
1. Explain the scope change
2. Show impact on timeline/priorities
3. Wait for user approval
4. Add ADR to DECISION_LOG.md

---

### 5. .cursor/README.md
**Contains:** Memory Bank protocol itself

**Modify When:**
- Protocol rules change
- New file types are added
- Workflow is refined

**Approval Process:**
1. Propose protocol change
2. Explain impact on workflow
3. Wait for user approval
4. Update both README.md AND .cursorrules

---

## Read/Write Files (No Approval Needed)

These files are updated frequently as part of normal development.

### LESSONS_LEARNED.md
**Update Triggers:**
- Bug fixed after debugging
- Gotcha discovered
- Performance insight found
- Workaround implemented

**Format:**
```markdown
## [Category]: [Title]
**Date:** YYYY-MM-DD
**Problem:** What went wrong?
**Root Cause:** Why?
**Solution:** How fixed?
**Prevention:** Avoid in future?
```

---

### DECISION_LOG.md
**Update Triggers:**
- Technology choice made
- Architecture pattern selected
- Schema designed
- Library chosen

**Format:**
```markdown
## ADR-XXX: [Title]
**Date:** YYYY-MM-DD
**Status:** Accepted
**Context:** Why needed?
**Decision:** What decided?
**Rationale:** Why this choice?
**Consequences:** Trade-offs?
```

---

### CURRENT_OBJECTIVE.md
**Update Triggers:**
- Session starts → Set current goal
- Pivot requested → Update objective
- Goal achieved → Update for next
- Session ends → Summarize state

---

### TASK_LOG.md
**Update Triggers:**
- Task started → Log it
- Task completed → Mark done
- Blocker found → Document it
- Decision made → Note it
- Session ends → Summarize

---

## Cascade Rules

When a protected file changes, other files may need updates:

| When This Changes | Also Update |
|-------------------|-------------|
| PROJECT_BRIEF.md (scope) | ARCHITECTURE.md (if design affected), DECISION_LOG.md (always) |
| TECH_STACK.md (new tech) | ARCHITECTURE.md (if integration needed), DECISION_LOG.md (always) |
| ARCHITECTURE.md (design) | PROJECT_BRIEF.md (if capabilities affected), DECISION_LOG.md (always) |
| PRODUCT_ROADMAP.md (scope) | PROJECT_BRIEF.md (if mission affected), DECISION_LOG.md (always) |
| .cursor/README.md (protocol) | .cursorrules (to match), DECISION_LOG.md (always) |

---

## Quick Decision Tree

```
Need to update a file?
│
├── Is it protected? (PROJECT_BRIEF, TECH_STACK, ARCHITECTURE, .cursor/README)
│   ├── YES → Ask for approval first
│   │         └── After approval, also add ADR to DECISION_LOG.md
│   └── NO → Update freely
│
├── Is it PRODUCT_ROADMAP.md?
│   ├── Scope change (add/remove epics)? → Ask for approval
│   └── Task status update? → Update freely
│
└── What triggered the update?
    ├── Completed task → PRODUCT_ROADMAP.md (status only)
    ├── Fixed bug → LESSONS_LEARNED.md
    ├── Made architecture choice → DECISION_LOG.md
    ├── Starting session → CURRENT_OBJECTIVE.md
    └── Working on task → TASK_LOG.md
```

---

## Git Branch Permissions

| Branch | Direct Commit | Via PR |
|--------|:-------------:|:------:|
| `main` | ❌ Requires approval | ✅ |
| `master` | ❌ Requires approval | ✅ |
| `feat/*` | ✅ | ✅ |
| `fix/*` | ✅ | ✅ |
| `refactor/*` | ✅ | ✅ |
| `docs/*` | ✅ | ✅ |

See `guides/BRANCH_PROTECTION.md` for detailed branch workflow.

---

**END OF FILE BOUNDARIES CHEATSHEET**
