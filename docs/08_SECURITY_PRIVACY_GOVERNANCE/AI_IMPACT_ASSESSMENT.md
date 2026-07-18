# AI Impact Assessment

[//]: # (Document ID: BERUNDA-SEC-005 | Version: 1.0 | Status: DRAFT | Classification: CONFIDENTIAL | Owner: Berunda Team | Audience: Governance, Compliance | Source: 01_Enterprise_Blueprint §12 + SRS security/privacy reqs | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Purpose

This AI Impact Assessment evaluates the ethical and societal implications of Berunda's AI capabilities. It follows the principles established in RESPONSIBLE_AI_AND_HUMAN_OVERSIGHT.md.

## 2. AI Capability Inventory

| Capability | Impact Level | Human Oversight | Automation |
|-----------|-------------|-----------------|------------|
| NER entity extraction from FIR narrative | LOW | Optional (review) | Full |
| Entity resolution (cross-case person matching) | MEDIUM | Required (grey zone) | Partial (high confidence only) |
| Repeat-offender risk scoring | MEDIUM | Required (review explanation) | Full (advisory) |
| Anomaly/spike detection | LOW | Required (review alert) | Full (advisory) |
| RAG natural language query | LOW | Optional (verify citations) | Full (advisory) |

## 3. Impact Assessment per Capability

### 3.1 NER Entity Extraction

| Dimension | Assessment |
|-----------|-----------|
| **Beneficiaries** | Investigators, analysts — reduced manual data entry |
| **Potential harm** | Missed entities due to NER inaccuracy |
| **Mitigation** | Confidence scoring; entities below threshold flagged for review |
| **Fairness** | English-only in Phase 1; Kannada NER in STRETCH |
| **Transparency** | NER tool labels extracted entities with confidence |

### 3.2 Entity Resolution

| Dimension | Assessment |
|-----------|-----------|
| **Beneficiaries** | Investigators — hidden link discovery |
| **Potential harm** | False match merges distinct persons; false negative misses real link |
| **Mitigation** | Grey zone requires human review; confidence threshold is configurable |
| **Fairness** | Rule-based approach uses only name, age, address — not caste/religion |
| **Transparency** | Per-feature similarity breakdown shown to reviewer |

### 3.3 Risk Scoring

| Dimension | Assessment |
|-----------|-----------|
| **Beneficiaries** | Investigators — prioritization of high-risk persons |
| **Potential harm** | False positive labels a person as high risk incorrectly; false negative misses a genuine repeat offender |
| **Mitigation** | Advisory only; feature importance shown; human must review before action; no automated enforcement |
| **Fairness** | CasteID/ReligionID hard-excluded; proxy variable monitoring; district-aware evaluation |
| **Transparency** | Full feature importance; model version tracked; explainability panel in UI |

### 3.4 Anomaly Detection

| Dimension | Assessment |
|-----------|-----------|
| **Beneficiaries** | SCRB analysts — early warning of crime spikes |
| **Potential harm** | False alarm consumes analyst time; missed spike delays response |
| **Mitigation** | Z-score threshold configurable; analyst reviews before any action |
| **Fairness** | District-aware; no demographic profiling |

### 3.5 RAG

| Dimension | Assessment |
|-----------|-----------|
| **Beneficiaries** | All users — natural-language access to case data |
| **Potential harm** | Hallucinated answers; PII leakage through prompt injection |
| **Mitigation** | Retrieval-before-generation; citation required; insufficient-evidence response; role-aware filtering |
| **Fairness** | No caste/religion data in RAG corpus |
| **Transparency** | Citations shown; "AI-generated" label |

## 4. Cumulative Risk Assessment

| Risk | Level | Mitigation |
|------|-------|------------|
| Profiling based on AI-derived risk scores | MEDIUM | Advisory only; human review required; feature importance visible |
| Entity resolution creating a surveillance profile | LOW | PersonEntity only within FIR context; no external data |
| RAG hallucination leading to incorrect investigative action | MEDIUM | Citation requirement; insufficient-evidence fallback; human in loop |
| Bias amplification from synthetic training data | LOW | Synthetic data is balanced by design; real-world retraining would require new assessment |

## 5. Human Oversight Summary

| Capability | What Human Does | Frequency | Escalation |
|-----------|----------------|-----------|------------|
| Entity resolution | Review grey-zone matches; confirm or reject | Per match | N/A |
| Risk scoring | Review score + feature importance before action | Per person reviewed | Flag to SCRB Analyst if score > 0.90 |
| Anomaly detection | Review alert details; decide on action | Per alert (daily expected: 0-5) | N/A |
| RAG | Verify citations if doubt | As needed | N/A |

## 6. Governance Recommendations

| Recommendation | Owner | Timeline |
|---------------|-------|----------|
| Establish a human review SLA for grey-zone ER decisions (< 24h) | Team lead | Day 5 of development |
| Create a risk score "champion/challenger" comparison for Phase 2 | Developer | Phase 2 |
| Conduct a bias audit on risk scores across districts and genders | Compliance | Before public demo |
| Monitor proxy variables for caste/religion in model features | Developer + Compliance | Per model version |
| Document all retraining events and model version changes | Developer | Continuous |
