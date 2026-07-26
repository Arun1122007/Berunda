"""Berunda AI Module — LLM, RAG, agents, and prompt management.

This package provides the artificial intelligence capabilities for the Berunda
crime intelligence platform, including:
- **Agents**: Specialized AI agents (investigation, analyst, admin)
- **Prompts**: Versioned, modular prompt templates
- **Providers**: Abstraction layer over LLM providers
- **Orchestration**: Chain-of-thought reasoning and tool-calling
- **Tools**: Domain-specific tools for crime data
- **Guardrails**: Input/output validation and content filtering
- **Memory**: Session conversation memory
- **Retrieval**: RAG pipeline — loading, chunking, embedding, retrieval
- **Inference**: Robust LLM interaction with retry and fallback
- **Evaluation**: Metrics for correctness, faithfulness, relevance
- **Observability**: Token counting, cost tracking, latency monitoring
- **Schemas**: Pydantic models for AI subsystem contracts
"""

from src.ai.agent import Agent, AnalystAgent, InvestigatorAgent, ReviewerAgent, create_agent
from src.ai.evaluation import (
    Evaluator,
    FaithfulnessEvaluator,
    HallucinationEvaluator,
    PrecisionEvaluator,
    RelevanceEvaluator,
)
from src.ai.guardrails import GuardrailManager, InputGuardrail, OutputGuardrail
from src.ai.inference import ChainOfThought, InferenceEngine, ToolRouter
from src.ai.memory import BaseMemory, InMemoryMemory, Message, TokenWindowMemory, create_memory
from src.ai.observability import TelemetryEvent, TelemetryMiddleware, TelemetryStore, telemetry
from src.ai.orchestration import Orchestrator
from src.ai.prompts import PromptManager, get_prompt_metadata, list_prompts, load_prompt
from src.ai.providers import (
    BaseProvider,
    CatalystProvider,
    MockProvider,
    OpenAICompatibleProvider,
    ProviderRegistry,
    create_provider,
)
from src.ai.schemas import AgentConfig, AgentRequest, AgentResponse, ToolCall, ToolResult
from src.ai.tools import BaseTool, get_all_tools, get_tool, register_tool

__all__ = [
    "Agent",
    "AgentConfig",
    "AgentRequest",
    "AgentResponse",
    "AnalystAgent",
    "BaseMemory",
    "BaseProvider",
    "BaseTool",
    "CatalystProvider",
    "ChainOfThought",
    "Evaluator",
    "FaithfulnessEvaluator",
    "GuardrailManager",
    "HallucinationEvaluator",
    "InMemoryMemory",
    "InferenceEngine",
    "InputGuardrail",
    "InvestigatorAgent",
    "Message",
    "MockProvider",
    "OpenAICompatibleProvider",
    "Orchestrator",
    "OutputGuardrail",
    "PrecisionEvaluator",
    "PromptManager",
    "ProviderRegistry",
    "RelevanceEvaluator",
    "ReviewerAgent",
    "TelemetryEvent",
    "TelemetryMiddleware",
    "TelemetryStore",
    "TokenWindowMemory",
    "ToolCall",
    "ToolResult",
    "ToolRouter",
    "create_agent",
    "create_memory",
    "create_provider",
    "get_all_tools",
    "get_prompt_metadata",
    "get_tool",
    "list_prompts",
    "load_prompt",
    "register_tool",
    "telemetry",
]
