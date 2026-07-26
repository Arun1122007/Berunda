from __future__ import annotations

from typing import Any

from src.config import settings
from src.shared.logging import get_logger

logger = get_logger(__name__)


class Neo4jService:
    """Neo4j graph database integration scaffold.

    Berunda's primary graph operations run on NetworkX over PostgreSQL
    (see graph_service.py). This service provides an optional Neo4j backend
    for large-scale link analysis, community detection, and graph queries
    that benefit from a native graph store.

    To enable:
      1. pip install neo4j
      2. Set NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD env vars
      3. Spin up Neo4j via docker-compose.neo4j.yml
      4. Call Neo4jService.get_instance() from graph_service.py
    """

    _instance: Neo4jService | None = None

    def __init__(self) -> None:
        self._driver: Any = None
        self._enabled = False

    @classmethod
    def get_instance(cls) -> Neo4jService:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def connect(self) -> bool:
        uri = settings.NEO4J_URI or None
        user = settings.NEO4J_USER
        password = settings.NEO4J_PASSWORD or None
        if not uri or not password:
            logger.info("Neo4j not configured — falling back to NetworkX/PostgreSQL")
            return False
        try:
            from neo4j import AsyncGraphDatabase

            self._driver = AsyncGraphDatabase.driver(uri, auth=(user, password))
            await self._driver.verify_connectivity()
            self._enabled = True
            logger.info("Connected to Neo4j at %s", uri)
            return True
        except Exception as exc:
            logger.warning("Neo4j connection failed — using NetworkX fallback", exc_info=exc)
            return False

    async def close(self) -> None:
        if self._driver:
            await self._driver.close()
            self._enabled = False

    @property
    def enabled(self) -> bool:
        return self._enabled

    async def upsert_person_node(
        self,
        person_entity_id: int,
        canonical_name: str,
        **props: Any,
    ) -> None:
        if not self._enabled:
            return
        async with self._driver.session() as session:
            await session.run(
                (
                    "MERGE (p:Person {personEntityId: $id}) "
                    "SET p.name = $name, p.updatedAt = timestamp()"
                ),
                id=person_entity_id,
                name=canonical_name,
            )

    async def upsert_relationship(
        self,
        person_a_id: int,
        person_b_id: int,
        relationship_type: str,
        confidence: float,
    ) -> None:
        if not self._enabled:
            return
        async with self._driver.session() as session:
            await session.run(
                (
                    "MATCH (a:Person {personEntityId: $aId}) "
                    "MATCH (b:Person {personEntityId: $bId}) "
                    "MERGE (a)-[r:RELATED {type: $relType}]->(b) "
                    "SET r.confidence = $confidence, r.updatedAt = timestamp()"
                ),
                aId=person_a_id,
                bId=person_b_id,
                relType=relationship_type,
                confidence=confidence,
            )

    async def get_connected_component(
        self,
        person_entity_id: int,
        max_depth: int = 3,
    ) -> list[dict[str, Any]]:
        if not self._enabled:
            return []
        async with self._driver.session() as session:
            result = await session.run(
                (
                    "MATCH path = (p:Person {personEntityId: $id})-"
                    "[:RELATED*1..$maxDepth]-(connected) "
                    "RETURN connected.personEntityId AS id, "
                    "connected.name AS name, "
                    "length(path) AS depth"
                ),
                id=person_entity_id,
                maxDepth=max_depth,
            )
            return [dict(record) async for record in result]

    async def detect_communities(self) -> list[list[int]]:
        if not self._enabled:
            return []
        async with self._driver.session() as session:
            result = await session.run(
                "CALL gds.louvain.stream('person-graph') "
                "YIELD nodeId, communityId "
                "RETURN communityId, collect(gds.util.asNode(nodeId).personEntityId) AS members"
            )
            communities = []
            async for record in result:
                communities.append(list(record["members"]))
            return communities
