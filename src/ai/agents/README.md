# Agent System (`src/ai/agents/`)

> **Module:** AI Agents
> **Classification:** INTERNAL

---

## Overview

Agents are the primary entry point for AI-driven crime intelligence tasks. Each
agent combines an LLM with a set of domain-specific tools to accomplish a
particular class of tasks.

---

## Architecture

```
Agent (abstract base)
├── InvestigationAgent  — Case analysis, entity linking, timeline reconstruction
├── AnalystAgent        — Trend analysis, pattern recognition, report generation
└── AdminAgent           — System config, user management, audit queries
```

All agents subclass the `Agent` base class and register themselves via
`AgentRegistry.register()`.

---

## Defining an Agent

```python
from berunda.ai.agents import Agent
from berunda.ai.tools import ToolRegistry


class CustomAgent(Agent):
    name = "custom"
    description = "Handles custom crime analysis tasks"

    def __init__(self, config: dict | None = None):
        super().__init__(config)
        self.tools = ToolRegistry.get_tools(["search_cases", "get_risk_score"])

    async def run(self, request) -> AgentResponse:
        # Custom logic here
        ...
```

Register the agent at module import time:

```python
from berunda.ai.agents.registry import AgentRegistry

AgentRegistry.register(CustomAgent)
```

---

## Agent Types

### InvestigationAgent
- **Purpose**: Deep-dive into individual cases or entities
- **Tools**: `search_cases`, `get_entity_details`, `run_link_analysis`
- **Persona**: Methodical detective — asks clarifying questions, builds
  evidence chains, produces timeline visualizations

### AnalystAgent
- **Purpose**: Identify patterns across multiple cases
- **Tools**: `search_cases`, `get_hotspot_data`, `get_risk_score`
- **Persona**: Data-driven analyst — uses statistics, generates trend reports,
  produces hotspot maps and charts

### AdminAgent
- **Purpose**: System administration and configuration
- **Tools**: Restricted set of system tools
- **Persona**: System operator — manages users, roles, audit logs,
  configuration settings

---

## Invocation

```python
from berunda.ai.agents import create_agent
from berunda.ai.schemas import AgentRequest, AgentResponse

agent = create_agent("investigation", config={"verbose": True})
request = AgentRequest(query="Find connections between FIR #142 and #189")
response: AgentResponse = await agent.run(request)

print(response.answer)
for tool_call in response.tool_calls:
    print(f"Used tool: {tool_call.name} → {tool_call.result}")
```

Agents can also be invoked in streaming mode for progressive output:

```python
async for chunk in agent.run_stream(request):
    print(chunk.delta, end="", flush=True)
```
