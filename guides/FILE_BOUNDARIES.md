# File Boundaries Cheatsheet

Quick reference for Memory Bank file access permissions and update triggers.

---

## Access Control Matrix

| File | Read | Write | Approval Required | When to Modify |
|------|:----:|:-----:|:-----------------:|----------------|
| **PROJECT_BRIEF.md** | ✅ Always | ⚠️ Rarely | **YES** | Only if project scope changes |
| **TECH_STACK.md** | ✅ Always | ⚠️ Rarely | **YES** | Only when adding new technology |
| **ARCHITECTURE.md** | ✅ Always | ⚠️ Rarely | **YES** | Only for significant design changes |
| **.cursor/README.md** | ✅ Always | ⚠️ Rarely | **YES** | Only when protocol changes |
| **PRODUCT_ROADMAP.md** | ✅ Always | ✅ Often | No | After completing tasks, adding new work |
| **LESSONS_LEARNED.md** | ✅ Always | ✅ Often | No | After debugging sessions |
| **DECISION_LOG.md** | ✅ Always | ✅ Often | No | After architectural choices |
| **CURRENT_OBJECTIVE.md** | ✅ Always | ✅ Every session | No | At session start and when pivoting |
| **TASK_LOG.md** | ✅ Always | ✅ Frequently | No | Throughout session |

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

### 4. .cursor/README.md
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

### PRODUCT_ROADMAP.md
**Update Triggers:**
- Task completed → Mark `[x]`
- New work identified → Add tasks
- Priorities change → Reorder/relabel
- Sprint ends → Update statuses

---

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
| .cursor/README.md (protocol) | .cursorrules Section 9 (to match), DECISION_LOG.md (always) |

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
└── What triggered the update?
    ├── Completed task → PRODUCT_ROADMAP.md
    ├── Fixed bug → LESSONS_LEARNED.md
    ├── Made architecture choice → DECISION_LOG.md
    ├── Starting session → CURRENT_OBJECTIVE.md
    └── Working on task → TASK_LOG.md
```

---

**END OF FILE BOUNDARIES CHEATSHEET**

