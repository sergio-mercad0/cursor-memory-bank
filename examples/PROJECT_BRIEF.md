# Project Brief

**Last Updated:** 2026-01-03  
**Purpose:** Define Photo Factory's mission, scope, and future direction

> **Note:** This is a real example from the Photo Factory project. Use it as a reference for structure and content depth.

---

## Mission

**Photo Factory** is a self-hosted, automated photo and video management system that provides:
- **Automatic ingestion** from multiple devices
- **Date-based organization** using true capture metadata
- **Duplicate detection** to prevent storage waste
- **Full observability** through real-time monitoring

---

## Problem Solved

| Problem | Solution |
|---------|----------|
| Manual photo organization is tedious | Automatic organization by capture date |
| Cloud services lack control & privacy | Self-hosted with full data ownership |
| Duplicates waste storage space | SHA256 hash-based deduplication |
| Hard to know if sync is working | Real-time dashboard with heartbeats |
| Photos get lost or disorganized | Immutable originals with database catalog |

---

## Primary Directives

All development must prioritize:

1. **Portability** - No hardcoded paths, works on any system
2. **Stability** - Idempotent operations, graceful error handling
3. **Automation** - Minimal manual intervention required

---

## Current Scope

### Core Features (Implemented ✅)

| Feature | Description | Status |
|---------|-------------|--------|
| **File Ingestion** | Watch inbox for new files | ✅ Implemented |
| **Date Organization** | Move to `{YYYY}/{YYYY-MM-DD}/` structure | ✅ Implemented |
| **Metadata Extraction** | Extract capture date and GPS from EXIF | ✅ Implemented |
| **Duplicate Detection** | SHA256 hash comparison | ✅ Implemented |
| **Database Catalog** | PostgreSQL with full asset metadata | ✅ Implemented |
| **Service Heartbeats** | Track service health in database | ✅ Implemented |
| **Monitoring Dashboard** | Streamlit UI with real-time status | ✅ Implemented |
| **Docker Deployment** | Containerized services with health checks | ✅ Implemented |

### Supported File Types

| Category | Extensions |
|----------|------------|
| Images | .jpg, .jpeg, .png, .gif, .webp, .heic, .heif |
| RAW | .cr2, .nef, .arw, .dng, .raf, .orf |
| Video | .mp4, .mov, .avi, .mkv, .m4v |

---

## Future Capabilities (Architectural Awareness)

**⚠️ PURPOSE:** These are listed to ensure current architectural decisions support future growth. **DO NOT plan implementation tasks for these yet.**

### 1. Reverse Geocoding
Convert GPS coordinates to human-readable place names.

**Architecture Consideration:**
- JSONB `location` field preserves raw coordinates (immutable)
- Geocoded labels stored in separate column or table
- `is_geocoded` flag tracks processing status

### 2. Thumbnail Generation
Create optimized thumbnails for gallery viewing.

**Architecture Consideration:**
- Derivatives path reserved for processed files
- `is_thumbnailed` flag and `thumbnailed_at` timestamp ready
- Originals never modified (thumbnails are derivatives)

### 3. Cloud Archival
Backup originals to cloud storage.

**Architecture Consideration:**
- `is_backed_up` flag and `backed_up_at` timestamp ready
- Backup service queries `WHERE is_backed_up = FALSE`
- Supports multiple backup destinations

---

## User Personas

### Primary: Home User
- Has thousands of photos on phone, tablet, laptop
- Wants automatic organization without cloud dependency
- Needs to know system is working (observability)
- Values privacy and data ownership

### Secondary: Power User
- Manages family photo archive (100K+ photos)
- Wants duplicate detection and deduplication
- Needs historical data for troubleshooting
- May extend system with custom services

---

## Success Metrics

| Metric | Target |
|--------|--------|
| File Processing Latency | < 30 seconds from drop to organized |
| Duplicate Detection Rate | 100% (based on content hash) |
| Service Uptime | 99.9% (tracked via heartbeats) |
| Manual Intervention | Near zero for normal operation |
| Dashboard Response Time | < 2 seconds for all views |

---

## Non-Goals (Explicit Exclusions)

| Feature | Reason |
|---------|--------|
| Cloud-first architecture | Self-hosted is primary directive |
| Mobile app development | Use existing sync apps |
| Social sharing features | Privacy-focused, no public sharing |
| Photo editing UI | Should be automated, keep derivatives |

---

## Key Takeaways for Your Project

1. **Be Specific:** Define what your project does and doesn't do
2. **Future-Proof:** List future capabilities to guide architecture
3. **User-Centered:** Identify who uses your system and why
4. **Measurable:** Define success metrics you can track
5. **Honest:** Non-goals prevent scope creep

---

**END OF PROJECT BRIEF**

