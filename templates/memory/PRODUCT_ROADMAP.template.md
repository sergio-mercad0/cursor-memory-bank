# Product Roadmap

**Last Updated:** <YYYY-MM-DD>  
**Purpose:** Track epics, workstreams, and tasks for <Project Name> development

---

## Roadmap Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Completed |
| 🔄 | In Progress |
| ⏳ | Pending |
| ❌ | Blocked/Cancelled |
| 🔥 | High Priority |
| 📋 | Low Priority |

---

## Epic 0: <Foundation/Setup Epic> 🔥 ✅

**Goal:** <One-sentence goal for this Epic>

### Workstream 0.1: <Workstream Name> ✅
- [x] <Completed task>
- [x] <Completed task>
- [x] <Completed task>

### Workstream 0.2: <Workstream Name> ✅
- [x] <Completed task>
- [x] <Completed task>
- [x] <Completed task>

---

## Epic 1: <Core Feature Epic> 🔥 ✅

**Goal:** <One-sentence goal for this Epic>
**Branch:** `feat/epic-1-<slug>` · **Plan:** `.cursor/plans/epic_1_<slug>.plan.md` · **PR:** #<N>

<!-- From Epic 1 on, workstreams are grouped into phases and numbered <phase>.<ordinal>
     (the ordinal resets each phase). Epic 0 above keeps the flat form. -->

### Phase 1 — <Phase Name> ✅

#### Workstream 1.1: <Workstream Name> ✅
- [x] <Completed task>
- [x] <Completed task>

#### Workstream 1.2: <Workstream Name> ✅
- [x] <Completed task>

### Phase 2 — <Phase Name> 🔄

#### Workstream 2.1: <Workstream Name> 🔄
- [x] <Completed task>
- [~] <In progress task>
- [ ] <Pending task>

---

## Epic 2: <Feature Epic> ⏳ 📋

**Goal:** <One-sentence goal for this Epic>
**Branch:** — · **Plan:** — (planned when the Epic is kicked off)

### Phase 1 — <Phase Name> ⏳

#### Workstream 1.1: <Workstream Name> ⏳
- [ ] <Pending task>
- [ ] <Pending task>

#### Workstream 1.2: <Workstream Name> ⏳
- [ ] <Pending task>

### Phase 2 — Closeout ⏳

#### Workstream 2.1: Roadmap + memory + closeout PR ⏳
- [ ] Update roadmap statuses, record ADRs / lessons
- [ ] Push; open `Epic 2: <Title>` PR against `main`

---

## Backlog (Future Epics)

<!-- List epics that are planned but not yet detailed -->

### Epic N: <Future Epic Name>
- <Brief description of goals>
- <Key features to implement>

### Epic N+1: <Future Epic Name>
- <Brief description of goals>
- <Key features to implement>

---

## Milestone Timeline

| Quarter | Focus |
|---------|-------|
| <Q1 Year> | <Focus areas> |
| <Q2 Year> | <Focus areas> |
| <Q3 Year> | <Focus areas> |
| <Q4 Year> | <Focus areas> |

---

## Task Status Reference

### Status Markers
* `[ ]` - Pending
* `[x]` - Completed
* `[~]` - In Progress (use sparingly, prefer atomic tasks)
* `[-]` - Cancelled/Skipped (with reason)

### Priority Labels
* 🔥 High Priority - Do immediately
* 📋 Low Priority - Do when high priority work is complete

### Progress Indicators
* ✅ Complete - All workstreams finished **and pushed**; for an Epic, its closeout PR exists
* 🔄 In Progress - At least one workstream active
* ⏳ Pending - Not yet started
* ❌ Blocked - Cannot proceed until blocker resolved

### Numbering
* Workstreams are `<phase>.<ordinal>`; the ordinal resets in each phase (`1.1, 1.2 | 2.1, 2.2, 2.3 | 3.1`).
* Plan todo IDs mirror this: `e{epic}-ws{phase}.{ordinal}-{shortname}`.
* Flipping a task `[ ]` → `[x]` needs no approval; adding/removing Epics or changing scope does.

---

**END OF PRODUCT ROADMAP**

