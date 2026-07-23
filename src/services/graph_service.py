from __future__ import annotations

from sqlalchemy import or_, select

from src.models.int_models import PersonEntity, PersonEntityLink, RelationshipEdge
from src.schemas.graph import GraphEdgeResponse, GraphNodeResponse, GraphResponse
from src.services.base import BaseService


class GraphService(BaseService):
    async def get_entity_graph(
        self,
        person_entity_id: int | None = None,
        case_id: int | None = None,
        max_depth: int = 2,
        min_confidence: float = 0.5,
    ) -> GraphResponse:
        nodes: dict[int, GraphNodeResponse] = {}
        edges: list[GraphEdgeResponse] = []
        visited: set[int] = set()

        if person_entity_id is not None:
            entity = await self.session.get(PersonEntity, person_entity_id)
            if entity:
                nodes[entity.PersonEntityID] = GraphNodeResponse(
                    id=str(entity.PersonEntityID),
                    label=entity.CanonicalName,
                    type="person",
                )
                await self._traverse(
                    entity.PersonEntityID, nodes, edges, visited, 0, max_depth, min_confidence
                )

        if case_id is not None:
            links_result = await self.session.execute(
                select(PersonEntityLink).where(PersonEntityLink.CaseMasterID == case_id)
            )
            links = list(links_result.scalars().all())
            for link in links:
                entity = await self.session.get(PersonEntity, link.PersonEntityID)
                if entity:
                    nodes[entity.PersonEntityID] = GraphNodeResponse(
                        id=str(entity.PersonEntityID),
                        label=entity.CanonicalName,
                        type="person",
                    )
                    await self._traverse(
                        entity.PersonEntityID, nodes, edges, visited, 0, max_depth, min_confidence
                    )

        return GraphResponse(nodes=list(nodes.values()), edges=edges)

    async def _traverse(
        self,
        entity_id: int,
        nodes: dict,
        edges: list,
        visited: set,
        depth: int,
        max_depth: int,
        min_confidence: float,
    ) -> None:
        if depth >= max_depth or entity_id in visited:
            return
        visited.add(entity_id)

        edge_query = select(RelationshipEdge).where(
            or_(
                RelationshipEdge.PersonEntityA == entity_id,
                RelationshipEdge.PersonEntityB == entity_id,
            ),
            RelationshipEdge.Confidence >= min_confidence,
        )
        result = await self.session.execute(edge_query)
        rel_edges = list(result.scalars().all())

        for edge in rel_edges:
            neighbor_id = (
                edge.PersonEntityB if edge.PersonEntityA == entity_id else edge.PersonEntityA
            )
            neighbor = await self.session.get(PersonEntity, neighbor_id)
            if neighbor and neighbor.PersonEntityID not in nodes:
                nodes[neighbor.PersonEntityID] = GraphNodeResponse(
                    id=str(neighbor.PersonEntityID),
                    label=neighbor.CanonicalName,
                    type="person",
                )

            if not any(e.source == str(entity_id) and e.target == str(neighbor_id) for e in edges):
                edges.append(
                    GraphEdgeResponse(
                        source=str(edge.PersonEntityA),
                        target=str(edge.PersonEntityB),
                        label=edge.RelationshipType or "related",
                        weight=float(edge.Confidence or 0.5),
                    )
                )

            await self._traverse(
                neighbor_id, nodes, edges, visited, depth + 1, max_depth, min_confidence
            )
