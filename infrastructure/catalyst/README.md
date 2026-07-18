# Zoho Catalyst Deployment Guide

## Prerequisites

1. **Catalyst CLI** installed:
   ```powershell
   npm install -g zoho-catalyst-cli
   ```

2. **Catalyst Account** with an active project.

3. **Authentication**:
   ```powershell
   catalyst auth login
   ```

4. **Project initialized** (one-time):
   ```powershell
   catalyst init
   ```

## Project Setup

### Initialize Catalyst in your project

```powershell
catalyst init --project <project-name> --org <org-id>
```

This creates a `catalyst-config.json` and a `.catalyst` folder.

### Configure Catalyst Services

The following Catalyst services are used by Berunda:

| Service | Purpose | Catalyst Console Section |
|---------|---------|-------------------------|
| **Data Store** | Relational database (PostgreSQL-compatible) | `Data Store > Tables` |
| **NoSQL** | Document store for unstructured data | `NoSQL > Collections` |
| **Stratus** | In-memory cache (Redis-compatible) | `Stratus > Cache` |
| **Authentication** | User auth (login, SSO, MFA) | `Authentication > Policies` |
| **QuickML** | AutoML model training and deployment | `QuickML > Models` |
| **AppSail** | ML inference hosting | `AppSail > Apps` |
| **Cron** | Scheduled job execution | `Cron > Jobs` |

#### Data Store Setup

1. Go to Catalyst Console > Data Store.
2. Create a table for each entity (FIRs, entities, users, etc.).
3. Run migrations:
   ```powershell
   catalyst migration:run
   ```

#### NoSQL Setup

1. Go to Catalyst Console > NoSQL.
2. Create collections: `sessions`, `audit_logs`, `analytics_events`.

#### Stratus Setup

1. Go to Catalyst Console > Stratus.
2. Create cache tables for: `session_cache`, `entity_cache`, `rate_limit`.

## Deploying Functions

Catalyst Functions are deployed from `apps/api/` and `apps/worker/`.

### Deploy API Functions

```powershell
cd apps/api
catalyst deploy --project <project-id> --environment <env>
```

### Deploy Frontend (Stratus/Static Hosting)

```powershell
cd apps/web
npm run build
catalyst deploy:static --source ./dist --environment <env>
```

### Deploy Worker (Cron Job)

```powershell
cd apps/worker
catalyst deploy --project <project-id> --environment <env>
```

## Environment Variables

Set environment variables in the Catalyst Console:

1. Go to **Cloud Console > Your Project > Functions > Environment Variables**.
2. Add each variable from the relevant `.env` file.
3. Click **Save** and redeploy functions.

**Do not commit `.env` files with real secrets to git.**

## Monitoring

### Logs

Access logs per function:
```
Catalyst Console > Functions > [Function Name] > Logs
```

### Metrics

View metrics in Catalyst Console:
- **Functions**: Invocations, errors, duration, memory.
- **Data Store**: Query performance, storage.
- **QuickML**: Model accuracy, inference count.

### Alerts

Configure alerts in Catalyst Console > Monitoring > Alerts.

## Official Documentation

For detailed Catalyst documentation, visit: [help.catalyst.zoho.com](https://help.catalyst.zoho.com)
