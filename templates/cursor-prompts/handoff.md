# Phase-boundary handoff prompt

<!--
Copy to .cursor/prompts/handoff.md. The orchestrator (or any agent closing out a session) fills this
in and prints it at every phase boundary, or whenever its context window is about half full.
The next agent is started in a FRESH chat from .cursor/prompts/orchestrate.md with this pasted in.
Everything here must also be true on disk (plan todos, TASK_LOG.md, commits) — the prompt is a
convenience, not the source of truth. Verify against git before trusting it.
-->

```
## Handoff — <Project Name>, Epic <N>, after Phase <P>

**Completed**
- WS <P.1> <name> — <role> → <resolved slug> — <one-line outcome>
- WS <P.2> <name> — <role> → <resolved slug> — <one-line outcome>

**Branch + gate state**
- Branch: <feature branch>, last commit <sha> "<subject>", pushed: yes/no
- Gates at last run: typecheck <pass/fail>, test <pass/fail (counts)>, lint <pass/fail>, format:check <pass/fail>
- CI on the PR (if open): <green/red/not yet>

**In progress / partial work in the working tree**
- <none> | <WS id: what exists uncommitted; do NOT wipe it>

**Remaining phases**
- Phase <P+1> — <name>: WS <..> (<run_as>, <model_role>), WS <..> (<run_as>, <model_role>)
- Phase <P+2> — <name>: ...

**Pending human gates**
- <protected file / ADR / PR approvals the next orchestrator must ask for, and any already granted>

**Blocked**
- <none> | <what, and what would unblock it>

**Stop conditions for the next agent**
- Stop at the end of Phase <P+1> and write this prompt again.
- Stop on any red gate after one retry, any protected-file need without relayed approval, any conflict
  with working-tree files you did not create.

**Single next action**
- <e.g. "Dispatch WS 2.1 as BUILDER.">
```
