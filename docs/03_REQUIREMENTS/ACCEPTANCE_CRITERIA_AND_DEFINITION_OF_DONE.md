# Acceptance Criteria and Definition of Done

[//]: # (Document ID: BERUNDA-DOD-001 | Status: DRAFT | Classification: INTERNAL)

---

## Definition of Done (Per Feature)

A feature is complete when all of the following are true:

- [ ] Acceptance criteria pass (Given/When/Then format)
- [ ] All related unit tests pass
- [ ] Integration test with real data passes
- [ ] Security review: no new vulnerabilities introduced
- [ ] Privacy review: no PII exposure risks
- [ ] Audit hooks are wired and verified
- [ ] Feature is documented (API/UX/data flow)
- [ ] Demo path is rehearsed and evidence captured
- [ ] No regressions in existing features

## Acceptance Criteria by Feature

### F-001: Synthetic FIR Import

```
Given: A structured CSV/Excel file with synthetic FIR data
When: The import pipeline processes the file
Then: All records are inserted into CaseMaster with linked Accused/Victim/Complainant records
And: Referential integrity is maintained (no orphaned FK references)
And: A validation report is generated showing pass/fail counts
```

### F-002: English NER Extraction

```
Given: A synthetic FIR with an English narrative in BriefFacts
When: The NER pipeline processes the brief facts
Then: Person names, locations, and vehicles are extracted with confidence scores >= 0.5
And: Extracted entities are written to PersonEntityLink and VehicleLink tables
```

### F-003: Cross-Case Entity Resolution

```
Given: Four synthetic FIRs where one person appears under different name variants
When: Entity resolution processes each new FIR
Then: All four records resolve to the same PersonEntity
And: The match confidence for each link is recorded in PersonEntityLink
And: No auto-merge occurs without human confirmation
```

### F-004: Relationship Graph

```
Given: A PersonEntity with linked cases, co-accused, and vehicles
When: An Investigator clicks on the PersonEntity
Then: A force-directed graph renders showing all connections
And: Edge thickness is proportional to confidence score
And: Clicking a node shows the underlying case details
```

### F-005: Geospatial Hotspot Map

```
Given: Synthetic FIRs with latitude/longitude coordinates
When: The Hotspot Map dashboard is loaded
Then: A hexbin/heatmap layer is rendered over Karnataka
And: Drill-down from state → district → station works
And: Filters (crime type, date range, district) update the map
```

### F-006: Explainable Risk Score

```
Given: A PersonEntity with 3+ prior cases
When: The risk score is computed
Then: A score value is returned with a feature-importance JSON breakdown
And: The breakdown is human-readable in the Investigator Console
And: CasteID/ReligionID do NOT appear in the feature set
```

### F-007: Anomaly Detection

```
Given: A manufactured hotspot week with 3x the historical baseline
When: The anomaly detection runs
Then: An alert record is created with the deviation magnitude
And: The alert is visible on the dashboard
```

### F-008: "Ask Berunda" RAG

```
Given: A curated corpus of case summaries
When: An Investigator types "Show me all open cases linked to vehicle KA-05-XXXX"
Then: The system returns a grounded answer with source citations
And: If insufficient evidence exists, the system states "Insufficient evidence"
And: The query and answer are logged to AuditLog
```

### F-009: Auth + RBAC

```
Given: An unauthenticated user
When: They attempt to access any dashboard page
Then: They are redirected to login
And: After authentication with Investigator role, they see only their assigned jurisdiction's data
And: After authentication with Compliance role, they see the Fairness Dashboard
And: After authentication with SCRB role, they see the State Command View
```

### F-010: Audit Logging

```
Given: An Investigator views a person-level record
When: The record is loaded
Then: An AuditLog entry is created: actor ID, action "PERSON_READ", entity type, entity ID, timestamp
And: When an AI recommendation is viewed, an additional AuditLog entry is created with the justification
And: The AuditLog is queryable by the Governance Officer
```

### F-011: Fairness Check

```
Given: Risk scores have been computed
When: The Fairness Check runs
Then: The system confirms CasteID/ReligionID do not appear in any RiskScore.feature_importance
And: The system confirms that general dashboard roles cannot query CasteID/ReligionID columns
And: A green "PASS" indicator is shown on the Fairness Dashboard
```

## Feature Acceptance Gates

| Gate | Criteria | Pass/Fail |
|------|----------|-----------|
| Unit test | All component-level tests pass | Automated |
| Integration test | Feature works with real synthetic data | Automated |
| Security scan | No OWASP Top 10 violations | Tool + Review |
| Privacy check | No PII exposure in output | Review |
| Audit verification | Audit hooks fire correctly | Automated test |
| Demo rehearsal | Feature works in full demo walkthrough | Manual |
| Documentation | Feature documented in relevant docs | Review |
