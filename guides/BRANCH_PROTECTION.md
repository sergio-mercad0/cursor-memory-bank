# Branch Protection Guide

Feature branch workflow and naming conventions for safe, organized development.

---

## Overview

Branch protection ensures:
- No accidental commits to main/master
- Clear traceability from code to tasks
- Safe experimentation in isolated branches
- Clean git history with meaningful commits

---

## Branch Naming Conventions

### Format

```
<type>/<identifier>-<description>
```

### Types

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feat/` | New features | `feat/e2-user-authentication` |
| `fix/` | Bug fixes | `fix/issue-123-login-timeout` |
| `refactor/` | Code restructuring | `refactor/ws2.1-database-layer` |
| `docs/` | Documentation only | `docs/api-reference-update` |
| `test/` | Test additions/fixes | `test/integration-coverage` |
| `chore/` | Maintenance tasks | `chore/dependency-updates` |

### Identifier Patterns

Use one of these identifiers:

| Pattern | When to Use | Example |
|---------|-------------|---------|
| `e{N}` | Epic-level work | `feat/e3-reporting-dashboard` |
| `e{N}-ws{N.N}` | Workstream-level | `feat/e2-ws2.1-auth-flow` |
| `issue-{N}` | Issue tracker reference | `fix/issue-456-null-check` |
| Descriptive | Standalone work | `docs/readme-update` |

---

## Session Startup: Branch Check

At session start, verify the current branch:

```bash
git branch --show-current
git status
```

### Decision Tree

```
Current branch?
│
├── main OR master
│   └── WARN: "You are on the main branch"
│       └── Suggest: Create feature branch first
│
├── Feature branch (feat/, fix/, etc.)
│   └── Check for uncommitted changes
│       ├── Changes exist → List them, ask what to do
│       └── Clean → Safe to proceed
│
└── Unknown branch
    └── Ask user about the branch purpose
```

### Example Warning

```
⚠️ You are currently on the `main` branch.

Before making changes, I recommend creating a feature branch:
  git checkout -b feat/e2-ws2.1-<description>

Should I create a feature branch, or do you want to proceed on main?
```

---

## Creating Feature Branches

### Epic Kickoff (v3.0) — one Epic, one branch, one PR

`main` accepts changes **only through merged Pull Requests**. When starting a new Epic, always cut a
fresh branch from an up-to-date `main` before writing any code:

```bash
git switch main
git pull --ff-only origin main
git switch -c feat/epic-3-history-log
```

(The same three commands work in PowerShell; chain them with `;`, not `&&`.)

Rules:

- **Do not reuse a feature branch whose Epic PR has merged** — its history is closed. Follow-up fixes
  get their own branch from `main` (`fix/<slug>`).
- **Always branch off `main`**, not off another feature branch, so each Epic's PR diff is clean.
- **One active orchestrator per repository.** Two agents driving different Epics on the same clone
  collide on shared memory-bank files, sequential artifacts (migration numbers), and untracked files.
  If parallel Epics are unavoidable, each plan declares the files it owns.
- The Epic's closing PR is opened from this branch (see "Epic Closeout PR" below).

### Workstream-level branches (optional)

Within a large Epic you may branch per workstream and PR into the Epic branch:

```bash
git switch -c feat/e2-ws2.2-auth-ui
```

---

## Commit Message Conventions

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types (Conventional Commits)

| Type | Purpose |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring (no behavior change) |
| `docs` | Documentation only |
| `test` | Test additions/fixes |
| `chore` | Maintenance (deps, config) |
| `style` | Formatting (no code change) |
| `perf` | Performance improvement |

### Scope

Reference the epic/workstream when applicable:

```bash
git commit -m "feat(e2-ws2.1): add JWT token generation"
git commit -m "fix(auth): handle expired refresh tokens"
git commit -m "docs(readme): update installation steps"
```

### Examples

```bash
# Feature with plan reference
git commit -m "feat(e2-ws2.1): implement login endpoint

Plan: epic_2_auth_system.plan.md
Workstream: e2-ws2.1-login-api"

# Bug fix with issue reference
git commit -m "fix(api): handle null user in response

Fixes #123"

# Refactor with rationale
git commit -m "refactor(db): extract connection pooling

Centralizes database connection management for better
resource utilization. See ADR-015."
```

---

## Session Closeout: Git Workflow

When ending a session with changes:

### 1. Stage Changes

```bash
# Review changes
git status
git diff

# Stage all changes (or selectively)
git add -A
# or
git add <specific-files>
```

### 2. Commit with Context

```bash
git commit -m "<type>(<scope>): <description>

