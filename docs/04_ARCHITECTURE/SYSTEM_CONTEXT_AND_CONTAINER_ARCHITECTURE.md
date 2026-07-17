# System Context and Container Architecture

[//]: # (Document ID: BERUNDA-ARCH-001 | Status: DRAFT | Classification: PUBLIC)

---

## System Context Diagram

```mermaid
flowchart LR
    subgraph External["External Actors"]
        IO[Investigating Officer]
        SHO[Station House Officer]
        SCRB[SCRB Analyst]
        GOV[Governance Officer]
        ADMIN[System Admin]
    end

    subgraph Berunda["Project Berunda System"]
        UI[Web Dashboard]
        API[API Gateway]
        CORE[Core Engine]
        AI[AI/ML Engine]
        DATA[(Data Layer)]
    end

    subgraph ExternalSystems["External Systems"]
        CCTNS[CCTNS - System of Record]
        OSM[OpenStreetMap]
    end

    IO --> UI
    SHO --> UI
    SCRB --> UI
    GOV --> UI
    ADMIN --> UI
    UI --> API
    API --> CORE
    CORE --> AI
    CORE --> DATA
    CORE -.-> CCTNS
    CORE -.-> OSM
```

## Phase 1 Container Diagram

```mermaid
flowchart TB
    subgraph Frontend["Frontend — Catalyst Slate / Web Client Hosting"]
        F1[React SPA]
        F2[MapLibre GL — Hotspot Map]
        F3[Cytoscape.js — Link Graph]
        F4[Recharts — Analytics Charts]
    end

    subgraph Gateway["Catalyst API Gateway"]
        GW[Auth + Routing + Rate Limiting]
    end

    subgraph Compute["Catalyst Functions"]
        FN1[FIR Ingestion Function]
        FN2[NER Entity Extraction Function]
        FN3[Entity Resolution Function]
        FN4[Link Analysis Function]
        FN5[Anomaly Detection Function]
        FN6[Fairness Check Function]
    end

    subgraph AppSail["Catalyst AppSail (Python)"]
        AS1[NetworkX Graph Engine]
        AS2[scikit-learn Inference]
    end

    subgraph AI["Catalyst QuickML"]
        QML1[LLM Serving — RAG]
        QML2[AutoML — Risk Scoring]
    end

    subgraph Storage["Catalyst Storage"]
        DS[(Data Store — Relational)]
        NS[(NoSQL — Unstructured)]
        STR[Stratus — File Storage]
        CACHE[Cache — Hot Data]
    end

    subgraph Automation["Catalyst Automation"]
        CRON[Cron — Nightly Recompute]
    end

    F1 --> GW
    F2 --> GW
    F3 --> GW
    F4 --> GW
    GW --> FN1
    GW --> FN2
    GW --> FN3
    GW --> FN4
    GW --> FN5
    GW --> FN6
    FN1 --> DS
    FN2 --> DS
    FN3 --> DS
    FN4 --> AS1 --> DS
    FN2 --> QML1
    FN1 --> NS
    FN5 --> DS
    FN6 --> DS
    QML2 --> DS
    AS2 --> DS
    CRON --> FN5
    DS --> CACHE
```

## Target State Container Diagram (Phase 3+)

```mermaid
flowchart TB
    subgraph Frontend["Frontend — Catalyst Slate"]
        SPA[React SPA]
    end

    subgraph API["Catalyst API Gateway + CDN"]
        GW[API Gateway]
    end

    subgraph EventMesh["Event-Driven Mesh"]
        SIGNALS[Catalyst Signals — Event Bus]
        CIRCUITS[Catalyst Circuits — Workflow]
    end

    subgraph Services["Microservices (AppSail + Functions)"]
        SVC1[Ingestion Service]
        SVC2[NER Service]
        SVC3[Entity Resolution Service]
        SVC4[Graph Service]
        SVC5[Analytics Service]
        SVC6[RAG Service]
        SVC7[Governance Service]
        SVC8[OSINT Service]
    end

    subgraph AI["AI Layer"]
        QML[QuickML — LLM, RAG, AutoML]
        ZIA[Zia Services — OCR, Vision]
    end

    subgraph Data["Data Layer"]
        DS[(Data Store)]
        NOSQL[(NoSQL)]
        GDB[(Neo4j Graph DB)]
        STRAT[Stratus]
        CACHE[Cache]
    end

    subgraph Observability["Observability"]
        LOG[Structured Logging]
        TRACE[Distributed Tracing]
        METRICS[Metrics Dashboard]
    end

    SPA --> GW --> EventMesh
    EventMesh --> SVC1
    EventMesh --> SVC2
    EventMesh --> SVC3
    EventMesh --> SVC4
    EventMesh --> SVC5
    EventMesh --> SVC6
    EventMesh --> SVC7
    EventMesh --> SVC8
    SVC2 --> QML
    SVC1 --> DS
    SVC3 --> DS
    SVC4 --> GDB
    SVC5 --> DS
    SVC8 --> ZIA
    SVC6 --> QML
    DS --> CACHE
    SVC7 --> DS
    EventMesh --> LOG
    EventMesh --> TRACE
    EventMesh --> METRICS
```
