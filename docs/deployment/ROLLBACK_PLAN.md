# Project Berunda — Rollback and Operational Recovery Plan

> **Document ID:** BERUNDA-DEP-008 | **Version:** 1.0  

---

## 1. Rollback Strategy

In the event of a deployment failure or critical runtime issue:

### Frontend Rollback
Re-deploy the previous verified frontend build artifact from git tag:
```bash
git checkout tags/v0.4.0-stable
cd apps/web && npm run build
catalyst deploy --only client
```

### Backend AppSail Rollback
Re-deploy the stable backend release artifact:
```bash
git checkout tags/v0.4.0-stable
catalyst deploy appsail --name berunda-api --build-path appsail/berunda_api --stack python_3_10 --command "python3 main.py"
```

### Database Recovery
1. Backup file `berunda.db.bak` is created prior to schema migrations.
2. To restore: Copy `berunda.db.bak` to `appsail/berunda_api/berunda.db`.
