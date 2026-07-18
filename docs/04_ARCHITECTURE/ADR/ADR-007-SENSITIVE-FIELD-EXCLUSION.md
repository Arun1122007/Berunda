# ADR-007: Sensitive Field Exclusion

[//]: # (Document ID: ADR-007 | Version: 1.0 | Status: APPROVED | Classification: CONFIDENTIAL | Owner: Berunda Team | Audience: Architects, Team Lead | Source: 01_Enterprise_Blueprint + ERD PDF + ADR decisions | Last Verified: 2026-07-17 | Review: Monthly)

---

## Context

The source FIR schema includes `ComplainantDetails.CasteID` and `ComplainantDetails.ReligionID` fields. These exist for a legitimate, legally-mandated purpose (SC/ST Act and communal-crime statutory reporting). However, if used in predictive models or exposed in general investigative interfaces, they would enable discriminatory profiling.

## Decision

1. **Hard feature exclusion** — CasteID and ReligionID are never in the input feature set for any predictive model. This is enforced in code via a checked allow-list of permitted features per model, not just policy
2. **Access restriction** — These columns are visible only to a narrow "Compliance" role for statutory aggregate reporting. They are never surfaced in the Investigator Console, link-analysis graph, or "Ask Berunda" answers
3. **No general-purpose indexing** — CasteID and ReligionID columns are NOT indexed for general search, preventing them from being used as dashboard filters
4. **Aggregate-only outward reporting** — The only outward-facing use is aggregate district-wise counts (same format as NCRB's own published statistics)
5. **Audited by design** — The Fairness Check specifically verifies that no model's feature-importance report references these fields or their proxies

## Rationale

- The fields exist for a protective, legally-mandated reason — removing them would break statutory reporting capability
- Caste and religion describe the complainant in a victim-protection context; there is no legitimate reason for any predictive model in this system to consume them
- Most competing teams will either ignore these fields or naively expose them as dashboard filters
- This governance control is demonstrable live and is a key differentiator

## Consequences

- Positive: Prevents discriminatory profiling by design
- Positive: Demonstrable compliance with responsible-AI principles
- Positive: Statutory reporting still possible via restricted Compliance role
- Negative: Requires explicit permission model for Compliance role
- Negative: Proxy variables (surname, neighborhood) must also be monitored

## Status

APPROVED
