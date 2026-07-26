# AI Data Flow, Privacy, and Authorization

> **Document ID:** BERUNDA-AI-P8-002 | **Version:** 1.0 | **Status:** APPROVED

## 1. Data Minimization
- Retrieve only required FIRs.
- Exclude unrelated cases and operational secrets.
- Apply redaction to PII before prompt generation.

## 2. Authorization Boundaries
- Apply Station scope filters BEFORE AI embedding retrieval.
- No "search all cases" bypass permitted.
