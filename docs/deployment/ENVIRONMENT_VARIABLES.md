# Project Berunda — Environment Variables Specification

> **Document ID:** BERUNDA-DEP-003 | **Version:** 1.0  
> **Classification:** Security / Operations  

---

## 1. Frontend Production Environment Variables (`apps/web/.env.production`)

| Variable Name | Type | Required | Configured Value | Description |
| :--- | :---: | :---: | :--- | :--- |
| `VITE_API_BASE_URL` | Public | Yes | `https://berunda-api-50044292022.development.catalystappsail.in/api/v1` | Base URL for FastAPI backend endpoints |
| `VITE_API_URL` | Public | Yes | `https://berunda-api-50044292022.development.catalystappsail.in` | Root backend domain |
| `VITE_CATALYST_ENABLED` | Public | Yes | `true` | Enables Catalyst Web SDK initialization |
| `VITE_APP_ENV` | Public | Yes | `production` | Active runtime environment label |

---

## 2. Backend Production Environment Variables (`appsail/berunda_api/.env`)

| Variable Name | Type | Required | Configured Source | Description |
| :--- | :---: | :---: | :--- | :--- |
| `APP_ENV` | Private | Yes | Catalyst AppSail Config / Environment | Active environment (`production` / `development`) |
| `LOG_LEVEL` | Private | Yes | Environment Config | Application log verbosity (`INFO` / `WARNING`) |
| `HOST` | Private | Yes | Injected (`0.0.0.0`) | Network interface binding |
| `PORT` | Private | Yes | Injected (`X_ZOHO_CATALYST_LISTEN_PORT`) | HTTP listening port |
| `DATABASE_URL` | Private | Yes | `sqlite+aiosqlite:///./berunda.db` | Async SQLAlchemy database URL |
| `JWT_SECRET` | Secret | Yes | Environment Secret | Secret key for signing auth tokens |
| `OPENAI_API_KEY` | Secret | Optional | Environment Secret | API key for OpenAI LLM RAG queries |
| `GROQ_API_KEY` | Secret | Optional | Environment Secret | API key for Groq fast inference |
| `CATALYST_PROJECT_ID` | Private | Yes | `48591000000013025` | Catalyst project identifier |
