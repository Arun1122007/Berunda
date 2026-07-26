# Defect Register

| Defect ID | Phase | Severity | Category | File path | Section | Description | Evidence | Expected | Actual | Product impact | Arch impact | Security impact | Future impact | Required correction | Correction performed | Revalidation evidence | Blocking | Recommended owner | Final status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P123V-CRT-001 | 1 | CRITICAL | Documentation | PROBLEM_STAKEHOLDERS_AND_PERSONAS.md | Problem Statement | Missing explicit mention of unstructured FIR info and AI human review. | File inspection | Explicit constraints defined | Vague constraints | High | Med | Med | AI drift | Rewrite statement | Yes | Re-read file | No | Architect | CLOSED |
| P123V-MAJ-001 | 1 | MAJOR | Requirements | MVP_SCOPE_AND_RELEASE_PLAN.md | MVP Scope | Missing standard P0-P3 classifications. | File inspection | Matrix format | Loose table | Med | Low | Low | Scope creep | Rewrite table | Yes | Re-read file | No | Architect | CLOSED |
| P123V-MIN-001 | 2 | MINOR | API | docs/api-and-contracts/openapi.yaml | N/A | Duplicate OpenAPI spec. | File search | One authoritative file | Two files | Low | Low | Low | Confusion | Delete duplicate | Yes | File deleted | No | Architect | CLOSED |
| P123V-OBS-001 | 3 | OBSERVATION | Architecture | Multiple | N/A | PostgreSQL references remain despite Catalyst pivot. | Grep search | Clean Catalyst docs | Postgres refs | Low | Low | Low | Confusion | Document local dev exception | No | N/A | No | Architect | OPEN |
