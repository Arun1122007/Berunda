# 10 Catalyst Staging Verification

This document verifies the operational readiness of the Catalyst Staging environment for Project Berunda.

## 1. Environment Status
- **Environment:** Catalyst Development / Staging
- **Project ID:** 48591000000013025 (Cloudscale)
- **AppSail Build Target:** `appsail/berunda_api`

## 2. Component Verification Checklist

### 2.1 Catalyst Data Store
- [x] Schema deployed (32 tables verified).
- [x] PII `audit_consent` flags configured.
- [x] `ROWID` relationships validated.
- [x] Synthentic data (`smoke` tier, 200 records) successfully imported via ZCQL bridge script.

### 2.2 Catalyst Stratus (Blob Storage)
- [ ] Staging bucket `berunda_evidence_staging` created.
- [ ] AppSail IAM permissions granted for Stratus read/write.
- [ ] PDF upload test successful.

### 2.3 Catalyst AppSail (Compute)
- [x] FastAPI build artifact created via `scripts/build_appsail.ps1`.
- [x] `app-config.json` validates `uvicorn src.main:app` command.
- [ ] Catalyst deployment command `catalyst deploy` executes without memory constraint errors (Limit: 256MB).

### 2.4 Catalyst QuickML & Zia (AI)
- [ ] QuickML RAG Knowledge Base initialized for Staging.
- [ ] Zia OCR endpoint accessible from AppSail runtime.
- [ ] External keys removed from Staging environment variables.
