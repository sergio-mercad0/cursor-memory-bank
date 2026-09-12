# Orchestration Guide

How to execute a multi-workstream plan with a fleet of short-lived agents instead of one long chat,
without running the coordinating agent out of context.

This guide explains the concepts. The enforceable parts live in the templates:

| Concern | Template |
| --- | --- |
| Plan metadata contract | `templates/cursor-rules/orchestrator-ready-plans.template.mdc`, `templates/cursor-skills/orchestrate-epic/plan-template.md` |
| The execution loop | `templates/cursor-skills/orchestrate-epic/SKILL.md` |
| Model roles | `templates/docs/MODEL_ROUTING.md` |
| Starting / resuming an orchestrator | `templates/cursor-prompts/orchestrate.md`, `templates/cursor-prompts/handoff.md` |
| The rules the orchestrator must obey | `templates/.cursorrules` §1.3.1–§1.3.3 |

---

## 1. The problem this solves

A single agent driving a whole Epic accumulates every file it read, every test log, every subagent
reply, and every doc edit in one window. Nothing is evicted. Somewhere in the middle of the Epic it
either runs out of context or starts working from a degraded memory of the plan ("context rot").

The manual workaround is well known: plan in one chat, then for each workstream start a **fresh** chat,
paste the workstream, pick the right model, run it, repeat. It works. It is also tedious, and every
step is a place where a human forgets to record what happened.

Orchestration automates the loop, not the judgement.

---

## 2. Principles

### 2.1 The plan file is the job queue

The plan is not documentation that happens to have a todo list. It is the queue the executor
consumes. That is why each workstream carries machine-readable metadata:

- `phase` — which batch it belongs to
- `run_as` — whether a human gate stands in front of it
- `model_role` — which capability tier executes it
- `exit_gates` — how completion is verified
- `heavy` — whether its output is too large for the coordinator to ingest

If Plan mode writes the plan somewhere outside the repo, or strips fields it does not recognise, the
first step of execution is to copy it into `.cursor/plans/` and backfill.

### 2.2 One fresh agent per workstream; the parent only routes gates

The orchestrator (the "parent") never edits a file, never runs a build, never opens a PR. It reads
the queue, dispatches a fresh subagent per workstream, runs the exit gates, updates status, and stops
at human gates. Every piece of actual work happens in a subagent that starts with an empty window and
reads what it needs from disk.

This is the anti-context-rot guarantee: no subagent ever sees more than one workstream.

### 2.3 `run_as` routes the gate; `heavy` absorbs the tokens

These are two different questions and conflating them is the single most common failure:

- **Does a human need to approve something here?** → `run_as: parent`. The parent stops, asks, and
  relays the approval in the dispatch prompt. A subagent still does the work.
- **Will this step produce a wall of output?** → `heavy: true`. A throwaway subagent runs the build,
  reads the log or screenshot, and returns a verdict plus the few relevant lines.

A "rebuild the client and open the PR" workstream is both: the parent gets PR approval from the user,
then a subagent performs the build and returns `BUILD OK` + the PR URL. The parent never sees the build log.

The failure mode this prevents: treating "needs a human" as "parent does it", so the parent runs the
build inline, reads twenty screenshots, and exhausts its window on work that had no human in it.

### 2.4 Phases are context boundaries

A phase is a batch of workstreams that share an execution context and end at a human checkpoint.
Draw the boundary when:

| Trigger | Implication |
| --- | --- |
| WS A's output is consumed by WS B | Different phases |
| WS A and B share types, files, or design tokens | Same phase |
| A verifiable artifact exists (store, schema set, route shell) | Boundary candidate |
| A protected file or PR is touched | `run_as: parent` |

Workstreams are numbered `<phase>.<ordinal>`, and the ordinal resets per phase, so `WS 3.2` always
means "phase 3, second workstream" within an Epic.

**At every phase boundary the orchestrator chat ends — unconditionally.** It writes a handoff prompt,
and the next phase starts in a fresh chat. Because the durable state is on disk (plan todo statuses,
`TASK_LOG.md`, commits), nothing is lost. This one habit is the biggest lever against exhaustion;
making it conditional ("if the window feels full") is how it gets skipped.

### 2.5 Context economy in the parent

Even a well-behaved orchestrator accumulates. Rules that keep it lean:

1. **Dispatch by reference.** Point the subagent at the plan's WS section on disk. Do not paste the spec.
2. **Cap returns.** Subagents return at most ~8 lines: role + resolved model, files changed, gate
   results, blockers. No tables, no code unless a gate failed.
