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

try:
    from ai.agents.admin import AdminAgent
    from ai.agents.analyst import AnalystAgent
    from ai.agents.base import Agent
    from ai.agents.investigation import InvestigationAgent
    from ai.agents.registry import AgentRegistry
except ImportError:
    # Stub: implementation files not yet created
    Agent = None  # type: ignore
    AgentRegistry = None  # type: ignore
    InvestigationAgent = None  # type: ignore
    AnalystAgent = None  # type: ignore
    AdminAgent = None  # type: ignore


def create_agent(name: str, config: dict | None = None) -> Agent:  # type: ignore
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
