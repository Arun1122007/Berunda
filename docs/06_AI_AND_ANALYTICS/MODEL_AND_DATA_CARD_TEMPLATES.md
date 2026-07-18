# Model and Data Card Templates

[//]: # (Document ID: BERUNDA-AI-005 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Data Scientists, Governance | Source: 01_Enterprise_Blueprint §8 | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Model Card Template

Each Berunda AI model has a model card following the standard model card format (Mitchell et al., 2019).

### 1.1 Template

```markdown
# Model Card: {Model Name}

**Model ID:** {e.g., M-003}
**Version:** {e.g., 1.0.0}
**Date:** {YYYY-MM-DD}
**Owner:** {Developer name}

## Model Details

- **Type:** {Classification / NER / LLM / Rule-based}
- **Framework:** {spaCy / scikit-learn / QuickML / Python}
- **Training data:** {Description or reference}
- **Input:** {Feature schema}
- **Output:** {Prediction schema}

## Intended Use

- **Primary use:** {Purpose}
- **Out-of-scope:** {What it should NOT be used for}
- **Human role:** {Human-in-the-loop / Fully automated / Advisory}

## Factors

- **Relevant groups:** {e.g., Accused persons, complainants}
- **Sensitive features:** {None / Restricted features excluded / Checked}
- **Evaluation factors:** {e.g., Gender balance check, district balance check}

## Metrics

| Metric | Phase 1 Target | Current |
|--------|---------------|---------|
| {Metric 1} | {Target} | {Value} |
| {Metric 2} | {Target} | {Value} |

## Evaluation Data

- **Dataset:** {Reference to synthetic dataset version}
- **Size:** {Number of records}
- **Split:** {Train/val/test ratio}

## Ethical Considerations

- **Fairness checks passed:** {Yes/No}
- **Restricted features excluded:** {Verified / Not applicable}
- **Human oversight:** {Description}

## Caveats and Recommendations

- {Known limitations}
- {Recommended usage patterns}
- {When to retrain}
```

### 1.2 Completed Example: Risk Scoring Model

```markdown
# Model Card: Risk Scoring Model

**Model ID:** M-003
**Version:** 1.0.0
**Date:** 2026-07-16
**Owner:** Berunda Team

## Model Details

- **Type:** Binary classification (repeat offender vs. first-time)
- **Framework:** QuickML AutoML
- **Training data:** Synthetic FIR dataset v1.0 (2,000 labeled persons)
- **Input:** 8 features (num_prior_cases, num_districts, age_group, crime_type_diversity, has_co_accused, arrest_count, avg_case_severity, recency_days)
- **Output:** RiskScore (0.00000-1.00000) + Feature importance JSON

## Intended Use

- **Primary use:** Identify persons who may be repeat offenders for investigative prioritization
- **Out-of-scope:** Not for sentencing, bail determination, or any legal decision
- **Human role:** Advisory — scores are reviewed by Investigator before action

## Factors

- **Relevant groups:** Accused persons in Karnataka FIR records
- **Sensitive features:** CasteID, ReligionID — HARD EXCLUDED (verified)
- **Evaluation factors:** District balance check, gender balance check passed

## Metrics

| Metric | Phase 1 Target | Current |
|--------|---------------|---------|
| AUC-ROC | > 0.80 | 0.83 |
| Precision@10% | > 0.70 | 0.74 |
| Feature exclusion | 0 restricted fields | ✓ PASS |

## Evaluation Data

- **Dataset:** Synthetic FIR dataset v1.0
- **Size:** 2,000 labeled persons (1,000 repeat, 1,000 first-time)
- **Split:** 80/20 train/test

## Ethical Considerations

- **Fairness checks passed:** Yes
- **Restricted features excluded:** Verified — CasteID, ReligionID, and proxies absent from all features
- **Human oversight:** All risk scores are advisory; no automated actions

## Caveats and Recommendations

- Trained on synthetic data only — real-world performance may differ
- Retrain if feature distributions shift significantly
- Monitor for proxy variables (surname, neighborhood) in future versions
```

## 2. Data Card Template

Each Berunda dataset has a data card.

### 2.1 Template

```markdown
# Data Card: {Dataset Name}

**Dataset ID:** {e.g., D-001}
**Version:** {e.g., 1.0}
**Date:** {YYYY-MM-DD}

## Dataset Overview

- **Description:** {Purpose and contents}
- **Source:** {Generator / Extraction method}
- **Size:** {Record count}
- **Schema:** {Table or file reference}

## Composition

- **Domains represented:** {Districts, crime types, etc.}
- **Time period:** {Start date - End date}
- **Sensitive data:** {None / Restricted fields present but access-controlled}

## Collection Process

- **Method:** {Synthetic data generation / Manual entry / Import}
- **Tools:** {Faker / Custom scripts}

## Labeling

- **Labeled for:** {Entity resolution / Risk scoring / NER}
- **Label source:** {Planted / Generated / Manual}
- **Labeling process:** {Description}

## Intended Use

- **Primary use:** {Training / Evaluation / Demo}
- **Out-of-scope:** {Production use without retraining}

## Limitations

- {Synthetic data caveats}
- {Distributional differences from real data}
```
