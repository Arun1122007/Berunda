from __future__ import annotations

from typing import Any

from src.ai.evaluation import Evaluator
from src.ai.guardrails import GuardrailManager
from src.ai.memory import BaseMemory, create_memory
from src.ai.observability import TelemetryMiddleware
from src.ai.orchestration import Orchestrator
from src.ai.providers import BaseProvider, create_provider
from src.ai.schemas import AgentConfig
from src.ai.tools import get_all_tools


class Agent:
    """Base agent that combines all AI components."""

    def __init__(
        self,
        config: AgentConfig,
        provider: BaseProvider | None = None,
        memory: BaseMemory | None = None,
    ):
        self.config = config
        self.provider = provider or create_provider("mock", model="default")
        self.memory = memory or create_memory(config.memory_type, **config.memory_kwargs)
        self.guardrails = GuardrailManager()
        self.tools = get_all_tools()
        self.telemetry = TelemetryMiddleware()
        self.orchestrator = Orchestrator(
            provider=self.provider,
            memory=self.memory,
            guardrails=self.guardrails,
            tools=self.tools,
            max_tool_rounds=config.max_tool_rounds,
        )
        self.evaluator = Evaluator()

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Run the agent on user input."""
        result = await self.orchestrator.process(
            user_input=user_input,
            system_prompt=self.config.system_prompt,
            enable_guardrails=self.config.enable_guardrails,
        )

        # Evaluate response quality
        evaluation = {}
        if not result.get("blocked"):
            evaluation = self.evaluator.evaluate_all(
                question=user_input,
                answer=result.get("content", ""),
                context=str(context or ""),
            )

        return {
            **result,
            "evaluation": {
                k: {"score": v.score, "passed": v.passed} for k, v in evaluation.items()
            },
            "overall_quality": self.evaluator.overall_score(evaluation) if evaluation else 0.0,
        }


class InvestigatorAgent(Agent):
    """Agent specialized for case investigation."""

    def __init__(self, **kwargs):
        prompt = (
            "You are a police investigation AI assistant for Karnataka Police. "
            "Your role is to help investigate crime cases by searching records, "
            "analyzing patterns, and generating insights. "
            "Always be precise, factual, and cite case numbers when making claims. "
            "Do not speculate beyond available data."
        )
        config = AgentConfig(
            system_prompt=prompt,
            max_tool_rounds=5,
            enable_guardrails=True,
        )
        super().__init__(config, **kwargs)


class AnalystAgent(Agent):
    """Agent specialized for pattern analysis."""

    def __init__(self, **kwargs):
        config = AgentConfig(
            system_prompt="""You are a crime pattern analysis AI assistant for Karnataka Police.
Your role is to identify trends, hotspots, and anomalies in crime data.
Support all claims with data and statistical evidence.
Flag potential biases or data quality issues.""",
            max_tool_rounds=3,
            enable_guardrails=True,
        )
        super().__init__(config, **kwargs)


class ReviewerAgent(Agent):
    """Agent specialized for case review and quality assurance."""

    def __init__(self, **kwargs):
        prompt = (
            "You are a case review AI assistant for Karnataka Police. "
            "Your role is to review investigation completeness, "
            "flag missing information, and ensure procedural compliance. "
            "Be thorough and constructive in your feedback."
        )
        config = AgentConfig(
            system_prompt=prompt,
            max_tool_rounds=3,
        )
        super().__init__(config, **kwargs)


# Agent registry
AGENTS = {
    "investigator": InvestigatorAgent,
    "analyst": AnalystAgent,
    "reviewer": ReviewerAgent,
}


def create_agent(agent_type: str = "investigator", **kwargs) -> Agent:
    if agent_type not in AGENTS:
        raise ValueError(f"Unknown agent type: {agent_type}")
    return AGENTS[agent_type](**kwargs)
