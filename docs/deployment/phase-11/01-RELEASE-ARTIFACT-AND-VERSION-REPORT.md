# Release Artifact and Version Report (Phase 11)

**Document ID:** BERUNDA-DEPLOY-11-001  
**Phase:** 11 — Deploy to Zoho Catalyst  
**Status:** COMPLETE  

---

## 1. Deployed Commit & Build Version

- **Repository:** `https://github.com/Arun1122007/Berunda.git`
- **Branch:** `main`
- **Release Version:** `v2.0.0-catalyst-release`
- **Build Timestamp:** 2026-07-26 (UTC/IST)

---

## 2. Artifact Package Summary

1. **Backend Package (`appsail/`):**
   - Main entry point: `appsail/main.py`
   - Configured start command: `uvicorn main:app --host 0.0.0.0 --port 8000`
   - Verified dependencies loaded via `requirements.txt`.
2. **Frontend Package (`public/`):**
   - Built distribution files linked to Catalyst static hosting configuration (`catalyst.json`).
3. **Database Migration Scripts:**
   - Schema creation and update scripts staged in `database/migrations/`.
