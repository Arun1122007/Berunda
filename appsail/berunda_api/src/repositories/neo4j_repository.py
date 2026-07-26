"""Neo4j Graph Database Repository Adapter for Phase 3 Enterprise Scale.

Provides graph node and edge management, multi-hop traversals, shortest path computation,
and fallback execution when Neo4j driver is unavailable or disconnected.
"""
import logging
from typing import Any

logger = logging.getLogger("berunda.neo4j")

try:
    from neo4j import Driver, GraphDatabase
    HAS_NEO4J = True
except ImportError:
    HAS_NEO4J = False
    Driver = Any


class Neo4jRepository:
    """Repository adapter for Neo4j Graph Database."""

    def __init__(self, uri: str = "bolt://localhost:7687", auth: tuple = ("neo4j", "password")):
        self.uri = uri
        self.auth = auth
        self.driver: Driver | None = None
        if HAS_NEO4J:
            try:
                self.driver = GraphDatabase.driver(uri, auth=auth)
                logger.info(f"Initialized Neo4j driver connected to {uri}")
            except Exception as e:
                logger.warning(f"Could not connect to Neo4j at {uri}: {e}. Running in fallback mode.")
        else:
            logger.warning("neo4j python package not installed. Neo4jRepository running in mock mode.")

    def close(self):
        """Close Neo4j driver connection."""
        if self.driver:
            self.driver.close()

    async def create_node(self, label: str, node_id: str, properties: dict[str, Any]) -> dict[str, Any]:
        """Create or update a graph node with specified label and properties."""
        if not self.driver:
            logger.info(f"[MOCK NEO4J] Created node {label}:{node_id}")
            return {"id": node_id, "label": label, **properties}

        query = f"""
        MERGE (n:{label} {{id: $node_id}})
        SET n += $props
        RETURN n
        """
        with self.driver.session() as session:
            result = session.run(query, node_id=node_id, props=properties)
            record = result.single()
            return dict(record["n"]) if record else {"id": node_id, **properties}

    async def create_relationship(
        self,
        from_label: str,
        from_id: str,
        to_label: str,
        to_id: str,
        rel_type: str,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a directed relationship between two nodes."""
        props = properties or {}
        if not self.driver:
            logger.info(f"[MOCK NEO4J] Created relationship ({from_label}:{from_id})-[{rel_type}]->({to_label}:{to_id})")
            return {"from": from_id, "to": to_id, "type": rel_type, **props}

        query = f"""
        MATCH (a:{from_label} {{id: $from_id}})
        MATCH (b:{to_label} {{id: $to_id}})
        MERGE (a)-[r:{rel_type}]->(b)
        SET r += $props
        RETURN r
        """
        with self.driver.session() as session:
            result = session.run(query, from_id=from_id, to_id=to_id, props=props)
            record = result.single()
            return dict(record["r"]) if record else {"from": from_id, "to": to_id, "type": rel_type}

    async def find_neighbors(self, node_id: str, depth: int = 2) -> list[dict[str, Any]]:
        """Find connected neighbors up to N hops away."""
        if not self.driver:
            return [
                {"source": node_id, "target": f"MOCK_NEIGHBOR_{i}", "relationship": "ASSOCIATED_WITH", "hops": 1}
                for i in range(1, 4)
            ]

        query = """
        MATCH path = (n {id: $node_id})-[r*1..%d]-(m)
        RETURN m.id AS target, [x in relationships(path) | type(x)] AS rels, length(path) AS hops
        LIMIT 50
        """ % max(1, min(depth, 5))  # noqa: UP031
        with self.driver.session() as session:
            result = session.run(query, node_id=node_id)
            return [
                {"target": rec["target"], "relationships": rec["rels"], "hops": rec["hops"]}
                for rec in result
            ]

    async def find_shortest_path(self, from_id: str, to_id: str, max_hops: int = 4) -> dict[str, Any]:
        """Find the shortest relationship path between two entities in the crime graph."""
        if not self.driver:
            return {
                "found": True,
                "path": [from_id, "FIR_CR_2026_0042", to_id],
                "relationships": ["ACCUSED_IN", "VICTIM_OF"],
                "hops": 2,
            }

        query = """
        MATCH (a {id: $from_id}), (b {id: $to_id}),
        p = shortestPath((a)-[*..%d]-(b))
        RETURN [n in nodes(p) | n.id] AS nodes, [r in relationships(p) | type(r)] AS rels, length(p) AS hops
        """ % max_hops  # noqa: UP031
        with self.driver.session() as session:
            result = session.run(query, from_id=from_id, to_id=to_id)
            record = result.single()
            if record:
                return {
                    "found": True,
                    "path": record["nodes"],
                    "relationships": record["rels"],
                    "hops": record["hops"],
                }
            return {"found": False, "path": [], "relationships": [], "hops": 0}
