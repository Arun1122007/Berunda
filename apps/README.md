# Berunda — Apps Monorepo

This monorepo contains three application packages that together form the Berunda Crime Intelligence Platform, deployed on Zoho Catalyst.

## Package Overview

| Package | Path | Role | Runtime |
|---------|------|------|---------|
| `@berunda/web` | `apps/web/` | React SPA frontend | Browser (Vite dev server) |
| `@berunda/api` | `apps/api/` | Catalyst Functions backend | Node.js on Catalyst |
| `@berunda/worker` | `apps/worker/` | Background job processor | Node.js on Catalyst Cron |

## Architecture

```
User Browser
     │
     ▼
  ┌─────────────┐     ┌─────────────────────────────────────┐
  │  @berunda    │────▶│  @berunda/api                       │
  │  /web        │     │  ┌──────────┐ ┌───────────┐        │
  │  (React SPA) │     │  │ FIR      │ │ NER       │        │
  │              │     │  │ Ingestion│ │ Extraction│        │
  │  MapLibre    │     │  ├──────────┤ ├───────────┤        │
  │  Cytoscape   │     │  │ Entity   │ │ Risk      │        │
  │  Recharts    │     │  │Resolution│ │ Scoring   │        │
  │              │     │  ├──────────┤ ├───────────┤        │
  │              │     │  │ Hotspot  │ │ Anomaly   │        │
  │              │     │  │ Analysis │ │ Detection │        │
  │              │     │  ├──────────┤ ├───────────┤        │
  │              │     │  │ Link     │ │ RAG       │        │
  │              │     │  │ Analysis │ │ Query     │        │
  │              │     │  ├──────────┤ ├───────────┤        │
  │              │     │  │ Audit    │ │ Fairness  │        │
  │              │     │  │ Logging  │ │ Check     │        │
  │              │     │  └──────────┘ └───────────┘        │
  └─────────────┘     └──────────┬──────────────────────────┘
                                 │
                                 ▼
                        ┌────────────────┐
                        │  @berunda      │
                        │  /worker       │
                        │  (Cron Jobs)   │
                        │                │
                        │  Nightly:      │
                        │  · Hotspot     │
                        │  · Freshness   │
                        │  · Reports     │
                        └────────────────┘
```

### `@berunda/web`
The frontend single-page application built with React 18, TypeScript, and Vite. It provides:
- Interactive maps via MapLibre GL for hotspot visualisation
- Relationship graphs via Cytoscape.js for link analysis
- Charts and dashboards via Recharts
- RAG-powered natural language query interface ("Ask Berunda")
- Admin panel for configuration

### `@berunda/api`
Ten Catalyst Functions that implement the backend logic:
- **fir-ingestion** — Import and validate FIR data
- **ner-extraction** — Named entity extraction from FIR narratives
- **entity-resolution** — Resolve person entities across cases
- **risk-scoring** — Compute repeat-offender risk scores
- **hotspot-analysis** — KDE/hexbin hotspot computation
- **anomaly-detection** — Spike detection against baselines
- **link-analysis** — Graph traversal and hidden link discovery
- **rag-query** — Natural language Q&A over case corpus
- **audit-logging** — Immutable audit trail
- **fairness-check** — Model fairness verification

### `@berunda/worker`
Background job processor triggered by Catalyst Cron schedules. Handles nightly recomputation, data freshness checks, and report generation.

## Development

Each package has its own `package.json` and can be developed independently. See individual READMEs for setup instructions.

```bash
# Install dependencies for all packages
cd apps/web && npm install
cd apps/api && npm install
cd apps/worker && npm install
```
