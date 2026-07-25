"""Agent tool definitions wired to backend services."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from src.database import get_session
from src.services.entity_service import EntityService
from src.services.fir_service import FIRService
from src.services.graph_service import GraphService
from src.services.hotspot_service import HotspotService
from src.services.risk_service import RiskService


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
        district_id = kwargs.get("district_id")
        async with get_session() as session:
            service = FIRService(session)
            items, total = await service.list_firs(
                page=kwargs.get("page", 1),
                page_size=kwargs.get("page_size", 20),
                district_id=district_id,
            )
            return {
                "results": [
                    {
                        "id": c.CaseMasterID,
                        "crime_no": c.CrimeNo,
                        "date": str(c.CrimeRegisteredDate) if c.CrimeRegisteredDate else None,
                        "status_id": c.CaseStatusID,
                        "station_id": c.PoliceStationID,
                    }
                    for c in items
                ],
                "total": total,
            }


class GetEntityDetailsTool(BaseTool):
    """Get person/entity details."""

    name = "get_entity_details"
    description = "Get detailed profile for a person entity including linked cases"

    async def execute(self, query: str, **kwargs) -> dict:
        entity_id = kwargs.get("entity_id")
        if not entity_id:
            try:
                entity_id = int(query.strip())
            except (ValueError, TypeError):
                return {"entity": None, "message": "Please provide a valid entity ID"}
        async with get_session() as session:
            service = EntityService(session)
            entity = await service.get_entity(entity_id)
            if not entity:
                return {"entity": None, "message": f"Entity {entity_id} not found"}
            links = await service.get_entity_links(entity_id)
            return {
                "entity": {
                    "id": entity.PersonEntityID,
                    "name": entity.CanonicalName,
                    "gender": entity.Gender,
                    "age": entity.Age,
                    "district_id": entity.PrimaryDistrictID,
                },
                "linked_cases": [
                    {"case_id": link.CaseMasterID, "role": link.Role}
                    for link in links
                    if link.CaseMasterID
                ],
            }


class GetHotspotDataTool(BaseTool):
    """Get crime hotspot statistics."""

    name = "get_hotspot_data"
    description = "Get crime hotspot density data for a district/date range"

    async def execute(self, query: str, **kwargs) -> dict:  # noqa: ARG002
        district_id = kwargs.get("district_id")
        async with get_session() as session:
            service = HotspotService(session)
            items, total = await service.get_hotspots(
                district_id=district_id,
                page=kwargs.get("page", 1),
                page_size=kwargs.get("page_size", 50),
            )
            return {
                "hotspots": [
                    {
                        "id": h.HotspotLayerID,
                        "district": h.DistrictID,
                        "density": h.DensityScore,
                        "week_start": str(h.WeekStart) if h.WeekStart else None,
                        "week_end": str(h.WeekEnd) if h.WeekEnd else None,
                    }
                    for h in items
                ],
                "total": total,
            }


class GetRiskScoreTool(BaseTool):
    """Get risk score for an entity."""

    name = "get_risk_score"
    description = "Compute or retrieve risk score for a person entity"

    async def execute(self, query: str, **kwargs) -> dict:
        entity_id = kwargs.get("entity_id")
        if not entity_id:
            try:
                entity_id = int(query.strip())
            except (ValueError, TypeError):
                return {"score": None, "message": "Please provide a valid entity ID"}
        async with get_session() as session:
            service = RiskService(session)
            scores, _ = await service.get_scores(person_entity_id=entity_id, page=1, page_size=1)
            if scores:
                s = scores[0]
                return {"score": s.Score, "model_version": s.ModelVersion, "entity_id": entity_id}
            score_obj = await service.compute_risk_score(entity_id)
            return {
                "score": score_obj.Score,
                "model_version": score_obj.ModelVersion,
                "entity_id": entity_id,
            }


class RunLinkAnalysisTool(BaseTool):
    """Build entity relationship graph."""

    name = "run_link_analysis"
    description = "Build relationship graph showing connections between entities"

    async def execute(self, query: str, **kwargs) -> dict:
        entity_id = kwargs.get("entity_id")
        if not entity_id:
            try:
                entity_id = int(query.strip())
            except (ValueError, TypeError):
                return {"graph": None, "message": "Please provide a valid entity ID"}
        async with get_session() as session:
            service = GraphService(session)
            graph = await service.get_entity_graph(
                person_entity_id=entity_id,
                max_depth=kwargs.get("max_depth", 2),
                min_confidence=kwargs.get("min_confidence", 0.5),
            )
            return {
                "graph": {
                    "nodes": [{"id": n.id, "label": n.label, "type": n.type} for n in graph.nodes],
                    "edges": [
                        {
                            "source": e.source,
                            "target": e.target,
                            "label": e.label,
                            "weight": e.weight,
                        }
                        for e in graph.edges
                    ],
                }
            }


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
