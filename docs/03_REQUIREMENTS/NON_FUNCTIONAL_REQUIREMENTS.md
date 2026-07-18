# Non-Functional Requirements

[//]: # (Document ID: BERUNDA-NFR-001 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Developers, Architects, QA | Source: 01_Enterprise_Blueprint + SRS references | Last Verified: 2026-07-17 | Review: Monthly)

---

| ID | Category | Title | Description | Target | Priority | Scope |
|----|----------|-------|-------------|--------|----------|-------|
| NFR-001 | Performance | Dashboard Response | Dashboard pages shall load within 3 seconds under demo dataset load | <3s P95 | MUST | MVP |
| NFR-002 | Performance | Entity Resolution Latency | Entity resolution for a new person record shall complete within 5 seconds | <5s P95 | MUST | MVP |
| NFR-003 | Performance | RAG Query Latency | RAG query responses shall return within 10 seconds | <10s P95 | MUST | MVP |
| NFR-004 | Performance | Graph Traversal | Graph traversal queries shall complete within 5 seconds at demo scale | <5s P95 | MUST | MVP |
| NFR-005 | Scalability | Horizontal Scaling | Architecture shall support scaling to 1M+ records without structural redesign | Documented path | MUST | MVP |
| NFR-006 | Scalability | Data Volume | System shall handle 5000+ synthetic records for the demo | 5000 records | MUST | MVP |
| NFR-007 | Availability | Uptime | 99.5% availability target at state deployment (not MVP concern) | 99.5% | VISION | VISION |
| NFR-008 | Availability | Demo Uptime | System shall be available for the entire demo session | 100% during demo | MUST | MVP |
| NFR-009 | Security | Encryption at Rest | All data encrypted at rest using Catalyst-native encryption | AES-256 | MUST | MVP |
| NFR-010 | Security | Encryption in Transit | All communications over TLS | TLS 1.2+ | MUST | MVP |
| NFR-011 | Security | Authentication | All users authenticated via Catalyst Authentication | MFA for person-level | MUST | MVP |
| NFR-012 | Security | Authorization | RBAC with minimum 3 roles | Role enforcement | MUST | MVP |
| NFR-013 | Accessibility | Kannada UI | UI labels, filters, and navigation shall be bilingual | Kannada + English | SHOULD | MVP |
| NFR-014 | Accessibility | Kannada NLP | Kannada-language FIR narrative support | Phase 2 target | SHOULD | STRETCH |
| NFR-015 | Accessibility | Screen Reader | Dashboard components shall be navigable via keyboard | WCAG 2.1 AA | COULD | STRETCH |
| NFR-016 | Usability | Training Time | New user shall complete primary tasks within 15 minutes of first use | Within 15 min | SHOULD | MVP |
| NFR-017 | Usability | Error Messages | Error messages shall be human-readable, not technical stack traces | User-facing | MUST | MVP |
| NFR-018 | Reliability | Data Integrity | Synthetic data import shall maintain referential integrity | 100% integrity | MUST | MVP |
| NFR-019 | Reliability | Audit Completeness | Every auditable action shall produce exactly one AuditLog entry | No gaps | MUST | MVP |
| NFR-020 | Maintainability | Documentation | All API endpoints and data models shall have documentation | Complete | MUST | MVP |
| NFR-021 | Maintainability | Code Style | Code shall follow consistent conventions across the codebase | Per language standard | SHOULD | MVP |
| NFR-022 | Portability | Catalyst-Bound | System shall run entirely on Catalyst; no external dependencies that violate Catalyst mandate | Full compliance | MUST | MVP |
| NFR-023 | Portability | Open Core | Non-sensitive components shall be publishable as open source | Apache 2.0 | SHOULD | MVP |
| NFR-024 | Compliance | DPDP Act | Design shall align with DPDP Act 2023 principles | Design alignment | MUST | MVP |
| NFR-025 | Explainability | Model Transparency | Every AI score shall have a feature-importance breakdown | Always present | MUST | MVP |
| NFR-026 | Explainability | Answer Grounding | Every RAG answer shall cite source documents | Always cited | MUST | MVP |
| NFR-027 | Fairness | Feature Exclusion | CasteID/ReligionID shall never appear in any model feature set | Enforced in code | MUST | MVP |
| NFR-028 | Fairness | Parity Monitoring | Score distributions shall be monitorable across demographic groups | Read-only | SHOULD | MVP |
| NFR-029 | Human Oversight | Human-in-the-Loop | No AI output shall trigger automatic action | Always advisory | MUST | MVP |
| NFR-030 | Auditability | Audit Trail | All sensitive reads and AI outputs logged with actor, action, timestamp, justification | Complete trail | MUST | MVP |
| NFR-031 | Auditability | Log Integrity | AuditLog shall be append-only at application layer | Append-only | MUST | MVP |
