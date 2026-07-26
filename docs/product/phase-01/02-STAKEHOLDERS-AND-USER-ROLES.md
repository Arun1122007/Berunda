# 02 — Stakeholders, User Roles, Personas, and Access Boundaries

**Document ID:** BERUNDA-PH1-ROLES-001
**Version:** 1.0 | **Status:** APPROVED — Authoritative Phase 1 role definition
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

> This document defines the authorised users of Berunda, what each user needs to accomplish,
> which information they may access, and which actions they may perform.
> It is the authoritative input for frontend navigation design, backend authorization,
> database access rules, and audit logging.

---

## 1. Stakeholder Overview

Project Berunda serves the Karnataka State Police investigation and analytics ecosystem. Stakeholders range from front-line investigating officers who need fast cross-case lookups to governance officers who need fairness verification. The hackathon demo involves a small subset of these stakeholders operating on synthetic data.

---

## 2. Stakeholder Classification

### 2.1 Primary Users — Core MVP (must be in the demo)

| STK-ID | Stakeholder | Role in System | Priority |
|--------|-------------|----------------|---------|
| STK-001 | Investigating Officer (IO) | Registers FIRs, views cases, searches entities, adds investigation notes, uses graph and RAG | MUST |
| STK-002 | Station House Officer (SHO) | Assigns cases, reviews dashboards, monitors jurisdiction hotspots and anomalies | MUST |
| STK-003 | SCRB Analyst | State-wide analytics, cross-district pattern analysis, statutory report generation | MUST |
| STK-004 | Compliance / Governance Officer | Fairness audit, audit log review, restricted field access for statutory reporting | MUST |

### 2.2 Secondary Users — Operational (exist in system, not demo spotlight)

| STK-ID | Stakeholder | Role | Priority |
|--------|-------------|------|---------|
| STK-005 | System Administrator (ADMIN) | User provisioning, configuration, system health | MUST (functional; not demo-spotlighted) |
| STK-006 | Hackathon Demo Administrator | Demo setup — creates test users, loads seed data, role-switching during judging | DEMO ONLY |

### 2.3 Operational Stakeholders (indirectly affected)

| STK-ID | Stakeholder | Relationship |
|--------|-------------|-------------|
| STK-007 | Karnataka SCRB | Data owner; system produces statutory reports |
| STK-008 | District Superintendent of Police (SP) | Consumes analytics; maps to SCRB_ANALYST role in MVP |
| STK-009 | Karnataka State Police (KSP) | Platform operator; oversight body |

### 2.4 Technical Stakeholders

| STK-ID | Stakeholder | Role |
|--------|-------------|------|
| STK-010 | Berunda Dev Team (Phoenix Coder) | Builders; also fill ADMIN role during demo |
| STK-011 | Hack2Skill Judging Panel | Evaluators; evaluate as demo viewers with SCRB_ANALYST perspective |
| STK-012 | Zoho Catalyst Platform | Infrastructure provider; not a human stakeholder |

### 2.5 Governance Stakeholders

| STK-ID | Stakeholder | Role |
|--------|-------------|------|
| STK-013 | Compliance / Governance Officer | Fairness audits, privacy oversight, audit log review |
| STK-014 | Data Protection Authority (future) | Regulatory compliance; Phase 3+ concern |

### 2.6 Future Users (not in MVP — do not implement)

| STK-ID | Stakeholder | Target Phase |
|--------|-------------|-------------|
| STK-015 | Citizens / Complainants | Phase 3+ citizen portal |
| STK-016 | Courts / Judiciary | Phase 3+ read-only case timeline access |
| STK-017 | Forensic Labs | Phase 2+ evidence metadata linkage |
| STK-018 | OSINT / Cyber Crime Cells | Phase 4+ external data correlation |
| STK-019 | Cross-state or national police | Phase 5+ national intelligence layer |

---

## 3. Approved MVP Roles

The MVP implements exactly **4 system roles**, as confirmed by DEC-016 and `ACCESS_CONTROL_MATRIX.md`.

| Role | Display Name | Assigned To | Jurisdiction |
|------|-------------|-------------|-------------|
| INVESTIGATOR | Investigating Officer | Front-line IOs and SHOs | Own district / assigned stations only |
| SCRB_ANALYST | State Analyst | SCRB analysts, District SPs | All districts |
| COMPLIANCE | Compliance Officer | Governance / audit roles | All districts (including restricted fields) |
| ADMIN | System Administrator | Dev team, system admin | All districts (full system access) |

