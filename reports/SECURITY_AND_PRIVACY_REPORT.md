# Security and Privacy Report

> **Generated:** 2026-07-23T08:20:30Z
> **Scanner:** scan_sensitive_data.py

---

## Result: ⚠️ 50 FILE(S) WITH FINDINGS

> [!WARNING]
> Review each finding below. Not all matches are real PII —
> some may be false positives (e.g., random 12-digit numbers).

### `data\interim\SYNTHETIC_CaseMaster_demo_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 4004 | 2054 | `100160068202500001`, `100050021202300008`, `100120054202400008` |

### `data\interim\SYNTHETIC_CaseMaster_demo_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 4004 | 2054 | `100160068202500001`, `100050021202300008`, `100120054202400008` |

### `data\interim\SYNTHETIC_CaseMaster_demo_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 4004 | 2054 | `100160068202500001`, `100050021202300008`, `100120054202400008` |

### `data\interim\SYNTHETIC_CaseMaster_demo_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 4004 | 2054 | `100160068202500001`, `100050021202300008`, `100120054202400008` |

### `data\interim\SYNTHETIC_CaseMaster_smoke_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100050019202300001`, `100050030202500004`, `100270105202500001` |

### `data\interim\SYNTHETIC_CaseMaster_smoke_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100050019202300001`, `100050030202500004`, `100270105202500001` |

### `data\interim\SYNTHETIC_CaseMaster_smoke_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100050019202300001`, `100050030202500004`, `100270105202500001` |

### `data\interim\SYNTHETIC_CaseMaster_smoke_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100050019202300001`, `100050030202500004`, `100270105202500001` |

### `data\interim\SYNTHETIC_ComplainantDetails_demo_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `7853 5704 3376`, `4466 7547 4837`, `1562 7503 4710` |
| PAN Card | 635 | 635 | `GQWTJ1418Q`, `HTUKX5412U`, `GKHCS1799W` |

### `data\interim\SYNTHETIC_ComplainantDetails_demo_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `7853 5704 3376`, `4466 7547 4837`, `1562 7503 4710` |
| PAN Card | 635 | 635 | `GQWTJ1418Q`, `HTUKX5412U`, `GKHCS1799W` |

### `data\interim\SYNTHETIC_ComplainantDetails_demo_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `7853 5704 3376`, `4466 7547 4837`, `1562 7503 4710` |
| PAN Card | 635 | 635 | `GQWTJ1418Q`, `HTUKX5412U`, `GKHCS1799W` |

### `data\interim\SYNTHETIC_ComplainantDetails_demo_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `7853 5704 3376`, `4466 7547 4837`, `1562 7503 4710` |
| PAN Card | 635 | 635 | `GQWTJ1418Q`, `HTUKX5412U`, `GKHCS1799W` |

### `data\interim\SYNTHETIC_ComplainantDetails_smoke_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `1498 8713 8446`, `8701 8933 2070`, `6329 3973 1445` |
| PAN Card | 62 | 62 | `KNZKZ2945V`, `UNYWP5743D`, `GETAW5610J` |

### `data\interim\SYNTHETIC_ComplainantDetails_smoke_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `1498 8713 8446`, `8701 8933 2070`, `6329 3973 1445` |
| PAN Card | 62 | 62 | `KNZKZ2945V`, `UNYWP5743D`, `GETAW5610J` |

### `data\interim\SYNTHETIC_ComplainantDetails_smoke_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `1498 8713 8446`, `8701 8933 2070`, `6329 3973 1445` |
| PAN Card | 62 | 62 | `KNZKZ2945V`, `UNYWP5743D`, `GETAW5610J` |

### `data\interim\SYNTHETIC_ComplainantDetails_smoke_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `1498 8713 8446`, `8701 8933 2070`, `6329 3973 1445` |
| PAN Card | 62 | 62 | `KNZKZ2945V`, `UNYWP5743D`, `GETAW5610J` |

### `data\interim\SYNTHETIC_VehicleLink_demo_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-04-FG-1194`, `KA-25-HF-7104`, `KA-25-EF-2004` |

### `data\interim\SYNTHETIC_VehicleLink_demo_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-04-FG-1194`, `KA-25-HF-7104`, `KA-25-EF-2004` |

### `data\interim\SYNTHETIC_VehicleLink_demo_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-04-FG-1194`, `KA-25-HF-7104`, `KA-25-EF-2004` |

### `data\interim\SYNTHETIC_VehicleLink_demo_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-04-FG-1194`, `KA-25-HF-7104`, `KA-25-EF-2004` |

### `data\interim\SYNTHETIC_VehicleLink_smoke_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-02-CA-2581`, `KA-25-GG-1987`, `KA-09-AD-6634` |

### `data\interim\SYNTHETIC_VehicleLink_smoke_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-02-CA-2581`, `KA-25-GG-1987`, `KA-09-AD-6634` |

### `data\interim\SYNTHETIC_VehicleLink_smoke_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-02-CA-2581`, `KA-25-GG-1987`, `KA-09-AD-6634` |

### `data\interim\SYNTHETIC_VehicleLink_smoke_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-02-CA-2581`, `KA-25-GG-1987`, `KA-09-AD-6634` |

