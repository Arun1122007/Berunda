# Demo Data and Evidence Validation Plan

[//]: # (Document ID: BERUNDA-QA-004 | Status: DRAFT | Classification: INTERNAL)

---

## 1. Pre-Demo Validation Checklist

Run `scripts/validate_demo_data.py` before every demo:

```
CHECKLIST:
[✓] Synthetic data tag present and visible
[✓] Total FIRs between 2,000-5,000
[✓] All planted hidden links present (20-30)
    [✓] "One person, four names" test case
    [✓] Co-accused clusters (2-3)
    [✓] Accused-victim reversals (5 pairs)
    [✓] Vehicle-linked cases (10 vehicles)
    [✓] Family relationship clusters (5)
    [✓] Anomaly spike week present
[✓] Entity resolution finds all planted matches
[✓] Risk scores computed for all PersonEntities with cases
[✓] Anomaly alert exists for planted spike
[✓] RAG corpus indexed and searchable
[✓] Fairness checks all pass
[✓] All 5 demo questions produce correct answers
[✓] Audit log contains expected entries
[✓] "SYNTHETIC DATA" watermark visible on all interfaces
```

## 2. Evidence Pack Contents

The demo evidence pack is a pre-assembled ZIP file containing:

| Item | Format | Location |
|------|--------|----------|
| Data generation manifest | JSON | `output/planting_manifest.json` |
| Case statistics summary | PDF | `output/evidence/case_statistics.pdf` |
| Entity resolution proof (4→1) | Screenshot | `output/evidence/er_4_to_1.png` |
| Relationship graph screenshots | Screenshot | `output/evidence/graph_hidden_links.png` |
| Anomaly spike detection | Screenshot | `output/evidence/anomaly_spike.png` |
| Risk score with feature importance | Screenshot | `output/evidence/risk_score_explanation.png` |
| RAG Q&A with citations | Screenshot | `output/evidence/rag_citations.png` |
| Fairness check report | Screenshot | `output/evidence/fairness_check.png` |
| Audit log extract | CSV | `output/evidence/audit_log_sample.csv` |
| All screenshots annotated with "SYNTHETIC DATA" | PNG | `output/evidence/` |

## 3. "Smoking Gun" Demo Flow

The shortest path that demonstrates the entire value chain:

```
Step 1: Show FIR intake dashboard (5000 cases loaded)
Step 2: Search "Venkatesh" → PersonEntity with 4 linked cases
Step 3: Click PersonEntity → see relationship graph with 3 co-accused
Step 4: Search vehicle "KA-01-AB-1234" → see 2 linked cases
Step 5: Click hot district on map → drill down to anomalies
Step 6: Click anomaly → see 5x spike in Bengaluru Urban last week
Step 7: Click person with risk score 0.85 → feature importance shows 5 priors
Step 8: "Ask Berunda" → "What is the connection between FIR-001 and FIR-042?"
Step 9: System answers with cited case numbers
Step 10: Verify all AI outputs in audit log
Step 11: Show fairness check dashboard — all green
```

**Total demo time:** 3-4 minutes.

## 4. Fallback Plans

### 4.1 If Entity Resolution Fails

- Show pre-computed PersonEntity from the planting manifest
- Explain the expected behavior and that it's a known bug being debugged
- Move to next demo feature (geospatial / risk scoring / RAG)

### 4.2 If RAG Fails

- Have pre-typed the demo questions and expected answers on a backup PDF
- Show the RAG pipeline architecture on a slide
- Move to relationship graph demo

### 4.3 If QuickML / LLM Unavailable

- Risk scoring: show pre-computed scores from local test run
- RAG: show the architecture slide and pre-computed answers
- All other features (entity resolution, geospatial, anomaly) work independently

### 4.4 If Dashboard UI Is Unstable

- Catalyst Slate SPA is cached in the browser after first load
- If fresh load fails, show the app from a pre-loaded device
- Worst case: walk through the evidence pack PDF on screen

## 5. Post-Demo Validation

After the demo, run `scripts/validate_demo_output.py` to generate the documentation coverage report:

- Confirm all planted test cases were exercised (or explain why not)
- Collect any system errors or unexpected behavior for the bug log
- Generate the DOCUMENTATION_COVERAGE_MATRIX.md (Phase N)
