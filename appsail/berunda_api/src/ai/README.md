# Berunda AI Module (`src/ai/`)

> **Module:** Artificial Intelligence
> **Classification:** INTERNAL
> **Last Updated:** 2026-07-18

---

## Architecture Overview

The AI module provides a complete LLM-integration layer for the Berunda platform,
following a modular, pluggable architecture.

```
┌─────────────────────────────────────────────────────────┐
│                     User Query                           │
└──────────┬──────────────────────────────────────────────┘
           │
           ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────┐
│   Guardrails     │───▶│   Orchestration  │───▶│   Agents     │
│  (input filter)  │    │  (CoT + routing) │    │  (specialised)│
└──────────────────┘    └────────┬─────────┘    └──────────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
            ┌──────────┐ ┌──────────┐ ┌──────────────┐
            │  Tools   │ │  Memory  │ │  Retrieval   │
            │(domain)  │ │(session) │ │ (RAG pipeline)│
            └──────────┘ └──────────┘ └──────┬───────┘
                                             │
                                    ┌────────▼────────┐
                                    │   Providers     │
                                    │ (LLM backends)  │
                                    └────────┬────────┘
                                             │
                                    ┌────────▼────────┐
                                    │   Inference     │
                                    │ (retry/fallback)│
                                    └────────┬────────┘
                                             │
                                    ┌────────▼────────┐
                                    │   Evaluation    │
                                    │  + Observability │
                                    └─────────────────┘
```

---

## Submodules

### Agents (`src/ai/agents/`)
Specialized AI agents that combine LLM reasoning with domain-specific tools.
- **Investigation Agent**: Deep-dive case analysis, entity linking, timeline reconstruction
- **Analyst Agent**: Trend analysis, pattern recognition, report generation
- **Admin Agent**: System configuration, user management, audit queries

### Prompts (`src/ai/prompts/`)
Versioned prompt templates organized by purpose:
- `system/` — System-level prompts defining agent persona and constraints
- `tasks/` — Task-specific prompts for each operation
- `evaluation/` — Prompts for grading answer quality
- `versions/` — Version registry for prompt rollback

### Providers (`src/ai/providers/`)
Abstract base class `BaseProvider` with concrete implementations:
- **Catalyst QuickML**: Zoho Catalyst's serverless ML inference endpoint
- **OpenAI-compatible**: Any OpenAI API-compatible provider (Azure, Together, etc.)
- Configuration via environment variables (`LLM_PROVIDER`, `LLM_API_KEY`, etc.)

### Orchestration (`src/ai/orchestration/`)
Manages multi-step reasoning chains:
- Chain-of-thought (CoT) decomposition of complex queries
- Tool selection and sequencing
- Context window management
- Streaming response handling

### Tools (`src/ai/tools/`)
Domain-specific tools registered via `BaseTool` subclassing:
- `search_cases` — Query FIR database by criteria
- `get_entity_details` — Retrieve person/vehicle/place profile
- `get_hotspot_data` — Fetch crime hotspot statistics
- `get_risk_score` — Compute risk score for an entity
- `run_link_analysis` — Build entity relationship graph

### Guardrails (`src/ai/guardrails/`)
Multi-layer safety system:
- **Input guard**: Prompt injection detection, PII/sensitive field exclusion
- **Output guard**: Hallucination detection, sensitive content filtering
- **Role-based access**: Content restrictions per user role

### Memory (`src/ai/memory/`)
Dual-layer memory:
- **Short-term**: In-memory session context with sliding window
- **Long-term**: Persistent storage via Catalyst NoSQL for cross-session continuity

### Retrieval (`src/ai/retrieval/`)
Complete RAG pipeline:

```
Documents ──▶ Loaders ──▶ Chunking ──▶ Embeddings ──▶ Index ──▶ Retrieval ──▶ Reranking
(Excel,PDF,CSV)  (split)    (vectorize)   (store)    (search)    (re-rank)
```

### Inference (`src/ai/inference/`)
Robust LLM interaction layer:
- Configurable model, temperature, max tokens
- Exponential backoff retry with jitter
- Fallback provider chain
- Streaming and non-streaming modes

### Evaluation (`src/ai/evaluation/`)
Metrics for AI output quality:
- **Faithfulness**: Does the answer stay true to retrieved context?
- **Answer Relevance**: Is the answer directly responding to the query?
- **Context Precision**: Are retrieved documents relevant?
- **Hallucination Rate**: Ratio of unsupported claims

### Observability (`src/ai/observability/`)
Telemetry data collection:
- Token count per request per model
- Cost estimation per provider
- Latency percentiles (p50, p95, p99)
- Error rate tracking

### Schemas (`src/ai/schemas/`)
All Pydantic models defining structured I/O contracts:
`AgentRequest`, `AgentResponse`, `ToolCall`, `ToolResult`,
`Message`, `Conversation`, `RetrievalResult`, `EvaluationResult`

---

## RAG Pipeline Flow

1. **Document Loading**: Raw FIR Excel/CSV or PDF documents are loaded via
   loaders in `src/ai/retrieval/loaders/`
2. **Chunking**: Documents are split into overlapping chunks using configurable
   strategies (recursive character, sentence, semantic)
3. **Embedding**: Each chunk is vectorized via the configured embedding provider
4. **Indexing**: Vectors stored in a vector store (InMemoryIndex for dev,
   Catalyst NoSQL for production)
5. **Retrieval**: User query is embedded and approximate nearest neighbors are
   retrieved
6. **Reranking**: Retrieved chunks are re-ranked by a cross-encoder or LLM-based
   reranker for precision
7. **Augmented Generation**: Top-k chunks are injected into the prompt context
   for the LLM to generate the final answer

---

## Configuration

The AI module is configured via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `catalyst` | Provider name |
| `LLM_MODEL` | `catalyst/llm-model` | Model identifier |
| `LLM_API_KEY` | — | API key |
| `LLM_TEMPERATURE` | `0.3` | Generation temperature |
| `LLM_MAX_TOKENS` | `4096` | Max output tokens |
| `LLM_RETRY_ATTEMPTS` | `3` | Retry count |
| `LLM_FALLBACK_PROVIDER` | — | Fallback source |
| `EMBEDDING_PROVIDER` | `catalyst` | Embedding source |
| `EMBEDDING_MODEL` | `catalyst/embed-model` | Embedding model |

See `src/shared/config/` for the full configuration loading framework.
