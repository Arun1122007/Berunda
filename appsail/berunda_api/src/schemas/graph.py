from __future__ import annotations

from typing import Any

from src.schemas.base import APIBase


class GraphNodeResponse(APIBase):
    id: str
    label: str
    type: str
    properties: dict[str, Any] | None = None


class GraphEdgeResponse(APIBase):
    source: str
    target: str
    label: str
    weight: float
    properties: dict[str, Any] | None = None


class GraphResponse(APIBase):
    nodes: list[GraphNodeResponse]
    edges: list[GraphEdgeResponse]


class GraphQuery(APIBase):
    person_entity_id: int | None = None
    case_id: int | None = None
    max_depth: int = 2
    min_confidence: float = 0.5
