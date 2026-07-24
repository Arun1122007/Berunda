"""Agent tools — search, data lookup, analysis, and external API tool definitions for agent use."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """Abstract base class for domain tools."""

    name: str = ""
    description: str = ""

    @abstractmethod
    async def execute(self, query: str, **kwargs) -> Any:
        """Execute the tool with the given query."""
        pass


class SearchCasesTool(BaseTool):
    """Search FIR cases by criteria."""

    name = "search_cases"
    description = "Search FIR cases by keywords, date range, district, crime type"

    async def execute(self, query: str, **kwargs) -> dict:  # noqa: ARG002
        return {"results": [], "message": "SearchCasesTool not yet wired to backend"}


class GetEntityDetailsTool(BaseTool):
    """Get person/entity details."""

    name = "get_entity_details"
    description = "Get detailed profile for a person entity including linked cases"

    async def execute(self, query: str, **kwargs) -> dict:  # noqa: ARG002
        return {"entity": None, "message": "GetEntityDetailsTool not yet wired to backend"}


class GetHotspotDataTool(BaseTool):
    """Get crime hotspot statistics."""

    name = "get_hotspot_data"
    description = "Get crime hotspot density data for a district/date range"

    async def execute(self, query: str, **kwargs) -> dict:  # noqa: ARG002
        return {"hotspots": [], "message": "GetHotspotDataTool not yet wired to backend"}


class GetRiskScoreTool(BaseTool):
    """Get risk score for an entity."""

    name = "get_risk_score"
    description = "Compute or retrieve risk score for a person entity"

    async def execute(self, query: str, **kwargs) -> dict:  # noqa: ARG002
        return {"score": 0.5, "message": "GetRiskScoreTool not yet wired to backend"}


class RunLinkAnalysisTool(BaseTool):
    """Build entity relationship graph."""

    name = "run_link_analysis"
    description = "Build relationship graph showing connections between entities"

    async def execute(self, query: str, **kwargs) -> dict:  # noqa: ARG002
        return {"graph": None, "message": "RunLinkAnalysisTool not yet wired to backend"}


TOOL_REGISTRY: dict[str, BaseTool] = {
    "search_cases": SearchCasesTool(),
    "get_entity_details": GetEntityDetailsTool(),
    "get_hotspot_data": GetHotspotDataTool(),
    "get_risk_score": GetRiskScoreTool(),
    "run_link_analysis": RunLinkAnalysisTool(),
}


def get_tool(name: str) -> BaseTool | None:
    return TOOL_REGISTRY.get(name)


def get_all_tools() -> dict[str, BaseTool]:
    return TOOL_REGISTRY.copy()


def register_tool(tool: BaseTool) -> None:
    TOOL_REGISTRY[tool.name] = tool
