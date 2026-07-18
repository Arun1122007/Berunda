# AI/ML System Specification

[//]: # (Document ID: BERUNDA-AI-001 | Version: 1.0 | Status: DRAFT | Classification: CONFIDENTIAL | Owner: Berunda Team | Audience: Developers, Data Scientists | Source: 01_Enterprise_Blueprint §8 | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Overview

Berunda uses AI/ML for four specific capabilities:

| Capability | Technique | Phase | Deployment |
|-----------|-----------|-------|------------|
| Entity extraction from FIR narrative | Named Entity Recognition (spaCy) | MVP | Catalyst Function (Python) |
| Cross-case entity resolution | Rule-based blocking + weighted scoring | MVP | Catalyst Function (Python) |
| Repeat-offender risk scoring | AutoML classification (QuickML) | MVP | Catalyst QuickML |
| Natural language query over cases | RAG + LLM (QuickML) | MVP | Catalyst QuickML |

## 2. Named Entity Recognition (NER)

### 2.1 Pipeline

```
BriefFacts (NVARCHAR(MAX))
  → Catalyst Function: spaCy en_core_web_lg
  → Custom entity patterns for Indian names, vehicle numbers
  → Post-processing: deduplicate within case, confidence scoring
  → Output: PersonEntityLink, VehicleLink records
```

### 2.2 Entities Extracted

| Entity Type | spaCy Label | Custom Pattern | Example |
|------------|------------|---------------|---------|
| Person name | PERSON | NER default | "Ramesh Kumar" |
| Vehicle number | — | `[A-Z]{2}-\d{2}-[A-Z]{1,2}-\d{4}` | "KA-01-AB-1234" |
| Phone number | — | `\d{10}` | "9876543210" |
| Location | GPE, LOC | NER default | "Bangalore", "MG Road" |
| Organization | ORG | NER default | "SBI Bank" |
| Date | DATE | NER default | "15 January 2024" |

### 2.3 Confidence Scoring

| Signal | Points |
|--------|--------|
| Exact match to existing source record | +0.20 |
| Matches extracted with high NER confidence (> 0.95) | +0.10 |
| Partial match (e.g., first name only) | +0.05 |
| Multiple occurrences within same BriefFacts | +0.05 per occurrence (max +0.15) |

### 2.4 Kannada NER (STRETCH)

Use `indic-faker` trained spaCy model for Kannada text. Same pipeline as English NER but with Kannada-language model.

## 3. Entity Resolution

Specified in detail in `docs/05_DATA/ENTITY_RESOLUTION_SPECIFICATION.md`.

## 4. Risk Scoring

### 4.1 Model Type

Binary classification (repeat offender vs. first-time) trained via QuickML AutoML. Interpretability is required for explainable scoring.

### 4.2 Feature Engineering

**Features used:**
- `num_prior_cases` — count of prior FIRs where PersonEntity appears
- `num_districts` — number of distinct districts in prior cases
- `age_group` — binned (18-25, 26-35, 36-50, 50+)
- `crime_type_diversity` — number of distinct crime heads
- `has_co_accused` — whether person appears with co-accused
- `arrest_count` — number of arrest records
- `avg_case_severity` — average gravity of prior cases
- `recency_days` — days since last case appearance

**Features explicitly excluded:**
- CasteID
- ReligionID
- Any column from CasteMaster or ReligionMaster tables
- District-level caste/religion demographic aggregates (proxy avoidance)

### 4.3 Model Output

| Output | Type | Description |
|--------|------|-------------|
| Score | DECIMAL(6,5) | 0.00000 (low risk) to 1.00000 (high risk) |
| Feature importance | JSON array | Per-feature importance values |

### 4.4 Training Plan

| Step | Description | Owner |
|------|-------------|-------|
| 1 | Generate synthetic training data with labeled repeat offenders | Developer |
| 2 | Train baseline model (logistic regression) | Developer |
| 3 | QuickML AutoML with interpretability constraint | Developer |
| 4 | Compare baseline vs AutoML on held-out set | Developer |
| 5 | Fairness check: verify no restricted features in top-20 importance | Developer + Compliance |
| 6 | Deploy best model | Developer |

## 5. Natural Language Query (RAG)

### 5.1 Architecture

```
User Question (English)
  → Intent Classification (predefined template OR free-text RAG)
  → [Template path] → Parameterized Catalyst Data Store query → Response
  → [RAG path] → Retrieve from int_RAGCorpusChunk (vector similarity)
                → QuickML LLM with chunk context → Grounded answer + citations
```

### 5.2 Query Templates (Predefined)

| Intent | Template | Example |
|--------|----------|---------|
| Case count by district | `SELECT DistrictName, COUNT(*) FROM ... GROUP BY ...` | "How many FIRs in Bengaluru Urban?" |
| Crime head breakdown | `SELECT CrimeGroupName, COUNT(*) FROM ... GROUP BY ...` | "Show me theft cases by district" |
| Person search | `SELECT * FROM PersonEntity WHERE CanonicalName LIKE '%?%'` | "Tell me about Ramesh Kumar" |
| Risk score lookup | `SELECT Score, FeatureImportance FROM ... WHERE PersonEntityID = ?` | "What is the risk score for accused in case FIR-2024001?" |

### 5.3 Free-Text RAG

For questions that do not match a template, the system uses retrieval-augmented generation:

1. Embed the question (QuickML LLM embedding)
2. Vector similarity search in `int_RAGCorpusChunk` (top-k=5)
3. Retrieve full chunk text
4. Build prompt: context + question
5. Generate answer via QuickML LLM
6. Post-process: verify citations, append disclaimer

### 5.4 Safety Controls

| Control | Implementation |
|---------|---------------|
| Insufficient evidence response | If max similarity < 0.7, respond "Insufficient evidence" |
| Role-aware filtering | Before retrieval, filter chunks by CaseMaster.PoliceStationID against user's jurisdiction |
| Query auditing | Every question, retrieved chunks, and answer logged to gov_AuditLog |
| No PII in responses | Person names returned but CasteID/ReligionID fields stripped |

## 6. Model Governance

| Model | Version Strategy | Retraining Trigger | Champion/Challenger |
|-------|-----------------|-------------------|---------------------|
| NER (spaCy) | Fixed model version (en_core_web_lg) | None (Phase 1) | No |
| Risk scoring | Semver (e.g., 1.0.0, 1.1.0) | New synthetic dataset or feature addition | Yes (compare accuracy) |
| LLM (RAG) | QuickML managed version | QuickML platform updates | No (single model) |

## 7. Per-Component Specification Contracts

### 7.1 NER (Named Entity Recognition)

| Aspect | Detail |
|--------|--------|
| **User Decision Supported** | Which entities (persons, vehicles, locations, dates) to extract from FIR narrative text |
| **Input Contract** | BriefFacts (NVARCHAR(MAX)) from CaseMaster |
| **Output Contract** | PersonEntityLink, VehicleLink records with entity type, value, confidence score, position |
| **Training/Inference Approach** | Inference only — pre-trained spaCy `en_core_web_lg`; no custom training for MVP |
| **Baseline Method** | Regex patterns for vehicle number (`[A-Z]{2}-\d{2}-[A-Z]{1,2}-\d{4}`) and phone (`\d{10}`); spaCy defaults for person/location/ORG |
| **Explainability** | Confidence score per entity via per-signal scoring table |
| **Confidence/Uncertainty** | Sum of signal points (exact match +0.20, high NER confidence +0.10, partial match +0.05, multiple occurrences +0.05 each, max +0.15) |
| **Human Review Point** | None (fully automated); entities are always extracted with no manual curation step |
| **Evaluation Metrics** | Precision, recall, F1 on planted entities in synthetic FIRs |
| **Failure Modes** | Missed entities (low NER confidence for Indian name patterns), wrong entity type classification, missed Kannada names |
| **Monitoring/Drift** | Entity count per case, confidence score distribution, entity-type breakdown by district |
| **Bias/Privacy Risks** | May under-extract Kannada-language names with `en_core_web_lg`; no privacy risk since all data is synthetic |
| **Catalyst Mapping** | Catalyst Function (Python) triggered on CaseMaster INSERT |
| **MVP Fallback** | Manual entity entry via Investigator Console |

### 7.2 Entity Resolution

| Aspect | Detail |
|--------|--------|
| **User Decision Supported** | Whether two source records (ComplainantDetails/Victim/Accused) refer to the same real-world person |
| **Input Contract** | Source record fields: Name, Age, DistrictID, Address |
| **Output Contract** | PersonEntityID assignment with Confidence score; int_PersonEntityLink record |
| **Training/Inference Approach** | Rule-based blocking + weighted similarity scoring (Phase 1); learned model deferred to Phase 3+ |
| **Baseline Method** | Exact match on Name + DistrictID |
| **Explainability** | Per-feature similarity breakdown displayed in Investigator Console |
| **Confidence/Uncertainty** | Weighted composite score 0.00000–1.00000; grey zone (0.50–0.85) triggers manual review |
| **Human Review Point** | Grey zone (LOW_THRESHOLD 0.50 < score ≤ HIGH_THRESHOLD 0.85); reviewed in Investigator Console |
| **Evaluation Metrics** | Recall (> 90%), precision (> 95%), processing time (< 500ms), manual review ratio (< 20%) |
| **Failure Modes** | False positive auto-link (score > 0.85 but different persons), false negative missed match, blocking filter removes true candidate |
| **Monitoring/Drift** | Grey zone ratio alert (> 0.30), false positive audit log review, threshold adjustment |
| **Bias/Privacy Risks** | Name-based features may favor certain name patterns; CasteID/ReligionID explicitly excluded from similarity computation |
| **Catalyst Mapping** | Catalyst Function (Python) triggered on source record INSERT |
| **MVP Fallback** | Manual linking only via "Link to existing person" UI with confidence set to 1.0 |

### 7.3 Risk Scoring

| Aspect | Detail |
|--------|--------|
| **User Decision Supported** | Risk level of a person (repeat-offender probability) |
| **Input Contract** | PersonEntity features: num_prior_cases, num_districts, age_group, crime_type_diversity, has_co_accused, arrest_count, avg_case_severity, recency_days |
| **Output Contract** | Score DECIMAL(6,5) (0.00000–1.00000) + Feature importance JSON array |
| **Training/Inference Approach** | QuickML AutoML binary classification on synthetic labeled data |
| **Baseline Method** | Heuristic: score = min(1.0, prior_case_count / 10) |
| **Explainability** | Per-feature importance values returned alongside score |
| **Confidence/Uncertainty** | Raw score value 0–1; higher values indicate stronger recidivism signal |
| **Human Review Point** | Score > 0.70 may trigger additional review; investigator can override score |
| **Evaluation Metrics** | AUC, precision-recall, fairness metrics (score distribution by gender and district) |
| **Failure Modes** | Over-reliance on limited synthetic training data, distribution shift between synthetic and real data, feature importance instability |
| **Monitoring/Drift** | Score distribution tracking, feature importance drift, fairness check cron job (CRON-004) |
| **Bias/Privacy Risks** | CasteID, ReligionID, and demographic proxies explicitly excluded from feature set; fairness check validates exclusion |
| **Catalyst Mapping** | Catalyst QuickML model; inference via Catalyst Function |
| **MVP Fallback** | Rule-based heuristic: score = min(1.0, count of prior cases / 10) |

### 7.4 Natural Language Query (RAG)

| Aspect | Detail |
|--------|--------|
| **User Decision Supported** | Which cases, persons, or statistics answer the investigator's natural language question |
| **Input Contract** | User question (English, free-text) |
| **Output Contract** | Natural language answer + citations from retrieved chunks |
| **Training/Inference Approach** | Pre-trained LLM (QuickML managed) + vector similarity over int_RAGCorpusChunk |
| **Baseline Method** | Template-only queries (5 predefined SQL intents) |
| **Explainability** | Retrieved chunk citations shown alongside the answer |
| **Confidence/Uncertainty** | Max vector similarity score; < 0.7 triggers "Insufficient evidence" response |
| **Human Review Point** | None (disclaimer appended to every answer); query audit logged |
| **Evaluation Metrics** | Answer relevance, citation accuracy, hallucination rate, insufficient-evidence rate |
| **Failure Modes** | Hallucination (LLM generates ungrounded content), irrelevant chunk retrieval, template misclassification, missing evidence |
| **Monitoring/Drift** | Query audit log (every question + chunks + answer logged to gov_AuditLog), insufficient evidence rate, template vs RAG ratio |
| **Bias/Privacy Risks** | Role-aware filtering by jurisdiction; PII stripped from responses; may only retrieve from available chunk corpus |
| **Catalyst Mapping** | Catalyst QuickML LLM + vector search; Catalyst Cache for template parameters |
| **MVP Fallback** | Template-only queries when LLM unavailable or similarity < 0.7 |
