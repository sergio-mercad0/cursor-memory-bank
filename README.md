# Cursor Memory Bank

**v3.0** | A persistent context framework for Cursor AI that enables seamless agent handoffs without hallucinations — and, since v3.0, an execution protocol for running an Epic as a fleet of short-lived agents without the coordinator running out of context.

---

## The Problem

LLMs suffer from **context window amnesia**. Each chat session starts fresh. Your AI agent forgets:
- Why you made architectural decisions
- What patterns work in your codebase
- What tasks are in progress
- What lessons you've learned

This leads to:
- 🔄 Repeated explanations every session
- 🎭 Hallucinated code that doesn't match your patterns
- 📉 Lost productivity rebuilding context
- 🐛 Repeated mistakes from forgotten lessons

---

## The Solution

The **Memory Bank** is a structured `.cursor/` directory that gives your AI agent persistent memory:

```
.cursor/
├── README.md                    # System documentation
├── plans/                       # The job queue (v2.0, metadata contract v3.0)
│   └── *.plan.md                # phase / run_as / model_role / exit_gates per workstream
├── rules/                       # Cursor rule files (v3.0)
│   ├── environment.mdc          # Shell quirks, loaded every turn so they stop recurring
│   ├── orchestrator-ready-plans.mdc
│   └── pr-artifact-verify.mdc   # Only if the project ships an installable artifact
├── skills/
│   └── orchestrate-epic/        # One fresh subagent per workstream; parent routes gates only (v3.0)
├── prompts/                     # Orchestrator bootstrap + phase-boundary handoff (v3.0)
├── memory/                      # Long-term context
│   ├── PROJECT_BRIEF.md         # What the project does
│   ├── TECH_STACK.md            # Technologies used, capability tier
│   ├── ARCHITECTURE.md          # System design
│   ├── PRODUCT_ROADMAP.md       # Epics → phases → workstreams
│   ├── LESSONS_LEARNED.md       # Patterns, gotchas, workflow failures
│   └── DECISION_LOG.md          # ADRs (Architecture Decision Records)
└── active_sprint/               # Short-term state
    ├── CURRENT_OBJECTIVE.md     # Current session goal
    └── TASK_LOG.md              # Progress; one line per workstream with the model that ran
docs/MODEL_ROUTING.md            # Model roles — single source of truth (v3.0)
```

Combined with `.cursorrules` protocols, the agent:
- ✅ Reads context at session start
- ✅ Checks for active plan files (v2.0)
- ✅ Verifies branch state before coding (v2.0)
- ✅ Proposes plans before coding
- ✅ Executes approved plans one fresh subagent per workstream, and cycles its own chat at phase boundaries (v3.0)
- ✅ Routes each workstream to a model **role**, never a pinned version (v3.0)
- ✅ Records decisions and lessons
- ✅ Hands off cleanly to future sessions — and opens the Epic's closeout PR (v3.0)

---

## What's New in v3.0

v3.0 is what one production project's protocol looked like after 3½ months and ~80 agent sessions of
tuning. Every addition traces to a measured failure; the method is written up in `guides/RETROSPECTIVE.md`.

| Addition | Why |
|----------|-----|
| **Orchestrated execution** — plans carry `phase` / `run_as` / `model_role` / `exit_gates` / `heavy`; the `orchestrate-epic` skill dispatches one fresh subagent per workstream | One agent driving a whole Epic runs out of context; the manual "fresh chat per workstream" ritual worked but was tedious and lossy |
| **Phase grouping** — `WS <phase>.<ordinal>`, human checkpoint and a fresh orchestrator chat at every boundary | Phases are context boundaries, not just groupings |
| **"`run_as` routes the gate; `heavy` absorbs the tokens"** | Conflating "needs a human" with "parent does it" was the #1 cause of orchestrator exhaustion |
| **Model routing by role** (`docs/MODEL_ROUTING.md`) — six roles, resolved to live slugs at dispatch, resolved slug logged | Four pinned model slugs went stale in two months and kept being dispatched |
| **Branch strategy + mandatory Epic closeout PR** with a fixed body template; push is part of closeout | A roadmap ✅ with nothing on the remote misled the next agent for weeks |
| **Environment rule file** (`.cursor/rules/environment.mdc`, always applied) | Prose reminders did not stop the same failed shell command recurring once per session for months |
| **PR artifact ritual** — build, attach, verify on target, prove the installed artifact matches | Hours lost debugging a stale install |
| **Scoped TDD** replaces the pytest-bdd/Docker default (now an optional variant) | Stack-agnostic; strict red-green where mistakes ship silently, behavior tests where the user can see |
| **Expanded protected files** (`.cursorrules`, rules, skills, build config, schema) with **relayed approval** | The parent asks; the subagent edits |
| **Lean-rules layering** (`.cursorrules` §00) | A 400-line rules file re-sent every turn is a fixed cost |
| **CI skeleton**, advisory → required | 18 PRs merged on self-reported local gates before CI caught what they missed |
| **Reusable prompts** — orchestrator bootstrap, phase handoff | "Print the prompt for the next agent" was requested nine times |
| **Retrospective guide** | How to mine your own transcripts and turn friction into rules |

