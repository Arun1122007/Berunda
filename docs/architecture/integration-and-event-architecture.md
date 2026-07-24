# Integration and Event Architecture

[//]: # (Document ID: BERUNDA-INT-001 | Version: 1.1 | Status: APPROVED | Classification: INTERNAL | Owner: Berunda Team | Audience: Developers, Architects | Source: 01_Enterprise_Blueprint + ERD PDF + ADR decisions | Last Verified: 2026-07-24 | Review: Monthly)

---

## Phase 1 Integration Pattern

Phase 1 uses **direct REST calls** between components. Each Catalyst Function exposes an HTTP endpoint through the API Gateway. Subsequent processing is triggered by the caller, not by an event bus.

```mermaid
flowchart LR
    A[Ingestion Function] -- HTTP POST --> B[NER Function]
    B -- HTTP POST --> C[Entity Resolution Function]
    C -- HTTP POST --> D[Data Store]
    C -- HTTP POST --> E[AuditLog]
```

**Why not event-driven in Phase 1:**
- Reduces complexity for a 2-person team
- Eliminates the need for async error handling and retry queues
- Synchronous flow is acceptable at demo dataset scale
- Event-driven approach is documented for Phase 3+ migration

## Phase 1 Data Flows

### FIR Ingestion Flow

```mermaid
flowchart LR
    A[Upload CSV/Excel] --> B[Validate Schema]
    B --> C[Parse CrimeNo]
    C --> D[Insert CaseMaster]
    D --> E[Insert Accused/Victim/Complainant]
    E --> F[Trigger NER on BriefFacts]
    F --> G[Extract Entities]
    G --> H[Write PersonEntityLink]
    H --> I[Trigger Entity Resolution]
    I --> J[Log to AuditLog]
    J --> K[Return Success]
```

### Hotspot/Anomaly Pipeline Flow

```mermaid
flowchart LR
    A[Cron trigger - nightly] --> B[Query incident counts]
    B --> C[Compute hexbin aggregation]
    C --> D[Compute z-score deviation]
    D --> E[Write hotspot layers]
    E --> F[Write anomaly alerts]
    F --> G[Update Cache]
    G --> H[Send Mail alerts if anomalies found]
```

## Target State Event Architecture (Phase 3+)

```mermaid
flowchart LR
    subgraph Events["Catalyst Signals Event Bus"]
        E1[FIR.Ingested]
        E2[NER.Completed]
        E3[EntityResolved]
        E4[Score.Computed]
        E5[Anomaly.Detected]
    end

    subgraph Consumers["Event Consumers"]
        C1[Ingestion Service]
        C2[NER Service]
        C3[Entity Resolution Service]
        C4[Risk Scoring Service]
        C5[Alert Service]
        C6[Audit Service]
        C7[Notification Service]
    end

    C1 -- emits --> E1
    E1 --> C2
    C2 -- emits --> E2
    E2 --> C3
    C3 -- emits --> E3
    E3 --> C4
    C4 -- emits --> E4
    E4 --> C6
    C5 -- emits --> E5
    E5 --> C7
```

### Migration Path from Phase 1 to Phase 3+

| Step | Change | Risk |
|------|--------|------|
| 1 | Replace direct Function-to-Function HTTP calls with Queue/Message | Service coupling reduced |
| 2 | Add Catalyst Signals event definitions for each major action | Event schema design required |
| 3 | Convert consumers to async event handlers | Error handling complexity increases |
| 4 | Add Catalyst Circuits for multi-step workflows | Orchestration logic added |
| 5 | Implement CQRS (separate read/write paths for analytics) | Data consistency challenges |
| 6 | Add distributed tracing | Observability infrastructure required |
