# Physical Table Specifications

> **Document ID:** BERUNDA-PH5-TABLE-SPECS-001 | **Version:** 1.0

## Core Tables
- **CaseMaster**: Stores base FIR. Primary Key: ROWID. Public ID: CaseNo.
- **Employee**: Stores Officers. PII Enabled: EmployeeName.
- **Unit**: Stores Police Stations.
- **Inv_OccurrenceTime**: Case occurrence timeline. FK to CaseMaster.
- **PersonEntity**: (Accused/Victim/Complainant) Extracted individuals.
- **VehicleLink**: Extracted vehicles.

## Audit & AI
- **AuditLog**: Immutable. Tracks all views of sensitive PII or AI triggers.
- **AISuggestion**: AI generated insights. FK to CaseMaster.
- **AIReviewDecision**: Human decisions on AISuggestion.

*Note: All tables rely on Catalyst Data Store limitations. Integers may map to BigInt. Foreign keys map to ROWID.*
