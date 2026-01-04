# Decision Heuristic Guide

When to record a DECISION vs a LESSON in the Memory Bank.

---

## The Quick Rule

> **DECISION:** "We chose X because..."  
> **LESSON:** "We learned that X causes Y when..."

---

## DECISION_LOG.md

### When to Add

Record in DECISION_LOG.md when you're making a **choice that affects the future**:

| Trigger | Example |
|---------|---------|
| Choosing a technology | "We chose PostgreSQL over SQLite for..." |
| Selecting a library | "We chose axios over fetch for..." |
| Defining architecture | "We chose microservices over monolith for..." |
| Designing schema | "We designed the users table with..." |
| Picking a pattern | "We use the repository pattern for..." |
| Infrastructure choice | "We chose Docker Compose over Kubernetes for..." |

### Keyword Triggers

If you catch yourself saying:
- "I chose X over Y because..."
- "We're using X instead of Y..."
- "The architecture will be..."
- "This pattern works best for..."
- "Let's go with X..."

→ **Add a DECISION record**

### Format

```markdown
## ADR-XXX: [Title]

**Date:** YYYY-MM-DD
**Status:** Accepted

### Context
What situation required this decision?

### Decision
What was decided?

### Rationale
Why this choice over alternatives?

### Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| Option A | ... | ... |
| Option B | ... | ... |

### Consequences
What are the trade-offs?
```

---

## LESSONS_LEARNED.md

### When to Add

Record in LESSONS_LEARNED.md when you **discover something through experience**:

| Trigger | Example |
|---------|---------|
| Fixed a bug | "The session was leaking because..." |
| Found a gotcha | "SQLAlchemy requires closing sessions..." |
| Discovered a workaround | "To fix the race condition, we..." |
| Performance insight | "Batching queries reduced time by..." |
| Environment issue | "Docker on Windows requires..." |
| Library quirk | "This library silently fails when..." |

### Keyword Triggers

If you catch yourself saying:
- "The problem was..."
- "The fix was..."
- "Watch out for..."
- "I wish I knew..."
- "This happens because..."
- "The workaround is..."

→ **Add a LESSON record**

### Format

```markdown
## [Category]: [Title]

**Date:** YYYY-MM-DD
**Problem:** What went wrong or was confusing?
**Root Cause:** Why did it happen?
**Solution:** How was it fixed?
**Prevention:** How to avoid this in future?
```

---

## Examples

### Example 1: Database Choice

**Scenario:** Choosing between PostgreSQL and SQLite for a new project.

**This is a DECISION** because:
- It's a choice made before implementation
- It affects future development
- There are alternatives to consider

```markdown
## ADR-001: PostgreSQL over SQLite

**Date:** 2024-01-15
**Status:** Accepted

### Context
Choosing database for the application.

### Decision
Use PostgreSQL 15.

### Rationale
- Better concurrency handling
- JSONB support for flexible schemas
- Production-ready

### Consequences
- Requires Docker container
- More setup than SQLite
```

---

### Example 2: Session Leak Bug

**Scenario:** Found that database sessions weren't being closed properly.

**This is a LESSON** because:
- It was discovered through debugging
- It's an operational gotcha
- Future developers should know about it

```markdown
## Database: SQLAlchemy Session Leak

**Date:** 2024-01-20
**Problem:** Database connections exhausted after running app for hours.
**Root Cause:** Sessions not closed in context manager exit.
**Solution:** Added explicit session.close() in __exit__ method.
**Prevention:** Always use context managers, add integration test for connection count.
```

---

### Example 3: Framework Selection

**Scenario:** Choosing between FastAPI and Flask for the API.

**This is a DECISION** because:
- It's an architectural choice
- It affects the entire codebase
- It was made deliberately

```markdown
## ADR-002: FastAPI over Flask

**Date:** 2024-01-15
**Status:** Accepted

### Decision
Use FastAPI for the REST API.

### Rationale
- Automatic OpenAPI documentation
- Built-in validation with Pydantic
- Async support out of the box
```

---

### Example 4: Docker Volume Permissions

**Scenario:** Discovered that PostgreSQL fails on Windows with certain volume mounts.

**This is a LESSON** because:
- It was discovered through troubleshooting
- It's a platform-specific gotcha
- It's not a choice but a constraint

```markdown
## Docker: PostgreSQL Volume Permissions on Windows

**Date:** 2024-02-01
**Problem:** PostgreSQL container failed to start with permission error.
**Root Cause:** Windows Docker volumes have different permission model.
**Solution:** Use named volumes instead of bind mounts for PostgreSQL data.
**Prevention:** Document in README, test on Windows before release.
```

---

## Decision Tree

```
Something important happened?
│
├── Was it a CHOICE you made?
│   │
│   ├── YES → Does it affect future development?
│   │   │
│   │   ├── YES → DECISION_LOG.md
│   │   │         (Add ADR with context, rationale, consequences)
│   │   │
│   │   └── NO → Probably just implementation detail, skip it
│   │
│   └── NO → Was it DISCOVERED through experience?
│       │
│       ├── YES → Will others encounter this?
│       │   │
│       │   ├── YES → LESSONS_LEARNED.md
│       │   │         (Add lesson with problem, cause, solution)
│       │   │
│       │   └── NO → Might still be worth noting for your future self
│       │
│       └── NO → Probably routine work, skip it
│
└── Neither? → Might be a task update (TASK_LOG.md) or objective change (CURRENT_OBJECTIVE.md)
```

---

## Common Mistakes

### ❌ Wrong: Recording a bug fix as a Decision

```markdown
## ADR-005: Fix null pointer exception
```

**Why it's wrong:** This is a lesson learned, not an architectural decision.

### ✅ Right: Recording the bug fix as a Lesson

```markdown
## Null Safety: Unhandled null in user lookup
**Problem:** NullPointerException when user not found
**Solution:** Added null check before property access
```

---

### ❌ Wrong: Recording a technology choice as a Lesson

```markdown
## We learned to use React
```

**Why it's wrong:** This was a deliberate choice, not something discovered.

### ✅ Right: Recording the technology choice as a Decision

```markdown
## ADR-003: React for Frontend
**Decision:** Use React 18 for the frontend
**Rationale:** Team familiarity, ecosystem, component model
```

---

## Summary Table

| Characteristic | DECISION | LESSON |
|----------------|----------|--------|
| **Nature** | Proactive choice | Reactive discovery |
| **Timing** | Before/during implementation | After encountering issue |
| **Format** | ADR (formal) | Problem/Solution (informal) |
| **Purpose** | Document rationale | Prevent repetition |
| **Audience** | Future architects | Future debuggers |
| **Keywords** | "chose", "selected", "decided" | "found", "fixed", "discovered" |

---

**END OF DECISION HEURISTIC GUIDE**

