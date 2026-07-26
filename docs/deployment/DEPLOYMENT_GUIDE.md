# Project Berunda — Complete Catalyst Deployment Guide

> **Document ID:** BERUNDA-DEP-002 | **Version:** 1.0  
> **Classification:** Operational | **Owner:** DevOps Team  

---

## 1. Prerequisites

- Node.js `v18+` / `v20+` & npm `v9+`
- Python `3.10+`
- Zoho Catalyst CLI (`npm install -g zcatalyst-cli`)
- Authenticated Catalyst Session (`catalyst whoami`)

---

## 2. Step-by-Step Deployment Commands

### Step 1: Verify Catalyst Authentication
```bash
catalyst whoami
catalyst project:use 48591000000013025
```

### Step 2: Build & Deploy Web Client (Frontend)
```bash
cd apps/web
npm install
npm run build
cd ../..
catalyst deploy --only client
```

### Step 3: Package & Deploy AppSail (Backend)
```bash
# Ensure seeded database is present in AppSail folder
Copy-Item "berunda.db" "appsail/berunda_api/berunda.db" -Force

# Deploy AppSail service
catalyst deploy appsail --name berunda-api --build-path appsail/berunda_api --stack python_3_10 --command "python3 main.py"
```

---

## 3. Verification

1. Open Frontend: `https://project-rainfall-60079736152.development.catalystserverless.in/app/index.html`
2. Test Backend Health: `https://berunda-api-50044292022.development.catalystappsail.in/health`
