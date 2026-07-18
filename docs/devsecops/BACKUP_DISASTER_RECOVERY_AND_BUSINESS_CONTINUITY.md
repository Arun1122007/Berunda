# Backup, Disaster Recovery, and Business Continuity

[//]: # (Document ID: BERUNDA-OPS-004 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: DevOps, Developers | Source: Architecture docs + Catalyst docs | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Backup Strategy

### 1.1 Data Backups

| Data | Backup Method | Frequency | Retention | Location |
|------|--------------|-----------|-----------|----------|
| Source zone (src_*) | Catalyst Data Store automatic backup | Daily | 7 days | Catalyst managed |
| Intelligence zone (int_*) | Catalyst Data Store automatic backup | Daily | 7 days | Catalyst managed |
| Governance zone (gov_*) | Catalyst Data Store automatic backup | Daily | 30 days | Catalyst managed |
| Synthetic seed scripts | Git version control | On change | Permanent | GitHub |
| Configuration files | Catalyst Stratus + Git | On change | Permanent | GitHub + Stratus |
| Model artifacts | Catalyst Stratus | On deploy | Permanent | Stratus |
| Audit log export | Manual export to CSV | Weekly | 90 days | Stratus |

### 1.2 Application Backups

| Asset | Backup Method | Frequency |
|-------|--------------|-----------|
| Catalyst Function code | Git version control | On commit |
| Catalyst Function binaries | Catalyst Pipelines build artifacts | On build |
| Dashboard SPA | Git version control | On commit |
| Pipeline configuration | Git version control | On change |

## 2. Disaster Recovery Scenarios

### 2.1 Data Corruption

**Scenario:** Synthetic data in src_* tables is accidentally modified or corrupted.

**Recovery:**
1. Identify the time of corruption from gov_AuditLog
2. Restore Data Store from last clean daily backup
3. Re-run any dependent int_* computations (risk scores, hotspots, anomalies)
4. Verify against planting manifest

**RTO:** 2 hours
**RPO:** 24 hours (daily backup)

### 2.2 Full System Failure

**Scenario:** Catalyst project is deleted or becomes unavailable.

**Recovery:**
1. Create new Catalyst project
2. Re-deploy all Functions from Git (Catalyst Pipelines)
3. Restore Data Store from backup
4. Re-upload configuration to Stratus
5. Re-design authentication users

**RTO:** 4 hours
**RPO:** 24 hours (daily backup)

### 2.3 Function-Level Failure

**Scenario:** A specific Catalyst Function crashes repeatedly.

**Recovery:**
1. Catalyst auto-restarts the function (typically < 30s)
2. If crash persists: roll back to last known-good version
3. If rollback fails: disable the feature and proceed with remaining features

**RTO:** < 5 minutes (auto-restart) or < 30 minutes (rollback)

### 2.4 QuickML Outage

**Scenario:** QuickML LLM or AutoML endpoint unavailable.

**Recovery:**
1. RAG: Return "AI service temporarily unavailable" to users
2. Risk scoring: Use last computed scores (read-only)
3. Both features degrade gracefully without breaking the rest of the system

**RTO:** N/A (graceful degradation)
**RPO:** Last computed scores

## 3. Business Continuity for Demo

### 3.1 Pre-Demo Preparation

| Action | Owner | Timing |
|--------|-------|--------|
| Full dataset export as SQL file | Developer | Day 10 |
| Screenshots of all features as PDF | Developer | Day 10 |
| Demo recording (5 min) | Developer | Day 10 |
| Offline evidence pack | Developer | Day 10 |
| Backup laptop with pre-loaded demo | Developer | Day 11 |

### 3.2 Worst-Case Contingency

If the live Catalyst deployment is unavailable during the demo:

1. **Presentation backup**: Walk through the slide deck with embedded screenshots
2. **Demo recording**: Play the pre-recorded 5-minute demo video
3. **Evidence pack**: Share the evidence pack PDF with judges as supporting material
4. **Live coding (last resort)**: Run the Python scripts locally to show entity resolution and graph generation on command line (no UI)

## 4. Data Restoration Procedure

```bash
# Step 1: Identify the backup to restore
catalyst backup:list --project berunda-hackathon

# Step 2: Restore Data Store
catalyst backup:restore --backup-id BK-20260715 --target datastore

# Step 3: Verify integrity
python scripts/validate_demo_data.py

# Step 4: Re-run nightly cron jobs (if needed)
catalyst cron:run --job CRON-001
catalyst cron:run --job CRON-002
catalyst cron:run --job CRON-003
```
