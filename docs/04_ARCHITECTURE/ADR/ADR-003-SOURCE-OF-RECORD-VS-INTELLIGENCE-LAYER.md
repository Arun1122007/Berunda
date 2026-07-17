# ADR-003: Source of Record vs Intelligence Layer

[//]: # (Document ID: ADR-003 | Status: APPROVED | Classification: CONFIDENTIAL)

---

## Context

The source FIR schema (CaseMaster, Accused, Victim, etc.) is a system of record — it captures what happened. Berunda adds new entities (PersonEntity, RiskScore, RelationshipEdge, AuditLog) that are derivatives or extensions of the source data.

## Decision

Source tables and Berunda extension tables are kept in **separate logical schemas/namespaces** within the same Data Store instance.

- Source namespace: Mirrors the organizer's FIR ERD structure (CaseMaster, Accused, Victim, ComplainantDetails, etc.)
- Extension namespace: Berunda additions (PersonEntity, PersonEntityLink, RelationshipEdge, RiskScore, MoPattern, Vehicle, AuditLog)

## Rationale

- The source schema is the authoritative record; Berunda extensions are computed/derived data
- Separating them allows the AI layer to be rebuilt or retrained without touching (or risking) the official case record
- Both live in Catalyst Data Store for unified querying and referential integrity
- A future migration could move extensions to separate stores (e.g., PersonEntity to Neo4j)

## Consequences

- Positive: Clear separation of concerns — source data is never modified by the AI layer
- Positive: Easier to rebuild the intelligence layer if the AI models change
- Positive: Audit trail records which system produced each extension record
- Negative: Joins across namespaces require explicit cross-schema queries
- Negative: Some redundancy in storing both source person records and PersonEntity canonical records

## Status

APPROVED
