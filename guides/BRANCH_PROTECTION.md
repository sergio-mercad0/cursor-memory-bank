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

### From Main

```bash
# Ensure main is up to date
git checkout main
git pull origin main

# Create feature branch
git checkout -b feat/e2-ws2.1-user-auth
```

### From Existing Branch

```bash
# Create branch from current HEAD
git checkout -b feat/e2-ws2.2-auth-ui
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

Plan: e2-ws2.1-auth-system.plan.md
Task: task-3 (Create login API)"

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

### 3. Push to Remote (Optional)

```bash
git push origin <branch-name>
```

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

# Session closeout
git add -A && git commit -m "chore: session closeout - <progress>"
```

---

**Branches protect your work. Use them wisely.**
