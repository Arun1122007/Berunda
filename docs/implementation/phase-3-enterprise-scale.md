# Phase 3 — Enterprise Scale Implementation Plan

> **Document ID:** BERUNDA-IMPL-003 | **Version:** 1.0 | **Status:** PROPOSED
> **Classification:** INTERNAL | **Owner:** Berunda Team
> **Last Updated:** 2026-07-26

---

## 1. Executive Summary

Phase 3 transitions Project Berunda from a verified post-hackathon beta (Phase 2 Vertical Slice) into a scalable, high-concurrency **Enterprise Crime Intelligence Platform** deployed across Karnataka. The focus shifts from basic CRUD operations and rule-based algorithms to **Event-Driven Architecture (EDA)**, **Graph Database Migration (Neo4j)**, **Learned Entity Resolution**, **Modus Operandi (MO) Pattern Matching**, and fine-grained **Attribute-Based Access Control (ABAC)**.

---

## 2. Key Objectives & Scope

### 2.1 Architecture & Infrastructure Migration
- **Event-Driven Event Bus**: Replace synchronous function-to-function HTTP calls with **Catalyst Signals / Event Bus** (or Kafka/RabbitMQ in self-hosted deployments) for asynchronous, decoupled ingestion pipelines.
- **Dedicated Graph Database**: Migrate relational graph join tables (`RelationshipMaster`, `PersonEntity` graph edges) to **Neo4j** to support real-time deep traversal queries (3+ hops), shortest path computation, and graph centrality algorithms.
- **CQRS & Read Replicas**: Separate transactional write operations (FIR entry, user management) from analytical read queries (hotspot aggregations, link graph lookups) using Command Query Responsibility Segregation (CQRS).
- **Cluster Scaling**: Upgrade single AppSail container deployments to an auto-scaling AppSail cluster.

### 2.2 Advanced Intelligence & AI Features
- **Learned Entity Resolution Model**: Upgrade from rule-based phonetic matching (Soundex/Levenshtein) to a learned embedding-based entity resolution pipeline using IndicBERT for Kannada and English name deduplication.
- **MO Fingerprinting & Similarity Search**: Generate vector embeddings for FIR `briefFacts` and modus operandi details, storing them in vector index (Pgvector / Neo4j vector search) to automatically discover linked crimes across police districts.
- **Advanced Graph Analytics**: Implement Graph algorithms for gang detection (Louvain Community Detection), key facilitator identification (Betweenness Centrality), and influence scoring (PageRank).
- **OSINT & Cross-State Correlation**: Ingest public news, court status portals, and neighboring state crime bulletins with privacy-preserving entity linkage.

### 2.3 Security, Governance & Audit
- **Attribute-Based Access Control (ABAC)**: Extend RBAC with dynamic policy evaluations based on investigator clearance level, location boundary, time of access, and case sensitivity flags.
- **Cryptographic Hash Chain**: Implement SHA-256 hash chaining on all `gov_AuditLog` entries to guarantee tamper-evidence and legal admissibility in court.

### 2.4 Frontend Architecture Upgrades
- **Code-Splitting & Manual Chunking**: Configure Vite/Rollup `manualChunks` to isolate heavy visualization engines (MapLibre-GL, Cytoscape.js, Recharts) into deferred lazy chunks (< 500 kB uncompressed).
- **Real-Time WebSocket Subscription**: Implement `/ws/events` client hook (`useEventStream`) to push live alert notifications, ingestion progress, and high-risk suspect detections directly to the UI without polling.
- **Inline Nested Entity CRUD**: Extend `CreateCasePage` and `EditCasePage` with dynamic sub-forms to create and link Complainant, Victim, Accused, and Vehicle records simultaneously during FIR registration.

---

## 3. Workstreams & Deliverables

```
Phase 3 Enterprise Scale
├── Workstream 1: Data & Graph Architecture
│   ├── Neo4j schema & migration script (`scripts/migration/neo4j_migrate.py`)
│   ├── GraphRepository adapter (`src/infrastructure/neo4j_repo.py`)
│   └── CQRS read-replica routing middleware
├── Workstream 2: Event Bus & Real-Time Ingestion
│   ├── Catalyst Signals / Event Bus publisher & consumer (`src/infrastructure/events/`)
│   ├── CCTNS live stream ingestion worker
│   └── WebSocket event broadcaster (`/ws/events`)
├── Workstream 3: Advanced AI & Analytics
│   ├── IndicBERT embedding pipeline (`src/ai/embeddings/`)
│   ├── Learned Entity Resolution service (`src/application/entity_resolution_service.py`)
│   └── MO Similarity Search endpoint (`POST /api/v1/analytics/mo-match`)
├── Workstream 4: Security Hardening & ABAC
│   ├── ABAC policy evaluation engine (`src/domain/security/abac_policy.py`)
│   └── SHA-256 tamper-evident audit logger (`src/infrastructure/audit_chain.py`)
└── Workstream 5: Frontend Enterprise Polish
    ├── Rollup manual chunking optimization in `vite.config.ts`
    ├── `useWebSocket` hook & live notification toast banner
    └── Nested entity dynamic forms in `CreateCasePage.tsx`
```

---

## 4. Technical Specifications & API Contracts

### 4.1 New & Upgraded REST Endpoints
| Method | Path | Auth / ABAC | Description |
|--------|------|-------------|-------------|
| **POST** | `/api/v1/analytics/mo-match` | Required (Analyst/Admin) | Query similar FIRs by brief facts embedding similarity |
| **GET** | `/api/v1/graph/communities` | Required (Analyst/Admin) | Execute Louvain community detection to identify gang clusters |
| **GET** | `/api/v1/graph/centrality` | Required (Analyst/Admin) | Calculate betweenness centrality for suspect network ranking |
| **POST** | `/api/v1/entities/resolve-batch` | Required (Admin) | Trigger asynchronous ML-based entity resolution pipeline |
| **GET** | `/api/v1/audit/verify-chain` | Required (Admin/Auditor)| Validate SHA-256 cryptographic hash chain integrity |
| **WS** | `/ws/events` | JWT Bearer | WebSocket channel for real-time system alerts and pipeline updates |

### 4.2 ABAC Policy Schema (`abac_rules.json`)
```json
{
  "effect": "ALLOW",
  "actions": ["read:fir", "export:report"],
  "conditions": {
    "user.clearanceLevel": { "$gte": "resource.sensitivityLevel" },
    "user.assignedDistrict": { "$in": ["resource.districtId", "STATE_HQ"] },
    "env.timeOfDay": { "$between": ["06:00", "22:00"] }
  }
}
```

---

## 5. Verification & Quality Gates

1. **Graph Traversal Benchmark**: Verify 3-hop graph queries in Neo4j execute in `< 50 ms` for 100,000+ nodes.
2. **Entity Resolution F1-Score**: Achieve an F1-score of `> 0.92` on Kannada/English synthetic duplicate benchmarks.
3. **Audit Chain Integrity Test**: Verify that modifying any historic row in `gov_AuditLog` immediately fails `verify-chain` validation.
4. **Bundle Size Limit**: Verify all compiled frontend JS chunks remain `< 500 kB` after Vite minification.
5. **Full Automated Suite**: 100% pass rate on unit, integration, and end-to-end security regression tests.