### `data\processed\SYNTHETIC_CaseMaster_demo_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 4004 | 2054 | `100160068202500001`, `100050021202300008`, `100120054202400008` |

### `data\processed\SYNTHETIC_CaseMaster_smoke_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100050019202300001`, `100050030202500004`, `100270105202500001` |

### `data\processed\SYNTHETIC_ComplainantDetails_demo_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `7853 5704 3376`, `4466 7547 4837`, `1562 7503 4710` |
| PAN Card | 635 | 635 | `GQWTJ1418Q`, `HTUKX5412U`, `GKHCS1799W` |

### `data\processed\SYNTHETIC_ComplainantDetails_smoke_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `1498 8713 8446`, `8701 8933 2070`, `6329 3973 1445` |
| PAN Card | 62 | 62 | `KNZKZ2945V`, `UNYWP5743D`, `GETAW5610J` |

### `data\processed\SYNTHETIC_VehicleLink_demo_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-04-FG-1194`, `KA-25-HF-7104`, `KA-25-EF-2004` |

### `data\processed\SYNTHETIC_VehicleLink_smoke_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-02-CA-2581`, `KA-25-GG-1987`, `KA-09-AD-6634` |

### `data\raw\RSRC-003\promotions_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Email Address | 10 | 6 | `p.boyle@zylker.com`, `amelia.burrows@zylker.com`, `jason.c@zylker.com` |
| Credit Card (16 digits) | 30 | 19 | `1510000000085482`, `1510000000109474`, `2136000000034043` |
| Bank Account (long number) | 38 | 26 | `1510000000085482`, `944809860`, `81008807534807534` |

**Secrets Patterns:**

| Pattern | Matches | Note |
|---------|---------|------|
| Generic Secret | 1 | Potential credential — verify manually |

### `data\raw\RSRC-012\R006_resource_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 1 | 1 | `237745130315` |
| Bank Account (long number) | 4 | 3 | `237745130315`, `553852000000003`, `20231028004` |

### `data\raw\RSRC-014\R008_resource_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 1 | 1 | `999999999999` |
| Email Address | 2 | 2 | `pd.webportal@karnataka.gov.in`, `police@ksp.gov.in` |
| Bank Account (long number) | 18 | 9 | `1784199653`, `1749022262`, `1780900038` |

### `data\raw\RSRC-023\overpass_karnataka_police_20260718.json`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 3 | 3 | `918022943469`, `914972771093`, `918155286720` |
| Indian Phone (+91) | 829 | 725 | `9965906093`, `9789602049`, `8013123011` |
| Email Address | 7 | 7 | `Whitefieldbcp@ksp.gov.in`, `kl72@keralamvd.gov.in`, `devarajamyc@ksp.gov.in` |
| Indian Passport | 1 | 1 | `Q4855039` |
| Bank Account (long number) | 2616 | 2332 | `12528658871`, `11302388482`, `4058224793` |

### `data\raw\RSRC-032\openmeteo_bengaluru_2025_20260718.json`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 1 | 1 | `83825302124023` |

### `data\raw\RSRC-038\R020_resource_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 62 | 2 | `121785794`, `123456789` |

### `data\raw\RSRC-038\indiacode_bns_page_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 46 | 2 | `121785794`, `123456789` |

### `data\raw\RSRC-039\R021_resource_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 62 | 2 | `121785794`, `123456789` |

### `data\raw\RSRC-041\R022_resource_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 62 | 2 | `121785794`, `123456789` |

### `data\raw\RSRC-080\owasp_asvs_page_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 2 | 2 | `20250000000000`, `950526877` |

### `data\raw\RSRC-081\owasp_api_security_top10_page_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 1 | 1 | `214075229` |

### `data\raw\RSRC-082\nist_csf_page_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 3 | 2 | `1089704227`, `1134161994` |

### `data\raw\RSRC-083\nist_ai_main_page_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 13 | 3 | `1089704227`, `1776955625841`, `1134161994` |

### `data\raw\RSRC-083\nist_ai_rmf_page_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 3 | 2 | `1089704227`, `1134161994` |

### `data\synthetic\SYNTHETIC_CaseMaster_demo_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 4004 | 2054 | `100160068202500001`, `100050021202300008`, `100120054202400008` |

### `data\synthetic\SYNTHETIC_CaseMaster_smoke_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100050019202300001`, `100050030202500004`, `100270105202500001` |

### `data\synthetic\SYNTHETIC_ComplainantDetails_demo_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `7853 5704 3376`, `4466 7547 4837`, `1562 7503 4710` |
| PAN Card | 635 | 635 | `GQWTJ1418Q`, `HTUKX5412U`, `GKHCS1799W` |

### `data\synthetic\SYNTHETIC_ComplainantDetails_smoke_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `1498 8713 8446`, `8701 8933 2070`, `6329 3973 1445` |
| PAN Card | 62 | 62 | `KNZKZ2945V`, `UNYWP5743D`, `GETAW5610J` |

### `data\synthetic\SYNTHETIC_VehicleLink_demo_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-04-FG-1194`, `KA-25-HF-7104`, `KA-25-EF-2004` |

### `data\synthetic\SYNTHETIC_VehicleLink_smoke_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-02-CA-2581`, `KA-25-GG-1987`, `KA-09-AD-6634` |

