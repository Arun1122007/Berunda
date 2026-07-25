# Validation Rules

> **Document ID:** BERUNDA-CONTRACT-003 | **Version:** 1.0 | **Status:** APPROVED
> **Classification:** INTERNAL | **Owner:** Berunda Team
> **Last Verified:** 2026-07-25

---

## Principles

1. All input validated on **both** frontend and backend
2. Backend validation is authoritative
3. Frontend validates for UX (instant feedback, reduced server calls)
4. Both layers use the same rules

## Auth Validation

| Field | Rules | Error Code |
|-------|-------|------------|
| email | Required, valid email format | INVALID_EMAIL |
| password | Required, min 8 chars | INVALID_PASSWORD |
| role | One of: admin, officer, analyst | INVALID_ROLE |

## FIR Create Validation

| Field | Required | Type | Constraints |
|-------|----------|------|-------------|
| CrimeNo | Yes | string | Max 50 chars, unique |
| CaseNo | No | string | Max 50 chars |
| CrimeRegisteredDate | No | date | ISO 8601 date |
| PoliceStationID | No | integer | Must reference existing Unit |
| CaseCategoryID | No | integer | Must reference existing case category |
| GravityOffenceID | No | integer | Must reference existing gravity |
| CrimeMajorHeadID | No | integer | Must reference existing CrimeHead |
| CrimeMinorHeadID | No | integer | Must reference existing CrimeSubHead |
| CaseStatusID | No | integer | Must reference existing status |
| IncidentFromDate | No | datetime | ISO 8601 datetime |
| IncidentToDate | No | datetime | ISO 8601 datetime, must be >= from |
| BriefFacts | No | string | Max 5000 chars |
| Latitude | No | float | Range: -90 to 90 |
| Longitude | No | float | Range: -180 to 180 |

## FIR Update Validation

| Field | Required | Constraints |
|-------|----------|-------------|
| CaseStatusID | No | Must reference existing status |
| IncidentToDate | No | Must be >= IncidentFromDate |
| BriefFacts | No | Max 5000 chars |

## Cross-Field Rules

- If Latitude is provided, Longitude is required (and vice versa)
- IncidentToDate must be >= IncidentFromDate
- Officer role users cannot create cases
