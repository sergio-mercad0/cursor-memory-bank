# Changelog

All notable changes to the Cursor Memory Bank framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] - 2026-09-11

### Overview

Execution-layer release. v2.0 made the memory bank survive across sessions; v3.0 makes a multi-phase
Epic survivable *within* a project by running it as a fleet of short-lived agents coordinated by a
context-lean orchestrator. Every addition was distilled from one production project (~80 agent
sessions over 3½ months) and traces to a measured failure; the method is documented in
`guides/RETROSPECTIVE.md`.

### Gap Analysis Summary

| Aspect | v2.0 | v3.0 |
|--------|------|------|
| **Plan file** | Documentation with a todo list | Job queue: per-workstream `phase` / `run_as` / `model_role` / `exit_gates` / `heavy` |
| **Execution** | One chat does the work | `orchestrate-epic` skill: one fresh subagent per workstream; parent routes gates only |
| **Phases** | Generic 3-phase build gates | `WS <phase>.<ordinal>`; human checkpoint + fresh chat at every boundary |
| **Model selection** | Not mentioned | Six roles resolved to live slugs at dispatch; resolved slug logged (`docs/MODEL_ROUTING.md`) |
| **Branch strategy** | Warn if on main | One Epic = one branch off fresh `main`; `main` PR-only; one orchestrator per repo |
| **PRs** | One-line `gh pr create` example | Mandatory Epic closeout PR with fixed body template; push is part of closeout |
| **Environment** | Not mentioned | `.cursor/rules/environment.mdc` (always applied) replaces prose reminders |
| **Artifacts** | Not mentioned | Build → attach → verify on target → prove the installed artifact matches |
| **Protected files** | 5 memory files | + `.cursorrules`, `.cursor/rules`, `.cursor/skills`, build config, schema sources; approval relayable to subagents |
| **Testing** | pytest-bdd + Docker two-phase | Stack-agnostic Scoped TDD; BDD kept as an optional variant |
| **Rules layout** | Everything in `.cursorrules` | §00 layering: `.cursorrules` / rules / skills / docs, by per-turn cost |
| **CI** | Not mentioned | `templates/ci/ci.example.yml`; advisory first, required after one green run |
| **Todo IDs** | Three conflicting formats across files | One: `e{epic}-ws{phase}.{ordinal}-{shortname}` |

### Added

#### Orchestrated execution
- `templates/cursor-skills/orchestrate-epic/SKILL.md` — the dispatcher: preflight, model routing,
  context economy ("delegate the noise, keep the gate"), orchestration loop, dispatch prompt with a
  ≤8-line return contract, stop conditions, context hygiene.
- `templates/cursor-skills/orchestrate-epic/plan-template.md` — the workstream metadata contract.
- `templates/cursor-rules/orchestrator-ready-plans.template.mdc` — makes Plan mode emit the contract.
- `templates/cursor-prompts/orchestrate.md`, `handoff.md` — bootstrap and phase-boundary prompts.
- `.cursorrules` §1.3 rewritten: orchestratable plan structure, §1.3.1 Phase grouping, §1.3.2
  Orchestrated execution, §1.3.3 Model routing by role.
- `guides/ORCHESTRATION.md`.

#### Model routing by role
- `templates/docs/MODEL_ROUTING.md` — why roles not slugs; six roles with example ladders; resolution
  procedure (prefix match → highest numeric version → effort tiebreak → advance ladder → `inherit`);
  legacy-pin fallback; cost-of-being-wrong selection rule; never-do list; human-side picker guidance.

#### Branch, closeout, PR
- `.cursorrules` §1.2.1 Branch Strategy (Epic Kickoff); §1.4 push required at closeout; §1.4.1 Epic
  Closeout PR (mandatory) with body sections and "prove the artifact".
- `templates/cursor-rules/pr-artifact-verify.template.mdc`.
- `guides/BRANCH_PROTECTION.md` — Epic kickoff, closeout PR template, PowerShell variants.

#### Environment and layering
- `templates/cursor-rules/environment.template.mdc` — chaining, heredocs, redirection, search tools,
  output hygiene, line endings, artifact verification; PowerShell example + POSIX note.
- `.cursorrules` §00 (rules layering) and §1.6 (environment conventions pointer).
- `.gitattributes` (`* text=auto eol=lf`).

#### Quality
- `.cursorrules` §04 replaced with Scoped TDD (§4.1), forbidden test patterns (§4.2), test locations
  (§4.3), definition of done (§4.4), quality gates with placeholders (§4.5).
- `templates/ci/ci.example.yml`.

#### Memory bank
- `LESSONS_LEARNED.template.md` — new **Process** category seeded with six generic lessons.
- `TASK_LOG.template.md` — `[WS <id>] <role> → <resolved slug> — <outcome>` line format.
- `PRODUCT_ROADMAP.template.md` — Branch / Plan / PR fields per Epic; nested Phase → Workstream.
- `TECH_STACK.template.md` — optional capability **Tier**.
- `CURRENT_OBJECTIVE.template.md` — Branch / Plan / Phase fields.
- `.cursorrules` §1.7 External Tracker Mirror (optional).
- `guides/RETROSPECTIVE.md`.

### Changed

- `templates/.cursorrules` — protected-files table and permissions matrix expanded; relayed approval;
  cascade rule for schema; §02/§03 stubs now suggest CI, pre-commit hooks, runbooks, schema cascade.
- `templates/cursor-readme.template.md`, `prompts/initialize.md` — brought from v1-era content to v3
  (plans/rules/skills/prompts, branch check, phase-numbered todos, adoption ADR).
