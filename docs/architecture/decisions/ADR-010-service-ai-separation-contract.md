# ADR-010: Service-to-AI Separation Contract

**Document ID:** ADR-010 | **Version:** 1.0 | **Status:** APPROVED
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-23

---

## Status

APPROVED — accepted as Phase 1 debt; remediation deferred to Phase 2.

## Context

The phase-1-validated-architecture.md defines strict layer rules: L4 (services) should not import from L3 (ai/). However, runtime verification found two violations:

1. `src/services/guardrails_service.py` imports `from src.ai.guardrails import GuardrailManager, GuardrailResult`
2. `src/services/embedding_service.py` imports `from src.ai.providers import create_provider`

Additionally, `src/services/rag_service.py` imports `src.services.embedding_service`, creating cross-service coupling at the same layer.

These violations exist because:
- Guardrails are both an AI concern (content filtering, PII detection) and a governance concern (audit logging, fairness checks), straddling the L3/L4 boundary.
- Embedding generation is an AI concern, but embeddings are stored in the database via services.
- RAG query orchestration needs both AI providers (for generation) and data access (for context retrieval).

## Decision

### Phase 1 (Accept Debt)
Accept the current layering violations as Phase 1 architectural debt. The violations are:
- **Acyclic**: `ai/` does not import from `services/`, so no circular dependency exists.
- **Isolated**: Only 2 service files are affected (guardrails_service, embedding_service).
- **Functional**: The code runs correctly despite the layering violation.

### Phase 2 (Remediation Plan)
Extract shared interface contracts into a neutral location that both layers can depend on:

1. **Create `src/shared/interfaces/` package** with:
   - `guardrail.py`: `GuardrailProtocol` abstract class defining `check_input(text) -> GuardrailResult` and `check_output(text, context) -> GuardrailResult`
   - `embedding.py`: `EmbeddingProtocol` abstract class defining `generate(texts) -> list[list[float]]`
   - `provider.py`: `LLMProviderProtocol` abstract class defining `complete(messages) -> CompletionResult`

2. **Update `src/ai/` modules** to implement these protocols:
   - `ai.guardrails.GuardrailManager` implements `GuardrailProtocol`
   - `ai.providers.BaseProvider` implements `LLMProviderProtocol`

3. **Update `src/services/` modules** to depend on protocols only:
   - `guardrails_service.py` imports `shared.interfaces.guardrail.GuardrailProtocol` instead of `ai.guardrails`
   - `embedding_service.py` imports `shared.interfaces.embedding.EmbeddingProtocol` instead of `ai.providers`

4. **Inject implementations at runtime** via FastAPI dependency injection or a service factory, ensuring the service layer never directly imports AI implementation modules.

## Alternatives Considered

| Alternative | Reason Rejected |
|-------------|----------------|
| Merge AI functionality into services | Would violate separation of concerns; AI is a distinct architectural layer |
| Move guardrails and embedding into services | Duplicates AI logic; guardrails are AI-specific (PII detection, toxicity) |
| Ignore entirely | Risk increases as codebase grows; extraction becomes harder with more dependents |
| Extract AI into separate microservice | Premature; violates Catalyst single-project constraint |

## Consequences

### Positive
- Clean layer boundaries maintained for the 90%+ of code that follows the rules
- Explicit remediation path prevents the violation from spreading
- ADR serves as documentation for future developers

### Negative
- Phase 2 has a refactoring task before ai/ can be extracted or significantly modified
- Two service files contain technical debt that must be tracked

### Neutral
- All current tests pass despite the violations (165 tests, 65% coverage)

## Security Impact

None. The layering violation does not affect security boundaries. Guardrails are correctly applied at the service layer regardless of import direction. The auth boundary (`middleware/auth.py` → JWT → RBAC) remains clean.

## Operational Impact

None in Phase 1. All services deploy and function normally. The remediation in Phase 2 is purely a code quality improvement.

## Reversal Strategy

To reverse this decision: merge `src/shared/interfaces/` back into `src/ai/` if AI/ML becomes a separate service in Phase 3+ (event-driven architecture), at which point the protocol interfaces would move with the AI module.