> [!NOTE]
> SHO (Station House Officer) maps to the INVESTIGATOR role in the MVP. SHO-specific features (case assignment, jurisdiction dashboard) are differentiated by UI navigation, not by a separate system role. A dedicated SHO role may be introduced in Phase 2.

---

## 4. Deferred Roles

The following roles were evaluated and deferred from the MVP.

| Proposed Role | Decision | Reason |
|--------------|----------|--------|
| FIR Registration Officer (separate from IO) | Deferred | In most stations, the IO registers the FIR; a dedicated registration clerk role adds complexity without a distinct permission boundary for MVP |
| Supervisor (distinct from SHO) | Deferred | SHO and Supervisor capabilities map to the INVESTIGATOR role with station-scoped access; a dedicated Supervisor role is Phase 2 |
| Auditor (read-only audit log) | Deferred | COMPLIANCE role covers audit log review; a dedicated Auditor role is Phase 3 |
| Citizen / Complainant | Deferred | No citizen-facing portal in MVP; Phase 3+ |
| Field Officer (mobile-only) | Deferred | No mobile native app in MVP; Phase 2 |

---

## 5. Persona Definitions

### PERSONA-001 — Inspector Ananya (INVESTIGATOR)

| Field | Value |
|-------|-------|
| **Persona ID** | PERSONA-001 |
| **Role** | Investigating Officer — INVESTIGATOR |
| **Station** | Bengaluru City Police, Electronic City Division |
| **Responsibilities** | Registers FIRs, investigates assigned cases, interviews persons, collects evidence, prepares chargesheet |
| **Objectives** | Resolve cases faster; identify repeat offenders; find hidden connections to related cases |
| **Technical Comfort** | Medium — familiar with CCTNS data entry; uses smartphones; not a data analyst |
| **Main Tasks** | Create FIR manually or upload document → review AI extraction → search for related persons/vehicles → view relationship graph → add investigation notes → check Ask Berunda for quick answers |
| **Current Pain Points** | Spends 2-3 hours manually cross-referencing a suspect against prior cases; name spelling variations cause misses; no way to see if a vehicle appears in other cases |
| **Data Required** | FIR detail, Accused/Victim/Complainant records, prior cases for a person, relationship graph, BriefFacts text, vehicle links, investigation notes |
| **Decisions Made** | Which entity resolution merges to approve; which investigation leads to pursue; what to add to investigation notes |
| **Actions Permitted** | Create FIR, view own-district cases, search persons/vehicles, approve/reject entity resolution merges, view relationship graph, view risk scores, use Ask Berunda, add investigation notes, view own audit history |
| **Actions Prohibited** | Access cases from other districts (unless assigned cross-district), read CasteID/ReligionID, view full audit log, manage users, view fairness reports, delete records |
| **Common Failure Situations** | Name variation not resolved → miss repeat offender; FIR upload fails → manual entry required; Ask Berunda gives uncited answer → officer ignores it |
| **Success Definition** | Within 5 minutes of searching a suspect name, Ananya sees all prior cases, the relationship graph, and a risk score with explanation — without leaving Berunda |

---

### PERSONA-002 — SHO Ramesh (INVESTIGATOR with station-supervisor context)

| Field | Value |
|-------|-------|
| **Persona ID** | PERSONA-002 |
| **Role** | Station House Officer — INVESTIGATOR role; station-supervisor context |
| **Station** | Mysuru District, Kuvempunagar Police Station |
| **Responsibilities** | Overall crime management for the station; assigns cases to IOs; submits reports to SP office; approves investigation actions |
| **Objectives** | Real-time view of crime patterns in jurisdiction; proactive deployment based on hotspot data; fast case assignment |
| **Technical Comfort** | Low-Medium — comfortable with dashboards; not a data analyst |
| **Main Tasks** | Review jurisdiction dashboard → check hotspot map for emerging patterns → review anomaly alerts → assign cases to IOs → check AI-generated case summaries |
| **Current Pain Points** | Relies on manually compiled Excel reports; no real-time view; cannot see emerging patterns until they are reported; submits periodic reports that are already out of date |
| **Data Required** | Jurisdiction crime summary, hotspot map (own district), anomaly alerts, case list (own station), IO assignment status |
| **Decisions Made** | Case assignment to IOs; patrol deployment based on hotspot data; when to escalate to SP |
| **Actions Permitted** | Same as INVESTIGATOR + view station-wide case list + assign cases to IOs (Phase 2 feature) |
| **Actions Prohibited** | Same prohibitions as INVESTIGATOR |
| **Common Failure Situations** | Hotspot data delayed → reactive deployment; anomaly not flagged → spike missed; dashboard loads slowly → SHO skips it |
| **Success Definition** | Ramesh opens the dashboard each morning and immediately sees current crime patterns, active anomalies, and pending case assignments without running any manual queries |

