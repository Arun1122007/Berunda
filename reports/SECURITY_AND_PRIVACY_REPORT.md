# Security and Privacy Report

> **Generated:** 2026-07-26T17:58:54Z
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
| Bank Account (long number) | 646 | 291 | `48591000000028041`, `48591000000025522`, `48591000000030981` |

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
| Bank Account (long number) | 4004 | 2054 | `100120053202300001`, `100270104202500001`, `100120053202500003` |

### `data\interim\SYNTHETIC_CaseMaster_demo_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 4004 | 2054 | `100120053202300001`, `100270104202500001`, `100120053202500003` |

### `data\interim\SYNTHETIC_CaseMaster_demo_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 4004 | 2054 | `100120053202300001`, `100270104202500001`, `100120053202500003` |

### `data\interim\SYNTHETIC_CaseMaster_demo_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 4004 | 2054 | `100120053202300001`, `100270104202500001`, `100120053202500003` |

### `data\interim\SYNTHETIC_CaseMaster_smoke_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100110049202400001`, `100310117202300001`, `100250098202400002` |

### `data\interim\SYNTHETIC_CaseMaster_smoke_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100110049202400001`, `100310117202300001`, `100250098202400002` |

### `data\interim\SYNTHETIC_CaseMaster_smoke_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100110049202400001`, `100310117202300001`, `100250098202400002` |

### `data\interim\SYNTHETIC_CaseMaster_smoke_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100110049202400001`, `100310117202300001`, `100250098202400002` |

### `data\interim\SYNTHETIC_ComplainantDetails_demo_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `2979 2107 3963`, `1293 5824 6597`, `4144 7159 1330` |
| PAN Card | 635 | 635 | `BRTDX6372D`, `YYALD7001Q`, `FABHY7632G` |

### `data\interim\SYNTHETIC_ComplainantDetails_demo_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `2979 2107 3963`, `1293 5824 6597`, `4144 7159 1330` |
| PAN Card | 635 | 635 | `BRTDX6372D`, `YYALD7001Q`, `FABHY7632G` |

### `data\interim\SYNTHETIC_ComplainantDetails_demo_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `2979 2107 3963`, `1293 5824 6597`, `4144 7159 1330` |
| PAN Card | 635 | 635 | `BRTDX6372D`, `YYALD7001Q`, `FABHY7632G` |

### `data\interim\SYNTHETIC_ComplainantDetails_demo_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `2979 2107 3963`, `1293 5824 6597`, `4144 7159 1330` |
| PAN Card | 635 | 635 | `BRTDX6372D`, `YYALD7001Q`, `FABHY7632G` |

### `data\interim\SYNTHETIC_ComplainantDetails_smoke_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `1815 2038 7542`, `5952 3992 4660`, `6771 8870 7839` |
| PAN Card | 62 | 62 | `UNYWP5743D`, `GTJZA2415C`, `GETAW5610J` |

### `data\interim\SYNTHETIC_ComplainantDetails_smoke_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `1815 2038 7542`, `5952 3992 4660`, `6771 8870 7839` |
| PAN Card | 62 | 62 | `UNYWP5743D`, `GTJZA2415C`, `GETAW5610J` |

### `data\interim\SYNTHETIC_ComplainantDetails_smoke_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `1815 2038 7542`, `5952 3992 4660`, `6771 8870 7839` |
| PAN Card | 62 | 62 | `UNYWP5743D`, `GTJZA2415C`, `GETAW5610J` |

### `data\interim\SYNTHETIC_ComplainantDetails_smoke_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `1815 2038 7542`, `5952 3992 4660`, `6771 8870 7839` |
| PAN Card | 62 | 62 | `UNYWP5743D`, `GTJZA2415C`, `GETAW5610J` |

### `data\interim\SYNTHETIC_VehicleLink_demo_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-05-DE-7962`, `KA-25-EF-1808`, `KA-03-EF-2656` |

### `data\interim\SYNTHETIC_VehicleLink_demo_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-05-DE-7962`, `KA-25-EF-1808`, `KA-03-EF-2656` |

### `data\interim\SYNTHETIC_VehicleLink_demo_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-05-DE-7962`, `KA-25-EF-1808`, `KA-03-EF-2656` |

### `data\interim\SYNTHETIC_VehicleLink_demo_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-05-DE-7962`, `KA-25-EF-1808`, `KA-03-EF-2656` |

### `data\interim\SYNTHETIC_VehicleLink_smoke_42_01.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-19-HA-1982`, `KA-25-GG-1987`, `KA-25-BA-5822` |

### `data\interim\SYNTHETIC_VehicleLink_smoke_42_02.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-19-HA-1982`, `KA-25-GG-1987`, `KA-25-BA-5822` |

