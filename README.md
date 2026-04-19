# Cursor Memory Bank

**v2.0** | A persistent context framework for Cursor AI that enables seamless agent handoffs without hallucinations.

---

## The Problem

LLMs suffer from **context window amnesia**. Each chat session starts fresh. Your AI agent forgets:
- Why you made architectural decisions
- What patterns work in your codebase
- What tasks are in progress
- What lessons you've learned

This leads to:
- 🔄 Repeated explanations every session
- 🎭 Hallucinated code that doesn't match your patterns
- 📉 Lost productivity rebuilding context
- 🐛 Repeated mistakes from forgotten lessons

---

## The Solution

The **Memory Bank** is a structured `.cursor/` directory that gives your AI agent persistent memory:

```
.cursor/
├── README.md                    # System documentation
├── plans/                       # Active planning documents (v2.0)
│   └── *.plan.md                # Cursor plan files
├── memory/                      # Long-term context
│   ├── PROJECT_BRIEF.md         # What the project does
│   ├── TECH_STACK.md            # Technologies used
│   ├── ARCHITECTURE.md          # System design
│   ├── PRODUCT_ROADMAP.md       # Work to be done
│   ├── LESSONS_LEARNED.md       # Patterns and gotchas
│   └── DECISION_LOG.md          # ADRs (Architecture Decision Records)
└── active_sprint/               # Short-term state
    ├── CURRENT_OBJECTIVE.md     # Current session goal
    └── TASK_LOG.md              # Progress tracking
```

Combined with `.cursorrules` protocols, the agent:
- ✅ Reads context at session start
- ✅ Checks for active plan files (v2.0)
- ✅ Verifies branch state before coding (v2.0)
- ✅ Proposes plans before coding
- ✅ Records decisions and lessons
- ✅ Hands off cleanly to future sessions

---

## What's New in v2.0

### 4-Pillar Template Structure

The `.cursorrules` template now uses a cleaner, modular structure:

| Pillar | Purpose |
|--------|---------|
| **01_AGENT_PROTOCOL** | Memory bank, startup, planning, closeout |
| **02_INFRASTRUCTURE** | Project-specific (stub for customization) |
| **03_DEVELOPMENT** | Code standards, error handling (stub) |
| **04_QUALITY_ASSURANCE** | Testing protocol |

### New Features

- **Plan File Continuity** - Resume from `.plan.md` files across sessions
- **Branch Protection** - Verify branch state before making changes
- **Mode Switching Heuristic** - Clear triggers for when to plan vs execute
- **Incremental Build Gates** - Phased checkpoints for complex work
- **Session Closeout Protocol** - Git commit workflow with handoff verification
- **Tool Permissions Matrix** - Explicit read/write/approval requirements

See [CHANGELOG.md](CHANGELOG.md) for full details.

---

## Quick Start

### Option 1: Use the Initialization Prompt

1. Copy `prompts/initialize.md` to your first Cursor chat
2. The agent will analyze your codebase and create the Memory Bank
3. Approve the proposed roadmap
4. Start coding with persistent context!

### Option 2: Manual Setup

1. Copy the `.cursor/` structure from `templates/` to your project:
   ```bash
   mkdir -p .cursor/memory .cursor/active_sprint .cursor/plans
   cp templates/memory/*.template.md .cursor/memory/
   cp templates/active_sprint/*.template.md .cursor/active_sprint/
   cp templates/cursor-readme.template.md .cursor/README.md
   ```

2. Rename `.template.md` files to `.md` and fill in the content

3. Add Memory Bank protocols to your `.cursorrules`:
   ```bash
   cat templates/.cursorrules >> .cursorrules
   ```

4. (Optional) Set up BDD testing:
   ```bash
   mkdir -p tests/features
   cp templates/tests/conftest.py tests/
   cp templates/tests/sample.feature tests/features/
   ```

---

## Key Concepts

### Passive vs Active Memory

| Type | Files | Purpose |
|------|-------|---------|
| **Passive** (ReadOnly) | PROJECT_BRIEF, TECH_STACK, ARCHITECTURE | Stable context rarely changed |
| **Protected** (Approval) | PRODUCT_ROADMAP (scope changes) | Requires approval for changes |
| **Active** (Read/Write) | LESSONS, DECISIONS | Frequently updated knowledge |
| **Session** (High-frequency) | CURRENT_OBJECTIVE, TASK_LOG | Updated every session |

### The Plan-and-Confirm Protocol

Every session starts with:
1. Agent checks for active `.plan.md` files (v2.0)
2. Agent verifies current branch (v2.0)
3. Agent reads PRODUCT_ROADMAP.md
4. Agent proposes a numbered plan
5. User approves, modifies, or redirects
6. Agent executes and updates progress

