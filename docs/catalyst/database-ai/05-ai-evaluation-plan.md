# 05 AI Evaluation Plan

To ensure the safety, accuracy, and reliability of the AI systems deployed within Project Berunda, this evaluation plan defines the automated and manual testing gates required before any AI feature can be promoted to production.

## 1. RAG Hallucination Detection
**Risk:** QuickML generates facts about a case not present in the original FIR, potentially misguiding an investigation.
**Evaluation Strategy:**
- **Automated Metric (Faithfulness):** We will utilize an LLM-as-a-judge (using a distinct QuickML prompt) to evaluate the generated answer against the retrieved context chunks. If the answer contains entities or actions not found in the chunks, the faithfulness score drops.
- **Pass Threshold:** 0.95 (out of 1.0)
- **CI/CD Integration:** Regression tests running synthetic questions against a frozen vector DB must pass the faithfulness threshold.

## 2. Structured Output Compliance
**Risk:** The LLM fails to return valid JSON, breaking the frontend anomaly/risk visualization.
**Evaluation Strategy:**
- **Automated Metric:** JSON Schema Validation.
- **Pass Threshold:** 100%. If parsing fails, the system must fallback gracefully and log a parsing error to Catalyst NoSQL.

## 3. Crime Risk Model Fairness Audit
**Risk:** The automated risk scoring algorithm penalizes individuals based on proxy variables (e.g., location, name ethnicity).
**Evaluation Strategy:**
- **Metric (Disparate Impact):** The fairness service (in `src/services/fairness_service.py`) calculates the positive prediction rate across different protected groups in the testing data.
- **Pass Threshold:** The disparate impact ratio must be between 0.8 and 1.25 (the 80% rule).
- **Manual Gate:** Any new model weights deployed to Catalyst Zia AutoML require manual sign-off from the project administrator.
