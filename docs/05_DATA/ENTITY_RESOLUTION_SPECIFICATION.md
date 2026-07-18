# Entity Resolution Specification

[//]: # (Document ID: BERUNDA-DATA-005 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Developers, Data Engineers, QA | Source: 01_Enterprise_Blueprint §6.3 + ADR-005 | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Overview

Entity resolution (ER) is the process of identifying when multiple source records (across ComplainantDetails, Victim, and Accused tables) refer to the same real-world person. ER is the foundation of the hidden-link discovery feature.

**Phase 1 approach:** Rule-based blocking + weighted similarity scoring (per ADR-005). A learned model is deferred to Phase 3+.

## 2. Data Flow

```
Source Record (ComplainantDetails/Victim/Accused)
  │
  ▼
Blocking Step ──→ Candidate entities from int_PersonEntity
  │                    (same district, age band ±3 years)
  ▼
Feature Computation ──→ Phonetic similarity (Soundex)
                         Edit distance (Levenshtein)
                         Address/locality overlap (token-based Jaccard)
                         Age match (exact or band overlap)
  │
  ▼
Weighted Similarity Score
  │
  ├─ Score > HIGH_THRESHOLD (0.85) → Auto-link to existing PersonEntity
  ├─ Score > LOW_THRESHOLD (0.50)  → Create tentative link, flag for manual review
  └─ Score ≤ LOW_THRESHOLD (0.50) → Create new PersonEntity
```

## 3. Blocking Strategy

Blocking reduces the candidate search space. It is a coarse filter, designed for high recall at the cost of some precision.

| Blocking Key | Description | Rationale |
|-------------|-------------|-----------|
| DistrictID | Same district as the source record | Cross-jurisdiction matching is rare at hackathon scale |
| Age band (±3 years) | Source record age ±3 years | Accounts for age reporting variance |

**Implementation:** SQL WHERE clause filtering `int_PersonEntity` by `PrimaryDistrictID = sourceDistrict AND (YEAR(DOB) BETWEEN sourceAge-3 AND sourceAge+3)`.

**Fallback:** If the block returns < 5 candidates, widen age band to ±5 years.

## 4. Similarity Features

| Feature | Weight | Algorithm | Description |
|---------|--------|-----------|-------------|
| Name phonetic similarity | 0.40 | Soundex + Double Metaphone | Accounts for Kannada→English transliteration variance (e.g., "Venkatesh" vs "Venkatesha") |
| Name edit distance | 0.30 | Normalized Levenshtein | Detects minor spelling differences, typos |
| Address/locality overlap | 0.20 | Token-based Jaccard | Compares address and locality tokens (if address available in source) |
| Age match | 0.10 | Exact or band overlap | 1.0 if exact age match, 0.7 if within ±1 year, 0.3 if within ±3 years |

## 5. Threshold Configuration

| Threshold | Value | Action | Rationale |
|-----------|-------|--------|-----------|
| HIGH_THRESHOLD | 0.85 | Auto-link | Strong evidence of same person; no human review needed |
| LOW_THRESHOLD | 0.50 | Manual review | Moderate evidence; human judgement required |
| Below LOW_THRESHOLD | < 0.50 | New entity | Insufficient evidence for a match |

**Configuration format (JSON, in Catalyst Cache):**
```json
{
  "entity_resolution": {
    "high_threshold": 0.85,
    "low_threshold": 0.50,
    "weights": {
      "name_phonetic": 0.40,
      "name_edit_distance": 0.30,
      "address_overlap": 0.20,
      "age_match": 0.10
    },
    "blocking": {
      "age_band": 3,
      "age_band_fallback": 5,
      "min_candidates": 5
    }
  }
}
```

All thresholds and weights are configurable at runtime without redeployment.

## 6. Manual Review Interface

The Investigator Console presents the following for each grey-zone match:

| Field | Description |
|-------|-------------|
| Source Record | Name, Age, District, CaseMasterID, Source Table |
| Candidate Match(es) | CanonicalName, DOB, Gender, PrimaryDistrict, Existing RiskScore |
| Similarity Breakdown | Per-feature score + overall weighted score |
| Action Buttons | Confirm Match | Reject Match | View Case Details |

**Audit requirements:** Every Confirm/Reject action writes to `gov_AuditLog` with `Action = "MERGE_CONFIRM"` or `"MERGE_REJECT"`.

## 7. PersonEntityLink Table Population

After ER decision, the `int_PersonEntityLink` table is populated:

| Scenario | Action on int_PersonEntity | Action on int_PersonEntityLink |
|----------|---------------------------|-------------------------------|
| Auto-link (score > 0.85) | Link source to existing PersonEntity | INSERT with Confidence = score, IsReviewed = 0 |
| Manual confirm | Same as auto-link | UPDATE IsReviewed = 1, ReviewedBy, ReviewedAt |
| Manual reject | Create new PersonEntity | INSERT with new PersonEntityID, Confidence = score (informational) |
| New entity (no match) | Create new PersonEntity | INSERT with Confidence = 0 |

## 8. Test Data Strategy

The synthetic data generator creates the following test cases for entity resolution:

| Test Case | Description | Expected Outcome |
|-----------|-------------|-----------------|
| Exact match | Same name, same district, same age | Auto-link (score > 0.85) |
| Phonetic variant | "Venkatesh" vs "Venkatesha" | High match (score ~0.75-0.85, grey zone) |
| Typo variant | "Ramesh" vs "Rames" | High match (score ~0.70-0.80, grey zone) |
| Same person, 4 different names | Planted identity across 4 FIRs | All resolved to single PersonEntity |
| Different person, similar name | "Ramesh Kumar" vs "Ramesh Gupta", different district | Low match (score < 0.50) |
| Age discrepancy | Same name, district, age differs by 8 years | Low match (blocking filter removes candidate) |

## 9. Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Recall (auto-link + grey zone) | > 90% | Manual verification of planted test cases |
| Precision (auto-link) | > 95% | False positive rate on planted non-matches |
| Processing time per source record | < 500ms | End-to-end blocking + scoring |
| Manual review queue | < 20% of total source records | Tune thresholds to keep grey zone manageable |

## 10. Phase 3+ Migration

| Phase 1 (Rule-based) | Phase 3+ (Learned) |
|---------------------|-------------------|
| Hand-tuned weights | Model-trained weights (logistic regression or siamese network) |
| Soundex + Levenshtein | Learned string embedding (e.g., DeepER) |
| Manual review for grey zone | Active learning: model proposes, human confirms, model improves |
| Static thresholds | Dynamic threshold based on precision-recall curve |

## 11. Kannada Name Normalization

For Kannada-language names (STRETCH / Phase 2):

| Technique | Description |
|-----------|-------------|
| Transliteration normalization | Map common Kannada→English variations (e.g., ಶ → sha/sa, ಷ → sha) |
| Suffix stripping | Remove common suffixes (-appa, -anna, -ayya) before comparison |
| Vowel normalization | Normalize doubled vowels (e.g., "aa" → "a") |
| Initial normalization | Handle initial-letter abbreviations ("V." → "Venkatesh") |

Normalized names are stored alongside the original in PersonEntity.CanonicalName.

## 12. False Positive / False Negative Handling

| Scenario | Detection | Remediation |
|----------|-----------|-------------|
| False positive auto-link (score > 0.85 but different persons) | Audit log review; user reports incorrect merge | Admin can split PersonEntity; create separate entities; log the split |
| False negative (missed match, score < 0.50) | User discovers link manually via search | User can manually link via "Link to existing person" UI; confidence set to 1.0 (manual) |
| Grey zone overflow (> 30% of decisions) | Automated alert when grey zone ratio > 0.30 | Review thresholds; adjust HIGH_THRESHOLD downward or improve features |

## 13. Prohibited Identity Inference

Entity resolution MUST NOT:
- Infer caste, religion, or community from name or surname
- Use CasteID or ReligionID as blocking or similarity features
- Present "possible community" labels in the UI
- Score matches based on demographic similarity
- Auto-link persons based solely on shared address (require name similarity)
