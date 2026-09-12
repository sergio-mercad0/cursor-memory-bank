# Retrospective Guide: tuning the protocol from your own transcripts

Every rule in this framework's v3 came from the same source: reading the chat history of a real
project and counting what went wrong. Intuition said "the model should be smarter"; the transcripts
said "the same shell command failed once per session for three months". This guide makes that
practice repeatable.

---

## 1. When to run one

- At every Epic closeout (cheap: one subagent, ~10 minutes).
- Whenever an orchestrator ran out of context or a handoff went wrong.
- Before editing `.cursorrules` — measure first, then change the rule that the data points at.

---

## 2. Where the evidence is

Cursor stores agent transcripts per project, one folder per chat, as JSON Lines:

```
<user home>/.cursor/projects/<workspace-slug>/agent-transcripts/<chat-uuid>/<chat-uuid>.jsonl
<user home>/.cursor/projects/<workspace-slug>/agent-transcripts/<chat-uuid>/subagents/*.jsonl
```

Each line is one message: `{"role": "user" | "assistant", "message": {"content": [{"type": "text" | "tool_use", ...}]}}`.
User turns carry the prompt; assistant turns carry text and `tool_use` inputs (the commands that were
run). Tool *results* are generally not stored, so failed-call evidence comes from the assistant's
narration and from the command strings themselves.

The folder is large (tens of MB after a few months). **Do not read transcripts whole.** Search them.

---

## 3. What to count

Run this as a `generalPurpose` subagent so the raw hits never land in your main window. Ask it for
counts and short quotes only.

| Question | Search for | What it tells you |
| --- | --- | --- |
| How often did agents hit the wall? | `out of context`, `context window`, `running out`, `handoff`, `hand off` | Whether phase cycling is being skipped |
| Which environment quirks keep recurring? | The command strings themselves: `&&` in a PowerShell session, `2>nul`, `ls -R`, heredocs | Each one that appears in >3 sessions becomes a line in `environment.mdc` |
| Which rules were violated? | Quotes from the user like `you should have`, `why did you`, `I told you`, `again` | The rule is either missing, in the wrong file, or too long to be read |
| Did the memory bank get written? | Edits to `LESSONS_LEARNED.md`, `DECISION_LOG.md`, `TASK_LOG.md`; occurrences of `ADR-` | Whether closeout is actually happening |
| Did closeout produce a PR? | `gh pr create`, `Handoff Summary`, roadmap ✅ edits vs. `git push` | "Roadmap says done, remote says nothing" |
| What did sessions actually do? | Count sessions containing screenshots, builds, emulator/device commands, PR bodies, doc edits, feature code | Where the tokens go — usually governance and verification, not feature code |
| Which models actually ran? | `TASK_LOG.md` lines `[WS …] ROLE → slug`; in older sessions, the `model` argument on `Task` calls | Whether routing matches policy, and whether any slugs are dead |
| Were subagents used? | `Task` tool calls per session; sessions with zero `Task` calls but >100 tool calls | Work the parent absorbed that it should have delegated |

Also list the **first user message of every chat** — it gives you a timeline of what the project
actually spent sessions on, which is rarely what the roadmap says.

---

## 4. Turning findings into changes

Each finding maps to exactly one place. Resist adding it to a prompt.

| Finding | Goes to |
| --- | --- |
| A tool call that fails the same way in many sessions | `.cursor/rules/environment.mdc` (always applied) |
| A step agents skip (push, PR, prove the artifact) | `.cursorrules` §1.4 checklist — as a checkbox, not prose |
| A judgement the parent kept making inline (builds, debugging) | The skill's context-economy rules; `heavy: true` on the workstream type |
| A dead model slug | Delete it. Route by role (`docs/MODEL_ROUTING.md`). |
| A collision between concurrent agents | Branch strategy (§1.2.1) + plan file ownership |
| A one-off debugging win | `LESSONS_LEARNED.md` |
| A process choice (testing policy, tier, orchestration contract) | `DECISION_LOG.md` as an ADR |
| Something the framework itself gets wrong | A PR to this repository |

Write the numbers into the ADR or lesson ("`&&` appeared in 32 of 82 sessions") — a rule with a
measured cause is far less likely to be softened later.

---

## 5. A prompt to run it

```
Analyse the agent transcripts for <project> under <transcripts folder>. Do NOT read files whole; use
targeted searches and return counts plus quotes under 200 characters.

Report:
(a) timeline — first user message of each top-level chat, one line each, with date;
(b) environment friction — per pattern [list], number of sessions it appears in;
(c) context exhaustion — sessions with explicit exhaustion/handoff language;
(d) closeout hygiene — sessions that edited the roadmap vs. sessions that pushed / opened a PR;
(e) memory-bank writes — edits to LESSONS_LEARNED / DECISION_LOG / TASK_LOG per session;
(f) model routing — resolved slugs logged vs. models requested; any slug no longer in the live list;
(g) user corrections — quotes where the user corrected the agent's process (not its code).

Finish with: the three changes that would remove the most repeated friction, each mapped to the file
in section 4 of guides/RETROSPECTIVE.md where it belongs.
```

Run it in a fresh chat with a `SCRIBE`-tier model, and record the outcome as a lesson.
