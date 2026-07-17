# AI/ML System Specification

[//]: # (Document ID: BERUNDA-AI-001 | Status: DRAFT | Classification: CONFIDENTIAL)

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