3. **Delegate the noise.** Builds, logs, screenshots, long test runs → throwaway subagent → verdict.
4. **Delegate unplanned scope too.** A bug found during verification is investigated by a fresh
   subagent that returns root cause + fix, not inline in the parent.
5. **Delegate bookkeeping.** The WS subagent flips its own todo and appends its own `TASK_LOG.md` line.
6. **Trust single-subagent gate reports.** Re-run the whole suite in the parent only to reconcile a
   parallel merge — and hand even that to a subagent.
7. **Keep `.cursorrules` lean.** It is re-sent every turn. Move runbooks and contracts to
   `.cursor/rules/*.mdc` with `alwaysApply: false`, to skills, or to `docs/`.

### 2.6 Route models by role

Plans name a role (`BUILDER`, `ARCHITECT`, `SCRIBE`, `DEEP`, `OPERATOR`, `BULK`), never a model slug.
The orchestrator resolves the role against the live model list at dispatch time and **records the
resolved slug** in `TASK_LOG.md`. Full logic: `templates/docs/MODEL_ROUTING.md`.

### 2.7 Relayed approval

Protected-file edits still need the user's approval — but the approval does not require the parent
to make the edit. The parent asks; the user approves; the dispatch prompt states "the user approved
editing `<file>` for this workstream"; the subagent edits. A subagent that needs a protected-file
edit without that sentence stops and reports.

---

## 3. The loop, in one screen

```
Preflight ── plan approved? feature branch? metadata present? no other orchestrator?
   │
   ▼
Select next pending WS in the active phase (lowest P.O)
   │
   ├─ run_as: parent ──▶ STOP, present gate, wait for approval, relay it
   │
   ▼
Dispatch ONE fresh subagent (role → resolved slug), prompt by reference
   │
   ▼
Run exit_gates ── red? one retry via resume ── still red? STOP and report
   │
   ▼
Status: todo → completed; TASK_LOG line "[WS id] ROLE → slug — outcome"
   │
   ▼
More WS in phase? ──yes──▶ loop
   │ no
   ▼
Phase exit gates ──▶ human checkpoint ──▶ write handoff prompt ──▶ NEW CHAT for next phase
```

---

## 4. Stop conditions

The orchestrator hands back to the user when:

- an exit gate stays red after one retry;
- a subagent needs a protected-file edit, ADR, or schema change without relayed approval;
- a `run_as: parent` gate is reached;
- a phase boundary is reached;
- a subagent's changes conflict with working-tree files it did not create.

It does **not** stop for unplanned in-scope work — it delegates that to a fresh subagent and resumes.

---

## 5. Hazards seen in practice

**Concurrent orchestrators on one clone.** Two Epics driven in parallel collided on migration
sequence numbers, on an Epic name in the roadmap backlog, on shared memory-bank files, and on an
untracked design doc that every dispatch prompt then had to say "is not yours". Rule: one active
orchestrator per repository; if parallel Epics are unavoidable, each plan declares the files it owns.

**Roadmap ✅ that never shipped.** A closeout that updated the roadmap but never pushed or opened the
PR left an Epic "done" in memory and absent on the remote. Closeout is not done until the remote has it.

**Stale artifact under test.** Hours were spent debugging behaviour that belonged to an old install.
Prove the running artifact is the one you built before trusting any device-side result.

**Todo marked complete, work not done.** A subagent interrupted mid-workstream left the todo flipped
and the working tree half-changed. Re-dispatch prompts had to say "there is partial work — do not wipe
it". Flip the todo last, after the gates.

**Plan mode fights the contract.** Cursor's Plan mode may write plans outside the repo and strip
custom frontmatter. Make "copy into `.cursor/plans/` and re-check metadata" the first preflight step.

**Skill and prompt contradict each other.** A skill that said "protected-file workstreams run in the
parent" was overridden per-plan with "the parent never does the work" for a month before the skill was
fixed. When a per-plan override recurs, it is the skill that is wrong.

---

## 6. Adopting this in an existing project

1. Copy `templates/cursor-rules/orchestrator-ready-plans.template.mdc` → `.cursor/rules/orchestrator-ready-plans.mdc`.
2. Copy `templates/cursor-skills/orchestrate-epic/` → `.cursor/skills/orchestrate-epic/`; replace `<Project Name>` in the dispatch prompt.
3. Copy `templates/docs/MODEL_ROUTING.md` → `docs/MODEL_ROUTING.md`; review the ladders and prefix table against your editor's current model list.
4. Copy `templates/cursor-prompts/*.md` → `.cursor/prompts/`.
5. Re-plan (or backfill) your current plan with the metadata contract.
6. Start an orchestrator chat from `.cursor/prompts/orchestrate.md`.
