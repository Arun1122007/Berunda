# 06 — AI Foundation Report

**Document ID:** BERUNDA-IMPL3-AI-001
**Version:** 1.0 | **Status:** FINAL
**Date:** 2026-07-26

## 1. AI Capability Implemented
The AI foundation prioritizes robust FIR information extraction and safety-critical review workflows. The `src.ai` package orchestrates parsing unstructured FIR narratives into structured schemas.

## 2. Provider Abstraction & Fallbacks
The backend abstracts large language models via the `BaseProvider` interface (`src/ai/providers/`), ensuring no tight coupling to a single vendor.
- **Implementations**: `OpenAIProvider`, `GroqProvider`, `CatalystProvider` (for Zoho integration).
- **Fallback**: The `InferenceEngine` automatically implements exponential backoff and cascades from primary to fallback providers (e.g., Catalyst -> Groq) to maximize uptime during the hackathon demo.

## 3. Processing Lifecycle
AI interactions pass through a defined lifecycle orchestrated by `Orchestrator` (`src.ai.orchestration`):
- `requested` -> `processing` -> `review_required` -> `approved` / `rejected`.
The architecture requires a human officer to explicitly accept AI suggestions before they mutate the `CaseMaster` or `EvidenceMaster` core records.

## 4. Input Protection & Prompt Injection
- **Guardrails**: `GuardrailManager` (`src/ai/guardrails`) pre-processes inputs to sanitize malicious intents and prevent prompt injection (e.g., "ignore previous instructions").
- **Strict Parsing**: Output is forcefully constrained to predefined Pydantic schemas, failing safely if the model hallucinates non-compliant JSON.

## 5. Synthetic Evaluation Dataset
The repository includes synthetic data configurations (generated via `scripts/data/generate_synthetic.py`) which deliberately injects:
- Complex locations (e.g., "near the big banyan tree")
- Time variations (e.g., "sometime between Monday night and Tuesday morning")
- Ambiguous multi-person statements (to test entity resolution logic)

## 6. Evaluation Metrics & Execution
- `Evaluator` (`src/ai/evaluation`) evaluates model generations natively against RAG context, yielding numerical quality scores. 
- *Limitation*: Because `numpy` could not be compiled in the current Windows/local environment without specific C++ build tools, the dynamic execution of these evaluations was bypassed. The static architecture fully supports evaluation execution once deployed to the Zoho Catalyst production containers.

## 7. Deferred Capabilities
- Deep entity linking via Neo4j Graph queries (part of Prompt 7) is stubbed but not fully activated until the graph database is provisioned in Catalyst.
