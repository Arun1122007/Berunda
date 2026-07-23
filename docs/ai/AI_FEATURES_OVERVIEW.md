# AI Features Overview and Threat Model

## Architecture
The AI subsystem relies on a decoupled, provider-agnostic framework centered around the `BaseProvider` and `ProviderRegistry`. 

### Key Components
1. **Providers**: Configurable adapters (`OpenAICompatibleProvider`, `GroqProvider`) supporting streaming, embeddings, and structured outputs via generic schemas.
2. **Usage Tracking**: `AIUsageService` records tokens, latencies, and calculates costs.
3. **RAG Service**: Utilizing `EmbeddingService` for vector processing with dynamic batching. Embeddings are stored efficiently as JSON in Postgres.
4. **Guardrails**: `GuardrailsService` provides robust safety checks on input (prompt injection, PII stripping) and output (unsubstantiated claims, demographic fairness).

## Threat Model
### 1. Prompt Injection
- **Risk**: Malicious users injecting SQL or manipulating AI behavior.
- **Mitigation**: `InputGuardrail` regex checks prior to LLM interaction. Future: secondary LLM evaluator.

### 2. PII Leakage
- **Risk**: Sending Aadhaar, PAN, or phone numbers to third-party LLM providers.
- **Mitigation**: Mandatory regex masking on all outbound payloads in `InputGuardrail`.

### 3. Demographic Bias & Hallucinations
- **Risk**: AI generating biased assumptions based on caste/religion.
- **Mitigation**: `OutputGuardrail` detects sensitive terms. Triggered events log to `gov_FairnessCheckResult` for manual review.

### 4. Untrusted Outputs
- **Risk**: Direct execution of AI-generated SQL or code.
- **Mitigation**: Strict sandboxing. Model outputs are strictly presented as insights or parsed into restricted schemas via instructor.
