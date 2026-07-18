# Source ERD Reconciliation

[//]: # (Document ID: BERUNDA-DATA-002 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Developers, Data Engineers, QA | Source: ERD PDF (primary) | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Purpose

This document reconciles the official Police FIR ER Diagram (PDF) with the Berunda canonical data model. It identifies which tables are preserved as-is, which are extended, which are added, and one gap.

## 2. Source Tables (Preserved as `src_`)

All 27 tables from the FIR ER Diagram are preserved in the `src_` schema without structural modification.

| # | Table | Key | Notes |
|---|-------|-----|-------|
| 1 | CaseMaster | CaseMasterID (PK) | Central FIR record |
| 2 | ComplainantDetails | ComplainantID (PK) | FK → CaseMaster.CaseMasterID |
| 3 | Victim | VictimMasterID (PK) | FK → CaseMaster.CaseMasterID |
| 4 | Accused | AccusedMasterID (PK) | FK → CaseMaster.CaseMasterID |
| 5 | ArrestSurrender | ArrestSurrenderID (PK) | FK → CaseMaster.CaseMasterID, AccusedMasterID |
| 6 | Inv_OccuranceTime | CaseMasterID (PK, FK) | 1:1 with CaseMaster; includes IncidentFromDate, IncidentToDate, InfoReceivedPSDate, Lat, Long, BriefFacts |
| 7 | ActSectionAssociation | (CaseMasterID, ActID, SectionID) composite | Links cases to legal act-sections |
| 8 | Act | ActCode (PK) | Legal act code (e.g., IPC, NDPS) |
| 9 | Section | (ActCode, SectionCode) composite | Section under an act (e.g., 302, 307) |
| 10 | CrimeHeadActSection | (CrimeHeadID, ActCode) composite | Maps crime heads to act-sections |
| 11 | CrimeHead | CrimeHeadID (PK) | Major crime head (e.g., Crimes Against Body) |
| 12 | CrimeSubHead | CrimeSubHeadID (PK) | Minor crime sub-head (e.g., Murder, Robbery) |
| 13 | CasteMaster | caste_master_id (PK) | Lookup — caste values. NOTE: Restricted access per ADR-007 |
| 14 | ReligionMaster | ReligionID (PK) | Lookup — religion values. NOTE: Restricted access per ADR-007 |
| 15 | OccupationMaster | OccupationID (PK) | Lookup — occupation values |
| 16 | CaseStatusMaster | CaseStatusID (PK) | Lookup — case status (Under Investigation, Charge Sheeted, Closed) |
| 17 | Court | CourtID (PK) | Court reference data |
| 18 | District | DistrictID (PK) | District reference data |
| 19 | State | StateID (PK) | State reference data |
| 20 | Unit | UnitID (PK) | Police station/unit reference data |
| 21 | UnitType | UnitTypeID (PK) | Unit type lookup (Police Station, Circle Office) |
| 22 | Rank | RankID (PK) | Police rank lookup |
| 23 | Designation | DesignationID (PK) | Designation lookup (IO, SHO, etc.) |
| 24 | Employee | EmployeeID (PK) | Police employee records |
| 25 | CaseCategory | CaseCategoryID (PK) | FIR, UDR, PAR, Zero FIR |
| 26 | GravityOffence | GravityOffenceID (PK) | Heinous, Non-Heinous |
| 27 | ChargesheetDetails | CSID (PK) | Chargesheet metadata |

## 3. Berunda Extension Tables (New — `int_` Schema)

| # | Table | Purpose | Key Fields |
|---|-------|---------|------------|
| E1 | PersonEntity | Deduplicated cross-case identity for a real person | PersonEntityID (PK), CanonicalName, DOB (derived), RiskScoreID (FK) |
| E2 | PersonEntityLink | Links a PersonEntity to one or more source records | PersonEntityLinkID (PK), PersonEntityID (FK), SourceTable, SourceRecordID, Confidence, IsReviewed (BIT), ReviewedBy, ReviewedAt |
| E3 | RelationshipEdge | Declared or discovered relationship between two PersonEntities | RelationshipEdgeID (PK), PersonEntityA (FK), PersonEntityB (FK), RelationshipType, SourceCaseID (FK → CaseMaster), Confidence, DiscoveredAt |
| E4 | VehicleLink | Links a vehicle registration to a case | VehicleLinkID (PK), VehicleNumber, CaseMasterID (FK), Confidence, Source (NER/extracted) |
| E5 | RiskScore | Per-PersonEntity risk score computed by AutoML | RiskScoreID (PK), PersonEntityID (FK), Score (0.0-1.0), ModelVersion, ComputedAt |
| E6 | RiskScoreFeatureImportance | Per-score feature importance breakdown | RiskScoreImportanceID (PK), RiskScoreID (FK), FeatureName, ImportanceValue |
| E7 | MoPattern | Modus operandi pattern definition | MoPatternID (PK), PatternName, Embedding (vector), CreatedAt |
| E8 | MoPatternLink | Links a case to an MO pattern | MoPatternLinkID (PK), MoPatternID (FK), CaseMasterID (FK), SimilarityScore |
| E9 | AnomalyAlert | Spike/pattern anomaly record | AnomalyAlertID (PK), DistrictID (FK), CrimeHeadID (FK), WeekStart, ObservedCount, BaselineMean, StdDev, ZScore, AlertLevel (BIT) |
| E10 | HotspotLayer | Geospatial hotspot aggregate | HotspotLayerID (PK), DistrictID (FK), TileX, TileY, DensityScore, WeekStart, WeekEnd |
| E11 | RAGCorpusChunk | Chunked FIR narrative for RAG retrieval | ChunkID (PK), CaseMasterID (FK), ChunkIndex, ChunkText, Embedding (vector), CreatedAt |

## 4. Berunda Governance Tables (New — `gov_` Schema)

| # | Table | Purpose | Key Fields |
|---|-------|---------|------------|
| G1 | AuditLog | Append-only audit trail | AuditLogID (PK), UserID, Action, EntityType, EntityID, OldValue (JSON), NewValue (JSON), Timestamp, IPAddress |
| G2 | FairnessCheckResult | Automated fairness check outcome | FairnessCheckID (PK), CheckType (model_exclusion/access_control), Timestamp, Passed (BIT), Details (JSON), CheckedBy |
| G3 | DataProvenanceRecord | Lineage tracking for derived data | ProvenanceID (PK), TargetTable, TargetRecordID, SourceTable, SourceRecordID, TransformationDescription, CreatedAt |

## 5. GAP-001: inv_arrestsurrenderaccused Junction Table

**Status:** UNRESOLVED

**Issue:** The relationship matrix references `inv_arrestsurrenderaccused` as a junction table linking ArrestSurrender to Accused via a many-to-many relationship. However, the PDF provides NO column definitions for this table.

**Assumed Columns (for Phase 1):**
- `ArrestSurrenderID` (INT, FK → ArrestSurrender.ArrestSurrenderID)
- `AccusedMasterID` (INT, FK → Accused.AccusedMasterID)
- `LinkType` (VARCHAR, nullable — e.g., "primary", "secondary")

**Validation needed:** Confirm actual column structure from the organizing team or the CCTNS database documentation.

## 6. Schema Mapping Summary

```
Source ERD (src_)          Berunda Extensions (int_)          Governance (gov_)
┌─────────────────┐       ┌──────────────────────┐          ┌──────────────────┐
│ CaseMaster       │──────→│ PersonEntity         │          │ AuditLog         │
│ ComplainantDetails│──┐   │ PersonEntityLink     │          │ FairnessCheck    │
│ Victim           │──┤   │ RelationshipEdge     │          │ DataProvenance   │
│ Accused          │──┤   │ VehicleLink          │          └──────────────────┘
│ ArrestSurrender  │──┤   │ RiskScore            │
│ ActSectionAssoc  │  │   │ MoPattern            │
│ Inv_OccuranceTime│  │   │ AnomalyAlert         │
│ ... (27 total)   │  │   │ HotspotLayer         │
└─────────────────┘  │   │ RAGCorpusChunk       │
                     │   └──────────────────────┘
                     │
                     └───→ PersonEntityLink maps to
                           ComplainantDetails/Victim/Accused
                           via SourceTable + SourceRecordID
```

## 7. Column-Level Reconciliation Notes

| Source Column | Status | Berunda Action |
|--------------|--------|----------------|
| `ComplainantDetails.CasteID` | Preserved but RESTRICTED | Excluded from model features; visible only to Compliance role (ADR-007) |
| `ComplainantDetails.ReligionID` | Preserved but RESTRICTED | Same as CasteID |
| `CaseMaster.BriefFacts` | Preserved | Also indexed in int_RAGCorpusChunk as chunked+embedded text |
| `CaseMaster.Latitude` / `CaseMaster.Longitude` | Preserved | Used for geospatial aggregation in int_HotspotLayer |
| All BIT `Active` columns | Preserved | Used as soft-delete / status flags |
