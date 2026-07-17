# External Claim Verification Register

[//]: # (Document ID: BERUNDA-VERIFY-001 | Status: DRAFT | Classification: INTERNAL)

---

## Purpose

Catalog every externally-verifiable claim in the source documents. Each claim is classified by verification status.

## Legend

| Status | Meaning |
|--------|---------|
| ✅ VERIFIED | Confirmed against official source |
| ⚠️ UNVERIFIED | Claim exists in source but not yet checked against official docs |
| ❌ CONFLICTED | Official source contradicts the claim |
| 🔲 NOT CHECKED | Not yet attempted |

## Catalyst Platform Claims

| Claim ID | Claim | Source Document | Verification Status | Official Source | Notes |
|----------|-------|----------------|--------------------|-----------------|-------|
| CAT-001 | Catalyst Data Store is MySQL-compatible relational DB | Blueprint §5.3 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | help.catalyst.zoho.com | |
| CAT-002 | Catalyst QuickML supports Qwen 2.5-14B-Instruct model serving | Blueprint §8.9 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | help.catalyst.zoho.com | |
| CAT-003 | Catalyst QuickML supports native RAG | Blueprint §8.9 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | help.catalyst.zoho.com | |
| CAT-004 | Catalyst QuickML AutoML provides feature importance natively | Blueprint §8.5 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | help.catalyst.zoho.com | |
| CAT-005 | Catalyst Zia services include OCR, face, text, image recognition | Blueprint §15 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | help.catalyst.zoho.com | |
| CAT-006 | Catalyst SmartBrowz provides PDF/report generation | Blueprint §15 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | help.catalyst.zoho.com | |
| CAT-007 | Catalyst Signals provides event-driven messaging | Blueprint §5.1 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | help.catalyst.zoho.com | |
| CAT-008 | Catalyst Circuits provides workflow orchestration | Blueprint §15 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | help.catalyst.zoho.com | |
| CAT-009 | Catalyst Functions support Node.js and Python | Blueprint §9 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | help.catalyst.zoho.com | |
| CAT-010 | Catalyst AppSail supports custom OCI runtimes and managed runtimes | Blueprint §15 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | help.catalyst.zoho.com | |

## Legal Compliance Claims

| Claim ID | Claim | Source Document | Verification Status | Official Source | Notes |
|----------|-------|----------------|--------------------|-----------------|-------|
| LEG-001 | DPDP Act 2023 Section 17 allows government exemption for public order | Blueprint §13.4 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | indiacode.nic.in | |
| LEG-002 | DPDP Rules 2025 were notified in November 2025 | Blueprint §13.4 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | meity.gov.in | |
| LEG-003 | BNS 2023 effective 1 July 2024 replacing IPC | Resource Blueprint §D7 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | indiacode.nic.in | |
| LEG-004 | CDR access requires authorization under Indian Telegraph Act | Blueprint §6.6 | ✅ VERIFIED — Well-established legal principle | Indian Telegraph Act | |
| LEG-005 | SC/ST Act requires recording of caste for protective statistics | Blueprint §6.2 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | legislative.gov.in | |

## Data Source Claims

| Claim ID | Claim | Source Document | Verification Status | Notes |
|----------|-------|----------------|--------------------|-------|
| DAT-001 | Karnataka SCRB publishes district-wise IPC/SLL crime reviews on karnataka.data.gov.in | Blueprint §6.7 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | Check if URL still resolves |
| DAT-002 | OpenStreetMap Overpass API is free and requires no auth | Blueprint §6.7 | ✅ VERIFIED — Known public API | Rate limits apply |
| DAT-003 | Bhuvan (ISRO/NRSC) provides free WMS/WFS map layers | Blueprint §6.7 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | bhuvan.nrsc.gov.in |
| DAT-004 | Faker `en_IN` locale generates Indian names/addresses | Blueprint §6.7 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | github.com/joke2k/faker |
| DAT-005 | indic-faker generates Kannada-script synthetic text | Blueprint §6.7 | ⚠️ UNVERIFIED — OFFICIAL SOURCE CHECK REQUIRED | Smaller/newer library |

## Open-Source License Claims

| Claim ID | Claim | Source Document | Verification Status | Notes |
|----------|-------|----------------|--------------------|-------|
| OSS-001 | NetworkX is BSD-licensed | Blueprint §17 | ✅ VERIFIED — Known license | |
| OSS-002 | spaCy is MIT-licensed | Blueprint §17 | ✅ VERIFIED — Known license | |
| OSS-003 | Kepler.gl is MIT-licensed | Blueprint §17 | ⚠️ UNVERIFIED | |
| OSS-004 | Cytoscape.js is MIT-licensed | Blueprint §11 | ⚠️ UNVERIFIED | |
| OSS-005 | MapLibre GL JS is BSD-3-Clause | Resource Blueprint §D11 | ⚠️ UNVERIFIED | |
| OSS-006 | ODbL applies to OpenStreetMap data | Resource Blueprint §G | ✅ VERIFIED — Known license | |

## Verification Priority

| Priority | Claim IDs | Reason |
|----------|-----------|--------|
| HIGH | CAT-001 to CAT-005, CAT-009 | Core architecture depends on these |
| MEDIUM | CAT-006 to CAT-008, CAT-010 | Secondary dependencies |
| MEDIUM | LEG-001 to LEG-003, LEG-005 | Compliance framing |
| LOW | DAT-001 to DAT-005 | Data sourcing |
| LOW | OSS-001 to OSS-006 | Open-source strategy |
