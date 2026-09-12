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
| **.cursorrules** | ✅ Always | ⚠️ Rarely | **YES** | Only with explicit user approval |
| **.cursor/rules/*.mdc**, **.cursor/skills/** | ✅ Always | ⚠️ Rarely | **YES** | Protocol changes — record an ADR |
| **Build / app config** (e.g. `app.config.*`, `Dockerfile`, CI workflow) | ✅ Always | ⚠️ Rarely | **YES** | Affects every build |
| **Schema sources** (ORM schema, migrations, sync schema) | ✅ Always | ⚠️ Rarely | **YES** | Cascades to every layer |
| **LESSONS_LEARNED.md** | ✅ Always | ✅ Often | No | After debugging sessions or workflow failures |
| **DECISION_LOG.md** | ✅ Always | ✅ Often | No | After architectural or process choices |
| **CURRENT_OBJECTIVE.md** | ✅ Always | ✅ Every session | No | At session start and when pivoting |
| **TASK_LOG.md** | ✅ Always | ✅ Frequently | No | Throughout session; one line per workstream with the resolved model |
| **.cursor/plans/*.plan.md** | ✅ Always | ✅ Status flips | No | Statuses during execution; content only in Planning Mode |

> **Note (v2.0):** PRODUCT_ROADMAP.md requires approval for scope changes (adding/removing epics, changing priorities). Updating task statuses (`[ ]` → `[x]`) does NOT require approval.

> **Note (v3.0 — relayed approval):** in orchestrated execution the parent agent obtains approval for a
> protected-file edit and states it explicitly in the subagent's dispatch prompt ("the user approved
> editing `<file>` for this workstream"). The subagent then performs the edit. A subagent that needs a
> protected-file edit without that sentence stops and reports.

---

## Tool Permissions Matrix

| Tool/Action | Allowed | Requires Approval | Notes |
|-------------|:-------:|:-----------------:|-------|
| **Read any file** | ✅ | No | Always allowed |
| **Write to `.cursor/active_sprint/`** | ✅ | No | Session state files |
| **Write to LESSONS_LEARNED.md** | ✅ | No | After debugging |
| **Write to DECISION_LOG.md** | ✅ | No | After decisions |
| **Update task statuses in ROADMAP** | ✅ | No | `[ ]` → `[x]` transitions |
| **Write to `.cursor/plans/`** | ✅ | No | Status flips; content edits in Planning Mode |
| **Write to protected files** | ⚠️ | **YES** | May be relayed to a subagent (see note above) |
| **Add/remove epics from ROADMAP** | ⚠️ | **YES** | Scope changes |
| **Dispatch subagents for planned workstreams** | ✅ | No | One fresh subagent per workstream |
| **Git commit / push to feature branch** | ✅ | No | Normal workflow; push is part of closeout |
| **Git commit / push to main/master** | ❌ | **YES** | Protected branches — PR only |
| **Open a Pull Request** | ⚠️ | **YES** | The user gate of the closeout workstream |
| **Create new files in project** | ✅ | No | Normal workflow |
| **Delete files** | ⚠️ | **YES** | Destructive action |
| **Run shell commands** | ✅ | No | Normal workflow |
| **Install software / send data off-machine** | ⚠️ | **YES** | Confirm first |
| **Run destructive commands** | ❌ | **YES** | rm -rf, force push, drop database, etc. |

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

### 6. .cursorrules, .cursor/rules/*.mdc, .cursor/skills/** (v3.0)
**Contains:** The rules the agent runs under, environment conventions, orchestration procedures

**Modify When:**
- A retrospective (see `guides/RETROSPECTIVE.md`) shows a recurring failure the current rule does not prevent
- A per-plan override of a skill keeps recurring — then the skill is wrong, fix the skill
- The user states a standing preference ("always do X when Y") — capture it the same session

**Approval Process:**
1. Quote the evidence (which sessions, how often)
2. Show the exact rule text to add or change, and which file it belongs in (see `.cursorrules` §00)
3. Wait for user approval — a user instruction that *is* the rule counts as approval
4. Record an ADR

---

### 7. Build config and schema sources (v3.0)
**Contains:** Whatever affects every build (app config, Dockerfile, CI workflow) and whatever cascades to every layer (ORM schema, migrations, sync schema)

**Modify When:** the plan's workstream says so, with `run_as: parent` so the gate is routed to the user

**Approval Process:**
1. Show the diff and the cascade (what else must change)
2. Wait for approval; in orchestrated execution the parent relays it in the dispatch prompt
3. Apply the whole cascade in one workstream; generate the migration; add an ADR if non-trivial

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
- Workstream completed → `[WS <id>] <role> → <resolved model slug> — <outcome>` (this line is the only record of which model actually ran)
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
| Schema source of truth | Every mirrored schema layer, generated migration, DECISION_LOG.md if non-trivial |
| .cursorrules (rule added) | .cursor/README.md if the protocol summary is affected; never duplicate the rule text elsewhere |

---

## Quick Decision Tree

```
Need to update a file?
│
├── Is it protected? (PROJECT_BRIEF, TECH_STACK, ARCHITECTURE, .cursor/README, .cursorrules,
│                     .cursor/rules, .cursor/skills, build config, schema sources)
│   ├── YES → Ask for approval first (or check the dispatch prompt for relayed approval)
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