---

### PERSONA-003 — Analyst Priya (SCRB_ANALYST)

| Field | Value |
|-------|-------|
| **Persona ID** | PERSONA-003 |
| **Role** | SCRB Data Analyst — SCRB_ANALYST |
| **Office** | State Crime Records Bureau, Bengaluru |
| **Responsibilities** | Compiles district-wise crime statistics; prepares quarterly trend analyses; produces statutory reports; monitors state-wide patterns |
| **Objectives** | Replace manual Excel compilation with platform-generated reports; detect cross-district patterns; support senior leadership with data |
| **Technical Comfort** | High — data-literate; experienced with Excel, pivot tables, basic SQL queries |
| **Main Tasks** | View state command dashboard → filter by district, crime type, time period → drill down to district/station → generate cross-district comparison → export trend report → review cross-district entity resolution results |
| **Current Pain Points** | Manually collects data from 36 districts; formats are inconsistent; cannot see patterns that span districts; quarterly reports are out of date by the time they are published |
| **Data Required** | All-district crime summary, cross-district entity links, temporal trend charts, geographic hotspot data, aggregate risk indicators, statutory reporting data |
| **Decisions Made** | Which trends to escalate to DGP; which districts need attention; which statutory reports are ready |
| **Actions Permitted** | View all-district case data (read-only on structured fields, excluding restricted fields), view all entity resolution results, view all risk scores, use Ask Berunda, view own audit history, view fairness check results (read-only) |
| **Actions Prohibited** | Read CasteID/ReligionID on individuals, access full audit log (own actions only), manage users, update or delete case data, view system configuration |
| **Common Failure Situations** | Cross-district data is inconsistent → report cannot be generated; entity resolution has low confidence → links are unreliable; Ask Berunda gives an outdated answer → analyst ignores it |
| **Success Definition** | Priya generates a district-wise crime trend report directly from Berunda in 10 minutes, without opening Excel or waiting for station reports |

---

### PERSONA-004 — Krishnamurthy (COMPLIANCE)

| Field | Value |
|-------|-------|
| **Persona ID** | PERSONA-004 |
| **Role** | Compliance and Governance Officer — COMPLIANCE |
| **Office** | KSP Internal Oversight / SCRB Governance Unit |
| **Responsibilities** | Ensures AI recommendations are fair and auditable; monitors for bias; verifies protected-characteristic exclusion; produces statutory SC/ST aggregate reports |
| **Objectives** | Confirm on demand that no model uses caste or religion features; review audit trails for suspicious access patterns; produce statutory aggregate reports |
| **Technical Comfort** | Medium — understands policy; not a data scientist; relies on dashboard evidence |
| **Main Tasks** | Open fairness dashboard → verify CasteID/ReligionID exclusion from all models → review feature importance breakdown → search audit log for specific officer or date range → generate SC/ST aggregate count report |
| **Current Pain Points** | No tools to verify AI fairness; audit trails are paper-based; statutory reports require manual field counting |
| **Data Required** | Full audit log, fairness check results, feature importance for all risk scores, CasteID/ReligionID aggregate counts (restricted fields), data provenance records |
| **Decisions Made** | Whether to flag an AI output for human review; whether an audit pattern is suspicious; whether statutory reports are accurate |
| **Actions Permitted** | Read CasteID/ReligionID (aggregate only — individual records shown in aggregate, not individually), read full audit log, read all fairness check results, read all data provenance records, use Ask Berunda (within access bounds) |
| **Actions Prohibited** | Create or update FIRs, assign cases, change user roles, access system configuration, export raw individual-level Caste/Religion data |
| **Common Failure Situations** | Fairness check fails → must escalate to Admin to investigate; audit log search is slow → oversight task delayed; statutory aggregate fails → manual count required |
| **Success Definition** | Krishnamurthy can confirm within 5 minutes that all risk scoring models exclude CasteID and ReligionID, with programmatic evidence visible in the fairness dashboard |

