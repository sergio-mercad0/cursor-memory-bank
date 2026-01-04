# Customization Guide

Adapting the Cursor Memory Bank for different project types and tech stacks.

---

## Overview

The Memory Bank structure is designed to be **stack-agnostic**. This guide shows how to customize it for different project types.

---

## By Language/Framework

### Python Projects

**Dependencies:** Add `pytest-bdd>=7.0.0` to `requirements.txt`

**Directory Structure:**
```
project/
├── .cursor/
│   ├── memory/
│   └── active_sprint/
├── src/                    # or your source directory
│   ├── service_a/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── tests/
│   │       ├── conftest.py
│   │       └── features/
│   └── shared/
├── tests/                  # Project-wide tests
│   ├── conftest.py
│   └── features/
└── requirements.txt
```

**Customize in .cursorrules:**
```markdown
**TESTING PROTOCOL**
* Framework: pytest with pytest-bdd
* Command: `pytest src/*/tests/ -v -m "not slow"`
```

---

### Node.js/TypeScript Projects

**Dependencies:** Add to `package.json`:
```json
{
  "devDependencies": {
    "@cucumber/cucumber": "^10.0.0",
    "jest": "^29.0.0"
  }
}
```

**Directory Structure:**
```
project/
├── .cursor/
│   ├── memory/
│   └── active_sprint/
├── src/
│   ├── services/
│   │   └── service-a/
│   │       ├── index.ts
│   │       └── __tests__/
│   └── shared/
├── tests/
│   ├── features/
│   └── step-definitions/
├── package.json
└── tsconfig.json
```

**Customize in .cursorrules:**
```markdown
**TESTING PROTOCOL**
* Framework: Jest with Cucumber
* Build-time: `npm test -- --testPathIgnorePatterns integration`
* Runtime: `npm run test:integration`
```

---

### Rust Projects

**Dependencies:** Add to `Cargo.toml`:
```toml
[dev-dependencies]
cucumber = "0.20"
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

**Directory Structure:**
```
project/
├── .cursor/
│   ├── memory/
│   └── active_sprint/
├── src/
│   ├── lib.rs
│   └── main.rs
├── tests/
│   ├── features/
│   └── cucumber.rs
└── Cargo.toml
```

**Customize in .cursorrules:**
```markdown
**TESTING PROTOCOL**
* Framework: cargo test with cucumber-rs
* Build-time: `cargo test --lib`
* Runtime: `cargo test --test cucumber`
```

---

### Go Projects

**Dependencies:** 
```bash
go get github.com/cucumber/godog@latest
```

**Directory Structure:**
```
project/
├── .cursor/
│   ├── memory/
│   └── active_sprint/
├── cmd/
│   └── app/
│       └── main.go
├── internal/
│   ├── service/
│   └── repository/
├── features/
│   └── *.feature
├── go.mod
└── go.sum
```

**Customize in .cursorrules:**
```markdown
**TESTING PROTOCOL**
* Framework: go test with godog
* Build-time: `go test ./...`
* Runtime: `godog run`
```

---

## By Project Type

### Monolith Application

**Characteristics:**
- Single deployable unit
- Shared database
- Internal module communication

**Memory Bank Customization:**

```markdown
# In ARCHITECTURE.md

## Module Structure
project/
├── src/
│   ├── api/           # HTTP handlers
│   ├── services/      # Business logic
│   ├── models/        # Data models
│   └── repository/    # Database access
```

**TECH_STACK.md Focus:**
- Single runtime/language
- Database technology
- Web framework

---

### Microservices

**Characteristics:**
- Multiple deployable units
- Service-to-service communication
- Potentially different languages per service

**Memory Bank Customization:**

```markdown
# In ARCHITECTURE.md

## Service Map
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ API Gateway │──│ User Service│  │ Order Service│
└─────────────┘  └─────────────┘  └─────────────┘
                       │                │
                       ▼                ▼
               ┌─────────────┐  ┌─────────────┐
               │  User DB    │  │  Order DB   │
               └─────────────┘  └─────────────┘
```

**Separate Memory Banks Option:**
For large microservice projects, consider a Memory Bank per service:
```
services/
├── user-service/
│   ├── .cursor/      # Service-specific memory
│   └── src/
├── order-service/
│   ├── .cursor/      # Service-specific memory
│   └── src/
└── .cursor/          # Cross-service memory (architecture, roadmap)
```

---

### Frontend Application (React/Vue/Angular)

**Characteristics:**
- Component-based architecture
- State management
- API integration

**Memory Bank Customization:**

```markdown
# In ARCHITECTURE.md

## Component Structure
src/
├── components/       # Reusable UI components
├── pages/            # Route components
├── hooks/            # Custom React hooks
├── store/            # State management
├── services/         # API clients
└── utils/            # Helper functions
```

**TECH_STACK.md Focus:**
- UI framework (React, Vue, Angular)
- State management (Redux, Zustand, Pinia)
- Styling approach (CSS-in-JS, Tailwind, SCSS)
- Build tools (Vite, Webpack)

---

### Data Pipeline / ETL

**Characteristics:**
- Batch or stream processing
- Data transformations
- Scheduled jobs

**Memory Bank Customization:**

```markdown
# In ARCHITECTURE.md

## Pipeline Flow
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Sources │───▶│ Extract  │───▶│Transform │───▶│   Load   │
└─────────┘    └──────────┘    └──────────┘    └──────────┘
                    │               │               │
                    ▼               ▼               ▼
               ┌─────────────────────────────────────────┐
               │           Data Warehouse               │
               └─────────────────────────────────────────┘
```

**TECH_STACK.md Focus:**
- Processing framework (Spark, Airflow, dbt)
- Data storage (S3, BigQuery, Snowflake)
- Scheduling (Airflow, Prefect, cron)

---

## Without Docker

If your project doesn't use Docker, remove or modify these sections:

**In .cursorrules:**
- Remove Docker-specific sections
- Modify testing protocol:

```markdown
**TESTING PROTOCOL**
* **Build-Time Tests:** Run before committing
  * Command: `pytest tests/ -v -m "not slow"`
* **Integration Tests:** Run in CI/CD
  * Command: `pytest tests/ -v -m integration`
```

**Skip Multi-Stage Build Gate:**
Replace with CI/CD gate:
```markdown
**CI/CD GATE**
* Tests run in GitHub Actions / GitLab CI
* Merge blocked if tests fail
* Coverage requirements: 80%
```

---

## Without BDD/Gherkin

If you prefer traditional unit tests over BDD:

**In .cursorrules:**
```markdown
**TESTING PROTOCOL**
* Framework: pytest (Python) / Jest (JS) / etc.
* No Gherkin feature files
* Test naming: `test_<scenario>_<expected_outcome>`
* Markers: @unit, @integration, @slow (as decorators/tags)
```

**Remove:**
- `tests/features/` directories
- Step definitions in conftest.py
- pytest-bdd dependency

**Keep:**
- Test markers for two-phase strategy
- Sandbox testing rule
- Test fixtures

---

## Customization Checklist

When adapting for your project:

- [ ] Update language/framework references in `.cursorrules`
- [ ] Adjust directory structure in `ARCHITECTURE.md` template
- [ ] Modify test commands in testing protocol
- [ ] Customize TECH_STACK.md table structure
- [ ] Add/remove Docker sections as needed
- [ ] Update dependency file references (requirements.txt vs package.json)
- [ ] Adjust path examples for your language conventions
- [ ] Add framework-specific patterns to LESSONS_LEARNED.md

---

## Sample .cursorrules Sections for Different Stacks

### Python + FastAPI + PostgreSQL

```markdown
**5. PROJECT TOPOGRAPHY**
* **`./src/`**: Application code
    * `./src/api/`: FastAPI routes
    * `./src/services/`: Business logic
    * `./src/models/`: SQLAlchemy models
* **`./tests/`**: Test suite
* **`./alembic/`**: Database migrations
```

### Node.js + Express + MongoDB

```markdown
**5. PROJECT TOPOGRAPHY**
* **`./src/`**: Application code
    * `./src/routes/`: Express routes
    * `./src/controllers/`: Request handlers
    * `./src/models/`: Mongoose models
* **`./tests/`**: Test suite
```

### React + TypeScript + GraphQL

```markdown
**5. PROJECT TOPOGRAPHY**
* **`./src/`**: Application code
    * `./src/components/`: React components
    * `./src/graphql/`: Queries and mutations
    * `./src/hooks/`: Custom hooks
    * `./src/store/`: State management
* **`./tests/`**: Test suite
```

---

**END OF CUSTOMIZATION GUIDE**

