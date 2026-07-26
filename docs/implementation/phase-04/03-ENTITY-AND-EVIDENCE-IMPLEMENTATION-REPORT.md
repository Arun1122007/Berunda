# Project Berunda — Entity and Evidence Implementation Report

> **Document ID:** BERUNDA-P4-004  
> **Status:** COMPLETED  
> **Date:** 2026-07-26

---

## 1. Overview

This report documents Workstream B: person entities linked to FIRs, vehicle linking, location tracking via occurrence data, evidence metadata lifecycle, evidence file upload/download with Stratus integration, and audit events for entity/evidence operations. The implementation extends Phase 3 foundation tables (`int_PersonEntity`, `int_VehicleLink`, `src_EvidenceMaster`, `InvOccuranceTime`) with Phase 4 service and router methods.

---

## 2. Implementation Details

### 2.1 Persons Linked to FIRs

Person entities are managed via the `int_PersonEntity` and `int_PersonEntityLink` tables. Roles are implicitly tracked through CaseMaster relationships:

- **Complainants**: accessed via `CaseMaster.complainants` relationship on `src_Complainant`
- **Victims**: accessed via `CaseMaster.victims` relationship
- **Accused**: accessed via `CaseMaster.accused` relationship
- **Witness/Suspect**: tracked through `PersonEntityLink` with `SourceTable` and `SourceRecordID`

Entity search and merge are handled by the `EntityRepository`:

- `search_entities(name, district_id, page, page_size)` — searches by name with district scoping
- `get_entity(entity_id)` — single entity lookup
- `get_entity_links(entity_id)` — returns all cases linked to an entity
- `merge_entities(source_id, target_id)` — merges duplicates (deletes source)

**Implementation files**:
- Repository interface: `src/repositories/core.py:193-211`
- SQLite adapter: `src/repositories/sqlite_adapter.py:506-548`
- Router: `src/routers/entity_router.py`
- Schema: `src/schemas/entity.py`

### 2.2 Vehicles Linked to FIRs

- **Create Vehicle Link**: service method `add_vehicle()` in `fir_service.py:499-526` creates a `VehicleLink` record with `VehicleNumber`, `Source` (`manual`, `ai_extraction`, `witness`), and `Confidence` (float 0.0–1.0).
- **List Vehicles**: service method `list_vehicles()` in `fir_service.py:485-497` returns all vehicles linked to an FIR.
- **Schema**: `src/schemas/vehicle.py:8-20` defines `VehicleLinkCreate` and `VehicleLinkResponse`.
- **Repository**: `src/repositories/sqlite_adapter.py:424-439` implements `list_vehicles` and `create_vehicle_link`.

Vehicle links produce `ADD_VEHICLE` audit events.

**Implementation files**:
- Service: `src/services/fir_service.py:484-526`
- Repository interface: `src/repositories/core.py:139-146`
- SQLite adapter: `src/repositories/sqlite_adapter.py:424-439`
- Schema: `src/schemas/vehicle.py`

### 2.3 Locations Linked to FIRs

Locations are stored in `InvOccuranceTime` (created alongside `CaseMaster` in `FIRService.create_fir`). Fields include:

- `BriefFacts` — text description of the occurrence
- `Latitude`, `Longitude` — geographic coordinates

The repository method `list_locations()` in `src/repositories/sqlite_adapter.py:441-446` retrieves the occurrence record for a given FIR.

**Implementation files**:
- Repository interface: `src/repositories/core.py:148-151`
- SQLite adapter: `src/repositories/sqlite_adapter.py:441-446`
- Model: `src/models/src_models.py` (`InvOccuranceTime`)

### 2.4 Evidence Metadata and Lifecycle

Evidence is managed through `src_EvidenceMaster` with the following fields (from `src/schemas/evidence.py`):

- `EvidenceID`, `CaseMasterID`, `EvidenceType`, `Description`
- `StoragePath`, `CollectedAt`, `CollectedBy`, `Source`, `Location`
- `Checksum`, `FileType`, `FileSize`
- `Status` (lifecycle: `available`, `under_review`, `restricted`, `archived`)
- `Sensitivity`, `CreatedAt`, `UpdatedAt`

