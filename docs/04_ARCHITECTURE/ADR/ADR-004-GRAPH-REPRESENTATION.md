# ADR-004: Graph Representation

[//]: # (Document ID: ADR-004 | Status: APPROVED | Classification: INTERNAL)

---

## Context

The platform needs to represent and query relationships between persons, cases, vehicles, and locations. Options include: relational join tables, a dedicated graph database (Neo4j), or in-application graph computation.

## Decision

**Phase 1:** Relational join tables (RelationshipEdge, VehicleLink) queried and traversed in-application using NetworkX inside Catalyst AppSail.

**Target State (Phase 3+):** Dedicated graph database (Neo4j) for production scale.

## Rationale

- Catalyst has no native graph database service. Standing up Neo4j externally would violate the Catalyst-mandatory rule
- Relational join tables are sufficient to demo relationship discovery at hackathon dataset scale (2000-5000 records)
- NetworkX running in AppSail provides degree centrality, shortest path, and connected components — all the Phase 1 requirements
- A dedicated graph database earns its complexity only at 100K+ record volume with multi-hop queries at scale
- The join-table approach provides a clean migration path: the same entity/edge model maps directly to Neo4j nodes and relationships

## Consequences

- Positive: Full Catalyst compliance (no external Neo4j)
- Positive: Sufficient for demo-scale graph queries
- Positive: Same data model maps directly to Neo4j for Phase 3+
- Negative: Graph queries become slower at large scale (10M+ records)
- Negative: Community detection (Louvain) works but is less performant on relational joins vs native graph DB

## Status

APPROVED
