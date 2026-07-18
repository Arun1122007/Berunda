# rag-query

Natural language question-answering over the case corpus using QuickML LLM with Retrieval-Augmented Generation (RAG).

## Trigger

**HTTP** — POST

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/rag/query` | Submit a natural language query |
| POST | `/rag/feedback` | Submit feedback on a response |

## Input Schema

```json
{
  "query": "string (required)",
  "filters": {
    "districts": ["string"],
    "crimeTypes": ["string"],
    "dateRange": {
      "start": "ISO-8601",
      "end": "ISO-8601"
    }
  },
  "topK": 5
}
```

## Output Schema

```json
{
  "success": true,
  "data": {
    "answer": "string",
    "citations": [
      {
        "caseNumber": "string",
        "snippet": "string",
        "relevance": 0.95,
        "source": "string"
      }
    ],
    "confidence": 0.87,
    "processingTimeMs": 1234
  }
}
```

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| VALIDATION_ERROR | 400 | Empty or malformed query |
| RAG_FAILED | 500 | LLM or retrieval error |
| NO_CONTEXT | 404 | No relevant cases found |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `RAG_MODEL_ID` | — | QuickML LLM model ID |
| `RAG_EMBEDDING_MODEL` | — | Embedding model for vector search |
| `RAG_TOP_K` | `5` | Number of context chunks to retrieve |
| `RAG_MAX_TOKENS` | `1024` | Maximum generation tokens |
| `RAG_TEMPERATURE` | `0.3` | LLM temperature parameter |

## Processing Flow

```
POST /rag/query
  → Embed query using QuickML embedding model
  → Vector search over case corpus
  → Retrieve top-K relevant chunks
  → Build prompt with context
  → Call QuickML LLM for answer generation
  → Ground answer with citations
  → Log to audit trail
  -> Return answer + citations
```
