# 06 QuickML & Zia Integration

This document outlines how Catalyst's AI features are integrated into Berunda.

## 1. QuickML (LLM Generation and Structured Output)
- **Role:** Replaces OpenAI and Groq for generating unstructured summaries and structured evaluations (e.g. Anomaly Detection JSON outputs).
- **Current Implementation:** Handled by `CatalystProvider` which issues a POST to `/functions/llm-chat/execute`. 
- **Migration Plan:** The default `provider` injected into our Agent orchestrators will be forced to `CatalystProvider` in production via `.env.production` (i.e. `DEFAULT_AI_PROVIDER=catalyst`).

## 2. Zia OCR (Optical Character Recognition)
- **Role:** Extracts text from uploaded physical FIR documents and evidence (e.g., photos of license plates, handwritten police reports).
- **Implementation:** 
  We utilize the Catalyst Python SDK:
  ```python
  import zcatalyst_sdk
  app = zcatalyst_sdk.initialize()
  zia = app.zia()
  result = zia.extract_optical_characters(image_file, {"language": "eng", "modelType": "OCR"})
  ```
- **Pipeline:**
  1. A user uploads an image via the frontend.
  2. The backend stores it in Catalyst Stratus.
  3. A background task reads the image from Stratus and invokes `zia.extract_optical_characters`.
  4. The extracted text is sent to QuickML for summarization.

## 3. Zia Text Analytics & Translation
- **Role:** Sentiment Analysis, Keyword Extraction, and NER for incoming intelligence reports. 
- **Note on Translation:** Since Catalyst Zia Services Python SDK currently lacks a public translation API method directly comparable to its OCR component, any local language translation requirements (e.g., Kannada to English) will leverage an external fallback (like a supported specialized API) securely isolated in `src/ai/providers/translation.py`, or will utilize an LLM prompt via QuickML.
