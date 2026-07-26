# Project Berunda — Catalyst Stratus Storage & Operations

> **Document ID:** BERUNDA-DEP-005 | **Version:** 1.0  

---

## 1. Bucket Specifications

| Bucket Name | Access Policy | MIME Restrictions | Purpose |
| :--- | :---: | :--- | :--- |
| `berunda-data` | Private | PDF, DOCX, TXT, PNG, JPG | Original FIR document uploads |
| `berunda-artifacts` | Private | JSON, CSV, BIN | AI model artifacts & graph exports |
| `berunda-reports` | Private | PDF, CSV | Generated official investigation reports |

---

## 2. Security Safeguards

- **Access Scope:** All buckets are private. Download access requires authorized JWT token.
- **Path Traversal Protection:** File names are sanitized and assigned server-generated UUIDs.
- **Upload Validation:** Extension, file size (< 25MB), and MIME type are strictly validated.
