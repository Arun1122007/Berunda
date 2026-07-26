# 08 — Catalyst Deployment and Operations Design

**Document ID:** BERUNDA-ARCH2-DEPLOY-001
**Version:** 1.0 | **Status:** APPROVED — Phase 2 deployment baseline
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

> All deployment targets are Zoho Catalyst only (ADR-002).
> No external cloud infrastructure.
> This document defines deployment steps without executing them.

---

## 1. Environment Definitions

Three environments are defined. Additional environments are not supported given team size and hackathon timeline.

| Environment | Purpose | Data Permitted | Source | Access |
|-------------|---------|---------------|--------|--------|
| **local** | Active development; unit tests; rapid iteration | Synthetic only; SQLite for DB | Developer workstation | Developer only |
| **catalyst-dev** | Integration testing; Alembic migration verification; AppSail compatibility checks | Synthetic only; Catalyst Data Store | Push to dev branch | Team only |
| **catalyst-demo** | Final demo; judging; seed data loaded | Synthetic only; Catalyst Data Store | Push to main after Day-10 gate | Team + judges |

No staging environment. No production environment (not required for hackathon).

### Environment Specifications

#### local

| Field | Value |
|-------|-------|
| **Purpose** | Development and unit testing |
| **Backend** | `uvicorn src.main:app --reload` via `make dev-backend` |
| **Frontend** | `npm run dev` (Vite HMR on port 5173) |
| **Database** | SQLite (via SQLAlchemy async `aiosqlite` driver) or Catalyst Data Store with local credentials |
| **File storage** | Local filesystem mock (`data/uploads/` directory) |
| **AI** | MockProvider by default; LLM provider activated if key present in `.env` |
| **Config** | `.env` file (gitignored); `.env.example` documents required vars |
| **Secrets** | In `.env` file; never committed |
| **Reset** | `make reset-local` — drop SQLite, re-run Alembic, re-seed |
| **Log level** | DEBUG |

#### catalyst-dev

| Field | Value |
|-------|-------|
| **Purpose** | Integration test on Catalyst infrastructure; migration testing; AppSail compatibility |
| **Backend** | Catalyst AppSail (Python 3.11); deploy from `dev` branch |
| **Frontend** | Catalyst Slate (static; build from `apps/web/`) |
| **Database** | Catalyst Data Store; separate dev project or table prefix |
| **File storage** | Catalyst Stratus (dev bucket: `berunda-dev-docs`) |
| **AI** | MockProvider default; live providers if keys set |
| **Config** | Catalyst AppSail environment variables |
| **Secrets** | Catalyst AppSail env var store; not in git |
| **Reset** | `make reset-catalyst-dev` — re-run Alembic, re-seed |
| **Log level** | INFO |

#### catalyst-demo

| Field | Value |
|-------|-------|
| **Purpose** | Final hackathon demo; judging |
| **Backend** | Catalyst AppSail (production AppSail instance) |
| **Frontend** | Catalyst Slate (main domain URL) |
| **Database** | Catalyst Data Store (demo project) |
| **File storage** | Catalyst Stratus (demo bucket: `berunda-demo-docs`) |
| **AI** | MockProvider always available; live LLM if API key present |
| **Config** | Catalyst AppSail env vars; locked before Day 10 |
| **Secrets** | Catalyst AppSail env var store |
| **Access** | Team + judges only; login required |
| **Reset behavior** | `make reset-demo` — re-run seed with idempotent script; does NOT drop schema |
| **Log level** | INFO |

---

## 2. Catalyst Service Mapping

| Component | Catalyst Service | Configuration | Notes |
|-----------|----------------|--------------|-------|
| React SPA | Catalyst Slate | Deploy from `apps/web/dist/` | Static CDN; `VITE_API_BASE_URL` set at build time |
| FastAPI backend | Catalyst AppSail | Python 3.11 runtime; port 9000 | All business logic, AI, ML |
| PostgreSQL-compatible DB | Catalyst Data Store | Project-level; all tables in one project | Alembic manages schema |
| File storage | Catalyst Stratus | Bucket per environment | FIR document PDFs/images |
| Background tasks | FastAPI BackgroundTasks (in-process) | No separate service | ADR-011 |
| Scheduled jobs | Catalyst Scheduled Job | Risk batch, anomaly scan: nightly | Calls AppSail endpoints |
| Monitoring | AppSail stdout logs (Catalyst logging) | Structured JSON | Prometheus available in local only |

