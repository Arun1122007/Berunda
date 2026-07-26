# Database Architecture and Design

## Overview
Project Berunda originally targeted a custom PostgreSQL database with SQLAlchemy, but has pivoted to a **Zoho Catalyst Data Store** architecture to comply with the Hack2Skill platform constraints (ADR-012). 
The architecture relies on Catalyst Data Store for structured relational data, Catalyst Auth for user management, and Catalyst functions for query execution (ZCQL).

## Catalyst Data Store Tables

### 1. Source Data (Core FIR entities)
Contains ground-truth tables mirroring KSP FIR records:
- `CaseMaster`: The central FIR record.
- `PersonEntity`: Extracted persons (Accused/Victim/Complainant).
- `VehicleLink`: Extracted vehicles.
- `ComplainantDetails`, `VictimDetails`, `AccusedDetails`: Specific role details.

### 2. Intelligence & AI
Supports AI workflows, embeddings, and analytics:
- `PersonEntityLink`: Links raw extracted persons to resolved `PersonEntity` identities with confidence scores.
- `RelationshipEdge`: Graph relationships (co-accused, etc.).
- `RiskScore`: AI model outputs per PersonEntity.
- `AnomalyAlert`: Detected statistical anomalies.

### 3. Governance
Audit trails and fairness logs:
- `AuditLog`: Captures sensitive actions (viewing AI outputs, accessing demographic data).
- `FairnessCheckResult`: Logs AI guardrail failures (e.g., demographic bias detections).

### 4. Authentication (Catalyst Auth)
User authentication is managed directly by **Catalyst Authentication**, bypassing the need for a custom `auth_User` or `auth_Session` table. User IDs from Catalyst Auth are referenced in the Data Store for audit logging.

## Key Constraints & Enhancements
- **ZCQL**: Queries are executed via Zoho Catalyst Query Language (ZCQL) within Node.js AppSail/Basic functions.
- **Transactions**: No traditional long-running DB transactions. Data consistency is managed at the application layer through idempotency.
- **Security**: Sensitive fields (CasteID/ReligionID) are strictly isolated and not used in any analytical pipelines.