### `data\interim\SYNTHETIC_VehicleLink_smoke_42_03.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-19-HA-1982`, `KA-25-GG-1987`, `KA-25-BA-5822` |

### `data\interim\SYNTHETIC_VehicleLink_smoke_42_04.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-19-HA-1982`, `KA-25-GG-1987`, `KA-25-BA-5822` |

### `data\processed\SYNTHETIC_CaseMaster_demo_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 4004 | 2054 | `100120053202300001`, `100270104202500001`, `100120053202500003` |

### `data\processed\SYNTHETIC_CaseMaster_smoke_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100110049202400001`, `100310117202300001`, `100250098202400002` |

### `data\processed\SYNTHETIC_ComplainantDetails_demo_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `2979 2107 3963`, `1293 5824 6597`, `4144 7159 1330` |
| PAN Card | 635 | 635 | `BRTDX6372D`, `YYALD7001Q`, `FABHY7632G` |

### `data\processed\SYNTHETIC_ComplainantDetails_smoke_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `1815 2038 7542`, `5952 3992 4660`, `6771 8870 7839` |
| PAN Card | 62 | 62 | `UNYWP5743D`, `GTJZA2415C`, `GETAW5610J` |

### `data\processed\SYNTHETIC_VehicleLink_demo_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-05-DE-7962`, `KA-25-EF-1808`, `KA-03-EF-2656` |

### `data\processed\SYNTHETIC_VehicleLink_smoke_42_FINAL.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-19-HA-1982`, `KA-25-GG-1987`, `KA-25-BA-5822` |

### `data\raw\RSRC-003\promotions_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Email Address | 10 | 6 | `emma@zylker.com`, `p.boyle@zylker.com`, `amelia.burrows@zylker.com` |
| Credit Card (16 digits) | 30 | 19 | `1510000000109474`, `1510000000110121`, `2823000000014176` |
| Bank Account (long number) | 38 | 26 | `1510000000109474`, `1510000000110121`, `195000000042025` |

**Secrets Patterns:**

| Pattern | Matches | Note |
|---------|---------|------|
| Generic Secret | 1 | Potential credential — verify manually |

### `data\raw\RSRC-012\R006_resource_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 1 | 1 | `237745130315` |
| Bank Account (long number) | 4 | 3 | `553852000000003`, `20231028004`, `237745130315` |

### `data\raw\RSRC-014\R008_resource_20260718.html`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 1 | 1 | `999999999999` |
| Email Address | 2 | 2 | `pd.webportal@karnataka.gov.in`, `police@ksp.gov.in` |
| Bank Account (long number) | 18 | 9 | `1749022433`, `1784199622`, `1704973538` |

### `data\raw\RSRC-023\overpass_karnataka_police_20260718.json`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 3 | 3 | `918155286720`, `914972771093`, `918022943469` |
| Indian Phone (+91) | 829 | 725 | `7296738197`, `6958003375`, `8110746355` |
| Email Address | 7 | 7 | `devarajamyc@ksp.gov.in`, `kl72@keralamvd.gov.in`, `Whitefieldbcp@ksp.gov.in` |
| Indian Passport | 1 | 1 | `Q4855039` |
| Bank Account (long number) | 2616 | 2332 | `13018505641`, `249517268`, `4834367494` |

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
| Bank Account (long number) | 4004 | 2054 | `100120053202300001`, `100270104202500001`, `100120053202500003` |

### `data\synthetic\SYNTHETIC_CaseMaster_smoke_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Bank Account (long number) | 398 | 212 | `100110049202400001`, `100310117202300001`, `100250098202400002` |

### `data\synthetic\SYNTHETIC_ComplainantDetails_demo_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 617 | 617 | `2979 2107 3963`, `1293 5824 6597`, `4144 7159 1330` |
| PAN Card | 635 | 635 | `BRTDX6372D`, `YYALD7001Q`, `FABHY7632G` |

### `data\synthetic\SYNTHETIC_ComplainantDetails_smoke_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Aadhaar (12 digits) | 56 | 56 | `1815 2038 7542`, `5952 3992 4660`, `6771 8870 7839` |
| PAN Card | 62 | 62 | `UNYWP5743D`, `GTJZA2415C`, `GETAW5610J` |

### `data\synthetic\SYNTHETIC_VehicleLink_demo_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 477 | 477 | `KA-05-DE-7962`, `KA-25-EF-1808`, `KA-03-EF-2656` |

### `data\synthetic\SYNTHETIC_VehicleLink_smoke_42.csv`

**PII Patterns:**

| Pattern | Matches | Unique | Samples |
|---------|---------|--------|---------|
| Vehicle Registration (KA) | 44 | 44 | `KA-19-HA-1982`, `KA-25-GG-1987`, `KA-25-BA-5822` |

