# @berunda/api — Catalyst Functions Backend

Ten Zoho Catalyst Functions implementing the Berunda Crime Intelligence Platform backend.

## Architecture

```
                     ┌──────────────────────┐
                     │   Catalyst Router     │
                     │   (HTTP Gateway)      │
                     └──────┬─────┬──────────┘
                            │     │
              ┌─────────────┘     └─────────────┐
              ▼                                   ▼
   ┌────────────────────┐           ┌────────────────────┐
   │  fir-ingestion     │           │  ner-extraction     │
   │  POST /import      │           │  POST /extract      │
   │  POST /validate    │           └─────────┬──────────┘
   └─────────┬──────────┘                     │
             │                                ▼
             ▼                    ┌────────────────────┐
   ┌────────────────────┐         │  entity-resolution │
   │  Case Store        │◀────────│  POST /resolve     │
   │  (Catalyst DS)     │         └────────────────────┘
   └────────────────────┘
             │
    ┌────────┼────────┬───────────┬──────────┬──────────┐
    ▼        ▼        ▼           ▼          ▼          ▼
 ┌──────┐ ┌──────┐ ┌──────┐ ┌─────────┐ ┌────────┐ ┌──────┐
 │Risk  │ │Hot-  │ │Anom- │ │Link     │ │RAG     │ │Audit │
 │Scor- │ │spot  │ │aly   │ │Analysis │ │Query   │ │Log-  │
 │ing   │ │      │ │Detec-│ │         │ │        │ │ging  │
 └──────┘ └──────┘ └──────┘ └─────────┘ └────────┘ └──────┘
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Runtime | Zoho Catalyst (Node.js) |
| Language | TypeScript / JavaScript |
| SDK | catalyst-sdk-node |
| Auth | Catalyst Auth / JWT |
| Data Store | Catalyst Data Store / Zoho CRM |

## Available Functions

| Function | Trigger | Purpose |
|----------|---------|---------|
| fir-ingestion | HTTP | Import and validate FIR data |
| ner-extraction | HTTP/Event | Extract entities from FIR narratives |
| entity-resolution | HTTP/Event | Resolve persons across cases |
| risk-scoring | HTTP/Cron | Compute repeat-offender risk scores |
| hotspot-analysis | HTTP/Cron | KDE/hexbin hotspot computation |
| anomaly-detection | HTTP/Cron | Spike detection against baselines |
| link-analysis | HTTP | Graph traversal and link discovery |
| rag-query | HTTP | Natural language Q&A over cases |
| audit-logging | HTTP | Immutable audit trail |
| fairness-check | HTTP | Model fairness verification |

## Prerequisites

- Zoho Catalyst account with project access
- Node.js >= 18
- Catalyst CLI (`npm install -g catalyst-cli`)

## Local Development

```bash
# Navigate to the function directory
cd functions/fir-ingestion

# Install dependencies
npm install

# Run locally via Catalyst CLI
catalyst serve

# Deploy to Catalyst
catalyst deploy --project <project_id>
```

## Common Modules

Located in `apps/api/common/`:

| Module | Purpose |
|--------|---------|
| `errors.ts` | Error classes with standard API format |
| `response.ts` | Standard success/error response builders |
| `logger.ts` | Structured logger with correlation ID |
| `config.ts` | Environment variable loader with validation |
| `validation.ts` | Schema-based request validation |

## Middleware

Located in `apps/api/middleware/`:

| Middleware | Purpose |
|------------|---------|
| `auth.ts` | JWT/Catalyst token verification |
| `audit.ts` | Audit trail logging |
| `correlation.ts` | Correlation ID propagation |
| `rate-limit.ts` | Per-route rate limiting |
| `error-handler.ts` | Global error formatting |

## Deployment

```bash
# Deploy all functions
catalyst deploy all

# Deploy a single function
catalyst deploy --function fir-ingestion
```