---

### PERSONA-005 — Dev Admin (ADMIN)

| Field | Value |
|-------|-------|
| **Persona ID** | PERSONA-005 |
| **Role** | System Administrator — ADMIN |
| **Responsibilities** | Provision and manage user accounts; configure system settings; run seed scripts; monitor system health; manage role assignments |
| **Objectives** | System is available and correctly configured; all demo users have the right roles; seed data is loaded |
| **Technical Comfort** | High — developer or DevOps |
| **Main Tasks** | Create demo users with correct roles → seed database with synthetic data → monitor health endpoints → manage Catalyst project configuration |
| **Actions Permitted** | All actions across all resources; manage users; read and search full audit log; system configuration; delete records (with approval) |
| **Actions Prohibited** | Nothing is technically prohibited, but destructive actions (delete all records, change production configuration) require explicit approval per AGENTS.md safety rules |
| **Success Definition** | Demo environment is fully provisioned and stable; all 5 demo users (Ananya, Ramesh, Priya, Krishnamurthy, Admin) have correct roles and can log in |

---

## 6. Responsibilities Summary

| Responsibility | INVESTIGATOR | SCRB_ANALYST | COMPLIANCE | ADMIN |
|---------------|:---:|:---:|:---:|:---:|
| Register FIRs | ✅ Own district | ❌ | ❌ | ✅ |
| Review AI extraction | ✅ Own district | ❌ | ❌ | ✅ |
| Approve entity resolution merges | ✅ Own district | ❌ | ❌ | ✅ |
| View case list | ✅ Own district | ✅ All | ✅ All | ✅ All |
| Search persons/vehicles | ✅ Own district | ✅ All | ✅ All | ✅ All |
| View relationship graph | ✅ Own district | ✅ All | ✅ All | ✅ All |
| View hotspot map | ✅ Own district | ✅ All | ✅ All | ✅ All |
| View risk scores | ✅ Own district | ✅ All | ✅ All | ✅ All |
| Use Ask Berunda | ✅ | ✅ | ✅ | ✅ |
| Add investigation notes | ✅ Assigned cases | ❌ | ❌ | ✅ |
| View audit log | ✅ Own actions only | ✅ Own actions only | ✅ All | ✅ All |
| Access CasteID/ReligionID fields | ❌ | ❌ | ✅ Aggregate | ✅ |
| View fairness check results | ❌ | ✅ Read-only | ✅ Full | ✅ Full |
| Manage users | ❌ | ❌ | ❌ | ✅ |
| System configuration | ❌ | ❌ | ❌ | ✅ |

---

## 7. Data-Access Needs by Role

| Data Category | INVESTIGATOR | SCRB_ANALYST | COMPLIANCE | ADMIN |
|--------------|:---:|:---:|:---:|:---:|
| `CaseMaster` | Own district | All | All | All |
| `Accused` (excl. Caste/Religion) | Own district | All | All | All |
| `Accused.CasteRef / ReligionRef` | ❌ | ❌ | Aggregate only | ✅ |
| `Victim` (excl. Caste/Religion) | Own district | All | All | All |
| `Victim.CasteRef / ReligionRef` | ❌ | ❌ | Aggregate only | ✅ |
| `ComplainantDetails` (excl. Caste/Religion) | Own district | All | All | All |
| `ComplainantDetails.CasteRef / ReligionRef` | ❌ | ❌ | Aggregate only | ✅ |
| `PersonEntity` and `PersonEntityLink` | Own district | All | All | All |
| `RelationshipEdge` | Own district | All | All | All |
| `RiskScore` + `FeatureImportance` | Own district | All | All | All |
| `HotspotLayer` | Own district | All | All | All |
| `AnomalyAlert` | Own district | All | All | All |
| `RAGCorpusChunk` (query) | Own district | All | All | All |
| `gov_AuditLog` | Own entries only | Own entries only | All entries | All entries |
| `gov_FairnessCheckResult` | ❌ | Read-only | Full | Full |
| `gov_DataProvenanceRecord` | ❌ | ❌ | Full | Full |
| System configuration | ❌ | ❌ | ❌ | Full |
| User management | ❌ | ❌ | ❌ | Full |

