# Product Roadmap

**Last Updated:** 2026-01-03  
**Purpose:** Track epics, workstreams, and tasks for Photo Factory development

> **Note:** This is a real example from the Photo Factory project. Use it as a reference for structure and hierarchy.

---

## Roadmap Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Completed |
| 🔄 | In Progress |
| ⏳ | Pending |
| ❌ | Blocked/Cancelled |
| 🔥 | High Priority |
| 📋 | Low Priority |

---

## Epic 0: Memory Bank Initialization 🔥 ✅

**Goal:** Create persistent context structure for seamless agent handoffs.

### Workstream 0.1: Directory Structure Setup ✅
- [x] Create `.cursor/` directory
- [x] Create `.cursor/memory/` for long-term context
- [x] Create `.cursor/active_sprint/` for short-term state

### Workstream 0.2: Context Population ✅
- [x] Write TECH_STACK.md from docker-compose and requirements
- [x] Write ARCHITECTURE.md with data flow and modules
- [x] Write PROJECT_BRIEF.md with Future Capabilities section
- [x] Initialize LESSONS_LEARNED.md with patterns found
- [x] Initialize DECISION_LOG.md with implicit ADRs
- [x] Write PRODUCT_ROADMAP.md with all Epics

### Workstream 0.3: Agent Protocol Enforcement ✅
- [x] Update `.cursorrules` with Memory Bank Protocol
- [x] Update `.cursorrules` with User Story Testing Protocol
- [x] Add startup protocol (print roadmap, await approval)
- [x] Add hierarchical todo format rule

---

## Epic 1: Core Ingestion 🔥 ✅

**Goal:** Automated photo/video ingestion with date-based organization.

### Workstream 1.1: File Watching ✅
- [x] Implement file system watcher using watchdog
- [x] Add stability delay for in-progress files
- [x] Implement periodic scan fallback

### Workstream 1.2: Metadata Extraction ✅
- [x] Implement ExifTool integration
- [x] Add PIL/Pillow fallback for images
- [x] Add file mtime fallback
- [x] Extract GPS coordinates to JSONB

### Workstream 1.3: Duplicate Detection ✅
- [x] Implement SHA256 hash calculation
- [x] Check against database for existing hashes
- [x] Delete duplicates from inbox

### Workstream 1.4: File Organization ✅
- [x] Create `{YYYY}/{YYYY-MM-DD}/` folder structure
- [x] Handle filename collisions with suffixes
- [x] Use shutil.move for cross-device support

---

## Epic 2: Monitoring & Observability 🔥 ✅

**Goal:** Real-time visibility into system health and processing status.

### Workstream 2.1: Heartbeat System ✅
- [x] Create `system_status` table (fast lookup)
- [x] Create `system_status_history` table (time series)
- [x] Implement HeartbeatService class
- [x] Add heartbeat to services (configurable intervals)

### Workstream 2.2: Dashboard UI ✅
- [x] Implement Streamlit dashboard
- [x] Display container status via Docker API
- [x] Display heartbeat information
- [x] Show media asset statistics
- [x] Implement auto-refresh

---

## Epic 3: Docker Infrastructure ✅

**Goal:** Containerized, portable deployment with health checks.

### Workstream 3.1: Core Containers ✅
- [x] Create service Dockerfiles (multi-stage)
- [x] Implement test gate in builds
- [x] Add health checks

### Workstream 3.2: Docker Compose ✅
- [x] Define all services in docker-compose.yml
- [x] Configure health checks
- [x] Set up volume mounts
- [x] Configure networking

---

## Epic 4: Reverse Geocoding ⏳ 📋

**Goal:** Convert GPS coordinates to human-readable place names.

### Workstream 4.1: Geocoding Service ⏳
- [ ] Design geocoding table/column structure
- [ ] Choose geocoding provider
- [ ] Implement geocoding service
- [ ] Add rate limiting

### Workstream 4.2: Integration ⏳
- [ ] Query pending assets: `WHERE is_geocoded = FALSE AND location IS NOT NULL`
- [ ] Update `is_geocoded` flag on completion
- [ ] Add heartbeat tracking
- [ ] Create Dockerfile

---

## Epic 5: Thumbnail Generation ⏳ 📋

**Goal:** Generate optimized thumbnails for gallery viewing.

### Workstream 5.1: Thumbnail Service ⏳
- [ ] Create derivatives directory structure
- [ ] Implement thumbnail generation (multiple sizes)
- [ ] Handle image orientation
- [ ] Support video thumbnails

---

## Backlog (Future Epics)

### Epic 6: Cloud Backup
- Backup to S3, B2, GCS
- Incremental backup
- Encryption support

### Epic 7: Enhanced Dashboard
- Pipeline visualization
- Historical analytics
- Alerting (email, webhooks)

### Epic 8: Facial Recognition
- Face detection and extraction
- Person identification and tagging
- Album generation by person

---

## Milestone Timeline

| Quarter | Focus |
|---------|-------|
| Q1 2026 | Memory Bank, Testing Infrastructure |
| Q2 2026 | Geocoding, Thumbnails |
| Q3 2026 | Cloud Backup, Enhanced Dashboard |
| Q4 2026 | Facial Recognition, Smart Albums |

---

## Key Takeaways for Your Project

1. **Hierarchical Structure:** Epic > Workstream > Task
2. **Clear Status:** Use symbols consistently
3. **Prioritization:** Mark 🔥 high priority vs 📋 low priority
4. **Timeline:** Include milestone dates for accountability
5. **Backlog:** Keep future ideas organized but separate
6. **Task Checkboxes:** `[x]` completed, `[ ]` pending

---

**END OF PRODUCT ROADMAP**

