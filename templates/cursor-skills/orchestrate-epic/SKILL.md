---
name: orchestrate-epic
description: Execute an approved .cursor/plans/*.plan.md Epic by dispatching one fresh subagent per workstream, resolving the model per role, running exit gates between phases, and updating plan/memory status. Use after Plan mode when the user says "orchestrate", "execute the plan", "run Epic N", or wants per-workstream agents spun up automatically instead of manually.
disable-model-invocation: true
---

# Orchestrate Epic

Turn an approved plan file into an automated execution loop. The plan is the job queue; this skill is
the dispatcher. It replaces the manual "pick a workstream → start a fresh agent → repeat" ritual —
**not** the human approval gates.

## What this automates vs. what stays human

| Automated | Stays human (STOP and ask) |
| --- | --- |
| Reading the plan as a work queue | Plan approval (must already be approved) |
| Resolving the model role per workstream | Protected-file edits (`.cursorrules` §1.5) |
| Spawning a **fresh** subagent per workstream | ADR acceptance / schema-cascade sign-off |
| Running exit gates | Opening the closeout PR |
| Updating plan todos + `TASK_LOG.md` | Manual smoke on the target environment |
| Sequential dispatch across a phase | Any gate failure the subagent can't fix |

If the plan is not yet approved, stop and tell the user to approve it (or switch to Plan mode) first.
This skill never plans; it only executes. **The orchestrator never edits a source file, runs a build,
or opens a PR itself** — a fresh subagent performs every piece of work.

## Prerequisites

1. An approved plan at `.cursor/plans/<slug>.plan.md`. If Plan mode wrote it outside the repo, copy it in first.
2. Every workstream todo carries orchestration metadata (`phase`, `run_as`, `model_role`, `exit_gates`).
   If missing (Plan mode sometimes strips custom fields), offer to backfill using `plan-template.md`, then continue.
3. A feature branch checked out (not `main`). Verify with `git branch --show-current`; if on `main`, stop per `.cursorrules` §1.2.1.
4. No other orchestrator is active on this clone (one orchestrator per repository).

## Model routing

Workstreams carry a **`model_role`**, not a model name. Roles never change; the concrete slug is
resolved at dispatch time against the live model list in the Task tool description. Never write a
version number into a plan file or into this skill.

Roles: `BUILDER` (default), `ARCHITECT`, `SCRIBE`, `DEEP`, `OPERATOR`, `BULK`. When a workstream omits
`model_role`, infer it from the task type.

Definitions, family ladders, the resolution procedure, and the legacy-pin fallback live in
`docs/MODEL_ROUTING.md` — the single source of truth. Read it once per orchestration session; do not restate it here.

Two rules that always apply:

- **Record the resolved slug** next to the role in `TASK_LOG.md` for every workstream. Without it the
  routing policy has no feedback loop.
- `run_as` assigns the human-gate router, not the worker: `parent` stops, presents the gate to the
  user, and relays the approved context; a fresh subagent always performs the work.

## Context economy (do not exhaust the orchestrator's window)

`run_as` decides **who routes the human gate**, not **who absorbs the tokens**. Conflating the two is
what exhausts orchestrators on build/device-heavy plans: the token-heavy work (build logs, screenshots)
has no human in it, yet gets treated as parent-owned because it was packaged next to a PR or manual gate.

**Rule — delegate the noise, keep the gate.** In a `run_as: parent` workstream, the parent stops for
the user gate and then dispatches a fresh subagent to perform the work, returning **only a verdict
plus the few relevant lines** — never the raw log.

| Heavy sub-step | Subagent returns | Parent routes |
| --- | --- | --- |
| Native build / container build / long compile | `BUILD OK/FAIL` + last ~10 lines on failure + artifact path | the user gate |
| Log/CI scraping, dependency installs, long test runs | pass/fail + the failing lines only | the user decision |
| Screenshot capture **and** visual inspection | a one-line description + verdict | the manual sign-off ask |

**Rule — spawn a subagent for unplanned scope.** When live work appears that is not in the plan (a bug
surfaced during verification, a pivot in approach), do **not** absorb the investigation inline.
Dispatch a fresh subagent to do the debugging and return the root cause + the fix diff. The single
biggest context sink in an orchestration run is an unplanned debug loop done in the parent.

**Rule — screenshot discipline.** Reading a full-resolution image into the parent is expensive.
Capture-and-inspect inside a subagent and take back the text verdict.

**Flag heavy work at plan time.** A workstream marked `heavy: true` is a signal to apply the rules
above regardless of its `run_as`. See `plan-template.md`.

## Orchestration loop

Copy this checklist into the chat and track it:

```
Orchestration progress (Epic N, Phase P):
- [ ] Preflight: plan approved, branch OK, metadata present, no other orchestrator active
- [ ] WS P.1 dispatched → gates → status updated
- [ ] WS P.2 dispatched → gates → status updated
- [ ] Phase exit gates green
- [ ] Human checkpoint (phase review / protected files / PR)
- [ ] Handoff prompt written → new orchestrator chat
```

**Step 1 — Preflight.** Read the plan file. Confirm it's approved, the branch is a feature branch, and
the target phase's workstreams have metadata. Announce which phase and workstreams you'll run.

**Step 2 — Select the next pending workstream** in the active phase (lowest `<phase>.<ordinal>`). If it's
`run_as: parent`, stop at the human gate, present it to the user, and wait for approval; then relay
that approval and any required context in the dispatch prompt. Apply **Context economy** to all heavy sub-steps.

**Step 3 — Dispatch a fresh subagent** with the workstream's `model_role` resolved to a slug per
`docs/MODEL_ROUTING.md`, using the dispatch prompt below. One workstream per subagent — never batch
(this is the anti-context-rot guarantee). Run independent same-phase workstreams as parallel Task
calls only when they share no files and neither consumes the other's output.

**Step 4 — On completion, run exit gates** from the workstream's `exit_gates`. If a gate fails: give the
same subagent one focused retry via `resume`; if it still fails, STOP and report. Never mark a
workstream complete with a red gate.

**Step 5 — Update status.** Flip the plan todo to `completed`; append one line to
`.cursor/active_sprint/TASK_LOG.md` in the form `[WS <id>] <role> → <resolved slug> — <one-line outcome>`.
Prefer having the subagent do this as its last step (see Context hygiene). Do not touch
`PRODUCT_ROADMAP.md` (protected — that's a closeout step).

**Step 6 — Loop** to Step 2 until the phase's workstreams are done. Then run the **phase exit gates**,
STOP for the human checkpoint, write the handoff prompt (`.cursor/prompts/handoff.md`), and tell the
user to start the next phase in a **fresh chat**.

## Subagent dispatch prompt

Give each subagent everything it needs — it does not see this chat or the user's messages.

```
You are executing ONE workstream for the <Project Name> project. Do only this workstream; do not start the next one.

Read first (authoritative) — READ THESE YOURSELF, they are on disk (do not expect the prompt to inline them):
- .cursorrules (hard rules and testing policy)
- .cursor/plans/<slug>.plan.md → the "<WS id>" section IS YOUR TASK + ACCEPTANCE. Read it in full.
- <inputs listed on the workstream>

Task: implement the "<WS id>" section of the plan. <only the deltas / gotchas / clarifications the plan section doesn't already state — keep this short; do not re-paste the plan>

You were dispatched as role <model_role>, resolved to model <resolved slug>. Report that slug back verbatim in your return so it can be logged.

Constraints:
- Follow the testing strategy in .cursorrules §4.1 for every layer you touch.
- Do NOT edit protected files (.cursorrules §1.5) unless this prompt explicitly states the user approved that edit for this workstream; otherwise stop and report.
- <relayed approval, if any: "The user approved editing <file> for this workstream.">

Before returning, run and report results for: <exit_gates>.
Then flip this workstream's todo to `completed` in the plan file and append your TASK_LOG.md line.

Return — KEEP IT TO ≤8 LINES. No markdown tables. No code snippets unless a gate FAILED (then paste only the failing lines):
- the role + resolved model slug you were given
- files changed (bare names only)
- gate results (pass/fail + suite/test counts)
- blockers / protected-file needs / one-line notes the next workstream needs
```

Keep dispatch prompts SHORT: point the subagent at the plan's WS section on disk rather than
re-serializing the spec into your window.

## Failure & stop conditions

Stop the loop and hand back to the user when:

- Any exit gate stays red after one subagent retry.
- A subagent reports it needs a protected-file edit, ADR, or schema change without relayed approval.
- A `run_as: parent` workstream reaches its user gate without explicit approval.
- A phase boundary is reached (human reviews before the next phase dispatches).
- The subagent's changes conflict with uncommitted working-tree state that is not yours.

When stopping, report: what completed, current gate status, why you stopped, and the single next action.

**Do not stop for unplanned in-scope work** — but do not absorb it inline either. Dispatch a fresh
subagent to investigate and return the root cause + fix diff, then resume the loop. Only escalate to
the user if the fix needs a protected file, an ADR, or a decision you can't make.

## Context hygiene (keep the orchestrator's own window lean)

Orchestration is long-horizon and single-window: every subagent reply, gate dump, and doc edit stays
resident. The durable state lives **on disk** (plan todos + `TASK_LOG.md` + commits), so the
orchestrator is fully resumable — exploit that.

1. **Cycle the context at phase boundaries — unconditionally.** Do not drive a multi-phase Epic in
   one chat. At every phase boundary write the handoff prompt and start a fresh orchestrator chat.
   This is the single biggest lever against running out.
2. **Cap subagent returns.** The ≤8-line contract above. Verbose replies are the most frequent large ingest.
3. **Dispatch by reference, not by value.** Point at the plan's WS section on disk.
4. **Delegate the bookkeeping.** Each WS subagent flips its own todo and appends its own `TASK_LOG.md`
   line (with role + resolved slug) as its final step.
5. **Trust single-subagent gate reports; delegate reconciliation.** Re-run the full suite in the
   parent only for parallel-merge reconciliation — and even then, hand it to a throwaway subagent that
   returns the summary line.
6. **Kill recurring shell noise.** Filter every command. Environment conventions live in
   `.cursor/rules/environment.mdc` (always applied); don't restate them here.

## Notes

- This skill dispatches via the Task tool (`generalPurpose` subagents). It does not create Cursor Automations.
- Only slugs listed in the Task tool description can be dispatched; chat-only model variants cannot.
- See `plan-template.md` for the workstream metadata contract, `docs/MODEL_ROUTING.md` for the roles
  this skill resolves against, and `.cursor/prompts/orchestrate.md` for the prompt that starts an orchestrator chat.
