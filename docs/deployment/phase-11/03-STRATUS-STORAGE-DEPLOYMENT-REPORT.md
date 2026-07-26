# Stratus Storage Deployment Report (Phase 11)

**Document ID:** BERUNDA-DEPLOY-11-003  
**Phase:** 11 — Deploy to Zoho Catalyst  
**Status:** COMPLETE  

---

## 1. Stratus Storage Resource Configuration

- **Bucket Name:** `berunda-evidence-bucket`
- **Access Level:** **PRIVATE** (Public access disabled at bucket and object level)
- **Folder Structure:**
  - `raw_firs/{fir_id}/original_source.pdf` — Immutable raw FIR source documents.
  - `evidence/{fir_id}/{evidence_id}.bin` — Case file evidence attachments.
  - `exports/reports/{report_id}.pdf` — Generated redacted PDF exports.
- **Upload / Download Verification:** Presigned URLs generated with 900-second TTL. Direct unauthenticated HTTP requests return 403 Forbidden.
