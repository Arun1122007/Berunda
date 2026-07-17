# ADR-006: RAG and Natural Language Query Safety

[//]: # (Document ID: ADR-006 | Status: APPROVED | Classification: INTERNAL)

---

## Context

The "Ask Berunda" feature allows plain-English questions over case data. Without safety controls, this could expose sensitive data, hallucinate answers, or enable SQL injection through natural language.

## Decision

Apply the following safety controls:

1. **Retrieval-before-generation** — Every answer is grounded in retrieved source documents; no free-text generation from the model alone
2. **Parameterized query templates** — Natural language intent is classified into a predefined query template, not free-form SQL. NO free-form natural-language-to-SQL
3. **Citation requirement** — Every answer must cite the source document(s) it was derived from
4. **Role-aware retrieval** — Document retrieval respects RBAC; a user cannot retrieve documents outside their jurisdiction
5. **Field-level access control** — Restricted fields (CasteID/ReligionID) are excluded from the RAG corpus entirely
6. **Insufficient evidence response** — When retrieved documents do not support an answer, the system says "Insufficient evidence" rather than hallucinating
7. **Full query audit** — Every query, retrieved context, and generated answer is logged to AuditLog
8. **Pre-rehearsed demo questions** — 3-5 questions are prepared and tested against the frozen dataset for the live demo

## Rationale

- Unrestricted natural-language-to-SQL would create SQL injection and data exposure risks
- Retrieval-before-generation is the current best practice for production RAG systems
- Cited answers enable verification and build trust with human reviewers
- Role-aware retrieval prevents accidental data exposure across jurisdictions
- The rehearsed-question approach prevents live-demo LLM unpredictability while still demonstrating the capability

## Consequences

- Positive: Safe, auditable, and explainable natural-language access to case data
- Positive: Citations enable users to verify answers against source records
- Positive: Query audit creates accountability
- Negative: Rehearsed questions may appear staged if not handled naturally
- Negative: Template-based intent classification is less flexible than free-form NL-to-SQL

## Status

APPROVED
