# Security and Privacy Report

> **Generated:** 2026-07-26T17:23:33Z
> **Scanner:** scan_sensitive_data.py

---

## Result: ⚠️ 54 FILE(S) WITH FINDINGS

> [!WARNING]
> Review each finding below. Not all matches are real PII —
> some may be false positives (e.g., random 12-digit numbers).

### `data\actual_catalyst_schema.json`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 646 | 291 | `48591000000026960`, `48591000000031697`, `48591000000028826` |

### `data\evaluation\fir-extraction-evaluation.jsonl`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Indian Phone (+91) | 2 | 1 | `9876543210` |
| Vehicle Registration (KA) | 2 | 1 | `KA-01-AB-1234` |
| Bank Account (long number) | 2 | 1 | `9876543210` |

### `data\evaluation\related-case-evaluation.jsonl`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 2 | 1 | `KA-02-MM-1111` |

### `data\evaluation\summarization-evaluation.jsonl`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Indian Phone (+91) | 2 | 1 | `9876543210` |
| Bank Account (long number) | 2 | 1 | `9876543210` |

### `data\interim\SYNTHETIC_CaseMaster_demo_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 4004 | 2054 | `100050023202500013`, `100070036202400002`, `100220088202400004` |

### `data\interim\SYNTHETIC_CaseMaster_demo_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 4004 | 2054 | `100050023202500013`, `100070036202400002`, `100220088202400004` |

### `data\interim\SYNTHETIC_CaseMaster_demo_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 4004 | 2054 | `100050023202500013`, `100070036202400002`, `100220088202400004` |

### `data\interim\SYNTHETIC_CaseMaster_demo_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 4004 | 2054 | `100050023202500013`, `100070036202400002`, `100220088202400004` |

### `data\interim\SYNTHETIC_CaseMaster_smoke_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100040014202500001`, `100260101202500002`, `100250098202300001` |

### `data\interim\SYNTHETIC_CaseMaster_smoke_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100040014202500001`, `100260101202500002`, `100250098202300001` |

### `data\interim\SYNTHETIC_CaseMaster_smoke_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100040014202500001`, `100260101202500002`, `100250098202300001` |

### `data\interim\SYNTHETIC_CaseMaster_smoke_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100040014202500001`, `100260101202500002`, `100250098202300001` |

### `data\interim\SYNTHETIC_ComplainantDetails_demo_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `1007 8894 9832`, `9423 9604 8470`, `8333 5033 2712` |
| PAN Card | 635 | 635 | `SSULS4919E`, `QRCMX5356D`, `UCGKM1819U` |

### `data\interim\SYNTHETIC_ComplainantDetails_demo_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `1007 8894 9832`, `9423 9604 8470`, `8333 5033 2712` |
| PAN Card | 635 | 635 | `SSULS4919E`, `QRCMX5356D`, `UCGKM1819U` |

### `data\interim\SYNTHETIC_ComplainantDetails_demo_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `1007 8894 9832`, `9423 9604 8470`, `8333 5033 2712` |
| PAN Card | 635 | 635 | `SSULS4919E`, `QRCMX5356D`, `UCGKM1819U` |

### `data\interim\SYNTHETIC_ComplainantDetails_demo_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `1007 8894 9832`, `9423 9604 8470`, `8333 5033 2712` |
| PAN Card | 635 | 635 | `SSULS4919E`, `QRCMX5356D`, `UCGKM1819U` |

### `data\interim\SYNTHETIC_ComplainantDetails_smoke_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `3938 4656 9450`, `1815 2038 7542`, `6870 1960 8871` |
| PAN Card | 62 | 62 | `GJECF6623K`, `UZRTS2854U`, `UDCBB7183L` |

### `data\interim\SYNTHETIC_ComplainantDetails_smoke_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `3938 4656 9450`, `1815 2038 7542`, `6870 1960 8871` |
| PAN Card | 62 | 62 | `GJECF6623K`, `UZRTS2854U`, `UDCBB7183L` |

### `data\interim\SYNTHETIC_ComplainantDetails_smoke_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `3938 4656 9450`, `1815 2038 7542`, `6870 1960 8871` |
| PAN Card | 62 | 62 | `GJECF6623K`, `UZRTS2854U`, `UDCBB7183L` |

### `data\interim\SYNTHETIC_ComplainantDetails_smoke_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `3938 4656 9450`, `1815 2038 7542`, `6870 1960 8871` |
| PAN Card | 62 | 62 | `GJECF6623K`, `UZRTS2854U`, `UDCBB7183L` |

### `data\interim\SYNTHETIC_VehicleLink_demo_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-19-HA-2116`, `KA-09-GF-4644`, `KA-02-GH-7809` |

### `data\interim\SYNTHETIC_VehicleLink_demo_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-19-HA-2116`, `KA-09-GF-4644`, `KA-02-GH-7809` |

### `data\interim\SYNTHETIC_VehicleLink_demo_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-19-HA-2116`, `KA-09-GF-4644`, `KA-02-GH-7809` |

### `data\interim\SYNTHETIC_VehicleLink_demo_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-19-HA-2116`, `KA-09-GF-4644`, `KA-02-GH-7809` |

### `data\interim\SYNTHETIC_VehicleLink_smoke_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-04-EC-2336`, `KA-27-BC-7714`, `KA-09-AD-6634` |

### `data\interim\SYNTHETIC_VehicleLink_smoke_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-04-EC-2336`, `KA-27-BC-7714`, `KA-09-AD-6634` |

