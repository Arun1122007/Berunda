# 04 AI Feature Inventory

This document tracks all AI features in Project Berunda, assessing their current status and outlining the migration path to Catalyst AI services.

| AI Feature | Current Provider | Input | Output | Data Source | Current Status | Catalyst Target | Risk | Required Work |
| ---------- | ---------------- | ----- | ------ | ----------- | -------------- | --------------- | ---- | ------------- |
| **Document Q&A (RAG)** | Mixed (OpenAI/Groq/Catalyst) | User query, Document text | Grounded answer | Uploaded FIRs/PDFs | Partially implemented | Catalyst QuickML (RAG Pipeline) | High (Hallucination, Privacy leakage) | Connect Stratus blob extraction to QuickML knowledge base. Enforce user-isolation. |
| **Crime Risk Scoring** | Scikit-learn (local) / Mock | Case attributes | Risk Score (0-100) | `CaseMaster` | Mocked / Local | Zia AutoML / QuickML | High (Bias, Unfair profiling) | Replace local mock with Catalyst-deployed model inference or tabular prediction. Add fairness evaluation. |
| **Anomaly Detection** | Local stats | Time series crime data | Anomaly markers | `Inv_OccurrenceTime` | Partially implemented | Catalyst QuickML / Stats | Medium | Standardize output format. |
| **Text Summarization** | OpenAI/Groq | FIR `BriefFacts` | 1-paragraph summary | `Inv_OccurrenceTime` | Implemented via external API | Catalyst QuickML / Zia Text Analytics | Low | Migrate provider to Catalyst QuickML. |
| **Translation (Local Language)** | Missing | FIR `BriefFacts` | English text | `Inv_OccurrenceTime` | Planned | Catalyst Zia Translation | Low | Implement Zia translation endpoint. |

## Migration Strategy
- **Zia Services**: Utilize Catalyst's pre-trained Zia AI for standard tasks (OCR, Translation, Text Analytics).
- **QuickML**: Utilize QuickML for deploying custom models, large-language model (LLM) generation, and RAG pipelines.
- **Deprecation**: External API keys (`OPENAI_API_KEY`, `GROQ_API_KEY`) will be removed from `.env.production`. The Catalyst provider abstraction (`src/ai/providers/catalyst.py`) will become the default provider.
