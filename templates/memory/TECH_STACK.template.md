# Tech Stack

**Last Updated:** <YYYY-MM-DD>  
**Purpose:** Technology choices for <Project Name>

---

## Core Language & Runtime

| Technology | Version | Purpose |
|------------|---------|---------|
| **<Language>** | <Version> | Primary language |
| **<Runtime>** | <Version> | <Purpose> |

---

## Container Infrastructure

<!-- Remove this section if not using containers -->

### Docker Services (docker-compose.yml)

| Service | Image/Build | Purpose | Port |
|---------|-------------|---------|------|
| **<service-1>** | `<image:tag>` | <Purpose> | <Port> |
| **<service-2>** | Custom Dockerfile | <Purpose> | <Port> |
| **<service-3>** | `<image:tag>` | <Purpose> | - |

### Custom Docker Images

<Describe build strategy, base images, multi-stage builds if applicable>

Base Image: `<base-image:tag>`

---

## Dependencies

<!-- Adjust for your language: requirements.txt, package.json, Cargo.toml, etc. -->

### <Category 1>
| Package | Version | Purpose |
|---------|---------|---------|
| **<package-1>** | <version> | <Purpose> |
| **<package-2>** | <version> | <Purpose> |

### <Category 2>
| Package | Version | Purpose |
|---------|---------|---------|
| **<package-1>** | <version> | <Purpose> |
| **<package-2>** | <version> | <Purpose> |

### Testing
| Package | Version | Purpose |
|---------|---------|---------|
| **<test-framework>** | <version> | Testing framework |
| **<additional>** | <version> | <Purpose> |

---

## External Tools

| Tool | Installed In | Purpose |
|------|--------------|---------|
| **<tool-1>** | <Location> | <Purpose> |
| **<tool-2>** | <Location> | <Purpose> |

---

## Database Technology

<!-- Adjust or remove based on your database(s) -->

### <Database Name>
- **Engine:** <Database type and version>
- **ORM:** <ORM if applicable>
- **Features:** 
  - <Feature 1>
  - <Feature 2>
  - <Feature 3>

---

## Storage Architecture

| Path | Purpose | Notes |
|------|---------|-------|
| `<path-1>/` | <Purpose> | <Notes> |
| `<path-2>/` | <Purpose> | <Notes> |
| `<path-3>/` | <Purpose> | <Notes> |

---

## Networking

| Port | Service | Protocol |
|------|---------|----------|
| <Port> | <Service> | <Protocol> |
| <Port> | <Service> | <Protocol> |

---

## Version Pinning Policy

<Describe your version pinning approach>

Examples:
- Docker images: Always use specific versions, never `:latest`
- Dependencies: Use `>=X.Y.Z` for flexibility with major version bounds
- Lock files: Commit lock files (package-lock.json, Pipfile.lock, etc.)

---

## Additional Resources

<!-- GPU, external APIs, cloud services, etc. -->

| Resource | Configuration |
|----------|---------------|
| <Resource> | <Configuration details> |

---

**END OF TECH STACK**

