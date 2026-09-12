# Quick Start Guide

Get the Memory Bank running in your project in 10 minutes.

**Version:** 3.0

---

## Prerequisites

- A Cursor AI workspace
- An existing project (or starting a new one), on a feature branch
- `gh` (GitHub CLI) if you want the agent to open Pull Requests for you

---

## Option A: Automatic Initialization (Recommended)

### Step 1: Copy the Prompt

Open `prompts/initialize.md` and copy its entire contents.

### Step 2: Start a Chat

In Cursor, start a new chat session (Cmd/Ctrl + L). Pick a capable planning model — this is an
`ARCHITECT`-tier task (see `templates/docs/MODEL_ROUTING.md` §5).

### Step 3: Paste and Run

Paste the initialization prompt and press Enter.

### Step 4: Let the Agent Work

The agent will:
1. Analyze your codebase
2. Identify technologies and patterns
3. Create the `.cursor/` directory structure (memory, active_sprint, plans, rules, skills, prompts)
4. Populate context files
5. Propose a product roadmap

### Step 5: Approve the Roadmap

Review the proposed roadmap and approve it.

### Step 6: Add Rules to `.cursorrules`

Copy `templates/.cursorrules` into your project's `.cursorrules`, then:
- fill sections **02** and **03** for your stack (see `guides/CUSTOMIZATION.md`),
- replace every `<typecheck>` / `<test>` / `<lint>` / `<format:check>` placeholder in **§4.5** with real commands,
- add your build-config and schema-source paths to the protected-files table in **§1.5**.

### Step 7: Prune the environment rule

Open `.cursor/rules/environment.mdc` and delete the sections that do not apply to your machine
(PowerShell vs bash, line-ending setup). Keep it short — it is loaded every turn.

**Done!** Your Memory Bank is ready.

---

## Option B: Manual Setup

### Step 1: Create Directory Structure

```bash
# bash / zsh — from your project root
mkdir -p .cursor/memory .cursor/active_sprint .cursor/plans .cursor/rules .cursor/skills/orchestrate-epic .cursor/prompts docs
```

```powershell
# PowerShell
New-Item -ItemType Directory -Force .cursor/memory, .cursor/active_sprint, .cursor/plans, .cursor/rules, .cursor/skills/orchestrate-epic, .cursor/prompts, docs | Out-Null
```

### Step 2: Copy Templates

```bash
# bash / zsh
for f in PROJECT_BRIEF TECH_STACK ARCHITECTURE PRODUCT_ROADMAP LESSONS_LEARNED DECISION_LOG; do
  cp "templates/memory/$f.template.md" ".cursor/memory/$f.md"
done
cp templates/active_sprint/CURRENT_OBJECTIVE.template.md .cursor/active_sprint/CURRENT_OBJECTIVE.md
cp templates/active_sprint/TASK_LOG.template.md         .cursor/active_sprint/TASK_LOG.md
cp templates/cursor-readme.template.md                  .cursor/README.md

# v3.0 — execution layer
cp templates/cursor-rules/environment.template.mdc              .cursor/rules/environment.mdc
cp templates/cursor-rules/orchestrator-ready-plans.template.mdc .cursor/rules/orchestrator-ready-plans.mdc
cp templates/cursor-skills/orchestrate-epic/*                   .cursor/skills/orchestrate-epic/
cp templates/cursor-prompts/*.md                                .cursor/prompts/
cp templates/docs/MODEL_ROUTING.md                              docs/MODEL_ROUTING.md

# only if the project ships an installable artifact / has no CI yet
cp templates/cursor-rules/pr-artifact-verify.template.mdc .cursor/rules/pr-artifact-verify.mdc
mkdir -p .github/workflows && cp templates/ci/ci.example.yml .github/workflows/ci.yml
```

