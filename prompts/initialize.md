# Memory Bank Initialization Prompt

**Purpose:** Copy this prompt into your first Cursor AI chat session to bootstrap the Memory Bank system for your project.

---

## Prompt

You are the **Lead Architect** initializing the Memory Bank system for this project. The Memory Bank is a persistent context structure that enables seamless AI agent handoffs without hallucinations.

Your mission is to analyze this codebase and create a `.cursor/` directory structure that captures:
- What the project does (PROJECT_BRIEF.md)
- What technologies it uses (TECH_STACK.md)
- How it's architected (ARCHITECTURE.md)
- What's been decided and why (DECISION_LOG.md)
- What lessons have been learned (LESSONS_LEARNED.md)
- What work remains to be done (PRODUCT_ROADMAP.md)

---

## Phase 0: Analyze Codebase

Before creating any files, analyze the existing codebase:

1. **Find dependency files:**
   - `package.json` / `package-lock.json` (Node.js)
   - `requirements.txt` / `Pipfile` / `pyproject.toml` (Python)
   - `Cargo.toml` (Rust)
   - `go.mod` (Go)
   - `pom.xml` / `build.gradle` (Java)

2. **Identify architecture patterns:**
   - Monolith vs microservices
   - Frontend framework (React, Vue, Angular, etc.)
   - Backend framework (Django, FastAPI, Express, etc.)
   - Database technology

3. **Map module structure:**
   - Source directories
   - Test directories
   - Configuration locations
   - Infrastructure files (Docker, CI/CD)

4. **Check for existing documentation:**
   - README.md
   - CONTRIBUTING.md
   - Architecture diagrams

---

## Phase 1: Create Directory Structure

First confirm you are on a feature branch (`git branch --show-current`); if on `main`, create
`chore/memory-bank-init` before writing anything. Then create the following structure:

```
.cursor/
├── README.md                    # System documentation (from templates/cursor-readme.template.md)
├── plans/                       # Planning documents — create empty
├── rules/                       # Cursor rule files
│   ├── environment.mdc          # from templates/cursor-rules/environment.template.mdc — prune to this machine's shell
│   └── orchestrator-ready-plans.mdc   # from templates/cursor-rules/orchestrator-ready-plans.template.mdc
├── skills/
│   └── orchestrate-epic/        # copy templates/cursor-skills/orchestrate-epic/ ; replace <Project Name>
├── prompts/                     # copy templates/cursor-prompts/*.md
├── memory/                      # Long-term context
│   ├── PROJECT_BRIEF.md         # Mission, scope, future capabilities
│   ├── TECH_STACK.md            # Technologies, versions, capability tier
│   ├── ARCHITECTURE.md          # System design and data flow
│   ├── PRODUCT_ROADMAP.md       # Epics → phases → workstreams
│   ├── LESSONS_LEARNED.md       # Patterns and gotchas
│   └── DECISION_LOG.md          # Architecture Decision Records
└── active_sprint/               # Short-term state
    ├── CURRENT_OBJECTIVE.md     # Current session goal
    └── TASK_LOG.md              # Progress tracking

docs/MODEL_ROUTING.md            # from templates/docs/MODEL_ROUTING.md — review ladders against the live model list
```

Only add `.cursor/rules/pr-artifact-verify.mdc` and `.github/workflows/ci.yml` (from `templates/ci/ci.example.yml`)
if the project ships an installable artifact / has no CI yet. Fill every `<placeholder>` command.

---

## Phase 2: Populate Context (From Code)

### TECH_STACK.md
Extract from dependency files:
- List all languages and their versions
- List all frameworks and libraries
- Document database technologies
- Note infrastructure tools (Docker, Kubernetes, etc.)
- Document external services/APIs

### ARCHITECTURE.md
Infer from code structure:
- Create a system overview diagram (ASCII or Mermaid)
- Document data flow between components
- List all modules/services and their purposes
- Note design patterns in use
- Document path conventions

