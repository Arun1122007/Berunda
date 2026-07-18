# Security and Privacy Report

> **Generated:** 2026-07-18
> **Scanner:** scan_sensitive_data.py
> **Status:** PENDING — No scans executed yet.

---

## Result: ⏳ PENDING

No files have been scanned yet. Run the scanner after downloading resources:

```bash
python scripts/validation/scan_sensitive_data.py
```

---

## Scan Coverage Plan

| Directory | Purpose | Expected PII Risk |
|-----------|---------|-------------------|
| `data/raw/` | Downloaded public data | Low (aggregate stats) |
| `data/synthetic/` | Generated fake data | None (must be SYNTHETIC-labeled) |
| `quarantine/` | Untrusted downloads | Unknown — scan before promotion |
| `boundaries/` | Geospatial layers | None (admin boundaries) |
| `repositories/` | Cloned code repos | Low (code, not data) |

---

## Privacy Design Principles Applied

1. **No real PII acquired** — all person-level data is synthetic (Faker `en_IN`)
2. **CasteID/ReligionID access-restricted** — per Enterprise Blueprint §6.2
3. **No SECC/caste-linked datasets** — explicitly excluded (Section D5)
4. **Synthetic records clearly labeled** — `SYNTHETIC_` prefix + metadata table
5. **Quarantine-first** — nothing trusted until scanned and validated

---

*This report is auto-updated by `scan_sensitive_data.py`.*