```powershell
# PowerShell
foreach ($f in 'PROJECT_BRIEF','TECH_STACK','ARCHITECTURE','PRODUCT_ROADMAP','LESSONS_LEARNED','DECISION_LOG') {
  Copy-Item "templates/memory/$f.template.md" ".cursor/memory/$f.md"
}
Copy-Item templates/active_sprint/CURRENT_OBJECTIVE.template.md .cursor/active_sprint/CURRENT_OBJECTIVE.md
Copy-Item templates/active_sprint/TASK_LOG.template.md         .cursor/active_sprint/TASK_LOG.md
Copy-Item templates/cursor-readme.template.md                  .cursor/README.md
Copy-Item templates/cursor-rules/environment.template.mdc              .cursor/rules/environment.mdc
Copy-Item templates/cursor-rules/orchestrator-ready-plans.template.mdc .cursor/rules/orchestrator-ready-plans.mdc
Copy-Item templates/cursor-skills/orchestrate-epic/*                   .cursor/skills/orchestrate-epic/
Copy-Item templates/cursor-prompts/*.md                                .cursor/prompts/
Copy-Item templates/docs/MODEL_ROUTING.md                              docs/MODEL_ROUTING.md
```

### Step 3: Fill in Content

Edit each file, replacing `<placeholders>` with your project's information:

1. **PROJECT_BRIEF.md** — mission and scope
2. **TECH_STACK.md** — technologies, and the capability **Tier** if the stack has optional layers
3. **ARCHITECTURE.md** — system design
4. **PRODUCT_ROADMAP.md** — planned work, as Epics → Phases → Workstreams
5. **DECISION_LOG.md** — at least 1–2 key decisions (adopting this protocol is `ADR-001`)
6. **LESSONS_LEARNED.md** — keep the seeded Process lessons that apply; add known gotchas
7. **docs/MODEL_ROUTING.md** — review the example ladders and prefix patterns against your editor's live model list
8. **.cursor/skills/orchestrate-epic/SKILL.md** — replace `<Project Name>` in the dispatch prompt
9. **.cursor/rules/environment.mdc** — prune to your shell

### Step 4: Add `.cursorrules`

```bash
cat templates/.cursorrules >> .cursorrules      # bash
```
```powershell
Get-Content templates/.cursorrules | Add-Content .cursorrules   # PowerShell
```

Then fill **§02 / §03**, replace the gate placeholders in **§4.5**, and extend the protected-files table in **§1.5**.

> The template uses a 4-pillar structure:
> - **00** — how the rules are layered (what goes in `.cursorrules` vs `.cursor/rules` vs skills vs docs)
> - **01_AGENT_PROTOCOL** — memory bank, startup, branch strategy, planning, orchestration, closeout, PRs
> - **02_INFRASTRUCTURE** / **03_DEVELOPMENT** — customize for your project
> - **04_QUALITY_ASSURANCE** — Scoped TDD and quality gates

### Step 5: (Optional) BDD testing variant

If you want Gherkin user stories and the two-phase Docker test gate from v1–v2, follow
"Python + pytest-bdd + Docker" in `guides/CUSTOMIZATION.md` and copy `templates/tests/`.

---

## Recommended Cursor settings

- **Auto-run commands**, with confirmation only for installing software and sending data off the machine.
  The protocol's own permission matrix (`.cursorrules` §1.5) handles everything else; prompting on every
  `git status` costs a turn each time.
- **Plan mode writes plan files under your user profile**, not in the repo, and may drop custom frontmatter
  fields. After approving a plan, copy it into `.cursor/plans/` and re-check the metadata — the orchestrator
  does this as its first preflight step, but it is worth knowing why.
- Keep **one orchestrator chat per repository** at a time.

---

## Verify It Works

### Start a New Session

Open a new Cursor chat and ask:

> "Based on the product roadmap, what should we work on next?"

### Expected Behavior

The agent should:
1. ✅ Check for active `.plan.md` files
2. ✅ Verify current git branch (and warn if on `main`)
3. ✅ Reference `PRODUCT_ROADMAP.md`
4. ✅ Identify the next pending workstream as `[Epic X > WS P.O]`
5. ✅ Propose a numbered plan
6. ✅ Wait for your approval

### Run your first orchestrated Epic

1. In Plan mode, plan the Epic. The `orchestrator-ready-plans` rule makes the agent emit `phase` /
   `run_as` / `model_role` / `exit_gates` per workstream.
2. Approve. Copy the plan into `.cursor/plans/` if it landed elsewhere.
3. Open a **fresh** chat, paste `.cursor/prompts/orchestrate.md` filled in for Phase 1.
4. At the phase boundary the orchestrator prints a handoff prompt. Start Phase 2 in another fresh chat.
5. When the last workstream is ✅, the agent opens `Epic N: <Title>` against `main`.

