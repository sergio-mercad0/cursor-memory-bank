# Lessons Learned

**Last Updated:** <YYYY-MM-DD>  
**Purpose:** Technical patterns, gotchas, and operational wisdom discovered during development

---

## Development Patterns

### 1. <Pattern Name>

**Pattern:** <One-line description>

```python
# ✅ CORRECT - <Why this is right>
<correct code example>

# ❌ WRONG - <Why this is wrong>
<incorrect code example>
```

**Why:** <Explanation of why the correct pattern is important>

---

### 2. <Pattern Name>

**Pattern:** <One-line description>

```python
# ✅ CORRECT
<correct code example>

# ❌ WRONG
<incorrect code example>
```

**Why:** <Explanation>

---

### 3. <Pattern Name>

**Pattern:** <One-line description>

```python
# ✅ CORRECT
<correct code example>

# ❌ WRONG
<incorrect code example>
```

**Why:** <Explanation>

---

## Operational Gotchas

### 1. <Gotcha Title>

**Gotcha:** <Description of what can go wrong>

**Solution:** <How to avoid or fix it>

---

### 2. <Gotcha Title>

**Gotcha:** <Description of what can go wrong>

**Solution:** <How to avoid or fix it>

---

### 3. <Gotcha Title>

**Gotcha:** <Description of what can go wrong>

**Solution:** 
```bash
# Example fix or workaround
<command or code>
```

---

## Testing Patterns

### 1. <Testing Pattern Name>

**Pattern:** <Description>

```python
# ✅ CORRECT
<correct test pattern>

# ❌ WRONG
<incorrect test pattern>
```

---

### 2. <Testing Pattern Name>

**Pattern:** <Description>

```python
# Example
<test code example>
```

---

## Performance Insights

### 1. <Performance Topic>

**Insight:** <What was learned about performance>

**Pattern:** 
- <Recommendation 1>
- <Recommendation 2>
- <Recommendation 3>

---

### 2. <Performance Topic>

**Insight:** <What was learned about performance>

**Pattern:**
- <Recommendation 1>
- <Recommendation 2>

---

## Debugging Tips

### 1. <Debugging Scenario>

```bash
<useful debugging command>
```

### 2. <Debugging Scenario>

```bash
<useful debugging command>
```

### 3. <Debugging Scenario>

```bash
<useful debugging command>
```

---

## Process

<!--
Seeded from the project this framework's v3.0 was distilled from. Keep the ones that apply; every
one of them was learned the expensive way. Add your own workflow failures here with the measured
cause ("appeared in N of M sessions") — see guides/RETROSPECTIVE.md.
-->

### 1. Roadmap ✅ is not shipped

**Date:** <seed>
**Problem:** An Epic was marked complete in `PRODUCT_ROADMAP.md`, `TASK_LOG.md` and `CURRENT_OBJECTIVE.md` were closed out, and the next agent found no commit on the remote and no PR. The work sat in an unpushed local branch for weeks.
**Root Cause:** Closeout updated memory before pushing; the protocol treated `git push` and the PR as optional.
**Solution:** `.cursorrules` §1.4 makes push part of the commit step and §1.4.1 makes the Epic PR mandatory the instant the last workstream flips.
**Prevention:** Verify "done" against `git log origin/<branch>` and the PR list, never against the memory bank alone.

---

### 2. Prove the installed artifact is the one you built

**Date:** <seed>
**Problem:** Hours were spent debugging behaviour on a device that belonged to a stale install; a fix "did not work" because the new build was never the one running.
**Root Cause:** Hot-reload caches and leftover installs; nobody checked the version string or hash before trusting the device.
**Solution:** Every device/emulator/staging verification first confirms version or hash matches the build (`.cursor/rules/pr-artifact-verify.mdc`).
**Prevention:** A device-side FAIL is not evidence until the artifact identity is confirmed.

---

### 3. A pinned model slug is a time bomb

**Date:** <seed>
**Problem:** Plan files and the orchestration skill named specific model versions. Within two months four of them were retired and were still being dispatched — silently falling back or failing.
**Root Cause:** Model lineups turn over every few weeks; plan files and skills are durable.
**Solution:** Route by **role** (`docs/MODEL_ROUTING.md`), resolve to a live slug at dispatch time, and log the resolved slug in `TASK_LOG.md`.
**Prevention:** Never write a model version into anything under `.cursor/`. A slug table that lived in four files drifted in all four.

---

### 4. Concurrent orchestrators collide

**Date:** <seed>
**Problem:** Two Epics driven in parallel on one clone produced two migrations with the same sequence number, a duplicated Epic name in the roadmap backlog, and an untracked design doc that every dispatch prompt had to say "is not yours".
**Root Cause:** Shared memory-bank files and sequential artifacts have no owner.
**Solution:** One active orchestrator per repository (`.cursorrules` §1.2.1); a CI check for migration-number collisions.
**Prevention:** If parallel Epics are unavoidable, each plan declares the files it owns.

---

### 5. CI caught what self-reported gates missed

**Date:** <seed>
**Problem:** Eighteen PRs merged with "typecheck + test + lint green" in the body — every one a local run self-reported by an agent on a dirty checkout. The first CI run on a clean runner failed on a lockfile inconsistency that had been invisible across all of them.
**Root Cause:** No automated verification; the memory bank recorded claims, not evidence.
**Solution:** `.github/workflows/ci.yml` (from `templates/ci/ci.example.yml`), advisory first, then required.
**Prevention:** Treat local gate output as advisory. The PR body's "Quality gates" section links the CI run.

---

### 6. Keep `.cursorrules` lean; a rule file is re-sent every turn

**Date:** <seed>
**Problem:** The orchestrator nearly exhausted its window on a plan whose steps were individually cheap.
**Root Cause:** A ~400-line `.cursorrules` was part of every turn's fixed overhead, on top of verbose subagent returns and inline build logs.
**Solution:** Hard rules stay in `.cursorrules`; contracts and runbooks moved to `.cursor/rules/*.mdc` (`alwaysApply: false`), skills, and `docs/`; subagent returns capped at 8 lines (`.cursorrules` §00, §1.3.2).
**Prevention:** Before adding a paragraph to `.cursorrules`, ask which of the six locations in §00 it belongs in.

---

## Lesson Record Format

When adding new lessons, use this format:

```markdown
## [Category]: [Title]
**Date:** YYYY-MM-DD
**Problem:** What went wrong or was confusing?
**Root Cause:** Why did it happen?
**Solution:** How was it fixed?
**Prevention:** How to avoid this in future?
```

**Categories:**
- Development Patterns
- Operational Gotchas
- Testing Patterns
- Performance Insights
- Debugging Tips
- Process (workflow failures — closeout, verification, orchestration, environment)

---

**END OF LESSONS LEARNED**

