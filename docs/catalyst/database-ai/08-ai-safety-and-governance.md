# 08 - AI Safety and Governance

## Core Principles
The Berunda project deals with highly sensitive law enforcement data. The AI implementation must enforce strict safety, fairness, and accountability boundaries.

### Prompt Management
- Prompts will not be hardcoded in routes. They will be managed in `src/ai/prompts/` and version-controlled.
- Every prompt must include grounding instructions (e.g., "Answer only based on the provided FIR context. Do not invent details.").

### Prompt Injection Defenses
- User queries will be sanitized.
- System instructions will be strictly delineated from user input using clear XML tags or ChatML roles.

### Guardrails for Predictions
- **No Individual Criminal Inference**: Risk scoring and Anomaly detection models are explicitly prohibited from inferring criminality based on protected demographics (Caste, Religion).
- **Human in the Loop**: Models provide recommendations (e.g., "Anomaly Detected"), but require an Analyst to review and acknowledge the alert.

### RAG and Data Isolation
- When users query the AI, the Catalyst Data Store adapter will first retrieve the subset of FIRs the user is allowed to access.
- QuickML will only receive these filtered context chunks to ensure the LLM cannot accidentally reveal cross-jurisdictional data to unauthorized officers.

### Tracing and Observability
- All QuickML and Zia API calls are logged in `ai_UsageRecord` with latency, token usage, and status.
- **Sensitive Data Minimization**: The raw user prompt is only stored temporarily or pseudonymized. Full sensitive documents are never printed to application logs.

### Feature Flags
- All AI features will be wrapped in feature flags (e.g., `ENABLE_RAG`, `ENABLE_ZIA_OCR`). This allows administrators to immediately kill AI functionality if hallucinations or security breaches are detected.
