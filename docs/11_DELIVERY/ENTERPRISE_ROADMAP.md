# Enterprise Roadmap

[//]: # (Document ID: BERUNDA-DEL-006 | Status: DRAFT | Classification: INTERNAL)

---

## 1. Phase Overview

| Phase | Duration | Focus | Key Deliverables |
|-------|----------|-------|-----------------|
| **Phase 1** — Hackathon MVP | 11 days (current) | Core features, governance, synthetic demo | MVP with 12 BUILDABLE features |
| **Phase 2** — Post-hackathon | 3 months | Production hardening, Kannada NLP, richer analytics | Beta with real data trial |
| **Phase 3** — Enterprise scale | 6 months | Event-driven architecture, Neo4j, CQRS, OSINT | Production deployment at state level |
| **Phase 4** — Intelligence platform | 12 months | Multi-modal AI, voice intake, blockchain, cross-state | National-scale intelligence platform |

## 2. Phase 2: Post-Hackathon (3 Months)

### 2.1 Features

| Feature | Description | Priority |
|---------|-------------|----------|
| Kannada NLP (NER + search) | Full Kannada language support using fine-tuned IndicBERT | P1 |
| MO fingerprinting | Embedding-based modus operandi pattern matching across FIRs | P1 |
| Chain-of-custody hashing | SHA-256 hash chain on gov_AuditLog for tamper evidence | P1 |
| OpenStreetMap enrichment | Reverse geocode Lat/Long → locality, nearest landmarks | P2 |
| Push notifications | Alert Investigators when new anomaly or high-risk person detected | P2 |
| CSV/PDF report export | Generate formatted reports from any dashboard view | P2 |
| Multi-language RAG | RAG corpus in Kannada + English | P2 |

### 2.2 Non-Functional

| Area | Enhancement |
|------|------------|
| Performance | Index optimization; query profiling; cache tuning |
| Testing | Expand test coverage to 90%+; load testing with 50K records |
| Security | Penetration test; vulnerability disclosure policy |
| Documentation | User manual; admin guide; API reference |

## 3. Phase 3: Enterprise Scale (6 Months)

### 3.1 Architecture Migration

| Current (Phase 1) | Target (Phase 3) |
|-------------------|-----------------|
| Synchronous function calls | Catalyst Signals event bus |
| Relational graph join tables | Dedicated Neo4j graph database |
| Rule-based entity resolution | Learned entity resolution model |
| Single Data Store instance | CQRS: read replicas + write master |
| Single AppSail instance | Scaled AppSail cluster |

### 3.2 New Features

| Feature | Description | Source |
|---------|-------------|--------|
| OSINT integration | Public records, social media, news (privacy-controlled) | 01_Blueprint §9 |
| Cross-state correlation | Correlate FIRs across Karnataka + neighboring states | 01_Blueprint §9.2 |
| Attribute-based access control (ABAC) | Fine-grained: time, location, role, clearance level | 01_Blueprint §12.1 |
| Advanced graph algorithms | PageRank, community detection (Louvain), betweenness centrality | 01_Blueprint §8.3 |
| Real-time ingestion | Kafka/event stream for live FIR data from CCTNS | 01_Blueprint §4.1 |

## 4. Phase 4: Intelligence Platform (12 Months)

| Feature | Description | Strategic Value |
|---------|-------------|----------------|
| Voice-based FIR intake | Automated transcription + NER from voice call recordings | Accessibility |
| Multi-agent AI orchestration | Specialized AI agents for different crime types | Efficiency |
| Predictive crime modeling | Spatio-temporal prediction of crime hotspots | Proactive policing |
| Blockchain evidence anchoring | Immutable evidence hash chain on distributed ledger | Legal admissibility |
| 30-year historical backfill | Import and index 30 years of Karnataka FIR data | Historical analysis |
| National integration | Connect with other states' FIR databases via NCRB | National intelligence |

## 5. Strategic Considerations

| Factor | Consideration |
|--------|---------------|
| **Data privacy** | Each phase requires updated Privacy Impact Assessment (PIA) |
| **Legal compliance** | New data sources (OSINT, cross-state) require legal clearance |
| **Infrastructure cost** | Neo4j, Kafka, blockchain incur significant operational cost |
| **Team scaling** | Phase 3 requires dedicated DevOps + Data Engineering roles |
| **Vendor lock-in** | Catalyst dependency reduces over time; Phase 3 introduces portable abstractions |
