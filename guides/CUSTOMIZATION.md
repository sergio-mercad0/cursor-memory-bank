# Customization Guide

Adapting the Cursor Memory Bank for different project types, tech stacks, and machines.

---

## Overview

The Memory Bank structure is **stack-agnostic**. Sections 01 (agent protocol) and 04 (quality
assurance) of `templates/.cursorrules` apply everywhere; sections 02 (infrastructure) and 03
(development) are stubs you fill in. This guide shows what to fill in for common stacks, and which
optional template files to adopt.

Three things are customized on every project, whatever the stack:

| Concern | File | What to change |
| --- | --- | --- |
| Gate commands | `.cursorrules` §4.5 and every `exit_gates` list | Replace `<typecheck>`, `<test>`, `<lint>`, `<format:check>` with real commands |
| Environment quirks | `.cursor/rules/environment.mdc` | Keep only the sections that apply to the development machine's shell |
| Model roles | `docs/MODEL_ROUTING.md` §2–3 | Review the example ladders and prefix patterns against the editor's current model list |

---

## By Language/Framework

### TypeScript / mobile (React Native, Expo) — the stack v3.0 was tuned on

**Gate commands** (`package.json` scripts): `npm run typecheck` (tsc --noEmit), `npm run lint`,
`npm run test` (Jest + testing library), `npm run format:check` (Prettier).

**Directory Structure:**
```
project/
├── .cursor/                # memory, plans, rules, skills, prompts
├── app/                    # file-based routes
├── src/
│   ├── features/<name>/    # screens/, components/, store.ts, __tests__/
│   ├── components/ui/      # pure primitives
│   ├── db/schema/          # ORM schema (protected)
│   ├── lib/                # clients, sync, observability
│   └── theme/              # design tokens — no hardcoded values in components
├── docs/                   # runbooks (emulator, device testing), MODEL_ROUTING.md
└── app.config.ts           # protected — affects every build
```

**Customize in `.cursorrules`:**
```markdown
## 2.1 Stack (do not deviate)
- <router> on React Native, TypeScript strict
- Local DB via <ORM>; sync via <sync layer>; UI state via <ephemeral store> only
- Validation at every network and storage boundary

## 2.4 Schema Cascade
Source of truth is <backend schema>. Update it first → mirror ORM types → mirror sync schema →
generate migration → ADR if non-trivial. Never let the layers drift.

## 3.1 Hard Rules
- Functional components only. No `any`; use `unknown` and narrow. No casts without a `// cast: <reason>`.
- UI components are pure. Side effects live in stores, hooks, or /lib.
- No hardcoded colors, spacing, radii — add to the theme first.
```

**Adopt:** `pr-artifact-verify.mdc` (the APK/IPA is the artifact), a `docs/EMULATOR_TESTING.md`
runbook, and `heavy: true` on every build/emulator workstream.

---

### Python Projects

**Gate commands:** `mypy src`, `ruff check .`, `pytest -q`, `ruff format --check .`

**Directory Structure:**
```
project/
├── .cursor/
├── src/
│   ├── service_a/
│   │   ├── main.py
│   │   └── tests/
│   └── shared/
├── tests/                  # cross-cutting tests
└── pyproject.toml
```

**Customize in `.cursorrules`:**
```markdown
## 4.1 Testing Strategy (Scoped TDD)
| Layer | Strategy |
| Services, repositories, validators, utilities | Strict red-green-refactor with pytest |
| HTTP handlers / CLI | Behavior tests through the public interface |
```

For the BDD + Docker two-phase variant this framework shipped in v1–v2, see
"Python + pytest-bdd + Docker" below.

---

### Node.js / TypeScript (backend)

**Gate commands:** `npm run typecheck`, `npm run lint`, `npm test`, `npm run format:check`

**Directory Structure:**
```
project/
├── .cursor/
├── src/
│   ├── services/<name>/    # index.ts + __tests__/
│   └── shared/
├── tests/                  # cross-cutting
├── package.json
└── tsconfig.json
```

---

### Rust Projects

**Gate commands:** `cargo check`, `cargo clippy -- -D warnings`, `cargo test`, `cargo fmt --check`

```
project/
├── .cursor/
├── src/
│   ├── lib.rs
│   └── main.rs
├── tests/
└── Cargo.toml
```

---

### Go Projects

**Gate commands:** `go vet ./...`, `golangci-lint run`, `go test ./...`, `gofmt -l .`

```
project/
├── .cursor/
├── cmd/app/main.go
├── internal/
│   ├── service/
│   └── repository/
├── go.mod
└── go.sum
```

---

## By Project Type

### Monolith Application

**Characteristics:** single deployable unit, shared database, internal module communication.

```markdown
# In ARCHITECTURE.md
## Module Structure
src/
├── api/           # HTTP handlers
├── services/      # Business logic
├── models/        # Data models
└── repository/    # Database access
```

**TECH_STACK.md focus:** single runtime, database, web framework.

---

### Microservices

**Characteristics:** multiple deployable units, service-to-service communication, possibly mixed languages.

```markdown
# In ARCHITECTURE.md
## Service Map
┌─────────────┐  ┌─────────────┐  ┌──────────────┐
│ API Gateway │──│ User Service│  │ Order Service│
└─────────────┘  └─────────────┘  └──────────────┘
                       │                │
                       ▼                ▼
               ┌─────────────┐  ┌─────────────┐
               │  User DB    │  │  Order DB   │
               └─────────────┘  └─────────────┘
