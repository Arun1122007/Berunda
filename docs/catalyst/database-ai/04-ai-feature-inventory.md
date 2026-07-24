# 04 - AI Feature Inventory

| AI Feature | Current Provider | Input | Output | Data Source | Current Status | Catalyst Target | Risk | Required Work |
| ---------- | ---------------- | ----- | ------ | ----------- | -------------- | --------------- | ---- | ------------- |
| **RAG (Case Search)** | OpenAI (via `.env`) | User Query | Answer with Citations | FIR Text | Partially implemented (Mocked) | **QuickML Knowledge Base** | Hallucinations, Data Exposure | Rip out OpenAI, use QuickML ZCQL integration. |
| **Anomaly Detection** | Custom/Placeholder | FIR Data | Anomaly Alert | FIR Records | Planned/Mocked | **QuickML Prediction** | False Positives | Train QuickML classification model or use basic ML. |
| **Risk Scoring** | Custom/Placeholder | Person History | Score (0-100) | `int_PersonEntity` | Planned/Mocked | **Zia AutoML** | Bias, Unfairness | Replace with structured Zia AutoML tabular prediction. |
| **Document OCR** | None | PDF/Image | Text | `FIR Scans` | Missing | **Zia OCR** | PII Leakage | Extract text from uploaded FIR scans and seed Knowledge Base. |
| **Translation** | None | Kannada/English | English/Kannada | `FIR BriefFacts` | Missing | **Zia Translation** | Mistranslation | Translate vernacular FIR text to English for analysis. |

## Action Plan
- Remove `OPENAI_API_KEY` dependencies.
- Replace LLM calls in `src/routers/rag_router.py` with `zcatalyst_sdk.zia()` calls.
- Integrate Zia OCR for uploaded FIRs.
