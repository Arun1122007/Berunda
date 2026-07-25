# Catalyst Schema Decisions Log

This document records the discrepancies identified in the provided ER Diagram for the Police FIR system and the decisions made to translate them into a Zoho Catalyst Cloud Scale Data Store compatible format.

## 1. ActID and SectionID Incompatible Types
- **Inconsistency:** The ER diagram specifies `ActID INT` referencing `Act.ActCode VARCHAR`, and similarly for `SectionID`. Catalyst Data Store requires foreign keys to map to the `ROWID` (BigInt) of the parent record.
- **Resolution:** Replaced the INT fields with Catalyst `Foreign Key` columns (`ActRef`, `SectionRef`) referencing the `ROWID` of the `Act` and `Section` tables. `ActCode` and `SectionCode` are retained as searchable string attributes within their respective parent tables.
- **Alternatives:** We could have mapped the INT to a custom sequence, but `ROWID` is the Catalyst-native relationship mechanism.
- **Compatibility Effect:** Backend services must now resolve `ActCode` to a `ROWID` before inserting a record.

## 2. Section Unique Primary Business Key
- **Inconsistency:** A section code like `302` is only unique within the context of its parent Act (e.g., IPC vs BNS). Catalyst enforces uniqueness on a per-column basis rather than composite keys natively.
- **Resolution:** Introduced a `SectionKey` column computed as `ActCode + ":" + SectionCode` by the application backend prior to insert. Marked `SectionKey` as unique.
- **Alternatives:** Enforcing uniqueness strictly at the application layer without a database unique constraint, which risks race conditions.
- **Organizer Confirmation:** Confirmation that the combined key format `ACT:SECTION` is acceptable for indexing.

## 3. Arrest-to-Accused Relationship Conflict
- **Inconsistency:** The ER diagram table definition places `AccusedMasterID` directly inside `ArrestSurrender` (suggesting 1:N or 1:1), but the relationship matrix indicates one arrest event can involve multiple accused via a junction table.
- **Resolution:** Dropped `AccusedMasterID` from `ArrestSurrender`. Created a new junction table `ArrestSurrenderAccused` mapping `ArrestSurrenderRef` to `AccusedRef` alongside metadata like `IsPrimaryAccused`.
- **Alternatives:** Storing an array of IDs in a text field, which violates Catalyst relational design best practices and breaks ZCQL joins.

## 4. Occurrence Table Incomplete Definition
- **Inconsistency:** The relationship matrix mentions `Inv_OccuranceTime`, but the schema lacks a full table heading or primary key. It is also misspelled.
- **Resolution:** Corrected spelling to `Inv_OccurrenceTime`. Assigned it a `CaseMasterRef` foreign key marked as `IsUnique` and `IsMandatory` to enforce a 1:1 relationship with an FIR. Added spatial and temporal fields mapping to `DateTime` and `Double`.
- **Alternatives:** Merging occurrence data directly into `CaseMaster`. Keeping it separated mirrors the source domain boundaries better and reduces row size for basic queries.

## 5. Chargesheet Employee Reference Inconsistent
- **Inconsistency:** The document refers to `employeeMaster.employee ID`, while the actual master table is `Employee`.
- **Resolution:** Normalized the column to `PolicePersonRef` pointing to `Employee.ROWID`.

## 6. Self-Referencing Unit Table
- **Inconsistency:** `Unit` needs to track hierarchy (e.g., Police Station belongs to District Police) but the ER diagram doesn't explicitly link them.
- **Resolution:** Implemented `ParentUnitRef` as a self-referencing foreign key within the `Unit` table to build the hierarchy.

## 7. Sensitive Fields Restrictions
- **Inconsistency:** Fields like names, dates of birth, religious demographics, and brief facts require strict confidentiality, but ER diagrams do not model data privacy natively.
- **Resolution:** Applied `Encrypted Text` for `BriefFacts`. Documented the requirement to set `PII enabled` flags (via Catalyst Data Store settings/metadata) for victim/complainant details. Access is restricted using role-based permissions (e.g., `Police Analyst` cannot read these fields).
- **Organizer Confirmation:** Requires confirmation on exact `PII` flagging scopes before production deployment.
