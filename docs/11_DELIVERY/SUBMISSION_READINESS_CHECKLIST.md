# Submission Readiness Checklist

[//]: # (Document ID: BERUNDA-DEL-005 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Team | Source: All source documents | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Pre-Submission Checklist

### 1.1 System Checks

| # | Check | Verified? | Notes |
|---|-------|-----------|-------|
| 1 | All 27 source tables populated | ☐ | Count rows per table |
| 2 | All 11 intelligence tables populated | ☐ | Count rows per table |
| 3 | All 3 governance tables populated | ☐ | Count rows per table |
| 4 | Health endpoint returns healthy | ☐ | GET /health |
| 5 | All API endpoints respond (non-error) | ☐ | Run test suite |
| 6 | Synthetic data tag present | ☐ | Check _synthetic_data_tag table |
| 7 | "SYNTHETIC DATA" watermark visible on UI | ☐ | Visual check |
| 8 | All Cron jobs completed in last 24h | ☐ | Check Cron logs |

### 1.2 Feature Checks

| # | Feature | Verified? | Demo Evidence |
|---|---------|-----------|--------------|
| 1 | FIR import (upload + manual entry) | ☐ | Screenshot |
| 2 | Entity resolution (planted 4→1 test) | ☐ | Screenshot |
| 3 | Manual merge review | ☐ | Screenshot |
| 4 | Relationship graph (hidden link) | ☐ | Screenshot |
| 5 | Hotspot map + drill-down | ☐ | Screenshot |
| 6 | Anomaly alerts | ☐ | Screenshot |
| 7 | Risk score with feature importance | ☐ | Screenshot |
| 8 | RAG Q&A with citations | ☐ | Screenshot |
| 9 | Fairness check dashboard | ☐ | Screenshot |
| 10 | Audit log viewer | ☐ | Screenshot |
| 11 | RBAC enforcement (3 roles) | ☐ | Test script output |
| 12 | Jurisdiction scoping | ☐ | Test script output |

### 1.3 Security Checks

| # | Check | Verified? | Notes |
|---|-------|-----------|-------|
| 1 | No CasteID/ReligionID in any API response for non-Compliance role | ☐ | Automated test |
| 2 | Cross-jurisdiction access returns 403 for Investigator | ☐ | Automated test |
| 3 | No SQL injection vulnerability | ☐ | OWASP ZAP scan |
| 4 | Tokens expire correctly | ☐ | Automated test |
| 5 | Rate limiting active | ☐ | Automated test |

### 1.4 Evidence Pack

| # | Item | Generated? |
|---|------|-----------|
| 1 | Case statistics summary (PDF) | ☐ |
| 2 | Entity resolution proof (screenshot) | ☐ |
| 3 | Relationship graph (screenshot) | ☐ |
| 4 | Anomaly spike (screenshot) | ☐ |
| 5 | Risk score explanation (screenshot) | ☐ |
| 6 | RAG Q&A with citations (screenshot) | ☐ |
| 7 | Fairness check report (screenshot) | ☐ |
| 8 | Audit log sample (CSV) | ☐ |
| 9 | Planting manifest (JSON) | ☐ |
| 10 | Synthetic dataset manifest (JSON) | ☐ |

### 1.5 Submission Package

| # | Item | Ready? |
|---|------|--------|
| 1 | GitHub repository URL with source code | ☐ |
| 2 | README with setup instructions | ☐ |
| 3 | Catalyst project deployment guide | ☐ |
| 4 | Demo script (this document) | ☐ |
| 5 | Slide deck (PDF) | ☐ |
| 6 | 5-min demo video (MP4) | ☐ |
| 7 | Evidence pack (ZIP) | ☐ |
| 8 | License file (MIT recommended) | ☐ |

## 2. Submission Day Timeline

| Time | Task | Owner |
|------|------|-------|
| T-3h | Final smoke test | Both |
| T-2h | Generate evidence pack | Dev2 |
| T-1h | Package submission | Dev2 |
| T-30m | Upload to submission platform | Both |
| T-0 | Submit | Both |
| T+30m | Confirmation screenshot | Dev2 |

## 3. Post-Submission

- [ ] Confirm submission receipt from organizers
- [ ] Store submission confirmation in project docs
- [ ] Begin post-hackathon retrospective