Session: 2024-01-15
Plan: <plan-file-if-applicable>
Progress: <brief progress note>"
```

### 3. Push to Remote (Required)

```bash
git push -u origin <branch-name>
```

Pushing is not optional at closeout. A roadmap ✅ with no pushed commit is the single most misleading
state the next agent can inherit: memory says "done", the remote says nothing happened. Closeout is
complete only when the remote has the work — and, at an Epic boundary, when the PR exists.

---

## Protected Branches

### Never Commit Directly To

| Branch | Policy |
|--------|--------|
| `main` | Requires PR and review |
| `master` | Requires PR and review |
| `production` | Requires PR and review |
| `release/*` | Requires PR and review |

### Agent Behavior

If on a protected branch:
1. **WARN** the user before any changes
2. **SUGGEST** creating a feature branch
3. **REQUIRE** explicit approval to proceed on protected branch

---

## Merge Workflow

### Feature Branch to Main

```bash
# Ensure feature branch is up to date
git checkout feat/e2-ws2.1-user-auth
git pull origin main
git rebase main  # or merge, per team preference

# Push and create PR
git push origin feat/e2-ws2.1-user-auth

# Create PR via CLI (if using GitHub)
gh pr create --title "feat(e2-ws2.1): User authentication" \
             --body "Implements login, logout, and token refresh."
```

### Epic Closeout PR (v3.0, mandatory)

The moment the last workstream of an Epic flips to ✅ in `PRODUCT_ROADMAP.md` and the closeout
commits are pushed, open the Epic's closing PR. Do not wait to be asked. No Epic is "done" until its
PR exists on the remote.

- **Source:** the Epic branch. **Target:** `main`.
- **Title:** `Epic N: <Epic Title>`.
- **Body** (sections required, in order):

```markdown
## Summary
- 2–4 bullets at user / architecture level (not a commit list)

## Workstreams completed
- [x] WS 1.1 <name>
- [x] WS 1.2 <name>
- [x] WS 2.1 <name>

## Decisions captured
- ADR-0NN <title> (DECISION_LOG.md)
- Lesson: <title> (LESSONS_LEARNED.md)

## Quality gates
- typecheck: pass | test: pass (N suites / M tests) | lint: pass | format:check: pass
- CI: <link to green run>

## Manual verification
- [ ] <smoke step that cannot be automated>

## Follow-ups
- <deferred item> → <where it is tracked>

## Test artifact   <!-- only if the project ships an installable/deployable artifact -->
- <link to the attached build> — verified on <target>; installed version <x> matches build <sha>
```

Write the body to a file and pass it, so multi-line text survives every shell:

```bash
gh pr create --base main --head feat/epic-3-history-log --title "Epic 3: History Log" --body-file .git/PR_BODY.md
```

If `gh` is unavailable, open `https://github.com/<owner>/<repo>/compare/main...<branch>?expand=1`
and ask the user to click "Create pull request".

If the project produces an installable artifact, the PR is not ready until the artifact is built,
attached, and verified on the target — see `templates/cursor-rules/pr-artifact-verify.template.mdc`.

### After Merge

```bash
# Update local main
git checkout main
git pull origin main

# Delete merged feature branch
git branch -d feat/e2-ws2.1-user-auth
git push origin --delete feat/e2-ws2.1-user-auth  # remote cleanup
```

---

## Handling Uncommitted Changes

When uncommitted changes are found at session start:

### Options

| Action | When to Use |
|--------|-------------|
| **Commit** | Changes are complete and tested |
| **Stash** | Changes are incomplete, need to switch context |
| **Discard** | Changes are experimental/unwanted |
| **Review** | Unsure what the changes are |

### Stash Workflow

```bash
# Save changes for later
git stash push -m "WIP: e2-ws2.1 login form"

# List stashes
git stash list

# Restore later
git stash pop
```

---

## Branch Cleanup

Periodically clean up merged branches:

```bash
# List merged branches
git branch --merged main

# Delete merged local branches
git branch -d <branch-name>

# Delete merged remote branches
git push origin --delete <branch-name>

# Prune remote tracking branches
git fetch --prune
```

---

## Best Practices

### DO

- ✅ Always check branch before making changes
- ✅ Use descriptive branch names with type prefix
- ✅ Reference epics/workstreams in branch names
- ✅ Write meaningful commit messages
- ✅ Commit frequently with atomic changes
- ✅ Push to remote regularly (backup)

### DON'T

- ❌ Commit directly to main/master
- ❌ Use vague branch names like `fix-stuff`
- ❌ Leave uncommitted changes across sessions
- ❌ Force push to shared branches
- ❌ Delete branches without merging (unless intentional)

---

## Quick Reference

```bash
# Check current state
git branch --show-current
git status

# Create feature branch
git checkout -b feat/e{N}-{description}

# Commit changes
git add -A
git commit -m "feat(scope): description"

# Push to remote
git push -u origin <branch-name>

# Session closeout (bash)
git add -A && git commit -m "chore: session closeout - <progress>" && git push

# Session closeout (PowerShell — `&&` is not a valid token)
git add -A; git commit -m "chore: session closeout - <progress>"; git push

# Epic closeout
gh pr create --base main --head <branch> --title "Epic N: <Title>" --body-file .git/PR_BODY.md
```

---

**Branches protect your work. Use them wisely.**