Also fixed: `.cursor/README.md` and `prompts/initialize.md` brought up to date, one todo-ID format
everywhere (`e{epic}-ws{phase}.{ordinal}-{shortname}`), `.gitattributes` for LF normalisation.

See [CHANGELOG.md](CHANGELOG.md) for full details.

### 4-Pillar Template Structure (since v2.0)

| Pillar | Purpose |
|--------|---------|
| **00** | How the rules are layered — what belongs in `.cursorrules` vs rules vs skills vs docs (v3.0) |
| **01_AGENT_PROTOCOL** | Memory bank, startup, branch strategy, planning, orchestration, closeout, PRs |
| **02_INFRASTRUCTURE** | Project-specific (stub for customization) |
| **03_DEVELOPMENT** | Code standards (stub for customization) |
| **04_QUALITY_ASSURANCE** | Scoped TDD and quality gates |

---

## Quick Start

### Option 1: Use the Initialization Prompt

1. Copy `prompts/initialize.md` to your first Cursor chat
2. The agent will analyze your codebase and create the Memory Bank
3. Approve the proposed roadmap
4. Start coding with persistent context!

### Option 2: Manual Setup

1. Copy the `.cursor/` structure from `templates/` to your project:
   ```bash
   mkdir -p .cursor/memory .cursor/active_sprint .cursor/plans .cursor/rules .cursor/skills/orchestrate-epic .cursor/prompts docs
   cp templates/memory/*.template.md .cursor/memory/
   cp templates/active_sprint/*.template.md .cursor/active_sprint/
   cp templates/cursor-readme.template.md .cursor/README.md
   cp templates/cursor-rules/environment.template.mdc .cursor/rules/environment.mdc
   cp templates/cursor-rules/orchestrator-ready-plans.template.mdc .cursor/rules/orchestrator-ready-plans.mdc
   cp templates/cursor-skills/orchestrate-epic/* .cursor/skills/orchestrate-epic/
   cp templates/cursor-prompts/*.md .cursor/prompts/
   cp templates/docs/MODEL_ROUTING.md docs/
   ```
   (PowerShell equivalents are in `QUICKSTART.md`.)

2. Rename `.template.md` files to `.md` and fill in the content; prune `environment.mdc` to your shell;
   review `docs/MODEL_ROUTING.md` ladders against your editor's live model list

3. Add Memory Bank protocols to your `.cursorrules`, fill §02/§03, and replace the gate placeholders in §4.5:
   ```bash
   cat templates/.cursorrules >> .cursorrules
   ```

4. (Optional) If the project ships an installable artifact or has no CI:
   ```bash
   cp templates/cursor-rules/pr-artifact-verify.template.mdc .cursor/rules/pr-artifact-verify.mdc
   mkdir -p .github/workflows && cp templates/ci/ci.example.yml .github/workflows/ci.yml
   ```

5. (Optional) BDD testing variant — see "Python + pytest-bdd + Docker" in `guides/CUSTOMIZATION.md`.

---

## Key Concepts

### Passive vs Active Memory

| Type | Files | Purpose |
|------|-------|---------|
| **Passive** (ReadOnly) | PROJECT_BRIEF, TECH_STACK, ARCHITECTURE | Stable context rarely changed |
| **Protected** (Approval) | PRODUCT_ROADMAP (scope changes) | Requires approval for changes |
| **Active** (Read/Write) | LESSONS, DECISIONS | Frequently updated knowledge |
| **Session** (High-frequency) | CURRENT_OBJECTIVE, TASK_LOG | Updated every session |