### PROJECT_BRIEF.md
Derive from README and code analysis:
- Define the project mission (what problem it solves)
- List current features (what's implemented)
- Identify future capabilities (architectural awareness)
- Define success metrics
- List explicit non-goals

### LESSONS_LEARNED.md
Look for patterns and gotchas:
- Common code patterns (with examples)
- Error handling approaches
- Configuration conventions
- Testing patterns
- Any workarounds or special cases

### DECISION_LOG.md
Document implicit decisions as ADRs:
- Why was this language/framework chosen?
- Why this database over alternatives?
- Why this project structure?
- Any significant library choices?

Use this format for each decision:
```markdown
## ADR-XXX: [Title]
**Date:** [When decision was made, or "Implicit" if unclear]
**Status:** Accepted

### Context
[What situation required this decision?]

### Decision
[What was decided?]

### Rationale
[Why this choice over alternatives?]

### Consequences
[What are the trade-offs and implications?]
```

---

## Phase 3: Propose Roadmap

Based on your analysis, propose a PRODUCT_ROADMAP.md that:

1. **Documents completed work** - What Epics are already done?
2. **Identifies current state** - What's in progress?
3. **Proposes future Epics** - What logical next steps exist?
4. **Notes technical debt** - What needs cleanup?

Use this format:
```markdown
## Epic X: [Title] [Priority] [Status]

**Goal:** [One sentence description]
**Branch:** feat/epic-X-<slug>   **Plan:** .cursor/plans/epic_X_<slug>.plan.md

### Phase 1 — [Name] [Status]
#### Workstream 1.1: [Title] [Status]
- [x] Completed task
- [ ] Pending task
- [~] In progress task
```

**STOP HERE** and present the proposed roadmap to the user for approval before proceeding.

---

## Phase 4: Enforce Protocol

After user approves the roadmap, update or create `.cursorrules` from `templates/.cursorrules`:

1. **Startup Protocol:** check active plans, verify branch, read roadmap, await approval before coding
2. **Branch Strategy:** one Epic = one branch off fresh `main`; `main` is PR-only
3. **Planning:** plan files carry `phase` / `run_as` / `model_role` / `exit_gates`; todos use `[Epic X > WS P.O] (Phase P) Task`
4. **Orchestrated execution:** one fresh subagent per workstream; the parent only routes gates; cycle chats at phase boundaries
5. **Decision Heuristic:** when to use DECISION_LOG vs LESSONS_LEARNED (process decisions are ADRs too)
6. **Session Handoff:** update TASK_LOG and CURRENT_OBJECTIVE, commit **and push**; Epic closeout opens a PR
7. **Protected Files:** including `.cursorrules`, `.cursor/rules`, build config, schema sources
8. **Sections 02 / 03:** fill the stack-specific stubs; **§4.5:** replace `<typecheck>` / `<test>` / `<lint>` / `<format:check>` with real commands

Record the initialization itself as `ADR-001: Adopt cursor-memory-bank v3.0 protocol`.

---

## Approval Checkpoints

The initialization process has two approval checkpoints:

1. **After Phase 2:** "I've analyzed the codebase. Here's what I found... Do you want me to proceed with creating the Memory Bank files?"

2. **After Phase 3:** "Here's the proposed roadmap based on the current codebase state... Do you approve this roadmap?"

Do not proceed past these checkpoints without explicit user approval.

---

## Post-Initialization

After the Memory Bank is initialized:

1. The agent should start each session by reading `PRODUCT_ROADMAP.md`
2. The agent should propose a plan before writing code
3. The agent should update `TASK_LOG.md` throughout the session
4. The agent should update roadmap task statuses when complete
5. The agent should record decisions and lessons as they occur

---

## Success Criteria

The Memory Bank is successfully initialized when:

- [ ] All 8 memory / active_sprint files exist, plus `plans/`, `rules/environment.mdc`, `rules/orchestrator-ready-plans.mdc`, `skills/orchestrate-epic/`, `prompts/`
- [ ] `docs/MODEL_ROUTING.md` exists and its ladders were reviewed against the live model list
- [ ] TECH_STACK.md accurately reflects dependencies (and the capability tier, if any)
- [ ] ARCHITECTURE.md has a system diagram
- [ ] PROJECT_BRIEF.md defines scope and future capabilities
- [ ] DECISION_LOG.md has at least 3 ADRs (including the adoption ADR)
- [ ] PRODUCT_ROADMAP.md has at least one Epic with phases
- [ ] `.cursorrules` includes the Memory Bank Protocol with real gate commands in §4.5
- [ ] `environment.mdc` was pruned to this machine's shell
- [ ] User has approved the roadmap
- [ ] Everything is committed on a feature branch and pushed

---

**END OF INITIALIZATION PROMPT**

