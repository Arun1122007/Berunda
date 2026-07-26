# AI Threat Model and Adversarial Test Plan

> **Document ID:** BERUNDA-AI-P8-003 | **Version:** 1.0 | **Status:** APPROVED

## 1. Threat Vectors
- **Prompt Injection:** Attempt to extract system instructions.
- **Cross-Station Retrieval:** Attempt to fetch unauthorized FIR data via RAG.
- **Data Poisoning:** Embedding malicious instructions in FIR text.

## 2. Test Plan
- Create test suite in `tests/ai/test_adversarial.py` focusing on rejecting malicious instructions.
