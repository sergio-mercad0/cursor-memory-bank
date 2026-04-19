# Quick Start Guide

Get the Memory Bank running in your project in 5 minutes.

**Version:** 2.0

---

## Prerequisites

- A Cursor AI workspace
- An existing project (or starting a new one)

---

## Option A: Automatic Initialization (Recommended)

### Step 1: Copy the Prompt

Open `prompts/initialize.md` and copy its entire contents.

### Step 2: Start a Chat

In Cursor, start a new chat session (Cmd/Ctrl + L).

### Step 3: Paste and Run

Paste the initialization prompt and press Enter.

### Step 4: Let the Agent Work

The agent will:
1. Analyze your codebase
2. Identify technologies and patterns
3. Create the `.cursor/` directory structure
4. Populate context files
5. Propose a product roadmap

### Step 5: Approve the Roadmap

Review the proposed roadmap and approve it.

### Step 6: Add Rules to .cursorrules

Copy the contents of `templates/.cursorrules` into your project's `.cursorrules` file.

> **Note (v2.0):** The template now uses a 4-pillar structure. You can customize sections 02 (Infrastructure) and 03 (Development) for your project's specific needs.

**Done!** Your Memory Bank is ready.

---

## Option B: Manual Setup

### Step 1: Create Directory Structure

```bash
# From your project root
mkdir -p .cursor/memory
mkdir -p .cursor/active_sprint
mkdir -p .cursor/plans          # New in v2.0
```

### Step 2: Copy Templates

```bash
# Copy and rename templates
cp templates/memory/PROJECT_BRIEF.template.md .cursor/memory/PROJECT_BRIEF.md
cp templates/memory/TECH_STACK.template.md .cursor/memory/TECH_STACK.md
cp templates/memory/ARCHITECTURE.template.md .cursor/memory/ARCHITECTURE.md
cp templates/memory/PRODUCT_ROADMAP.template.md .cursor/memory/PRODUCT_ROADMAP.md
cp templates/memory/LESSONS_LEARNED.template.md .cursor/memory/LESSONS_LEARNED.md
cp templates/memory/DECISION_LOG.template.md .cursor/memory/DECISION_LOG.md

cp templates/active_sprint/CURRENT_OBJECTIVE.template.md .cursor/active_sprint/CURRENT_OBJECTIVE.md
cp templates/active_sprint/TASK_LOG.template.md .cursor/active_sprint/TASK_LOG.md

cp templates/cursor-readme.template.md .cursor/README.md
```

### Step 3: Fill in Content

Edit each file, replacing `<placeholders>` with your project's information:

1. **PROJECT_BRIEF.md** - Your project's mission and scope
2. **TECH_STACK.md** - Technologies you're using
3. **ARCHITECTURE.md** - Your system design
4. **PRODUCT_ROADMAP.md** - Your planned work
5. **DECISION_LOG.md** - At least 1-2 key decisions
6. **LESSONS_LEARNED.md** - Any known patterns/gotchas

### Step 4: Add .cursorrules

Copy the Memory Bank protocols to your `.cursorrules`:

```bash
cat templates/.cursorrules >> .cursorrules
```

> **Note (v2.0):** The template uses a 4-pillar structure:
> - **01_AGENT_PROTOCOL** - Memory bank, startup, planning, closeout
> - **02_INFRASTRUCTURE** - Customize for your project
> - **03_DEVELOPMENT** - Customize for your project
> - **04_QUALITY_ASSURANCE** - Testing protocol

### Step 5: (Optional) Set Up Testing

```bash
mkdir -p tests/features
cp templates/tests/conftest.py tests/
cp templates/tests/sample.feature tests/features/

# Add pytest-bdd to your dependencies
echo "pytest-bdd>=7.0.0" >> requirements.txt  # Python
# or add to package.json for Node.js
```

---

## Verify It Works

### Start a New Session

Open a new Cursor chat and ask:

> "Based on the product roadmap, what should we work on next?"

### Expected Behavior (v2.0)

The agent should:
1. ✅ Check for active `.plan.md` files
2. ✅ Verify current git branch
3. ✅ Reference PRODUCT_ROADMAP.md
4. ✅ Identify the next pending task
5. ✅ Propose a numbered plan
6. ✅ Wait for your approval

If this happens, your Memory Bank is working!

---

## First Session Checklist

- [ ] Agent checks for active plan files
- [ ] Agent verifies branch (warns if on main)
- [ ] Agent reads roadmap context
- [ ] Agent proposes plan before coding
- [ ] You approve or redirect the plan
- [ ] Agent updates TASK_LOG.md during work
- [ ] Agent marks completed tasks in roadmap
- [ ] Session ends with CURRENT_OBJECTIVE.md updated

---

## Common Issues

### Agent Doesn't Read Memory Bank

**Cause:** .cursorrules not updated with Memory Bank protocol

**Fix:** Ensure the 4-pillar template from `templates/.cursorrules` is in your `.cursorrules`

### Agent Starts Coding Without Plan

**Cause:** Protocol not enforced

**Fix:** Remind the agent: "Please follow the startup protocol in .cursorrules Section 1.2"

### Agent Commits to Main Branch

**Cause:** Branch protection not followed

**Fix:** Remind the agent: "Please check the current branch and create a feature branch"

### Files Not Created

**Cause:** Permissions or directory doesn't exist

**Fix:** Manually create directories and set permissions

### Agent Ignores Active Plan File

**Cause:** Plan file not in `.cursor/plans/`

**Fix:** Move plan file to `.cursor/plans/` directory

---

## Next Steps

1. **Read the Guides:**
   - `guides/FILE_BOUNDARIES.md` - Understand access controls
   - `guides/PLAN_CONTINUITY.md` - Multi-session workflow (v2.0)
   - `guides/BRANCH_PROTECTION.md` - Branch naming and safety (v2.0)
   - `guides/DECISION_HEURISTIC.md` - Know when to record what
   - `guides/CUSTOMIZATION.md` - Adapt for your stack

2. **Create a Feature Branch:**
   ```bash
   git checkout -b feat/e1-<your-first-feature>
   ```

3. **Record Your First Decision:**
   Add an ADR for a recent architectural choice

4. **Record Your First Lesson:**
   Document a gotcha you've encountered

5. **Complete Your First Task:**
   Pick a task from the roadmap and complete the full workflow

---

## Version 2.0 Key Changes

| Feature | What Changed |
|---------|--------------|
| **Template Structure** | Now uses 4-pillar layout instead of Sections 9-11 |
| **Plan Continuity** | Agent checks `.cursor/plans/` for active plans |
| **Branch Protection** | Agent verifies branch before making changes |
| **PRODUCT_ROADMAP.md** | Now requires approval for scope changes |
| **Session Closeout** | Includes git commit workflow |
| **Tool Permissions** | Explicit matrix of what requires approval |

See [CHANGELOG.md](CHANGELOG.md) for full details.

---

**You're ready to code with persistent memory!**
