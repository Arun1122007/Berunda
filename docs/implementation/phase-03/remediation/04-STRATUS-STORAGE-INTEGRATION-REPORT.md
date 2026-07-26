# Stratus Storage Integration Report

> **Document ID:** BERUNDA-REMEDIATION-004  
> **Defect:** P3V-MAJ-001  
> **Status:** CLOSED  

---

## 1. Defect Description

`FIRService` had no `FileStorage` abstraction injection. Evidence attachment creation bypassed the repository abstraction layer and did not validate file MIME types, sizes, or sanitize filenames. No audit events were emitted for evidence operations.

## 2. Remediation

### `fir_service.py` Changes

- `FileStorage` repository abstraction injected via `FIRService.__init__(self, repo, storage=None)`
- `upload_evidence()` method:
  1. Validates FIR existence via `self.repo.get_fir()`
  2. Sanitizes filename (rejects path traversal — `../`, `/`, `\`)
  3. Delegates byte storage to `self.storage.save_file()`
  4. Persists metadata to `src_EvidenceMaster` table
  5. Emits structured audit event `EVIDENCE_UPLOADED`
- `get_evidence()` method: lists all evidence records for a given FIR

### `fir_router.py` Changes

- `POST /api/v1/fir/{case_master_id}/evidence` — file upload endpoint
  - Validates MIME type against allowlist (PDF, JPEG, PNG, TIFF, DOC, DOCX, TXT, CSV, ZIP)
  - Rejects empty payloads and files exceeding 50 MB
  - Sanitizes filename (path traversal check)
  - Uses `Depends(get_file_storage)` for storage injection
- `GET /api/v1/fir/{case_master_id}/evidence` — evidence listing

### Audit Events

| Event | Source | Description |
|-------|--------|-------------|
| `EVIDENCE_UPLOADED` | `FIRService.upload_evidence` | Logged on successful upload |
| `EVIDENCE_ACCESSED` | `GET /evidence` endpoint | Logged on evidence retrieval |
| `EVIDENCE_DELETED` | Future | Available for future deletion endpoint |

## 3. Verification

- File validation: empty payload, path traversal, oversized file, unsupported MIME — all return 400
- Storage delegation: `LocalFileStorage` writes to `data/uploads/` using SHA-256 path
- Audit emission: `AuditService.log()` called with structured event data
