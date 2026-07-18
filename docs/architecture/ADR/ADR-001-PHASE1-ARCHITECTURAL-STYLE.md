# ADR-001: Phase 1 Architectural Style

[//]: # (Document ID: ADR-001 | Version: 1.0 | Status: APPROVED | Classification: INTERNAL | Owner: Berunda Team | Audience: Architects, Team Lead | Source: 01_Enterprise_Blueprint + ERD PDF + ADR decisions | Last Verified: 2026-07-17 | Review: Monthly)

---

## Context

The source documents use inconsistent architectural language. `Project_Berunda_01_Enterprise_Blueprint.md` calls for "modular microservices" while `CaseGraph_Datathon2026_Blueprint.md` states that Kubernetes microservices might violate the Catalyst mandate. The team has 11 days and 2 people.

## Decision

Phase 1 uses a **modular Functions + API Gateway** architecture.

- Business logic is deployed as Catalyst Functions (stateless, auto-scaling)
- Catalyst AppSail provides persistent Python runtime for NetworkX graph algorithms
- All requests route through Catalyst API Gateway for auth, throttling, and routing
- Communication between functions is synchronous REST (HTTP POST/call)
- No event bus (Catalyst Signals), no workflow engine (Catalyst Circuits), no Kubernetes

## Rationale

- Catalyst deployment is mandatory; Functions/AppSail/API Gateway are Catalyst-native
- A full microservices or event-driven architecture adds operational complexity that a 2-person, 11-day team cannot absorb
- The synchronous REST pattern is sufficient at demo dataset scale (2000-5000 records)
- Event-driven architecture is documented as the Phase 3+ target, not attempted now
- The term "microservices" in the source documents is interpreted as "modular code with clear boundaries" not "independently deployable services in containers"

## Consequences

- Positive: Faster development, simpler debugging, lower operational overhead
- Positive: Full Catalyst compliance
- Negative: Must refactor to event-driven pattern at Phase 3+ for scale
- Negative: Synchronous calls create temporal coupling between components

## Status

APPROVED
