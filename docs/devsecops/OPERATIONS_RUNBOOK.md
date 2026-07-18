# Operations Runbook

[//]: # (Document ID: BERUNDA-OPS-005 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: DevOps, Developers | Source: Architecture docs + Catalyst docs | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Common Tasks

### 1.1 Generate Synthetic Data

```bash
python scripts/generate_synthetic_data.py --count 5000 --seed 42
```

Output: SQL scripts in `output/sql/`, CSV files in `output/csv/`.

### 1.2 Import Data into Catalyst Data Store

```bash
# Import all tables
catalyst datastore:import --file output/sql/01_lookup_tables.sql
catalyst datastore:import --file output/sql/02_case_master.sql
catalyst datastore:import --file output/sql/03_persons.sql
# ... remaining tables
catalyst datastore:import --file output/sql/08_tag_synthetic.sql

# Verify
python scripts/validate_demo_data.py
```

### 1.3 Run All Tests

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests (requires deployed testing environment)
pytest tests/integration/ -v --base-url https://testing.catalystapps.io/api/v1

# Security tests
pytest tests/security/ -v --base-url https://testing.catalystapps.io/api/v1

# Acceptance tests (requires deployed staging environment)
pytest tests/acceptance/ -v --base-url https://staging.catalystapps.io/api/v1
```

### 1.4 Deploy to Staging

```bash
git tag v1.0.0
git push origin v1.0.0
# Catalyst Pipelines automatically deploys to Staging
```

### 1.5 Deploy to Production

1. Verify Staging acceptance tests pass: `python scripts/validate_demo_data.py`
2. Approve in Catalyst Pipelines (manual gate)
3. Run smoke test: `curl https://production.catalystapps.io/api/v1/health`

## 2. Troubleshooting

### 2.1 Entity Resolution Not Catching Planted Matches

**Symptoms:** "One person, four names" test case does not resolve to single PersonEntity.

**Checklist:**
- [ ] Verify thresholds: `catalyst cache:get --key entity_resolution`
- [ ] Verify weights: `catalyst cache:get --key entity_resolution.weights`
- [ ] Verify names are in the input data: `SELECT * FROM Accused WHERE AccusedName LIKE '%Venkat%'`
- [ ] Check function logs: `catalyst functions:logs --function entity-resolution --last 100`
- [ ] Re-run with debug: `python scripts/debug_entity_resolution.py --person-id <id>`

**Most likely cause:** Threshold too high for phonetic variants. Reduce HIGH_THRESHOLD to 0.80.

### 2.2 RAG Returning "Insufficient Evidence"

**Symptoms:** RAG query on a known case returns "Insufficient evidence."

**Checklist:**
- [ ] Verify RAG corpus is populated: `SELECT COUNT(*) FROM int_RAGCorpusChunk`
- [ ] Check similarity threshold: `catalyst cache:get --key rag.similarity_threshold`
- [ ] Verify embeddings exist: `SELECT COUNT(*) FROM int_RAGCorpusChunk WHERE Embedding IS NOT NULL`
- [ ] Check QuickML status: `GET /health`

**Most likely cause:** Embeddings not computed for newly imported cases. Re-run chunking pipeline.

### 2.3 Risk Score All Zero

**Symptoms:** All PersonEntities have risk score = 0.00000.

**Checklist:**
- [ ] Verify CRON-003 ran: `SELECT * FROM int_RiskScore ORDER BY ComputedAt DESC LIMIT 1`
- [ ] Check QuickML AutoML endpoint: `GET /health`
- [ ] Verify model deployed: `ls models/risk_scoring/`
- [ ] Check function logs: `catalyst functions:logs --function risk-scoring --last 100`

**Most likely cause:** QuickML AutoML model not deployed or feature mismatch.

### 2.4 Fairness Check Fails

**Symptoms:** FC-001 or FC-002 reports failure.

**Action:**
1. **IMMEDIATE:** Block any model deployment or API changes
2. Identify which feature contains restricted data: `SELECT * FROM gov_FairnessCheckResult ORDER BY Timestamp DESC LIMIT 1`
3. Remove restricted feature from the model
4. Re-train and re-deploy
5. Re-run fairness check
6. Document in incident register

### 2.5 Import Fails

**Symptoms:** POST /cases/import returns error.

**Checklist:**
- [ ] Check import log: `SELECT * FROM gov_AuditLog WHERE Action = 'CASE_IMPORT' AND Timestamp > NOW() - INTERVAL 1 HOUR`
- [ ] Verify CSV/JSON format against schema
- [ ] Check for duplicate CrimeNo
- [ ] Check Data Store connection: `GET /health`

## 3. Daily Operations Checklist

| Time | Task | Owner |
|------|------|-------|
| Morning (Day 1) | Verify synthetic data seed ran successfully | Developer |
| Morning (Daily) | Check health endpoint | Developer |
| Morning (Daily) | Review fairness check results | Compliance |
| Afternoon (Daily) | Review audit log for anomalies | Compliance |
| Evening (Daily) | Verify nightly cron jobs completed | Developer |
| Pre-Demo | Run full validation checklist | Developer + Team Lead |

## 4. Escalation Contacts

| Issue | Contact | Response Time |
|-------|---------|---------------|
| Catalyst platform down | Catalyst Support Portal | 4 hours (free tier) |
| QuickML outage | Catalyst Support Portal | 4 hours |
| Security incident | Developer + Team Lead | 1 hour |
| Data corruption | Developer | 2 hours |
