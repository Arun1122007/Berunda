# 07 Database Security and RBAC

This document outlines the security architecture for the Catalyst Data Store integration.

## 1. Role-Based Access Control (RBAC)

The system defines three primary roles:
- `admin`: Has global read/write access to all entities across all districts.
- `officer`: Has read/write access strictly limited to FIRs and Entities belonging to their assigned `DistrictID` and `PoliceStationID`.
- `analyst`: Has read-only access to aggregated data and predictive modeling tables.

### Implementation
- The user's role is determined by the JWT payload (issued by the `auth_router.py`).
- The `CatalystFIRRepository` and `SQLiteFIRRepository` implementations must enforce filtering based on the provided `district_id` and `police_station_id` from the injected user claims.
- Example: An `officer` querying `GET /api/v1/fir` will silently have their `district_id` appended to the query, preventing horizontal privilege escalation.

## 2. Personally Identifiable Information (PII) Protection

As audited in Phase 2, multiple tables contain sensitive PII:
- `ComplainantDetails` (Name, Age, Address, Phone)
- `Victim` (Name, Age, Address)
- `Accused` (Name, Age, Address)

### Catalyst specific requirements
- The Catalyst Data Store has been configured with `audit_consent: true` for all PII columns. This ensures that any direct read of these columns via the Catalyst console is logged for audit purposes.
- Synthetic data generation handles anonymization, but real production data must never be exported outside of the Catalyst secure boundary without passing through the Presidio anonymizer layer (already included in `requirements.txt`).

## 3. Row-Level Security

While Catalyst Data Store does not support native PostgreSQL-style Row Level Security (RLS) policies at the database engine level, RLS is enforced at the Application Service layer (in our case, the `Repository` implementations) by explicitly wrapping ZCQL queries with tenant-specific `WHERE` clauses.

```sql
-- Explicitly appended in CatalystFIRRepository for non-admins
SELECT * FROM CaseMaster WHERE PoliceStationID = <user.station_id>
```
