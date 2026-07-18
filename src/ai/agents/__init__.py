"""
Agent definitions — Base Agent class and registered agents.

Provides the abstract base class for all AI agents and a registry for
discovering and instantiating agent implementations.

Exports:
    Agent: Abstract base class that all agents must subclass.
    AgentRegistry: Singleton registry mapping agent names to classes.
    create_agent: Factory function to instantiate an agent by name.
    InvestigationAgent: Deep-dive case analysis agent.
    AnalystAgent: Trend and pattern analysis agent.
    AdminAgent: System configuration and administration agent.
"""

from berunda.ai.agents.base import Agent
from berunda.ai.agents.registry import AgentRegistry
from berunda.ai.agents.investigation import InvestigationAgent
from berunda.ai.agents.analyst import AnalystAgent
from berunda.ai.agents.admin import AdminAgent


def create_agent(name: str, config: dict | None = None) -> Agent:
    """Factory: instantiate an agent by its registered name.

    Args:
        name: Registered agent name (e.g. 'investigation', 'analyst', 'admin').
        config: Optional configuration overrides.

    Returns:
        An initialized Agent instance.

    Raises:
        KeyError: If no agent is registered under *name*.
    """
    return AgentRegistry.create(name, config)


__all__ = [
    "Agent",
    "AgentRegistry",
    "create_agent",
    "InvestigationAgent",
    "AnalystAgent",
    "AdminAgent",
]