---

## 8. Resource Permission Matrix

The following matrix uses explicit permission labels. No vague terms such as "appropriate access" are used.

**Permission Labels:**
- `ALLOW` — permitted without condition
- `DENY` — never permitted
- `OWN-DISTRICT` — permitted only for records scoped to the user's DistrictID
- `OWN-STATION` — permitted only for records scoped to the user's assigned stations
- `ASSIGNED-CASES` — permitted only for cases explicitly assigned to the user
- `OWN-ACTIONS` — user can see only audit entries they themselves generated
- `AGG-ONLY` — aggregated counts only; no individual-level records
- `READ-ONLY` — view is permitted; create, update, delete are denied
- `APPROVAL-REQUIRED` — action is permitted but requires a second authorisation step

| Resource | Action | INVESTIGATOR | SCRB_ANALYST | COMPLIANCE | ADMIN |
|----------|--------|:---:|:---:|:---:|:---:|
| **FIR / CaseMaster** | Create | OWN-DISTRICT | DENY | DENY | ALLOW |
| | Read | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| | Search | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| | Update (status only) | DENY | ALLOW | DENY | ALLOW |
| | Archive | DENY | DENY | DENY | APPROVAL-REQUIRED |
| | Delete | DENY | DENY | DENY | APPROVAL-REQUIRED |
| **FIR Upload** | Upload document | OWN-DISTRICT | DENY | DENY | ALLOW |
| | View extracted entities | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| | Approve / reject extracted entities | OWN-DISTRICT | DENY | DENY | ALLOW |
| **Persons (Accused, Victim, Complainant)** | Create | OWN-DISTRICT | DENY | DENY | ALLOW |
| | Read (excl. restricted fields) | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| | Read CasteRef / ReligionRef | DENY | DENY | AGG-ONLY | ALLOW |
| | Search | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| | Update | DENY | DENY | DENY | ALLOW |
| **PersonEntity (resolved)** | Read | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| | Approve / reject merge | OWN-DISTRICT | DENY | DENY | ALLOW |
| | Search | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| **Vehicles** | Create | OWN-DISTRICT | DENY | DENY | ALLOW |
| | Read | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| | Search | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| **RelationshipEdge (graph)** | Read | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| | Shortest path traversal | DENY | ALLOW | DENY | ALLOW |
| **Evidence metadata** | Create | ASSIGNED-CASES | DENY | DENY | ALLOW |
| | Read | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| | Update | ASSIGNED-CASES | DENY | DENY | ALLOW |
| | Delete | DENY | DENY | DENY | APPROVAL-REQUIRED |
| **Investigation notes** | Create | ASSIGNED-CASES | DENY | DENY | ALLOW |
| | Read | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| | Update | ASSIGNED-CASES | DENY | DENY | ALLOW |
| **AI analysis (NER extraction)** | View | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| | Approve / reject | OWN-DISTRICT | DENY | DENY | ALLOW |
| **RiskScore + FeatureImportance** | Read | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| | Trigger recompute | DENY | ALLOW | DENY | ALLOW |
| **HotspotLayer** | Read | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| **AnomalyAlert** | Read | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| **RAG query (Ask Berunda)** | Query | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| **Reports** | Generate | DENY | ALLOW | ALLOW (restricted-field aggregate reports only) | ALLOW |
| | Export | DENY | ALLOW | ALLOW (aggregate only) | ALLOW |
| **gov_AuditLog** | Read | OWN-ACTIONS | OWN-ACTIONS | ALLOW | ALLOW |
| | Search | OWN-ACTIONS | OWN-ACTIONS | ALLOW | ALLOW |
| | Delete / modify | DENY | DENY | DENY | DENY |
| **gov_FairnessCheckResult** | Read | DENY | READ-ONLY | ALLOW | ALLOW |
| **gov_DataProvenanceRecord** | Read | DENY | DENY | ALLOW | ALLOW |
| **Police stations (Units)** | Read | OWN-DISTRICT | ALLOW | ALLOW | ALLOW |
| **System configuration** | Read | DENY | DENY | DENY | ALLOW |
| | Update | DENY | DENY | DENY | ALLOW |
| **User management** | Create / update / delete | DENY | DENY | DENY | ALLOW |
| | Assign roles | DENY | DENY | DENY | ALLOW |
| **Health / Info endpoints** | Read | ALLOW | ALLOW | ALLOW | ALLOW |

