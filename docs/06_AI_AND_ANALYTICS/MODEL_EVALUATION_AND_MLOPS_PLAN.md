# Model Evaluation and MLOps Plan

[//]: # (Document ID: BERUNDA-AI-003 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Data Scientists, DevOps | Source: 01_Enterprise_Blueprint §8 | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Model Inventory

| Model | ID | Type | Framework | Frequency of Use |
|-------|-----|------|-----------|-----------------|
| NER Extraction | M-001 | Pretrained NLP | spaCy | Per FIR ingestion |
| Entity Resolution | M-002 | Rule-based | Python | Per FIR ingestion |
| Risk Scoring | M-003 | Binary classification | QuickML AutoML | Nightly (Cron) |
| RAG Embedding + Generation | M-004 | LLM + Vector search | QuickML + Catalyst NoSQL | On demand |

## 2. Evaluation Metrics

### M-001: NER Extraction

| Metric | Target | Measurement |
|--------|--------|-------------|
| Precision | > 0.90 | On planted named entities in synthetic BriefFacts |
| Recall | > 0.85 | On planted named entities |
| F1 | > 0.87 | Harmonic mean |

### M-002: Entity Resolution

| Metric | Target | Measurement |
|--------|--------|-------------|
| Recall (auto-link + grey zone) | > 0.90 | Planted test cases |
| Precision (auto-link only) | > 0.95 | False positive rate |
| Grey zone ratio | < 0.20 | Fraction of decisions requiring manual review |

### M-003: Risk Scoring

| Metric | Target | Measurement |
|--------|--------|-------------|
| AUC-ROC | > 0.80 | Held-out test set (20% of synthetic data) |
| Precision@10% | > 0.70 | Among highest-scored 10% of persons |
| Feature importance stability | Rank correlation > 0.80 | Across 5-fold cross-validation |
| Fairness (exclusion check) | 0 restricted features in top-20 | Automated scan of feature importance |

### M-004: RAG

| Metric | Target | Measurement |
|--------|--------|-------------|
| Answer relevance | > 4.0/5.0 | Human rating on 20 test questions |
| Citation accuracy | 100% | Every claim maps to a retrieved chunk |
| Insufficient evidence rate | > 0.90 for out-of-scope questions | System correctly declines to answer |
| Latency (end-to-end) | < 5 seconds | From question submission to displayed answer |

## 3. Evaluation Dataset

| Dataset | Size | Composition | Hold-out |
|---------|------|-------------|----------|
| NER test | 200 BriefFacts | 50% simple (1-2 entities), 30% moderate, 20% complex | 20% |
| ER test | 500 person records | Includes all planted link types | 20% |
| Risk scoring test | 1,000 labeled persons | Balanced classes (50% repeat, 50% first-time) | 20% |
| RAG test | 20 questions | Mix of template-matching and free-text | None (human evaluation) |

## 4. MLOps Pipeline

```
[Data Generator] → [Feature Engineering] → [Model Training] → [Evaluation] → 
[Fairness Check] → [Model Registry] → [Deployment to QuickML]
```

### 4.1 Tools

| Stage | Phase 1 Tool | Phase 3+ Target |
|-------|-------------|-----------------|
| Feature engineering | Python scripts | Feature store (e.g., Feast) |
| Model training | QuickML AutoML + local scikit-learn | MLflow + QuickML |
| Model registry | Catalyst Stratus (file storage) | MLflow Model Registry |
| Deployment | Catalyst Function / QuickML | Kubernetes + Seldon Core |
| Monitoring | Custom Python health checks | Prometheus + Grafana |

### 4.2 Model Registry Schema (Catalyst Stratus)

```
models/
├── risk_scoring/
│   ├── v1.0.0/
│   │   ├── model.pkl
│   │   ├── feature_list.json
│   │   ├── metrics.json
│   │   └── fairness_check.json
│   └── v1.1.0/
│       └── ...
├── ner/
│   └── baseline/
│       └── spacy_en_core_web_lg/
└── registry_index.json
```

### 4.3 Trigger Conditions

| Model | Retraining Trigger | Approval Required |
|-------|-------------------|-------------------|
| NER | Never (frozen pretrained model) | N/A |
| Entity Resolution | Threshold/weight tuning session | Developer |
| Risk Scoring | New synthetic dataset OR performance degradation | Developer + Compliance |
| RAG | QuickML platform update | Developer |