- `guides/PLAN_CONTINUITY.md` — unified ID format, metadata fields, Plan-mode gotcha, phase-boundary handoff.
- `guides/FILE_BOUNDARIES.md` — new protected rows, plans, subagent dispatch, PR and install rows.
- `guides/CUSTOMIZATION.md` — rewritten for the 4-pillar section names; TypeScript/mobile variant
  added; pytest-bdd/Docker two-phase protocol moved here as an optional variant.
- `guides/DECISION_HEURISTIC.md` — process decisions are ADRs; workflow failures are lessons.
- `README.md`, `QUICKSTART.md` — v3.0; PowerShell equivalents for every setup command.

### Removed

- Root `.gitkeep` (leftover from the initial export).

### Migration from v2.0

1. Replace `.cursorrules` §01 and §04 with the v3 template sections (keep your §02/§03). Fill the
   `<gate>` placeholders in §4.5; add your build-config and schema paths to §1.5.
2. Add `.cursor/rules/environment.mdc` (prune to your shell) and `orchestrator-ready-plans.mdc`.
3. Add `.cursor/skills/orchestrate-epic/`, `.cursor/prompts/`, and `docs/MODEL_ROUTING.md` (review the
   example ladders against your live model list).
4. Existing plans keep working; backfill `phase` / `run_as` / `model_role` / `exit_gates` before
   orchestrating them. Any pinned `model:` slugs resolve via the legacy-pin fallback.
5. Existing `.cursor/memory/` files are compatible. Optionally add the **Process** lessons and the
   `Tier` field.
6. If you used the pytest-bdd/Docker testing protocol, keep it — it now lives in `guides/CUSTOMIZATION.md`.

---

## [2.0.0] - 2026-04-19

### Overview

Major framework upgrade based on reconciliation with production-evolved patterns. This release introduces a 4-pillar template structure, enhanced session continuity, and stronger guardrails for multi-agent workflows.

### Gap Analysis Summary

This release bridges the gap between the original v1.0 framework and production-evolved patterns:

| Aspect | v1.0 | v2.0 |
|--------|------|------|
| **Structure** | Sections 9-11 append style (~306 lines) | 4-pillar layout (~800 lines) |
| **Plan Continuity** | Not mentioned | Section 1.2 - MUST follow `.plan.md` files |
| **Branch Protection** | Not mentioned | Section 1.2 - MUST check branch before coding |
| **Mode Switching** | Brief mention in §11 | Detailed trigger: ">2 files or architectural changes" |
| **Build Gates** | Not mentioned | Incremental checkpoints per phase |
| **Session Closeout** | Brief handoff | Detailed with git commit workflow |
| **Handoff Verification** | Not mentioned | Checklist before marking tasks complete |
| **PRODUCT_ROADMAP.md** | No approval required | Approval required for scope changes |
| **Tool Permissions** | Not present | Detailed permission matrix |
| **`.cursor/plans/`** | Optional mention | Explicit in workflow |

### Added

#### 4-Pillar Template Structure
The `.cursorrules` template now uses a cleaner, modular structure:
- **01_AGENT_PROTOCOL** - Memory bank, startup, planning, closeout
- **02_INFRASTRUCTURE** - Project-specific (stub for customization)
- **03_DEVELOPMENT** - Code standards, error handling (stub for customization)
- **04_QUALITY_ASSURANCE** - Testing protocol

#### Plan File Continuity Protocol (Section 1.2)
- Agents MUST check for existing `.plan.md` files at session start
- Plan files serve as authoritative source during multi-session work
- Todo status markers persist across sessions

#### Branch Protection Rules (Section 1.2)
- Agents MUST verify current branch before making changes
- Feature branch naming conventions: `feat/`, `fix/`, `refactor/`, `docs/`
- Protection against unintended commits to main/master

#### Mode Switching Heuristic (Section 1.3)
- Clear trigger: "When task touches >2 files OR involves architectural changes"
- Explicit guidance on when to enter Planning Mode vs stay in Agent Mode
- Plan file structure with todo ID conventions

#### Incremental Build Gates (Section 1.3)
- Phased approach: Dependency → Implementation → Integration
- Quality gates checklist before phase transitions
- Prevents large PRs and ensures incremental progress

#### Session Closeout Protocol (Section 1.4)
- Detailed closeout triggers (context limit, task completion, pivot)
- Git commit workflow integrated into closeout
- Agent handoff verification checklist

#### PRODUCT_ROADMAP.md Approval Required
- Added to protected files list when scope changes
- Prevents unintended roadmap drift

#### Tool Permissions Matrix
- Explicit read/write/execute permissions
- File-by-file access control documentation

### New Guides

- **`guides/PLAN_CONTINUITY.md`** - How to use `.plan.md` files across sessions
- **`guides/BRANCH_PROTECTION.md`** - Feature branch workflow and naming conventions

### Changed

- **`guides/FILE_BOUNDARIES.md`** - Added PRODUCT_ROADMAP.md approval requirement and tool permissions table
- **`README.md`** - Updated for 4-pillar structure, added v2.0 notes
- **`QUICKSTART.md`** - Updated to match new template layout

### Migration from v1.0

1. **Template Update**: Replace your existing `.cursorrules` with the new 4-pillar template
2. **Review Guides**: Read the new PLAN_CONTINUITY and BRANCH_PROTECTION guides
3. **No Data Migration**: Your existing `.cursor/memory/` files remain compatible

---

## [1.0.0] - Initial Release

### Added

- Initial Memory Bank framework
- `.cursor/` directory structure
- Memory bank protocol (Section 9)
- User story testing protocol (Section 10)
- Planning mode protocol (Section 11)
- Template files for memory bank initialization
- Guides for file boundaries, decision heuristics, customization
- Initialization prompt for bootstrapping new projects