### The Plan-and-Confirm Protocol

Every session starts with:
1. Agent checks for active `.plan.md` files (v2.0)
2. Agent verifies current branch (v2.0)
3. Agent reads PRODUCT_ROADMAP.md
4. Agent proposes a numbered plan
5. User approves, modifies, or redirects
6. Agent executes and updates progress

This prevents the agent from going off-track and ensures alignment.

### Plan File Continuity (v2.0) and the Job Queue (v3.0)

For multi-session work, plan files are authoritative — and since v3.0 they are also the queue the
orchestrator executes, so every workstream carries routing metadata:

```markdown
---
name: Epic 2 — User Authentication System
todos:
  - id: e2-ws1.1-jwt
    content: "[Epic 2 > WS 1.1] (Phase 1) Implement JWT tokens"
    status: in_progress
    phase: 1
    run_as: subagent
    model_role: BUILDER
    exit_gates: [typecheck, test, lint]
---
```

See `guides/PLAN_CONTINUITY.md` and `guides/ORCHESTRATION.md`.

### Orchestrated Execution (v3.0)

```
Plan (approved) ──▶ orchestrator chat ──▶ fresh subagent per workstream ──▶ exit gates ──▶ status on disk
                         │                                                                    │
                         └── stops at human gates; never does the work ◀── phase boundary: new chat
```

- **`run_as`** answers *who routes the human gate*; **`heavy`** answers *who absorbs the tokens*.
- Subagents return ≤8 lines; builds, logs and screenshots never enter the coordinator's window.
- Models are chosen by **role**, resolved against the live list at dispatch, and the resolved slug is logged.

See `guides/ORCHESTRATION.md` and `templates/docs/MODEL_ROUTING.md`.

### Branch Protection (v2.0) and Epic Closeout (v3.0)

Agent verifies branch state at session start:
- Warns if on main/master
- One Epic = one branch off fresh `main`; `main` accepts PRs only
- Handles uncommitted changes gracefully

Closeout is not done until the branch is pushed; an Epic is not done until its `Epic N: <Title>` PR
exists with the fixed body template (Summary / Workstreams / Decisions / Quality gates / Manual
verification / Follow-ups / Test artifact).

See `guides/BRANCH_PROTECTION.md` for details.

---

## Package Contents

```
cursor-memory-bank/
├── README.md                 # This file
├── QUICKSTART.md             # Step-by-step first use (bash + PowerShell)
├── CHANGELOG.md              # Version history
├── LICENSE                   # MIT License
├── prompts/
│   └── initialize.md         # The "bootstrap" prompt
├── templates/
│   ├── .cursorrules          # Memory Bank rules (4-pillar structure)
│   ├── cursor-readme.template.md    # .cursor/README.md template
│   ├── memory/*.template.md  # Long-term context templates
│   ├── active_sprint/*.template.md  # Session templates
│   ├── cursor-rules/         # .cursor/rules/*.mdc templates (v3.0)
│   │   ├── environment.template.mdc
│   │   ├── orchestrator-ready-plans.template.mdc
│   │   └── pr-artifact-verify.template.mdc
│   ├── cursor-skills/
│   │   └── orchestrate-epic/ # SKILL.md + plan-template.md (v3.0)
│   ├── cursor-prompts/       # orchestrate.md, handoff.md (v3.0)
│   ├── docs/
│   │   └── MODEL_ROUTING.md  # Model roles — single source of truth (v3.0)
│   ├── ci/
│   │   └── ci.example.yml    # Quality-gate workflow skeleton (v3.0)
│   └── tests/
│       ├── conftest.py       # pytest-bdd boilerplate (optional variant)
│       └── sample.feature    # Gherkin example (optional variant)
├── guides/
│   ├── ORCHESTRATION.md      # Plan-as-job-queue, phases, context economy (v3.0)
│   ├── RETROSPECTIVE.md      # Tune the protocol from your transcripts (v3.0)
│   ├── PLAN_CONTINUITY.md    # Multi-session plan workflow
│   ├── BRANCH_PROTECTION.md  # Epic branches and closeout PRs
│   ├── FILE_BOUNDARIES.md    # Access control cheatsheet
│   ├── DECISION_HEURISTIC.md # When DECISION vs LESSON
│   └── CUSTOMIZATION.md      # Adapting for different stacks
└── examples/                 # Reference implementations
```

