# Project Berunda — Post-Deployment Verification Report

> **Document ID:** BERUNDA-DEP-009 | **Version:** 1.0  

---

## 1. Verified End-to-End Workflows

| Test Case ID | Workflow Description | Target URL | Result | Evidence |
| :--- | :--- | :--- | :---: | :--- |
| `TC-DEP-001` | Web Client Initial Load | `https://project-rainfall-60079736152.development.catalystserverless.in/app/index.html` | ✅ PASS | UI dashboard rendered |
| `TC-DEP-002` | API Health Check | `https://berunda-api-50044292022.development.catalystappsail.in/health` | ✅ PASS | Returns `{"status":"healthy"}` |
| `TC-DEP-003` | API Readiness Check | `https://berunda-api-50044292022.development.catalystappsail.in/ready` | ✅ PASS | Returns `{"status":"ready"}` |
| `TC-DEP-004` | CORS Configuration | Preflight OPTIONS request from Web Client origin | ✅ PASS | Headers allowed |
| `TC-DEP-005` | Auth & JWT Verification | POST `/api/v1/auth/login` | ✅ PASS | Valid JWT issued |
| `TC-DEP-006` | FIR Management | GET `/api/v1/fir` | ✅ PASS | Returns FIR list |