---

## 9. Role Hierarchy

```
ADMIN
  ├── Full access to all resources and all districts
  ├── Manages users and roles
  └── Authorises destructive actions (with approval)

COMPLIANCE
  ├── Full audit log access (all users, all districts)
  ├── Access to restricted CasteRef/ReligionRef fields (aggregate only)
  ├── Fairness check results (full)
  └── Data provenance records (full)

SCRB_ANALYST
  ├── Read access to all case data (all districts)
  ├── Can trigger risk score recompute
  ├── Shortest-path graph traversal
  ├── Report generation and export
  └── Audit log: own actions only

INVESTIGATOR
  ├── Full FIR workflow (own district)
  ├── Entity resolution merge approval (own district)
  ├── Risk score view (own district)
  ├── Ask Berunda (own district scope)
  └── Audit log: own actions only
```

No role inherits from another role. Each role's permissions are defined independently. A user may hold only one role at a time.

---

## 10. Station and Case Access Boundaries

### 10.1 Jurisdiction Scoping

| Role | Scoping Rule | Database Implementation |
|------|-------------|------------------------|
| INVESTIGATOR | Records where `CaseMaster.PoliceStationRef` is in `user.assigned_stations` | Extracted from `Employee.UnitRef` linked to JWT subject |
| SCRB_ANALYST | No jurisdiction filter — all records visible | No WHERE clause on district |
| COMPLIANCE | No jurisdiction filter — all records visible | No WHERE clause on district |
| ADMIN | No jurisdiction filter — all records visible | No WHERE clause on district |

### 10.2 Assigned-Case Scoping

Investigation note creation and evidence metadata creation are scoped to cases assigned to the officer. In Phase 1, case assignment is represented by a field in the FIR (investigating officer ID). In Phase 2, a formal case assignment table will be introduced.

### 10.3 Sensitive Evidence

Evidence files stored in Catalyst Stratus are access-controlled at the object level. Only the officer who uploaded the file and ADMIN can download raw evidence files. Metadata is readable by district scope.

### 10.4 AI-Generated Information

AI-generated content (NER suggestions, entity resolution proposals, risk scores, RAG answers) follows the same access boundaries as the underlying data. An INVESTIGATOR who cannot see a case cannot see AI output about that case. There is no separate AI-content access tier.

### 10.5 Exported Reports

Exported reports are generated in-session and not stored as persistent downloadable files in the MVP. The generating user's audit log records the export action. In Phase 2, reports will be stored in Catalyst Stratus with per-role download controls.

### 10.6 Demo Data

Demo data is labelled `SYNTHETIC` in all views. Demo administrator has ADMIN role. Demo role-switching is performed by logging out and logging in as a different demo user — there is no in-session role-switching feature in the MVP.

---

## 11. Separation-of-Duties Considerations

| Concern | Design Choice |
|---------|---------------|
| Investigation vs audit oversight | INVESTIGATOR cannot read the full audit log; COMPLIANCE cannot create or update case records |
| AI model control vs data access | ADMIN manages system configuration; SCRB_ANALYST can trigger model recompute but cannot change configuration |
| Case creation vs approval | In Phase 1, there is no separate approval workflow for FIR creation; the officer creates and submits. A supervisor-approval workflow is Phase 2. |
| Protected-field access | CasteRef/ReligionRef are inaccessible to INVESTIGATOR and SCRB_ANALYST; COMPLIANCE can access aggregate counts only; ADMIN has full access for system management |
| Audit log immutability | No role — including ADMIN — may delete or modify audit log entries |

---

## 12. Audit Requirements by Role Action

