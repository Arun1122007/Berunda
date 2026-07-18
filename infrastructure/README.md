# Infrastructure Overview

This document describes the infrastructure components for Project Berunda.

## Architecture

Berunda runs on **Zoho Catalyst** as the primary cloud platform, with Docker containers for local development and CI/CD verification.

```
┌─────────────────────────────────────────────────────────┐
│                    Zoho Catalyst                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │  Stratus  │  │ DataStore│  │   Catalyst Functions  │  │
│  │ (Cache)   │  │ (RDBMS)  │  │  ┌────┐ ┌────┐ ┌───┐ │  │
│  │           │  │          │  │  │API │ │Web │ │Wrk│ │  │
│  └──────────┘  └──────────┘  │  └────┘ └────┘ └───┘ │  │
│  ┌──────────┐  ┌──────────┐  └──────────────────────┘  │
│  │  NoSQL   │  │  Auth    │  ┌──────────────────────┐  │
│  │ (DocStore)│  │          │  │   AppSail            │  │
│  └──────────┘  └──────────┘  │ (ML Inference)        │  │
│  ┌──────────┐                └──────────────────────┘  │
│  │ QuickML  │  ┌──────────┐  ┌──────────────────────┐  │
│  │ (AutoML) │  │  Cron    │  │   Monitoring Stack   │  │
│  └──────────┘  └──────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Docker Setup

Each component has a production-grade multi-stage Dockerfile:

| Component | Dockerfile | Base Image | Port |
|-----------|-----------|------------|------|
| Frontend | `docker/frontend.Dockerfile` | nginx:alpine | 80 |
| API | `docker/api.Dockerfile` | node:20-slim | 9000 |
| Worker | `docker/worker.Dockerfile` | node:20-slim | (internal) |

### Building images

```powershell
docker build -f infrastructure/docker/frontend.Dockerfile -t berunda-frontend .
docker build -f infrastructure/docker/api.Dockerfile -t berunda-api .
docker build -f infrastructure/docker/worker.Dockerfile -t berunda-worker .
```

### Running locally with Docker Compose

```yaml
# docker-compose.yml (project root)
version: "3.9"
services:
  api:
    build:
      context: .
      dockerfile: infrastructure/docker/api.Dockerfile
    ports:
      - "9000:9000"
    env_file: infrastructure/environments/dev.env
  frontend:
    build:
      context: .
      dockerfile: infrastructure/docker/frontend.Dockerfile
      args:
        API_URL: http://localhost:9000
        ENVIRONMENT: development
    ports:
      - "8080:80"
    depends_on:
      - api
  worker:
    build:
      context: .
      dockerfile: infrastructure/docker/worker.Dockerfile
    env_file: infrastructure/environments/dev.env
    depends_on:
      - api
```

## Catalyst Deployment

See `infrastructure/catalyst/README.md` for detailed deployment instructions.

## Environment Management

Environment templates are in `infrastructure/environments/`:

| File | Purpose |
|------|---------|
| `dev.env.example` | Local development |
| `staging.env.example` | Staging environment |
| `prod.env.example` | Production (minimal defaults) |

## Local Development vs. Production

| Aspect | Local Dev | Production |
|--------|-----------|------------|
| Database | SQLite / local Catalyst emulator | Catalyst DataStore |
| Cache | In-memory / Redis (optional) | Catalyst Stratus |
| Auth | Mock tokens | Catalyst Authentication |
| AI/ML | Local models (Ollama) | Catalyst QuickML / AppSail |
| Logging | Console (pretty) | Structured JSON to Catalyst |
| Hot reload | Yes | No |
