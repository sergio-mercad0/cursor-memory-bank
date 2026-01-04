# Decision Log

**Last Updated:** 2026-01-03  
**Purpose:** Architecture Decision Records (ADRs) for Photo Factory

> **Note:** This is a real example from the Photo Factory project. Use it as a reference for ADR structure and content.

---

## How to Use This Document

**When to add a DECISION:**
- New technology choice
- Architecture pattern selection
- Schema design decision
- Infrastructure choice

**When to add to LESSONS_LEARNED instead:**
- Bug fixes and their causes
- Operational constraints discovered
- Performance insights
- Debugging tips

---

## ADR-001: PostgreSQL over SQLite

**Date:** 2024-12-28  
**Status:** Accepted  
**Author:** Initial Architecture

### Context
Choosing database for media asset tracking and system status.

### Decision
Use PostgreSQL 15 (Alpine) as the primary database.

### Rationale
- **JSONB Support:** Native JSONB type for flexible location data storage
- **Concurrency:** Better handling of concurrent writes from multiple services
- **Scalability:** Can handle large media asset catalogs efficiently
- **Production-Ready:** Industry-standard for production applications
- **Docker Integration:** Runs as containerized service

### Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| SQLite | Simple, no server | Poor concurrency, limited types |
| MySQL | Widely used | Less flexible JSON, licensing |
| MongoDB | Native JSON | Overkill, different paradigm |

### Consequences
- Requires Docker service
- More setup than SQLite
- Enables future capabilities (vector search, full-text)

---

## ADR-002: Docker Compose for Orchestration

**Date:** 2024-12-28  
**Status:** Accepted

### Context
Need container orchestration for multi-service architecture.

### Decision
Use Docker Compose with project root as build context.

### Rationale
- **Simple Local Development:** Single command to start all services
- **Portable:** Works on Windows, Mac, Linux
- **Infrastructure as Code:** Version-controlled configuration
- **Health Checks:** Built-in container health monitoring
- **Networking:** Automatic service discovery

### Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| Kubernetes | Scalable, production-grade | Overkill for home use |
| Docker Swarm | Simpler than K8s | Less ecosystem support |
| Bare metal | No container overhead | Not portable, hard to manage |

### Consequences
- All services containerized
- Health checks mandatory
- Volumes for persistence

---

## ADR-003: Originals vs Derivatives Separation

**Date:** 2024-12-28  
**Status:** Accepted

### Context
Need storage strategy for processed photos.

### Decision
Separate `Originals` (immutable source) from `Derivatives` (processed).

### Rationale
- **Immutability:** Originals are never modified after ingest
- **Separation of Concerns:** Source files vs processed files
- **Backup Strategy:** Only backup Originals (derivatives regenerable)
- **Data Integrity:** Original metadata preserved forever

### Storage Structure
```
Storage/
├── Originals/           # Immutable, organized by date
│   └── {YYYY}/
│       └── {YYYY-MM-DD}/
└── Derivatives/         # Processed files (future)
    ├── thumbnails/
    └── transcoded/
```

### Consequences
- Ingestion writes only to Originals
- Future services write to Derivatives
- Clear backup scope

---

## ADR-004: JSONB for Extensible Metadata

**Date:** 2024-12-28  
**Status:** Accepted

### Context
Need to store GPS coordinates with room for future expansion.

### Decision
Use PostgreSQL JSONB for location field.

### Rationale
- **Flexibility:** Can add altitude, accuracy, heading without schema migration
- **Native Queries:** PostgreSQL JSONB operators (`->`, `->>`, `@>`)
- **Indexable:** Can create GIN indexes on JSONB fields
- **Future-Proof:** Facial recognition coordinates, ML tags

### Format
```json
{
  "lat": 35.6762,
  "lon": 139.6503,
  // Future fields (no schema change needed):
  "altitude": 150.5,
  "accuracy": 5.0
}
```

### Consequences
- Flexible queries for location data
- Future-proof for new metadata types
- Pattern extensible to other services

---

## ADR-005: Status Flags Pattern

**Date:** 2024-12-28  
**Status:** Accepted

### Context
Need to track multi-stage processing pipeline.

### Decision
Use boolean flags (`is_X`) with corresponding timestamps (`X_at`) for each processing stage.

### Rationale
- **Clear Queue Queries:** `WHERE is_geocoded = FALSE AND location IS NOT NULL`
- **Extensible:** Each new service adds its own flag
- **Idempotent:** Re-processing sets same flag value
- **Observable:** Dashboard can show pipeline progress

### Current Flags
| Flag | Timestamp | Purpose |
|------|-----------|---------|
| `is_ingested` | `ingested_at` | File moved and cataloged |
| `is_geocoded` | `geocoded_at` | Location enriched |
| `is_thumbnailed` | `thumbnailed_at` | Thumbnails generated |
| `is_backed_up` | `backed_up_at` | Cloud backup complete |
| `has_errors` | - | Error during processing |

### Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| Single status enum | Simple | Can't track partial progress |
| Separate status table | Normalized | Join overhead |
| Message queue | Decoupled | Infrastructure complexity |

### Consequences
- Each service knows exactly what to process
- Dashboard shows pipeline visualization
- Easy to add new stages

---

## ADR-006: PyExifTool over FFmpeg for Metadata

**Date:** 2024-12-28  
**Status:** Accepted

### Context
Need to extract metadata from images, videos, and RAW files.

### Decision
Use PyExifTool (Python wrapper for `exiftool`) as primary extraction tool.

### Rationale
- **Comprehensive:** Handles images, videos, RAW (CR2, NEF, etc.)
- **Industry Standard:** ExifTool is the de-facto metadata tool
- **Python API:** Clean integration via PyExifTool package
- **Fallback Chain:** PIL/Pillow for images, file mtime as last resort

### Consequences
- `libimage-exiftool-perl` installed in Docker
- Reliable extraction across all file types

---

## ADR-007: Dual Heartbeat Strategy

**Date:** 2024-12-28  
**Status:** Accepted

### Context
Need to track service health for both real-time display and historical analysis.

### Decision
Combine Docker API (real-time) with database heartbeats (historical).

### Rationale
- **Real-time:** Docker knows immediately if container is running
- **Historical:** Database tracks trends, detects patterns
- **Separation:** Real-time = Docker, Historical = Database
- **Flexible Intervals:** Different services can have different intervals

### Implementation
| Source | Purpose | Latency |
|--------|---------|---------|
| Docker API | Container running/healthy | Immediate |
| `system_status` | Current heartbeat | Seconds |
| `system_status_history` | Trend analysis | Minutes/Hours |

### Consequences
- Dashboard polls Docker for immediate status
- Heartbeat thread in each service updates database
- Historical data enables uptime calculations

---

## Key Takeaways for Your Project

1. **ADR Format:** Context → Decision → Rationale → Alternatives → Consequences
2. **Number Them:** ADR-001, ADR-002, etc. for easy reference
3. **Status:** Proposed → Accepted → Deprecated → Superseded
4. **Date Them:** Know when decisions were made
5. **Explain Why:** The rationale is more important than the decision itself
6. **Show Alternatives:** Demonstrates due diligence in decision-making

---

**END OF DECISION LOG**