```

**Separate Memory Banks option** for large systems:
```
services/
├── user-service/.cursor/     # service-specific memory
├── order-service/.cursor/
└── .cursor/                  # cross-service memory (architecture, roadmap)
```

One orchestrator per repository still applies; with a monorepo, one orchestrator per service directory.

---

### Frontend Application (React/Vue/Angular)

```markdown
# In ARCHITECTURE.md
## Component Structure
src/
├── components/       # Reusable UI components
├── pages/            # Route components
├── hooks/            # Custom hooks
├── store/            # State management
├── services/         # API clients
└── utils/            # Helpers
```

**TECH_STACK.md focus:** UI framework, state management, styling approach, build tool.
**§4.1:** logic layers (store, hooks, services) strict TDD; components behavior tests; **no full-page snapshots**.

---

### Data Pipeline / ETL

```markdown
# In ARCHITECTURE.md
## Pipeline Flow
Sources ──▶ Extract ──▶ Transform ──▶ Load ──▶ Warehouse
```

**TECH_STACK.md focus:** processing framework, storage, scheduler.
**Heavy workstreams:** backfills and full-pipeline runs are `heavy: true` — a subagent runs them and returns row counts and a verdict.

---

## Optional variants

### Python + pytest-bdd + Docker (the v1–v2 default testing protocol)

Use this instead of §4.1–4.5 if user stories in Gherkin are a hard requirement and tests run inside a
multi-stage Docker build.

**Definition of Done:** a task is not complete until it has a passing user story test, persisted in
`tests/features/` (never only in chat or the task log).

**Directory structure:**
```
tests/
├── conftest.py                    # project-wide pytest-bdd fixtures
└── features/                      # cross-service integration stories
<src>/*/tests/
├── conftest.py                    # service-specific fixtures
└── features/                      # service behavior stories
```

**Two-phase strategy:**

| Phase | When | Scope | Command | Gate |
| --- | --- | --- | --- | --- |
| Build-time | inside `docker build` stage 1 | unit + mocked Gherkin; no DB, network, or external services | `pytest <src>/*/tests/ -v --ignore=**/integration* -m "not slow"` | build fails |
| Runtime | `docker compose run` or CI after containers start | full integration + real assets | `docker compose run --rm <service> pytest tests/ -v -m integration` | deployment blocked |

**Markers:** `@unit` (build-time, mocked), `@integration` (runtime, needs services), `@browser`,
`@real_asset`, `@slow` / `@heavy` (decoupled: runtime phase, dedicated CI stage, or manual pre-release only).
Rationale: a 30-second build with mocked tests enables rapid feedback; a 5-minute build with heavy processing destroys it.

**TDD workflow:** discuss the scenario → write the `.feature` file with markers → implement step
definitions (failing) → write minimum code → run build-time then runtime tests → mark complete only after both pass.

```gherkin
@unit
Feature: [Feature Name]
  As a [role]
  I want [capability]
  So that [benefit]

  Scenario: [Scenario Name]
    Given [precondition]
    When [action]
    Then [expected result]
```

Boilerplate: `templates/tests/conftest.py` and `templates/tests/sample.feature`.

### Without an installable artifact

Libraries and services with no build a human installs: skip `pr-artifact-verify.mdc`, and drop the
"Test artifact" section from the closeout PR body. Keep "Manual verification" for staging smoke steps.

### Without a tracker MCP

Delete `.cursorrules` §1.7. The memory bank is the source of truth either way.

### POSIX shell machines

Replace the PowerShell items in `environment.mdc` with the bash/zsh block at the bottom of the template
(most of the file disappears). Keep "Verify the artifact under test".

---

## Customization Checklist

- [ ] Fill `.cursorrules` §02 and §03 for your stack; replace every `<placeholder>` gate command in §4.5
- [ ] Add build config and schema source paths to the protected-files table (§1.5)
- [ ] Copy `templates/cursor-rules/environment.template.mdc` → `.cursor/rules/environment.mdc` and prune to your shell
- [ ] Copy `orchestrator-ready-plans.template.mdc` → `.cursor/rules/`; `pr-artifact-verify.template.mdc` only if you ship an artifact
- [ ] Copy `templates/cursor-skills/orchestrate-epic/` → `.cursor/skills/`; replace `<Project Name>` in the dispatch prompt
- [ ] Copy `templates/docs/MODEL_ROUTING.md` → `docs/`; review ladders and prefix patterns against the live model list
- [ ] Copy `templates/cursor-prompts/*.md` → `.cursor/prompts/`
- [ ] Copy `templates/ci/ci.example.yml` → `.github/workflows/ci.yml`; fill the commands; leave it advisory until it has gone green once
- [ ] Set the capability `Tier` in `TECH_STACK.md` if the stack has optional layers (auth, sync, payments)
- [ ] Adjust directory structure in `ARCHITECTURE.md`
- [ ] Seed `LESSONS_LEARNED.md` with framework-specific gotchas you already know

---

## Sample `.cursorrules` §3.3 (Code Organization) for different stacks

### Python + FastAPI + PostgreSQL

```markdown
## 3.3 Code Organization
- `src/api/` FastAPI routes · `src/services/` business logic · `src/models/` SQLAlchemy models
- `tests/` test suite · `alembic/` migrations (protected — schema source)
```

### Node.js + Express + MongoDB

```markdown
## 3.3 Code Organization
- `src/routes/` Express routes · `src/controllers/` handlers · `src/models/` Mongoose models (protected — schema source)
- `tests/` test suite
```

### React + TypeScript + GraphQL

```markdown
## 3.3 Code Organization
- `src/components/` · `src/graphql/` queries and mutations · `src/hooks/` · `src/store/`
- Co-located `*.test.tsx`; cross-cutting tests in `tests/`
```

---

**END OF CUSTOMIZATION GUIDE**