---

## 3. Catalyst AppSail Configuration

### AppSail Environment Variables

| Variable | Required | Environment | Value Template |
|----------|---------|------------|---------------|
| `DATABASE_URL` | Yes | All | `mysql+aiomysql://user:pass@host/berunda_demo` (Catalyst Data Store connection string) |
| `JWT_SECRET_KEY` | Yes | All | 256-bit hex string; generated with `openssl rand -hex 32` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | No | All | `15` |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | No | All | `7` |
| `OPENAI_API_KEY` | No | catalyst-demo | From OpenAI console |
| `GROQ_API_KEY` | No | catalyst-demo | From Groq console |
| `STRATUS_TOKEN` | Yes | catalyst-dev, catalyst-demo | Catalyst Stratus API token |
| `STRATUS_BUCKET` | Yes | All | `berunda-dev-docs` or `berunda-demo-docs` |
| `CORS_ORIGINS` | Yes | All | Catalyst Slate URL (e.g., `https://berunda.zohocatalyst.com`) |
| `APP_ENV` | No | All | `development` or `production` |
| `LOG_LEVEL` | No | All | `INFO` (demo), `DEBUG` (local) |
| `SENTRY_DSN` | No | catalyst-demo | Optional error tracking |

### AppSail Health Check Configuration

```yaml
health_check:
  path: /health
  interval: 30s
  timeout: 10s
  healthy_threshold: 1
  unhealthy_threshold: 3
```

---

## 4. Catalyst Slate Configuration

| Setting | Value |
|---------|-------|
| **Source directory** | `apps/web/dist/` (built with `npm run build`) |
| **Build command** | `npm run build` (Vite build with env vars) |
| **Environment variables (build-time)** | `VITE_API_BASE_URL=https://api.berunda.zohocatalyst.com` |
| **SPA routing** | Configure Slate to serve `index.html` for all non-file paths (SPA fallback) |
| **Cache headers** | Hashed assets: `max-age=31536000`; `index.html`: `max-age=0, must-revalidate` |

---

## 5. Catalyst Data Store Schema

| Setting | Value |
|---------|-------|
| **Schema management** | Alembic `upgrade head` run before backend start |
| **Initial setup** | Run `alembic upgrade head` from Catalyst Function or AppSail startup command |
| **Connection** | `DATABASE_URL` from AppSail env var |
| **Tables** | All `src_`, `int_`, `gov_`, `auth_` tables as defined in Doc 04 |
| **Permissions** | Application user: INSERT on `gov_AuditLog` only; full CRUD on all others |
| **Backups** | Catalyst Data Store managed backups (not verified for hackathon tier — open question ARCH-OQ-002) |

---

## 6. Catalyst Stratus Configuration

| Setting | Value |
|---------|-------|
| **Bucket naming** | `berunda-dev-docs` (dev); `berunda-demo-docs` (demo) |
| **Access** | Server-side only via Catalyst Stratus SDK with `STRATUS_TOKEN` |
| **Object naming** | `{case_master_id}/{iso8601_utc}/{sha256_prefix}.{ext}` |
| **CORS** | No browser-direct access; CORS not required on Stratus |
| **Size limit** | 10 MB per upload (enforced in application before Stratus call) |

---

## 7. Catalyst Scheduled Jobs

| Job | Schedule | Trigger | Target | Notes |
|-----|---------|---------|--------|-------|
| Risk score batch | Daily 02:00 IST | Catalyst Scheduled Job | `POST /api/v1/risk/batch-compute` (internal auth) | Fairness check before run |
| Anomaly detection | Daily 02:30 IST | Catalyst Scheduled Job | `POST /api/v1/anomaly/compute` (internal auth) | z-score computation |
| Hotspot rebuild | On FIR create + nightly 03:00 IST | BackgroundTask + Scheduled Job | `POST /api/v1/hotspot/rebuild` (internal) | Density aggregation |
| Refresh token cleanup | Weekly | Catalyst Scheduled Job | `POST /api/v1/auth/cleanup` (internal) | Delete expired tokens |

Internal scheduled job endpoints require `X-Internal-Job-Key` header for authorization.

---

## 8. Deployment Steps (Without Executing)

### Pre-Deployment Checklist (both environments)

Before any deployment, verify:

- [ ] All P0 feature tests passing locally (`make test-p0`)
- [ ] No secrets in `.env` committed to git (`git-secrets --scan`)
- [ ] Alembic migrations reviewed (`alembic history`)
- [ ] OpenAPI spec validated (`npx @redocly/cli lint docs/api/openapi.yaml`)
- [ ] Frontend build succeeds locally (`npm run build`)
- [ ] Health endpoint returns `{ "status": "healthy" }` locally

### Deployment Sequence

```
Step 1: Validate source
  → git pull origin main
  → git log -1 (verify commit)
  → git-secrets --scan-history

Step 2: Run tests
  → make test (unit + integration + security)
  → make evaluate-ai (NER F1, entity resolution recall)
  → Tests must pass at ≥ 70% coverage threshold

Step 3: Build frontend
  → cd apps/web
  → npm ci
  → VITE_API_BASE_URL=<target URL> npm run build
  → Verify dist/ size (warn if > 5 MB)

Step 4: Build backend artifact
  → pip install -r requirements.txt
  → python -m pytest (verify imports)
  → Catalyst AppSail deployment package (zip or git-push per Catalyst deploy method)

Step 5: Validate environment variables
  → Check all required env vars set in AppSail console
  → Verify DATABASE_URL, JWT_SECRET_KEY, STRATUS_TOKEN present
  → Verify no placeholder values

Step 6: Validate database prerequisites
  → Connect to Catalyst Data Store (test connection)
  → Verify current Alembic revision
  → Review pending migrations (alembic history)

Step 7: Validate Stratus prerequisites
  → Verify bucket exists (berunda-demo-docs)
  → Verify STRATUS_TOKEN has read/write access
  → Verify bucket is empty or has expected objects

Step 8: Deploy
  → Deploy AppSail: Catalyst console or `catalyst deploy` CLI
  → Wait for AppSail restart (60s)
  → Deploy Slate: upload dist/ to Catalyst Slate

Step 9: Run health checks
  → GET /health → { "status": "healthy", "checks": { "database": true } }
  → GET /ready → { "status": "ready" }
  → If degraded: check AppSail logs immediately

Step 10: Run smoke tests
  → POST /api/v1/auth/login (demo ADMIN) → 200
  → GET /api/v1/firs (demo INVESTIGATOR token) → 200 with items
  → GET /api/v1/hotspot → 200 with data
  → POST /api/v1/rag/query → 200 (MockProvider if no key)

Step 11: Seed demo data (if required)
  → python scripts/data/generate_synthetic.py --tier demo
  → Verify seed: python scripts/validation/validate_resources.py
  → Verify planted patterns: AC-SEED-001 assertions

Step 12: Verify rollback readiness
  → Note previous Alembic revision
  → Document rollback command: alembic downgrade -1
  → Verify previous AppSail artifact available
  → Document rollback procedure in this file
```

---

## 9. Demo Reset Procedure

On any demo day that requires a clean state:

```
make reset-demo

Steps:
1. Re-run seed script (idempotent UPSERT — does not drop schema)
   python scripts/data/generate_synthetic.py --tier demo --idempotent
2. Clear extraction queue items from previous sessions (OPTIONAL — discuss with team)
   python scripts/data/reset_queue.py  # deletes only PENDING queue items
3. Verify demo users have correct passwords
   python scripts/data/verify_demo_users.py
4. Verify planted patterns present
   python scripts/validation/validate_resources.py --check-patterns
5. Run smoke tests (Step 10 above)
6. Pre-load FAISS index (if not auto-built on startup)
   POST /api/v1/rag/rebuild-corpus  (ADMIN endpoint)
```

**Maximum reset time:** 10 minutes. Reset must complete before demo begins.

---

## 10. Monitoring and Observability

### Catalyst-Level Monitoring

| Signal | Source | Where Visible |
|--------|--------|-------------|
| AppSail health | `/health` endpoint | Catalyst console + Scheduled Job alert |
| Application logs | AppSail stdout (structured JSON) | Catalyst log viewer |
| Error rate | HTTP 5xx count from AppSail access logs | Catalyst console |
| Request latency | AppSail access logs `duration_ms` | Manual review |

### Local-Only Monitoring (Not Catalyst-Deployed)