---

## First Session Checklist

- [ ] Agent checks for active plan files
- [ ] Agent verifies branch (warns if on main)
- [ ] Agent reads roadmap context
- [ ] Agent proposes plan before coding
- [ ] You approve or redirect the plan
- [ ] Workstreams are dispatched to fresh subagents; the parent only routes gates
- [ ] `TASK_LOG.md` gains one `[WS …] ROLE → slug — outcome` line per workstream
- [ ] Session ends with `CURRENT_OBJECTIVE.md` updated and the branch **pushed**

---

## Common Issues

### Agent Doesn't Read Memory Bank

**Cause:** `.cursorrules` not updated with Memory Bank protocol
**Fix:** Ensure the template from `templates/.cursorrules` is in your `.cursorrules`

### Agent Starts Coding Without Plan

**Fix:** "Please follow the startup protocol in .cursorrules Section 1.2"

### Agent Commits to Main Branch

**Fix:** "Please check the current branch and create a feature branch per .cursorrules §1.2.1"

### Orchestrator does the work itself / runs out of context

**Cause:** It treated `run_as: parent` as "parent does it", or ingested build logs and screenshots.
**Fix:** "Re-read the Context economy section of the orchestrate-epic skill. Delegate the noise, keep the gate." And cycle the chat at the phase boundary.

### Agent Ignores Active Plan File / metadata missing

**Cause:** Plan mode wrote the plan outside the repo or stripped custom fields
**Fix:** Copy it into `.cursor/plans/`; backfill from `.cursor/skills/orchestrate-epic/plan-template.md`

### The same shell command keeps failing

**Cause:** An environment quirk documented in prose instead of a rule
**Fix:** Add the concrete rule to `.cursor/rules/environment.mdc`

### A model slug "does not exist"

**Cause:** A plan or skill pinned a model version that was retired
**Fix:** Replace it with a `model_role`; see `docs/MODEL_ROUTING.md` "Legacy pins never fail"

---

## Next Steps

1. **Read the Guides:**
   - `guides/ORCHESTRATION.md` — plan-as-job-queue, phases, context economy (v3.0)
   - `guides/RETROSPECTIVE.md` — tune the protocol from your own transcripts (v3.0)
   - `guides/PLAN_CONTINUITY.md` — multi-session workflow
   - `guides/BRANCH_PROTECTION.md` — Epic branches and closeout PRs
   - `guides/FILE_BOUNDARIES.md` — access controls
   - `guides/DECISION_HEURISTIC.md` — know when to record what
   - `guides/CUSTOMIZATION.md` — adapt for your stack

2. **Create an Epic branch:**
   ```bash
   git switch main; git pull --ff-only origin main; git switch -c feat/epic-1-<slug>
   ```

3. **Record Your First Decision:** `ADR-001: Adopt cursor-memory-bank v3.0`

4. **Record Your First Lesson:** document a gotcha you've encountered

5. **Complete Your First Epic:** plan → orchestrate → closeout PR

---

## Version 3.0 Key Changes

| Feature | What Changed |
|---------|--------------|
| **Orchestrated execution** | Plans carry per-workstream metadata; a skill dispatches one fresh subagent per workstream |
| **Phase grouping** | `WS <phase>.<ordinal>` numbering; human checkpoint and fresh chat at every phase boundary |
| **Model routing by role** | Six roles resolved to live slugs at dispatch; resolved slug logged |
| **Branch strategy** | One Epic = one branch off fresh `main`; `main` is PR-only |
| **Epic closeout PR** | Mandatory, with a fixed body template; push is part of closeout |
| **Environment rules** | `.cursor/rules/environment.mdc` replaces prose reminders |
| **Scoped TDD** | Replaces the pytest-bdd/Docker default (now an optional variant) |
| **Protected files** | Now include `.cursorrules`, rules, skills, build config, schema sources; approval can be relayed to subagents |

See [CHANGELOG.md](CHANGELOG.md) for full details.

---

**You're ready to code with persistent memory — and a fleet of short-lived agents.**
