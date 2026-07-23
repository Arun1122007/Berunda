# Berunda — Source Code (`src/`)

> **Module:** Source Code Root
> **Classification:** INTERNAL
> **Last Updated:** 2026-07-18

---

## Overview

The `src/` directory contains the core implementation of the Berunda crime intelligence platform. It is organized into four top-level modules:

| Module | Path | Purpose |
|--------|------|---------|
| **AI** | `src/ai/` | Large Language Model (LLM) integration, RAG pipeline, agent orchestration, prompt management, guardrails, memory, and evaluation |
| **ML** | `src/ml/` | Machine learning models — risk scoring, feature engineering, training (Catalyst AutoML), inference, model registry, and monitoring |
| **Pipelines** | `src/pipelines/` | End-to-end data pipelines: ingestion from FIR Excel/CSV, preprocessing, training workflows, evaluation, and inference |
| **Shared** | `src/shared/` | Cross-cutting utilities: configuration, logging, validation, common helpers used by AI, ML, and Pipelines |

---

## Architecture Principles

1. **Separation of concerns** — Each module owns a single responsibility. AI handles language understanding; ML handles numerical prediction; Pipelines orchestrate data flow; Shared provides reusable infrastructure.
2. **Pluggable design** — AI providers, ML models, document loaders, chunking strategies, vector stores, and tools are all registered via abstract base classes and registries. New implementations can be added without modifying existing code.
3. **Observability built-in** — Every module logs structured JSON with correlation IDs. AI calls track token usage and latency. ML models track prediction drift. Pipelines emit audit events.
4. **Defense in depth** — Guardrails filter inputs and outputs at every stage. Data validation occurs at pipeline boundaries. Secrets never leak to logs or git.

---

## Module Dependencies

```
src/pipelines  ──>  src/shared
src/pipelines  ──>  src/ai
src/pipelines  ──>  src/ml
src/ai         ──>  src/shared
src/ml         ──>  src/shared
```

No circular dependencies are permitted. `src/shared` must never import from `ai`, `ml`, or `pipelines`.

---

## Quick Start

```python
from ai import create_agent
from shared.config import load_config
from shared.logging import get_logger

config = load_config()
logger = get_logger(__name__)
agent = create_agent(config)
response = agent.run("Analyze FIR patterns in Bengaluru North division")
```

Refer to each submodule's `README.md` for detailed documentation.