This prevents the agent from going off-track and ensures alignment.

### Plan File Continuity (v2.0)

For multi-session work, plan files are authoritative:

```markdown
---
name: User Authentication System
todos:
  - id: e2-ws2.1-auth
    content: "[E2 > WS2.1] Implement JWT tokens"
    status: in_progress
---
```

See `guides/PLAN_CONTINUITY.md` for details.

### Branch Protection (v2.0)

Agent verifies branch state at session start:
- Warns if on main/master
- Suggests feature branch naming: `feat/`, `fix/`, `refactor/`, `docs/`
- Handles uncommitted changes gracefully

See `guides/BRANCH_PROTECTION.md` for details.

---

## Package Contents

```
cursor-memory-bank/
├── README.md                 # This file
├── QUICKSTART.md             # Step-by-step first use
├── CHANGELOG.md              # Version history (v2.0)
├── LICENSE                   # MIT License
├── prompts/
│   └── initialize.md         # The "bootstrap" prompt
├── templates/
│   ├── .cursorrules          # Memory Bank rules (4-pillar structure)
│   ├── memory/*.template.md  # Long-term context templates
│   ├── active_sprint/*.template.md  # Session templates
│   ├── cursor-readme.template.md    # .cursor/README.md template
│   └── tests/
│       ├── conftest.py       # pytest-bdd boilerplate
│       └── sample.feature    # Gherkin example
├── guides/
│   ├── FILE_BOUNDARIES.md    # Access control cheatsheet
│   ├── PLAN_CONTINUITY.md    # Multi-session plan workflow (v2.0)
│   ├── BRANCH_PROTECTION.md  # Branch naming and protection (v2.0)
│   ├── DECISION_HEURISTIC.md # When DECISION vs LESSON
│   └── CUSTOMIZATION.md      # Adapting for different stacks
└── examples/                 # Reference implementations
```

---

## Customization

The Memory Bank works with any tech stack. See `guides/CUSTOMIZATION.md` for:

- Python, Node.js, Rust, Go adaptations
- Monolith vs Microservices structures
- With or without Docker
- With or without BDD/Gherkin testing

---

## Best Practices

### 1. Start Every Session Right

Check for active plans, verify branch, read the roadmap, propose a plan, wait for approval. Don't dive into code.

### 2. Use Feature Branches

Always work on feature branches (`feat/`, `fix/`, `refactor/`). Never commit directly to main.

### 3. Record Decisions Immediately

When you make a choice ("Let's use X instead of Y"), add an ADR before you forget the rationale.

### 4. Record Lessons After Debugging

When you fix a tricky bug, document the problem, cause, and solution.

### 5. Keep the Roadmap Current

Update task statuses as you complete work. Mark items `[x]` done.

### 6. Hand Off Cleanly

At session end, update CURRENT_OBJECTIVE and TASK_LOG for the next session.

---

## Comparison

| Approach | Pros | Cons |
|----------|------|------|
| **No Memory** | Simple | Agent forgets everything |
| **Long System Prompt** | Always present | Static, no evolution |
| **RAG/Embeddings** | Semantic search | Complex setup, latency |
| **Memory Bank** | Structured, evolving, simple | Requires discipline |

The Memory Bank is designed for **practical simplicity**. No external services, no complex pipelines—just structured markdown files that the agent reads and writes.

---

## FAQ

### Q: Does this work with other AI editors?

The core concept works anywhere. The `.cursorrules` integration is Cursor-specific, but the Memory Bank structure can be adapted for other tools.

### Q: How do I handle multiple agents/contributors?

The Memory Bank is version-controlled. Multiple contributors (human or AI) can update it through normal git workflows. Merge conflicts in markdown are easy to resolve.

### Q: What if the context gets too long?

The agent reads files as needed. Long files can be split or summarized. The two-phase (passive/active) structure keeps critical context accessible.

### Q: Can I use this without the testing framework?

Absolutely. The BDD testing with pytest-bdd is optional. The core Memory Bank (`.cursor/` directory structure and protocols) works independently.

### Q: What's different in v2.0?

See [CHANGELOG.md](CHANGELOG.md) for the complete list. Key additions: 4-pillar structure, plan file continuity, branch protection, and tool permissions matrix.

---

## Contributing

This framework evolved from real project experience. Contributions welcome:

- New customization examples for different stacks
- Improved templates
- Additional guides
- Bug fixes in templates

---

## License

MIT License - see LICENSE file.

---

## Acknowledgments

Inspired by:
- Architecture Decision Records (ADRs)
- The "Second Brain" methodology
- Zettelkasten for knowledge management
- The pain of re-explaining context to AI agents

---

**Stop losing context. Start banking memories.**
