# Changelog

All notable changes to the Cursor Memory Bank framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-04-19

### Overview

Major framework upgrade based on reconciliation with production-evolved patterns. This release introduces a 4-pillar template structure, enhanced session continuity, and stronger guardrails for multi-agent workflows.

### Gap Analysis Summary

This release bridges the gap between the original v1.0 framework and production-evolved patterns:

| Aspect | v1.0 | v2.0 |
|--------|------|------|
| **Structure** | Sections 9-11 append style (~306 lines) | 4-pillar layout (~800 lines) |
| **Plan Continuity** | Not mentioned | Section 1.2 - MUST follow `.plan.md` files |
| **Branch Protection** | Not mentioned | Section 1.2 - MUST check branch before coding |
| **Mode Switching** | Brief mention in §11 | Detailed trigger: ">2 files or architectural changes" |
| **Build Gates** | Not mentioned | Incremental checkpoints per phase |
| **Session Closeout** | Brief handoff | Detailed with git commit workflow |
| **Handoff Verification** | Not mentioned | Checklist before marking tasks complete |
| **PRODUCT_ROADMAP.md** | No approval required | Approval required for scope changes |
| **Tool Permissions** | Not present | Detailed permission matrix |
| **`.cursor/plans/`** | Optional mention | Explicit in workflow |

### Added

#### 4-Pillar Template Structure
The `.cursorrules` template now uses a cleaner, modular structure:
- **01_AGENT_PROTOCOL** - Memory bank, startup, planning, closeout
- **02_INFRASTRUCTURE** - Project-specific (stub for customization)
- **03_DEVELOPMENT** - Code standards, error handling (stub for customization)
- **04_QUALITY_ASSURANCE** - Testing protocol

#### Plan File Continuity Protocol (Section 1.2)
- Agents MUST check for existing `.plan.md` files at session start
- Plan files serve as authoritative source during multi-session work
- Todo status markers persist across sessions

#### Branch Protection Rules (Section 1.2)
- Agents MUST verify current branch before making changes
- Feature branch naming conventions: `feat/`, `fix/`, `refactor/`, `docs/`
- Protection against unintended commits to main/master

#### Mode Switching Heuristic (Section 1.3)
- Clear trigger: "When task touches >2 files OR involves architectural changes"
- Explicit guidance on when to enter Planning Mode vs stay in Agent Mode
- Plan file structure with todo ID conventions

#### Incremental Build Gates (Section 1.3)
- Phased approach: Dependency → Implementation → Integration
- Quality gates checklist before phase transitions
- Prevents large PRs and ensures incremental progress

#### Session Closeout Protocol (Section 1.4)
- Detailed closeout triggers (context limit, task completion, pivot)
- Git commit workflow integrated into closeout
- Agent handoff verification checklist

#### PRODUCT_ROADMAP.md Approval Required
- Added to protected files list when scope changes
- Prevents unintended roadmap drift

#### Tool Permissions Matrix
- Explicit read/write/execute permissions
- File-by-file access control documentation

### New Guides

- **`guides/PLAN_CONTINUITY.md`** - How to use `.plan.md` files across sessions
- **`guides/BRANCH_PROTECTION.md`** - Feature branch workflow and naming conventions

### Changed

- **`guides/FILE_BOUNDARIES.md`** - Added PRODUCT_ROADMAP.md approval requirement and tool permissions table
- **`README.md`** - Updated for 4-pillar structure, added v2.0 notes
- **`QUICKSTART.md`** - Updated to match new template layout

### Migration from v1.0

1. **Template Update**: Replace your existing `.cursorrules` with the new 4-pillar template
2. **Review Guides**: Read the new PLAN_CONTINUITY and BRANCH_PROTECTION guides
3. **No Data Migration**: Your existing `.cursor/memory/` files remain compatible

---

## [1.0.0] - Initial Release

### Added

- Initial Memory Bank framework
- `.cursor/` directory structure
- Memory bank protocol (Section 9)
- User story testing protocol (Section 10)
- Planning mode protocol (Section 11)
- Template files for memory bank initialization
- Guides for file boundaries, decision heuristics, customization
- Initialization prompt for bootstrapping new projects
