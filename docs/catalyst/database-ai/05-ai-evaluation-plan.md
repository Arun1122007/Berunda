# 05 - AI Evaluation Plan

## Objective
Establish a repeatable AI evaluation suite for Berunda to measure the accuracy, fairness, and safety of QuickML and Zia Service integrations.

## Datasets
- **Golden FIR Dataset**: A curated dataset of 200 historically representative FIRs to test extraction and RAG queries.
- **Adversarial Query Dataset**: 50 prompt-injection attempts and restricted-information requests to verify safety guardrails.
- **Fairness Dataset**: Tabular risk score validation dataset to check equalized odds and demographic parity.

## Evaluation Metrics

### QuickML RAG & Knowledge Base
- **Groundedness**: Do the generated answers rely *only* on retrieved context? (Target: >95%)
- **Retrieval Relevance (MRR/NDCG)**: Did the system fetch the right documents? (Target: >85%)
- **Latency**: P95 response time under 3 seconds.
- **Citation Correctness**: Are citations accurate and linked to the source FIR? (Target: 100%)

### Zia OCR & Text Extraction
- **Extraction Accuracy (WER/CER)**: Character and Word Error Rates on scanned PDFs (Target: <5% CER).

### Zia AutoML (Risk Scoring / Anomaly)
- **Precision/Recall/F1**: For structured tabular predictions (Target: >80% F1).
- **Calibration**: Does the 80% risk score actually translate to an 80% empirical risk?
- **Bias / Fairness**: Verify that Protected Attributes (e.g., Religion, Caste) do not statistically skew the risk scores.

## Automation
Automated regression tests will run during Catalyst Pipelines deployment using an independent evaluator (e.g. LLM-as-a-judge or exact match checks) to ensure quality remains above thresholds.
