# 08 AI Safety and Governance

Project Berunda handles deeply sensitive criminal justice data. The AI Safety and Governance framework ensures that all deployments of LLMs, OCR, and predictive modeling adhere to legal and ethical standards.

## 1. Prompt Injection & Jailbreak Defenses
- **Defense Mechanism:** All inputs to QuickML are passed through the `guardrails_service.py` before hitting the model. The service scans for known jailbreak patterns and adversarial instructions.
- **System Prompt Hardening:** The system prompt explicitly forbids the AI from returning SQL commands, revealing internal logic, or modifying user identities.
- **Fail-Safe:** If an injection is detected, the API returns a generic `400 Bad Request` and flags the event in the `AuditLog` table.

## 2. Privacy and Data Leakage
- **Tenant Isolation in RAG:** The Vector Database (or Catalyst Knowledge Base) is partitioned by `DistrictID`. A user from District A cannot query or retrieve contextual chunks originating from District B's FIRs.
- **PII Scrubbing:** Before text is passed to any AI model for summarization or entity extraction, PII is scrubbed using the Presidio anonymizer. `[NAME_1]` replaces actual names to prevent the LLM from inadvertently memorizing and leaking real identities.

## 3. Human-in-the-Loop (HITL)
- **Review Requirements:** No AI-generated content (like an auto-generated Chargesheet summary) can be finalized or submitted to court without explicit human approval.
- **UI Indicators:** The frontend (`apps/web`) explicitly tags all AI-generated content with an `[AI Generated]` badge and provides a feedback loop (thumbs up/down) to report inaccuracies.

## 4. Auditability
- **Trace Logging:** Every request to QuickML or Zia is logged with the prompt, the response, the latency, and the `UserID` responsible for the action. These logs are stored in Catalyst NoSQL for a minimum of 90 days.
