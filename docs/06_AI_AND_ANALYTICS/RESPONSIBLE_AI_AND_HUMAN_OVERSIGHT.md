# Responsible AI and Human Oversight

[//]: # (Document ID: BERUNDA-AI-006 | Status: APPROVED | Classification: CONFIDENTIAL)

---

## 1. Principles

Berunda's AI capabilities operate under five responsible-AI principles:

| Principle | Application | Enforcement |
|-----------|-------------|-------------|
| **Fairness** | No predictive model uses caste, religion, or demographic identity features | Hard feature exclusion + automated fairness check (FC-001, FC-002) |
| **Explainability** | Every AI output includes a rationale or feature importance breakdown | Risk scores include feature importance; RAG answers include citations |
| **Human Oversight** | No AI output results in an automated action without human review | Entity resolution grey zone requires manual confirm; risk scores are advisory only |
| **Accountability** | Every AI-assisted decision is traceable to the human who reviewed it | gov_AuditLog records all AI output reviews + reviewer identity |
| **Transparency** | Users are informed when they are viewing AI-generated content | Badge/label on AI-generated content: "AI-assisted — Verify before acting" |

## 2. Human-in-the-Loop Controls

| AI Capability | Automation Level | Human Role | When Human Required |
|--------------|-----------------|------------|-------------------|
| NER extraction | Fully automated | Review only (if desired) | Never — NER is preprocessing |
| Entity resolution (high confidence) | Automated link | Informed of auto-link | Never — confidence > 0.85 |
| Entity resolution (grey zone) | Proposed match | Confirm or reject | Always — score 0.50-0.85 |
| Risk scoring | Fully automated | Review score + feature importance | Never — advisory output |
| Anomaly detection | Fully automated | Review alert details | Never — advisory output |
| RAG Q&A | Fully automated | Verify citations | Never — advisory output |
| Merge confirm | Manual only | Human clicks confirm | Always — only human can merge |

## 3. Prohibited Use Cases

The following use cases are explicitly prohibited for Berunda AI in Phase 1:

| Use Case | Reason | Enforcement |
|----------|--------|-------------|
| Caste/religion-based profiling | Discriminatory, illegal per ADR-007 | Hard feature exclusion from all models |
| Automated arrest/release recommendations | Unauthorized, high-risk decision | No model output type supports this |
| Sentencing recommendations | Outside scope, judicial function | Not implemented |
| Facial recognition or biometric matching | Not in scope, privacy concerns | No image data in MVP |
| Predictive policing at individual level | Ethical concerns, biased outcomes | Model operates at person-level, not area-level prediction |
| Automated alert dispatch without human review | Safety risk | All alerts require human review before action |

## 4. Explainability Requirements

| AI Output | Explanation Format | Visible To |
|-----------|-------------------|------------|
| Risk score | Feature importance bar chart (top N features by weight) | Investigator + SCRB Analyst |
| Entity resolution match | Per-feature similarity breakdown + overall score | Investigator |
| Anomaly alert | Observed vs expected count, z-score, rolling baseline period | SCRB Analyst |
| RAG answer | Source chunk citations (CaseNo + CrimeNo) | All users |
| Fairness check | Pass/fail per check, feature list audit | Compliance Officer |

## 5. Audit Trail Requirements

| Event | Audit Log Action | Data Captured |
|-------|-----------------|---------------|
| NER entity extracted | NER_EXTRACT | PersonEntityLink records created |
| Entity resolution auto-link | ER_AUTO_LINK | Source record → PersonEntity |
| Entity resolution manual confirm | ER_MANUAL_CONFIRM | Reviewer ID, timestamp |
| Entity resolution manual reject | ER_MANUAL_REJECT | Reviewer ID, timestamp |
| Risk score computed | RISK_SCORE_COMPUTE | PersonEntityID, Score, ModelVersion |
| Risk score viewed | RISK_SCORE_VIEW | User ID, PersonEntityID |
| RAG query executed | RAG_QUERY | Question, retrieved chunks, answer |
| Fairness check run | FAIRNESS_CHECK | Check type, pass/fail, details |
| Person record accessed | PERSON_READ | User ID, PersonEntityID |

## 6. Bias Monitoring Plan

| Bias Type | Monitoring Strategy | Frequency | Remediation |
|-----------|-------------------|-----------|-------------|
| Gender bias in risk scores | Compare score distributions by gender | Per model version | Rebalance training data or add fairness constraint |
| District bias in risk scores | Compare score distributions by district | Per model version | Add district-balanced training sampling |
| Socioeconomic proxy bias | Monitor feature importance of location-based features | Per model version | Review for proxy variables; exclude if found |
| NER accuracy by name origin | Compare precision/recall for Kannada vs. English names | Per training dataset | Add more Kannada name examples to training data |

## 7. Versioning and Audit of AI Config

| Config Item | Versioned? | Stored Where | Audited? |
|-------------|-----------|-------------|----------|
| Entity resolution thresholds | Yes | Catalyst Cache (with version key) | Changes logged to gov_AuditLog |
| Entity resolution weights | Yes | Catalyst Cache (with version key) | Changes logged to gov_AuditLog |
| Risk scoring model | Yes | Catalyst Stratus (model registry) | Model version in model card |
| RAG prompt template | Yes | Catalyst Function (code) | Code versioned in git |
| Feature allowlist | Yes | Code (hardcoded checked list) | Code review required for changes |

## 8. Synthetic Data Disclosure

Every system component that surfaces AI-generated content includes the following disclosure:

| Location | Disclosure |
|----------|------------|
| Risk score detail panel | "AI-assisted score — Review feature importance before acting" |
| Entity resolution pending review | "AI-proposed match — Requires human confirmation" |
| RAG answer footer | "Answer generated from synthetic demo corpus. Not based on real case data." |
| Anomaly alert sidebar | "AI-detected anomaly — Review context before action" |
| Fairness check report | "Automated fairness check — Results verified by Compliance Officer" |
