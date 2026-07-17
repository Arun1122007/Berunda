# Contradiction, Assumption, and Gap Register

[//]: # (Document ID: BERUNDA-GAP-REG-001 | Status: DRAFT | Classification: INTERNAL)

---

## Contradictions

| ID | Documents Involved | Contradiction | Resolution | Status |
|----|-------------------|---------------|------------|--------|
| CON-001 | `01_Blueprint` vs ERD PDF | Blueprint §4.3 says `Inv_OccuranceTime` ambiguity "worth a human check"; PDF relationship matrix confirms it IS a separate 1:1 table | **RESOLVED**: Confirmed separate table, not CaseMaster continuation | RESOLVED |
| CON-002 | `01_Blueprint` vs docs | Claims to be "companion doc 1 of 5" but package contains 12 files across 01-08 numbering and older drafts | **REGISTERED**: The "5-doc" claim is outdated; full inventory in SOURCE_INVENTORY | REGISTERED |
| CON-003 | Blueprint §5.1 vs CaseGraph §6 | Blueprint says "modular microservices"; CaseGraph says "Kubernetes microservices" would violate Catalyst rule | **RESOLVED by ADR-001**: Phase 1 uses Functions + API Gateway, NOT full microservices; event-driven deferred to Phase 3+ | RESOLVED |
| CON-004 | `project_berunda_blueprint.md` vs `01_Blueprint.md` | v1 uses generic schema (no real ERD); v2 uses real ERD | **RESOLVED**: v2 supersedes v1; v1 is historical reference only | RESOLVED |
| CON-005 | Blueprint §15 vs current Catalyst docs (UNVERIFIED) | Claims about QuickML capabilities (Qwen serving, RAG, AutoML feature importance) | **UNVERIFIED**: Need to verify against current help.catalyst.zoho.com | OPEN |

## Assumptions

| ID | Assumption | Rationale | Risk if Wrong |
|----|------------|-----------|---------------|
| ASM-001 | The ERD PDF is the latest version of the schema | No newer version found in package | Schema drift during build |
| ASM-002 | Catalyst QuickML supports Qwen model serving + RAG + AutoML feature importance natively | Blueprint §7-8 and §15 claim this | Architecture redesign needed if not supported |
| ASM-003 | A 2-person team can build 12 MVP features in 11 days | Implementation Plan Day 1-11 shows this | Scope must be cut; fallbacks defined |
| ASM-004 | Synthetic data (Faker + indic-faker) is acceptable for the demo | Hackathon brief states synthetic is preferred for sensitive data | Data not allowed or insufficient |
| ASM-005 | The Catalyst free tier / credits are sufficient for the demo | R003 mentions credit redemption | Cost overrun or service throttling |
| ASM-006 | CasteID/ReligionID are on ComplainantDetails only (not Accused/Victim) | Confirmed by ERD PDF | If also on Accused, governance scope widens |
| ASM-007 | BNS 2023 fully replaces IPC for mapping purposes | R020 mentions legacy IPC→BNS needs legal review | Legal mapping may be premature |

## Gaps

| ID | Gap | Impact | Owner | Action |
|----|-----|--------|-------|--------|
| GAP-001 | `inv_arrestsurrenderaccused` junction table referenced in relationship matrix but NO column definitions in ERD PDF | Incomplete schema for ArrestSurrender-Accused M:N relationship | Team | Design defensible junction schema (ArrestSurrenderID, AccusedMasterID, IsPrimaryAccused) |
| GAP-002 | Exact submission format unknown (video/live link/repo/deck?) | Day 11 undefined | Team | Check Hack2Skill Submissions tab |
| GAP-003 | Judging rubric not available | Cannot weight effort | Team | Check Hack2Skill Resources tab |
| GAP-004 | Catalyst credits not yet redeemed | Deployment blocked | Team | Redeem at catalyst.zoho.com promo link |
| GAP-005 | No sample data provided by organizer | Must generate synthetic dataset | Team | Use Faker + indic-faker per SYNTHETIC_DATA_SPECIFICATION |
| GAP-006 | No published API for CCTNS integration | MVP uses synthetic import only | Team | Document as Phase 2 target |
| GAP-007 | No organizing-body confirmation on which Catalyst services are mandatory | Risk of using non-mandated service | Team | Review challenge rules for service list |
| GAP-008 | Kannada NER model availability and quality unverified | Stretch feature may be infeasible | Team | Evaluate AI4Bharat/IndicNLP model status |
| GAP-009 | No data retention policy from organizer | Synthetic data lifecycle undefined | Team | Default: delete after contest or as per rules |
| GAP-010 | Open-source license strategy for the project itself not finalized | Apache 2.0 proposed but not confirmed | Team | Decide between Apache 2.0, MIT, or custom |

## Open Questions for Organizer

| QID | Question | Why It Matters |
|-----|----------|----------------|
| OQ-001 | What is the exact submission format and deliverable checklist? | Determines Day 11 effort |
| OQ-002 | Is there a list of mandatory Catalyst services for compliance? | Guides Catalyst service mapping |
| OQ-003 | Will real (sanitized) KSP data be provided, or must we use synthetic exclusively? | Affects demo authenticity |
| OQ-004 | Is there a specific judging rubric or scoring criteria? | Guides polish priorities |
| OQ-005 | Are there specific Catalyst resource limits for the hackathon? | Affects architecture scaling assumptions |