Status transitions are managed via `update_evidence_status()` in the repository, which validates against the allowed status values.

**Implementation files**:
- Schema: `src/schemas/evidence.py`
- Repository interface: `src/repositories/core.py:152-160`
- SQLite adapter: `src/repositories/sqlite_adapter.py:448-457`

### 2.5 Evidence File Upload/Download and Stratus Integration

- **Upload**: `FIRService.upload_evidence()` in `fir_service.py:135-184` performs:
  1. Validates FIR exists
  2. Path traversal check: rejects filenames containing `..`, `/`, or `\`
  3. Saves via `FileStorage` protocol (supports `LocalDiskStorage` and Catalyst Stratus adapter)
  4. Creates `EvidenceMaster` record
  5. Logs `EVIDENCE_UPLOADED` audit event
- **List Evidence**: `FIRService.get_evidence()` returns evidence metadata for an FIR
- **FileStorage Protocol**: defined in `src/repositories/core.py:232-248` with `save_file`, `get_file`, `delete_file`, `file_exists`

**Implementation files**:
- Service: `src/services/fir_service.py:135-210`
- FileStorage interface: `src/repositories/core.py:232-248`

### 2.6 Audit Events

| Action | Audit Event | Component |
|--------|-------------|-----------|
| Vehicle linked | `ADD_VEHICLE` → VehicleLink | `fir_service.py:512-518` |
| Evidence uploaded | `EVIDENCE_UPLOADED` → EvidenceMaster | `fir_service.py:164-171` |

---

## 3. API Endpoints

Entity and evidence operations are exposed via existing routers:

| Method | Endpoint | Router | Description |
|--------|----------|--------|-------------|
| GET | `/api/v1/entities/search` | entity_router | Search person entities |
| GET | `/api/v1/entities/{id}` | entity_router | Get entity details |
| GET | `/api/v1/entities/{id}/links` | entity_router | Get entity links to cases |
| POST | `/api/v1/entities/merge` | entity_router | Merge duplicate entities |

Evidence upload is accessed through FIR context (via `fir_router` or internal service calls).

---

## 4. Database Tables

| Table | Key Fields | Purpose |
|-------|------------|---------|
| `int_PersonEntity` | PersonEntityID, CanonicalName, DOB, Gender, PrimaryDistrictID | Entity resolution hub |
| `int_PersonEntityLink` | PersonEntityLinkID, PersonEntityID, SourceTable, SourceRecordID, CaseMasterID, Confidence | Links entities to source records |
| `int_VehicleLink` | VehicleLinkID, VehicleNumber, CaseMasterID, Confidence, Source | Vehicle-to-FIR associations |
| `InvOccuranceTime` | CaseMasterID, BriefFacts, Latitude, Longitude | Occurrence location data |
| `src_EvidenceMaster` | EvidenceID, CaseMasterID, EvidenceType, Description, StoragePath, Checksum, FileType, FileSize, Status, Sensitivity | Evidence metadata lifecycle |
| `int_RelationshipEdge` | RelationshipEdgeID, PersonEntityA, PersonEntityB, RelationshipType, Confidence | Entity relationship graph |

---

## 5. Authorization Rules

| Operation | Required Role | Notes |
|-----------|---------------|-------|
| Search entities | Any authenticated | District-scoped for non-admin |
| View entity | Any authenticated | — |
| Merge entities | admin | Sensitive operation |
| Upload evidence | admin, officer | Path traversal validation |
| List evidence | Any authenticated | FIR-scoped |
| Add vehicle | Service-internal | Via entity extraction pipeline |

---

## 6. Test Coverage

Entity and evidence operations are covered by existing tests:
- `tests/api/test_fir_api.py` (evidence upload/listing)
- `tests/unit/test_fir_service.py` (service layer)
- Phase 3 entity resolution tests

The vehicle link and evidence lifecycle are tested through integration tests and the end-to-end user journey test.

---

## 7. Status

**Verdict: COMPLETED** — All Workstream B features are implemented. Person entities support search and merge with district scoping. Vehicle linking supports multiple sources and confidence scoring. Evidence metadata lifecycle includes status transitions and sensitivity classification. File upload includes path traversal protection and Stratus storage integration via the FileStorage protocol.

