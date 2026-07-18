"""
Berunda AI Module — LLM, RAG, agents, and prompt management.

This package provides the artificial intelligence capabilities for the Berunda
crime intelligence platform, including:

- **Agents**: Specialized AI agents (investigation, analyst, admin) that combine
  LLM reasoning with tool use for crime analysis workflows
- **Prompts**: Versioned, modular prompt templates for system prompts, task
  prompts, and evaluation prompts
- **Providers**: Abstraction layer over LLM providers (Catalyst QuickML,
  OpenAI-compatible APIs)
- **Orchestration**: Chain-of-thought reasoning, multi-step planning, and
  tool-calling orchestration
- **Tools**: Domain-specific tools for searching cases, entity details,
  hotspot data, risk scores, and link analysis
- **Guardrails**: Input/output validation, prompt injection detection, content
  filtering, and sensitive field redaction
- **Memory**: Short-term (session) and long-term (persistent) conversation memory
- **Retrieval**: Full RAG pipeline — document loading, chunking, embedding,
  indexing, retrieval, reranking
- **Inference**: Robust LLM interaction with retry, timeout, fallback, and
  streaming support
- **Evaluation**: Metrics for answer correctness, faithfulness, relevance,
  and hallucination detection
- **Observability**: Token counting, cost tracking, latency monitoring,
  and dashboard integration
- **Schemas**: Pydantic models defining input/output contracts for every
  AI subsystem

Typical usage::

    from berunda.ai import create_agent
    from berunda.ai.schemas import AgentRequest

    agent = create_agent(config)
    result = agent.run(AgentRequest(query="Analyze crime trends"))
"""

from berunda.ai.agents import Agent, AgentRegistry, create_agent
from berunda.ai.prompts import PromptManager, load_prompt, list_prompts
from berunda.ai.providers import BaseProvider, ProviderRegistry
from berunda.ai.inference import InferenceEngine
from berunda.ai.memory import MemoryManager

__all__ = [
    "Agent",
    "AgentRegistry",
    "create_agent",
    "PromptManager",
    "load_prompt",
    "list_prompts",
    "BaseProvider",
    "ProviderRegistry",
    "InferenceEngine",
    "MemoryManager",
]
