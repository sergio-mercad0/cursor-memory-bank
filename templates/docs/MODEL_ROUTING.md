# Model Routing Guide

**Status:** Single source of truth for model routing. `.cursor/skills/orchestrate-epic/SKILL.md`,
`.cursor/skills/orchestrate-epic/plan-template.md`, and `.cursor/rules/orchestrator-ready-plans.mdc`
all point here and must not restate the tables below.
**Audience:** Whoever is driving the next Epic — human or orchestrator.

<!--
Copy to docs/MODEL_ROUTING.md. The ROLES in §2 are stable. The FAMILY LADDERS and PREFIX PATTERNS
are examples that reflect one point in time — review them against your editor's current model list
when you adopt this file, and again whenever the lineup changes. Never add a table of concrete
model slugs anywhere; that is exactly what this file exists to prevent.
-->

---

## 1. Why this file names roles, not models

Model lineups turn over every few weeks. In the project this guide came from, four slugs that were
valid when the orchestration skill was written were retired within two months — and were still being
dispatched from plan files long after, because a plan file is durable and a slug is not. A pinned
slug is a time bomb.

The subagent-dispatch tool accepts **only exact slugs** from an enumerated list — an alias like
`<vendor>-latest` will not dispatch — and there is no locally cached model list to look one up from.
The only component that can see the live list is the orchestrating agent itself, in its own tool description.

So routing is expressed as a **role**, which never changes, plus a **family ladder** the orchestrator
resolves against the live list at dispatch time. Plans name the role. Nothing durable names a version.

---

## 2. The six roles

| Role | Use for | Family ladder (first available wins) — EXAMPLE, review on adoption |
| --- | --- | --- |
| `BUILDER` | Stores, hooks, queries, components, tests, wiring — **the default** | Editor-native fast model → editor-pool reasoning model → mid-tier third-party |
| `ARCHITECT` | Epic planning, architecture, ADR drafting, code review | Editor-pool reasoning model → top-tier third-party → high-tier third-party |
| `SCRIBE` | Docs, roadmap prose, PR bodies, memory-bank updates | Editor-pool reasoning model → cheapest third-party → editor-native fast model |
| `DEEP` | Subtle correctness: timing, persistence/rehydration, transactions, schema cascade | Top-tier third-party → its mid-tier sibling → editor-pool reasoning model |
| `OPERATOR` | Terminal, native builds, devices/emulators, CI debugging | High-tier third-party → editor-pool reasoning model → editor-native fast model |
| `BULK` | High-volume mechanical passes (renames, token sweeps, scaffolds) | Cheapest third-party → editor-native fast model |

`BUILDER` is the default. When a workstream omits `model_role`, infer it from the task type using the "Use for" column.

---

## 3. Resolution procedure

The orchestrator runs this once per dispatch:

1. **Read the live list.** The subagent tool's description enumerates every accepted model slug.
   That list is authoritative — never a table in a file, including this one.
2. **Match the role's first family by prefix**, not by exact string. Maintain the prefix table for
   your editor here (example shape):

   | Family | Prefix pattern (EXAMPLE) |
   | --- | --- |
   | Editor-native fast | `<editor>-*` |
   | Editor-pool reasoning | `<editor>-<vendor>-*` |
   | Top-tier third-party | `<vendor>-<flagship>-*` |
   | Mid-tier third-party | `<vendor>-<mid>-*` |
   | High-tier third-party | `<vendor2>-*-<high-variant>*` |
   | Cheapest third-party | `<vendor2>-*-<cheap-variant>*` |

3. **Pick the highest version** within that family. Compare the numeric version, not the string
   (`4.10` beats `4.9`). Tie-break on effort suffix, most capable first (e.g. `-thinking-high` →
   `-high-fast` → `-high` → `-medium` → bare).
4. **Family absent → advance the ladder.** If every family in the ladder is missing, fall back to
   `inherit` and say so explicitly in the dispatch note. Never hard-fail, and never invent a slug.
5. **Record the resolved slug** alongside the role in `.cursor/active_sprint/TASK_LOG.md`:
   `[WS <id>] <role> → <resolved slug> — <outcome>`.

Step 5 exists because chat history preserves which model a prompt _requested_ and never which one
_executed_ — a routing policy with no feedback loop cannot be tuned.

### Legacy pins never fail

Plan files written before this convention may carry `model: <slug>` directly. If that slug is not in
the live list, **map it to a role and resolve normally** rather than erroring:

| Retired slug pattern | Role |
| --- | --- |
| Anything from the top-tier or mid-tier third-party families | `DEEP` |
| Anything from the cheap third-party family | `SCRIBE` |
| Anything else unrecognized | `BUILDER` |

A pinned `model:` that _does_ resolve is still honoured — it is a deliberate override, not a mistake.

---

## 4. The selection rule

> **Pick on cost-of-being-wrong, not on task difficulty.**
> If a failing gate catches the mistake in under a minute → cheap and fast.
> If the mistake ships silently, corrupts data, or forces a migration → expensive and careful.

Two modifiers:

- **Prefer the included-usage pool** when quality is comparable. Editor-pool models typically have
  generous included usage; third-party models draw down a hard monthly allowance. This is why
  `ARCHITECT` and `SCRIBE` lead with an editor-pool model rather than a flagship.
- **Escalate only after a failure.** `BUILDER` → `ARCHITECT` → `DEEP` is roughly a 2x cost jump per
  rung. Do not pre-emptively skip to the top.

Under a strict red-green test discipline, a gate catches most errors in seconds. Reserve `DEEP` for
what tests _cannot_ catch: clock drift, state after process death, transaction atomicity, schema cascade.

### Never do this

- Never route planning or architecture to `BUILDER` — fast models optimize for speed over exploring alternatives.
- Never leave a `DEEP`-tier model on boilerplate, doc edits, or roadmap ticks.
- Never use an "Auto" model setting for orchestration. A failed workstream needs reproducible model identity.
- Never select a "fast"/priority mode by default for background subagents. It multiplies the token rate for latency nobody is waiting on.

---

## 5. Role selection in one screen

| Signal in the request | Role |
| --- | --- |
| "add a component / hook / query, with tests" | `BUILDER` |
| "plan Epic N" / "should we use X or Y?" | `ARCHITECT` |
| "review this diff before I merge" | `ARCHITECT` |
| "update the roadmap / write the PR body" | `SCRIBE` |
| "why does state drift after backgrounding / restart?" | `DEEP` |
| "add a column / change the schema" | `DEEP` |
| "the build fails with…" | `OPERATOR` |
| "rename this across 40 files" | `BULK` |

### For the human at the chat model picker

The roles apply to your own chat sessions too:

| Session type | Pick |
| --- | --- |
| Plan mode for an Epic | an `ARCHITECT`-tier model — alternatives matter more than speed |
| Orchestrator chat | a cheap model — the parent only routes gates; subagents carry the roles |
| One-off deep bug hunt | a `DEEP`-tier model, in a fresh chat, with the lesson recorded at the end |
| Doc / roadmap edits | a `SCRIBE`-tier model |

---

## 6. Maintenance

Roles in §2 are version-free and should need no upkeep. The two things that do:

- **§3 prefix table** — when a provider introduces a new naming scheme, add the pattern.
- **§2 ladders and §4 pool membership** — re-check when the editor announces a lineup or pricing change.

Do not reintroduce a slug table anywhere. In the source project one lived in four files and drifted
silently in all of them.

---

**END OF MODEL ROUTING GUIDE**
