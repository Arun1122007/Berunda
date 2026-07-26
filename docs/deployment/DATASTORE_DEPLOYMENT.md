# Project Berunda — Catalyst Data Store Deployment & Schema Report

> **Document ID:** BERUNDA-DEP-004 | **Version:** 1.0  

---

## 1. Schema Architecture

Project Berunda utilizes a dual-adapter data layer:
- **Primary Persistent Storage:** SQLite database (`berunda.db`), managed asynchronously via SQLAlchemy 2.0 ORM and Alembic migrations (revision `006 (head)`).
- **Catalyst Data Store ZCQL Adapter:** `catalyst_adapter.py` mapping relational tables to Catalyst Data Store ZCQL queries.

---

## 2. Table Manifest (Alembic Revision 006)

| Table Name | Record Count | Description | Primary Key |
| :--- | :---: | :--- | :--- |
| `case_master` | 40,823 | Core First Information Report cases | `CaseMasterID` |
| `person_entity` | 15,200 | Accused, Victim, and Complainant identities | `PersonID` |
| `investigation_occurance_time` | 40,823 | Date, time, and shift breakdown | `OccuranceID` |
| `vehicle_link` | 4,200 | Vehicle linkages across crime scenes | `VehicleID` |
| `chargesheet_details` | 12,400 | Chargesheet records and IPC/BNS mappings | `ChargesheetID` |
| `evidence_master` | 8,900 | Evidence files and metadata | `EvidenceID` |
| `relationship_master` | 6,500 | Entity-to-entity graph relationships | `RelationshipID` |
| `users` | 3 | Default system user accounts | `UserID` |
| `audit_log` | Immutable | Action audit logs | `AuditID` |
