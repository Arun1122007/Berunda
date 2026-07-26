# Summarization and Category Suggestion Report

> **Document ID:** BERUNDA-AI-P8-005 | **Version:** 1.0 | **Status:** APPROVED

## 1. Summarization
- Concise chunking implemented for long FIRs.
- Mandatory warning: "AI Generated Summary".

## 2. Crime Category
- Implemented in `src/ai/services/crime_category.py`.
- Supports Top-K suggestions with 'insufficient-info' fallback.