---

## Customization

The Memory Bank works with any tech stack. See `guides/CUSTOMIZATION.md` for:

- Python, Node.js, Rust, Go adaptations
- Monolith vs Microservices structures
- With or without Docker
- With or without BDD/Gherkin testing

---

## Best Practices

### 1. Start Every Session Right

Check for active plans, verify branch, read the roadmap, propose a plan, wait for approval. Don't dive into code.

### 2. Use Feature Branches

Always work on feature branches (`feat/`, `fix/`, `refactor/`). Never commit directly to main.

### 3. Record Decisions Immediately

When you make a choice ("Let's use X instead of Y"), add an ADR before you forget the rationale.

### 4. Record Lessons After Debugging

When you fix a tricky bug, document the problem, cause, and solution.

### 5. Keep the Roadmap Current

Update task statuses as you complete work. Mark items `[x]` done.

### 6. Hand Off Cleanly

At session end, update CURRENT_OBJECTIVE and TASK_LOG for the next session — and **push**. A roadmap
✅ with nothing on the remote is the most misleading state the next agent can inherit.

### 7. Let the Coordinator Coordinate

The orchestrator never edits a file, runs a build, or reads a screenshot. It dispatches, gates, and
stops. If it is doing anything else, it is about to run out of context.

### 8. Measure Before You Add a Rule

Before adding a paragraph to `.cursorrules`, find the sessions where its absence cost something
(`guides/RETROSPECTIVE.md`). A rule with a measured cause is far less likely to be softened later.

---

## Comparison

| Approach | Pros | Cons |
|----------|------|------|
| **No Memory** | Simple | Agent forgets everything |
| **Long System Prompt** | Always present | Static, no evolution |
| **RAG/Embeddings** | Semantic search | Complex setup, latency |
| **Memory Bank** | Structured, evolving, simple | Requires discipline |

The Memory Bank is designed for **practical simplicity**. No external services, no complex pipelines—just structured markdown files that the agent reads and writes.

---

## FAQ

### Q: Does this work with other AI editors?

The core concept works anywhere. The `.cursorrules` integration is Cursor-specific, but the Memory Bank structure can be adapted for other tools.

### Q: How do I handle multiple agents/contributors?

The Memory Bank is version-controlled. Multiple contributors (human or AI) can update it through normal git workflows. Merge conflicts in markdown are easy to resolve.

### Q: What if the context gets too long?

Don't drive a whole Epic in one chat. v3.0's orchestration model gives every workstream a fresh
subagent and ends the coordinator's chat at every phase boundary; durable state is on disk, so nothing
is lost. Keep `.cursorrules` lean (it is re-sent every turn) and move detail into `.cursor/rules/*.mdc`
with `alwaysApply: false`. See `guides/ORCHESTRATION.md`.

### Q: Do I have to use the orchestration skill?

No. Sections 01–04 of `.cursorrules` work with plain chat sessions. The skill, the plan metadata, and
the model roles are what make multi-phase Epics survivable; adopt them when a single chat stops being enough.

### Q: Which models should I use?

Pick by **role**, not by name: `docs/MODEL_ROUTING.md` defines six roles and a resolution procedure
that survives model lineup changes. Never write a model version into a plan or skill.

### Q: Can I use this without the testing framework?

The default testing section is now stack-agnostic Scoped TDD. The pytest-bdd/Docker two-phase gate
from v1–v2 is still available as an optional variant in `guides/CUSTOMIZATION.md`.

### Q: What's different in v3.0?

See [CHANGELOG.md](CHANGELOG.md). Key additions: orchestrated execution, phase grouping, model routing
by role, mandatory Epic closeout PR, environment rule file, Scoped TDD, expanded protected files.

---

## Contributing

This framework evolved from real project experience. Contributions welcome:

- New customization examples for different stacks
- Improved templates
- Additional guides
- Bug fixes in templates

---

## License

MIT License - see LICENSE file.

---

## Acknowledgments

Inspired by:
- Architecture Decision Records (ADRs)
- The "Second Brain" methodology
- Zettelkasten for knowledge management
- The pain of re-explaining context to AI agents

---

**Stop losing context. Start banking memories.**