| Action | Audit Event Generated | Who Can See It |
|--------|----------------------|----------------|
| User login | `AUTH.LOGIN` | COMPLIANCE, ADMIN |
| FIR created | `FIR.CREATE` with case ID | COMPLIANCE, ADMIN, own user |
| FIR document uploaded | `FIR.UPLOAD` with file hash | COMPLIANCE, ADMIN, own user |
| AI extraction viewed | `AI.EXTRACTION.VIEW` with case ID | COMPLIANCE, ADMIN, own user |
| AI extraction approved | `AI.EXTRACTION.APPROVE` | COMPLIANCE, ADMIN, own user |
| AI extraction rejected | `AI.EXTRACTION.REJECT` | COMPLIANCE, ADMIN, own user |
| Entity merge approved | `ENTITY.MERGE.APPROVE` with confidence | COMPLIANCE, ADMIN, own user |
| Entity merge rejected | `ENTITY.MERGE.REJECT` | COMPLIANCE, ADMIN, own user |
| Person record read | `PERSON.READ` with person ID | COMPLIANCE, ADMIN, own user |
| Risk score viewed | `RISK.VIEW` with score + feature importance | COMPLIANCE, ADMIN, own user |
| Ask Berunda query | `RAG.QUERY` with question (not answer) | COMPLIANCE, ADMIN, own user |
| Restricted field accessed | `RESTRICTED.FIELD.ACCESS` with field name | COMPLIANCE, ADMIN |
| Report exported | `REPORT.EXPORT` with report type | COMPLIANCE, ADMIN, own user |
| User created / role changed | `ADMIN.USER.CREATE` / `ADMIN.ROLE.CHANGE` | COMPLIANCE, ADMIN |

---

## 13. Unresolved Authorization Questions

The following authorization decisions must be made before the items listed in "Blocked Work" can be implemented.

| AQ-ID | Question | Blocked Work | Target Resolved By |
|-------|---------|-------------|-------------------|
| AQ-001 | Can an INVESTIGATOR access cases from another district if formally cross-assigned? | Cross-district assignment feature | Phase 2 design |
| AQ-002 | Should SHO have a distinct system role with additional case-assignment permissions, or stay in INVESTIGATOR role with UI differentiation? | SHO-specific UI | Phase 2 design |
| AQ-003 | Should evidence file download require a separate MFA step in MVP, or is the standard JWT session sufficient? | Evidence download endpoint | Day 3 |
| AQ-004 | Should the SCRB_ANALYST be able to approve or reject entity resolution merges across all districts, or only ADMIN? | Entity resolution merge UI | Day 4 |
| AQ-005 | What is the aggregate-only access model for COMPLIANCE and restricted CasteRef/ReligionRef fields? (e.g., must show only district-level counts, never individual records) | Statutory report feature | Day 3 |
| AQ-006 | How should the demo role-switching work during judging — separate login sessions, or a demo mode in the UI? | Demo preparation | Day 10 |

---

## 14. Implications for Implementation

### Frontend

- Navigation and feature visibility must be role-gated at the component level
- Protected routes must check the role from the JWT before rendering
- CasteID/ReligionID fields must not appear in any form or display component accessible to INVESTIGATOR or SCRB_ANALYST
- Risk score feature importance must be visible to all roles who can view the risk score
- Role-specific dashboards: INVESTIGATOR sees case-list + investigation tools; SCRB_ANALYST sees state command view; COMPLIANCE sees fairness + audit log; ADMIN sees system panel

> [!IMPORTANT]
> Frontend role-gating is a convenience layer only. It must NOT be the sole enforcement mechanism. Backend must independently verify role on every API request.

### Backend

- Every API endpoint must verify the JWT role claim before processing the request
- Jurisdiction scoping (DistrictID filter) must be applied in the service layer, not in the frontend or URL path
- Restricted field columns (CasteRef, ReligionRef) must be excluded from ORM query results for non-COMPLIANCE roles at the query level, not the serialisation level
- Audit log must be written before the response is returned — not asynchronously (to prevent audit loss on timeout)

### Database

- `gov_AuditLog` must have no UPDATE or DELETE permissions at the application user level
- `CasteRef` and `ReligionRef` columns on `Accused`, `Victim`, and `ComplainantDetails` must be excluded from default field selections
- Row-level security (filtering by DistrictID) must be implemented in the service layer for INVESTIGATOR role

### AI

- RAG query results must be scoped to the requesting user's district access; the RAG corpus must not return content from cases the user cannot access
- Entity resolution merge suggestions must be presented as proposals only; approval requires an officer action
- Risk score results must not include CasteRef or ReligionRef in feature importance — verified by fairness check

---

*End of 02-STAKEHOLDERS-AND-USER-ROLES.md*