### `data\interim\SYNTHETIC_VehicleLink_smoke_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-04-EC-2336`, `KA-27-BC-7714`, `KA-09-AD-6634` |

### `data\interim\SYNTHETIC_VehicleLink_smoke_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-04-EC-2336`, `KA-27-BC-7714`, `KA-09-AD-6634` |

### `data\processed\SYNTHETIC_CaseMaster_demo_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 4004 | 2054 | `100050023202500013`, `100070036202400002`, `100220088202400004` |

### `data\processed\SYNTHETIC_CaseMaster_smoke_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100040014202500001`, `100260101202500002`, `100250098202300001` |

### `data\processed\SYNTHETIC_ComplainantDetails_demo_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `1007 8894 9832`, `9423 9604 8470`, `8333 5033 2712` |
| PAN Card | 635 | 635 | `SSULS4919E`, `QRCMX5356D`, `UCGKM1819U` |

### `data\processed\SYNTHETIC_ComplainantDetails_smoke_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `3938 4656 9450`, `1815 2038 7542`, `6870 1960 8871` |
| PAN Card | 62 | 62 | `GJECF6623K`, `UZRTS2854U`, `UDCBB7183L` |

### `data\processed\SYNTHETIC_VehicleLink_demo_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-19-HA-2116`, `KA-09-GF-4644`, `KA-02-GH-7809` |

### `data\processed\SYNTHETIC_VehicleLink_smoke_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-04-EC-2336`, `KA-27-BC-7714`, `KA-09-AD-6634` |

### `data\raw\RSRC-003\promotions_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Email Address | 10 | 6 | `jason.c@zylker.com`, `p.boyle@zylker.com`, `mahesh.annamalai@zohotest.com` |
| Credit Card (16 digits) | 30 | 19 | `1510000000109545`, `1510000000109474`, `2823000000014176` |
| Bank Account (long number) | 38 | 26 | `1510000000109545`, `1510000000109474`, `2823000000014176` |

**Secrets Patterns:**

| Pattern | Matches | Note |
|---------|---------|------|
| Generic Secret | 1 | Potential credential — verify manually |

### `data\raw\RSRC-012\R006_resource_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 1 | 1 | `237745130315` |
| Bank Account (long number) | 4 | 3 | `553852000000003`, `237745130315`, `20231028004` |

### `data\raw\RSRC-014\R008_resource_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 1 | 1 | `999999999999` |
| Email Address | 2 | 2 | `pd.webportal@karnataka.gov.in`, `police@ksp.gov.in` |
| Bank Account (long number) | 18 | 9 | `1704973538`, `1784199653`, `1784199622` |

### `data\raw\RSRC-023\overpass_karnataka_police_20260718.json`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 3 | 3 | `918155286720`, `918022943469`, `914972771093` |
| Indian Phone (+91) | 829 | 725 | `9789766150`, `9830938826`, `8329608964` |
| Email Address | 7 | 7 | `kl72@keralamvd.gov.in`, `devarajamyc@ksp.gov.in`, `mandimyc@ksp.gov.in` |
| Indian Passport | 1 | 1 | `Q4855039` |
| Bank Account (long number) | 2616 | 2332 | `377600336`, `13152185641`, `9830938826` |

### `data\raw\RSRC-032\openmeteo_bengaluru_2025_20260718.json`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 1 | 1 | `83825302124023` |

### `data\raw\RSRC-038\R020_resource_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 62 | 2 | `123456789`, `121785794` |

### `data\raw\RSRC-038\indiacode_bns_page_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 46 | 2 | `123456789`, `121785794` |

### `data\raw\RSRC-039\R021_resource_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 62 | 2 | `123456789`, `121785794` |

### `data\raw\RSRC-041\R022_resource_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 62 | 2 | `123456789`, `121785794` |

### `data\raw\RSRC-080\owasp_asvs_page_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 2 | 2 | `950526877`, `20250000000000` |

### `data\raw\RSRC-081\owasp_api_security_top10_page_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 1 | 1 | `214075229` |

### `data\raw\RSRC-082\nist_csf_page_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 3 | 2 | `1134161994`, `1089704227` |

### `data\raw\RSRC-083\nist_ai_main_page_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 13 | 3 | `1134161994`, `1089704227`, `1776955625841` |

### `data\raw\RSRC-083\nist_ai_rmf_page_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 3 | 2 | `1134161994`, `1089704227` |

### `data\synthetic\SYNTHETIC_CaseMaster_demo_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 4004 | 2054 | `100050023202500013`, `100070036202400002`, `100220088202400004` |

### `data\synthetic\SYNTHETIC_CaseMaster_smoke_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100040014202500001`, `100260101202500002`, `100250098202300001` |

### `data\synthetic\SYNTHETIC_ComplainantDetails_demo_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `1007 8894 9832`, `9423 9604 8470`, `8333 5033 2712` |
| PAN Card | 635 | 635 | `SSULS4919E`, `QRCMX5356D`, `UCGKM1819U` |

### `data\synthetic\SYNTHETIC_ComplainantDetails_smoke_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `3938 4656 9450`, `1815 2038 7542`, `6870 1960 8871` |
| PAN Card | 62 | 62 | `GJECF6623K`, `UZRTS2854U`, `UDCBB7183L` |

### `data\synthetic\SYNTHETIC_VehicleLink_demo_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-19-HA-2116`, `KA-09-GF-4644`, `KA-02-GH-7809` |

### `data\synthetic\SYNTHETIC_VehicleLink_smoke_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-04-EC-2336`, `KA-27-BC-7714`, `KA-09-AD-6634` |

