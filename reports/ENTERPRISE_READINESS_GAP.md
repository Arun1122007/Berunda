# Enterprise Readiness Gap Analysis

> **Generated:** 2026-07-18
> **Scope:** Verified inventory vs. challenge requirements, feature-to-data matrix,
> Catalyst deployment needs, demo storyline, governance requirements.

---

## 1. Challenge Requirements vs. Inventory

| Requirement | Required Resource(s) | Status |
|-------------|---------------------|--------|
| Deployed on Zoho Catalyst | R003 (credits), R004-R005 (docs) | 🟡 Credits not yet redeemed, docs not bookmarked |
| Uses real KSP schema | R001 (ERD) | ✅ In hand |
| Submission format compliance | R002 (rules) | ❌ Not yet confirmed |
| Working demo | All P0 + P1 | 🟡 In progress |

## 2. Feature-to-Data Readiness

| Feature | Data Ready? | Blockers |
|---------|------------|----------|
| Trend dashboards | ⚠️ Partial | Synthetic data not yet generated (needs R032 Faker) |
| Hotspot analysis | ⚠️ Partial | R011 (OSM), R012 (Bhuvan) not acquired |
| Emerging-spike alerts | ⚠️ Partial | Synthetic baseline not yet generated |
| Repeat-pattern / MO similarity | ⚠️ Partial | Synthetic BriefFacts not yet generated |
| Cross-case entity resolution | ⚠️ Partial | Planted duplicates not yet seeded |
| POLE graph | ⚠️ Partial | Entity resolution prerequisite |
| Anomaly detection | ⚠️ Partial | Planted spike not yet seeded |
| Workload assistance | ⚠️ Partial | Synthetic officer data not yet generated |
| Ask Berunda (RAG) | ⚠️ Partial | Corpus not yet created |
| Report generation | ⚠️ Partial | Template not yet built |
| Data quality monitoring | ✅ Ready | Scripts created, schema known |
| Governance/audit dashboard | ✅ Ready | RBAC spec documented |

## 3. Catalyst Service Readiness

| Service | Doc Available? | Quickstart Tested? |
|---------|---------------|-------------------|
| Data Store | ❌ Not bookmarked | ❌ Not tested |
| Functions | ❌ Not bookmarked | ❌ Not tested |
| AppSail | ❌ Not bookmarked | ❌ Not tested |
| QuickML | ❌ Not bookmarked | ❌ Not tested |
| Authentication | ❌ Not bookmarked | ❌ Not tested |
| Cron | ❌ Not bookmarked | ❌ Not tested |
| API Gateway | ❌ Not bookmarked | ❌ Not tested |
| Stratus | ❌ Not bookmarked | ❌ Not tested |

## 4. Governance Readiness

| Item | Status |
|------|--------|
| No SECC/caste-linked dataset | ✅ Enforced by blueprint |
| CasteID/ReligionID access-restricted | 📋 Documented, not yet in deployed RBAC |
| BNS mapping flagged for legal review | ✅ Documented in transformation plan |
| Synthetic data labeling | 📋 Spec written, not yet generated |
| PII scan capability | ✅ Scanner script created |
| Audit logging specification | ✅ Documented |

## 5. Open-Source Release Readiness

| Item | Status |
|------|--------|
| License inventory | ✅ Created (`manifests/license_inventory.csv`) |
| Attribution list | ✅ Created (`reports/LICENSE_AND_ATTRIBUTION_REPORT.md`) |
| GPLv3 copyleft risk (Neo4j) | ⚠️ Flagged — Phase 1 uses BSD-licensed NetworkX |
| .gitignore excludes sensitive data | ✅ Created |

---

## 6. Ranked Gap Backlog

| Priority | Gap | Impact | Effort | Risk | Time Sensitivity |
|----------|-----|--------|--------|------|-----------------|
| 🔴 Critical | R032 Faker not installed | Blocks all synthetic data | 1 min | None | **Immediate** |
| 🔴 Critical | R002 Submission format unknown | Could invalidate submission | 10 min | None | **Day 1** |
| 🔴 Critical | R003 Catalyst credits not redeemed | Blocks deployment | 5 min | Time-limited | **Day 1** |
| 🟡 High | R004-R005 Catalyst docs | Blocks development | 30 min | None | Day 1 |
| 🟡 High | R020-R022 Legal texts | Blocks crime classification | 30 min | None | Day 1-2 |
| 🟡 High | R011 OSM POIs | Blocks enriched hotspot map | 15 min | API rate limit | Day 2-3 |
| 🟡 High | R017 Open-Meteo | Blocks weather feature | 10 min | API rate limit | Day 2-3 |
| 🟢 Medium | R006, R008 Crime stats | Blocks validation baseline | 20 min | None | Day 3-5 |
| 🟢 Medium | R014 Census data | Blocks socio-economic context | 15 min | None | Day 5-7 |
| ⚪ Low | R034-R035 Security standards | Reference only | 10 min | None | Week 2+ |

---

## 7. Recommended Next Steps

1. **Immediate:** `pip install Faker` → unblocks Day 1 synthetic data generation
2. **User action:** Log into Hack2Skill → confirm R002 submission format
3. **User action:** Redeem R003 Catalyst credits at `catalyst.zoho.com`
4. **First hour:** Run `download_resources.py --no-dry-run --priority P0`
5. **First day:** Run `download_resources.py --no-dry-run --priority P1`
6. **Parallel:** Begin Catalyst project setup (doesn't depend on downloads)