| Tool | Purpose | Where |
|------|---------|-------|
| Prometheus | Metrics collection | `docker-compose.yml` `prometheus` service |
| Grafana | Dashboard | `docker-compose.yml` `grafana` service (port 3000) |
| FastAPI `/metrics` | Prometheus scrape endpoint | `src/middleware/prometheus.py` (not exposed in production) |

### Alerting (Demo Day)

Demo day manual monitoring checklist (run every 15 minutes during judging):

- [ ] `/health` returns `healthy`
- [ ] Last audit event < 2 minutes ago (system is processing requests)
- [ ] AppSail log stream shows no ERROR level entries
- [ ] FAISS index size: `GET /api/v1/status` shows `rag_corpus_chunks > 0`

---

## 11. Error Diagnostics

### Log Location

| Environment | Log Location |
|-------------|-------------|
| local | Console stdout; `logs/app.log` if file handler configured |
| catalyst-dev | Catalyst AppSail log viewer (Project → AppSail → Logs) |
| catalyst-demo | Catalyst AppSail log viewer |

### Diagnostic Endpoints (ADMIN only)

| Endpoint | Purpose |
|----------|---------|
| `/api/v1/status` | AppSail metadata: uptime, rag_corpus_size, model_versions |
| `/health` | DB connectivity + Python version |
| `/ready` | DB ready |

### Common Failure Scenarios

| Failure | Symptom | Diagnosis | Resolution |
|---------|---------|-----------|-----------|
| AppSail cold start | 503 on first request | Catalyst console → AppSail status | Wait 30s; retry |
| DB migration not run | 500 on FIR create | `alembic current` shows mismatch | Run `alembic upgrade head` |
| JWT_SECRET_KEY wrong | 401 on all requests | Log shows "JWT decode error" | Set correct env var; restart AppSail |
| Stratus token expired | 503 on file upload | Log shows "Stratus SDK error" | Refresh token in Catalyst console |
| FAISS index empty | RAG returns "no information" | `GET /api/v1/status` shows 0 chunks | Run `POST /api/v1/rag/rebuild-corpus` |
| spaCy model missing | NER fails; EXTRACTION_FAILED | Log shows "spaCy model not found" | Verify model in requirements; rebuild AppSail |

---

## 12. Rollback Procedure

If deployment fails or demo is broken:

```
Rollback Steps:
1. Identify last known good Alembic revision
   alembic history → find previous
2. Run downgrade
   alembic downgrade <previous_revision>
3. Redeploy previous AppSail artifact
   Catalyst console → AppSail → Deployments → Rollback
4. Redeploy previous Slate build
   Re-upload previous dist/
5. Run health checks (Step 9 above)
6. If DB schema rollback not possible (data exists):
   Do NOT run alembic downgrade — deploy new code version that is compatible with existing schema
```

**Rollback decision point:** If demo demo-critical features (FIR create, RAG, graph) are broken > 5 minutes, initiate rollback. Non-critical features (analytics, reports) can wait.

---

## 13. Backup Assumptions

| Data | Backup Assumption | Verified? |
|------|-------------------|-----------|
| Catalyst Data Store | Platform-managed backup (Catalyst responsibility) | Not verified for hackathon tier — ARCH-OQ-002 |
| Catalyst Stratus | Platform-managed backup | Not verified |
| Seed script | Idempotent; can re-run — `scripts/data/generate_synthetic.py` | Yes |
| FAISS index | Rebuilt from DB on startup — not backed up separately | Yes |
| Application code | GitHub repository | Yes |

**Demo-day backup:** A `.sql` dump of the demo database is taken manually on Day 10 morning and stored in `data/backups/` (gitignored).

---

## 14. Open Deployment Questions

| ARCH-OQ-ID | Question | Impact | Due |
|-----------|---------|--------|-----|
| ARCH-OQ-001 | AppSail Python 3.11 + scikit-learn + spaCy compatibility | Critical — affects all ML | Day 1 |
| ARCH-OQ-002 | Data Store table/row limits for hackathon tier | High — affects schema | Day 1 |
| ARCH-OQ-003 | Catalyst Zia OCR availability | Medium — affects upload flow | Day 1 |
| ARCH-OQ-004 | Stratus streaming upload support | Medium — affects upload | Day 2 |
| ARCH-OQ-005 | API Gateway timeout for long NER calls (> 30s) | High — affects NER | Day 1 |

---

*End of 08-CATALYST-DEPLOYMENT-AND-OPERATIONS-DESIGN.md*
