# Environment and Deployment Strategy

[//]: # (Document ID: BERUNDA-OPS-001 | Status: DRAFT | Classification: INTERNAL)

---

## 1. Environment Strategy

| Environment | Purpose | Data | Access | Deploy Trigger |
|------------|---------|------|--------|---------------|
| **Development** | Active development, debugging | Synthetic (small: 500 FIRs) | Developer only | Manual (git push) |
| **Testing** | CI/CD automated tests | Synthetic (full: 5,000 FIRs) | CI/CD pipeline | Automated (PR merge) |
| **Staging** | Pre-demo verification | Synthetic (full: 5,000 FIRs) | Team only | Automated (tagged release) |
| **Production** | Hackathon demo | Synthetic (full: 5,000 FIRs) | Judges + Team | Manual (release approval) |

## 2. Infrastructure per Environment

All environments run on Catalyst. Differences are configuration-based (data volume, function settings, cache size).

| Resource | Development | Testing | Staging | Production |
|----------|-------------|---------|---------|------------|
| Data Store | 1 instance (small) | 1 instance (small) | 1 instance (medium) | 1 instance (medium) |
| Catalyst Functions | 1 instance each | 1 instance each | 2 instances each | 2-5 instances each |
| AppSail | 1 instance (small) | 1 instance (small) | 1 instance (medium) | 1 instance (medium) |
| QuickML | Development tier | Development tier | Standard tier | Standard tier |
| Cache | 1 instance (small) | 1 instance (small) | 1 instance (medium) | 1 instance (medium) |
| Synthetic data | 500 FIRs | 5,000 FIRs | 5,000 FIRs | 5,000 FIRs |

## 3. Deployment Pipeline

```
Developer → GitHub (main branch)
  → GitHub Actions (lint + unit tests)
    → Catalyst Pipelines (build + deploy to Testing)
      → Integration + Security tests pass
        → Create GitHub release tag
          → Catalyst Pipelines (deploy to Staging)
            → Manual approval gate
              → Deploy to Production
```

## 4. Environment-Specific Configuration

Configuration is stored in Catalyst Stratus as JSON files, one per environment:

```
config/
├── development.json
├── testing.json
├── staging.json
└── production.json
```

Keys per file:
- `database.max_connections`
- `entity_resolution.high_threshold`, `entity_resolution.low_threshold`
- `anomaly_detection.z_score_threshold`
- `rag.max_chunks`, `rag.similarity_threshold`
- `cron.enabled` (disabled in dev/test)
- `synthetic.dataset_size`
- `logging.level`

## 5. Database Migration Strategy

| Migration Type | Process | Rollback |
|---------------|---------|----------|
| Schema changes | Versioned SQL migration scripts in `migrations/` directory | Revert script included |
| Data changes | Seed scripts with deterministic seeds | Re-run seed with previous version |
| Lookup table updates | INSERT/UPDATE scripts with idempotent keys | Reverse INSERT/DELETE |

**Migration naming:** `V{YYYYMMDD}_{NNN}__description.sql` (e.g., `V20260716_001__add_person_entity_table.sql`)
