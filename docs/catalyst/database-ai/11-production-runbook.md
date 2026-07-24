# 11 - Production Runbook

## Deployment Pre-flight
- [ ] Ensure all code is merged to `main`.
- [ ] Ensure Catalyst CI/CD pipeline has completed Unit, Integration, and Security tests.
- [ ] Verify `staging` environment is healthy.

## Production Deployment
1. Set the Catalyst CLI context to production: `catalyst env:use production`.
2. Execute deployment: `catalyst deploy`.
3. Monitor logs for any startup failures in the AppSail instances.

## Data Migration
1. Run `python scripts/import_legacy_data.py --env production` to seed the database with reference data (Districts, Units, Acts, Sections).
2. Verify row counts in Data Store match expectations.

## Monitoring & Response
- **Alerting**: Catalyst Signals/Metrics will alert on API 500s or latency spikes >5s.
- **Incident Response**:
  - If AppSail crashes: Check Catalyst Logs, rollback to previous version via Console.
  - If Data Store is unresponsive: Check Catalyst Status Page, notify Zoho Support.
  - If QuickML/Zia returns errors: Ensure Quotas are not exceeded. Feature-flag the AI integration off to ensure core CRUD remains functional.
