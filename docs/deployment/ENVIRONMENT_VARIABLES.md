# Project Berunda — Environment Variables Specification

> **Document ID:** BERUNDA-DEP-003 | **Version:** 1.1  
> **Classification:** Security / Operations  
> **Last Updated:** 2026-07-27  

---

## 1. AI Provider & Multi-Provider Fallback Chain Configuration

Project Berunda includes an automatic multi-provider fallback engine (`FallbackProvider`). If a primary provider is unconfigured, times out, or returns an API error, the system automatically falls through to the next available provider:

$$\text{Priority Chain: } \text{Groq} \longrightarrow \text{NVIDIA NIM} \longrightarrow \text{OpenRouter} \longrightarrow \text{OpenAI} \longrightarrow \text{Catalyst AI} \longrightarrow \text{Mock}$$

| Environment Variable | Required | Default / Base URL | Recommended Models | Purpose / Provider |
| :--- | :---: | :--- | :--- | :--- |
| `DEFAULT_AI_PROVIDER` | Yes | `fallback` | `fallback`, `groq`, `nvidia`, `openrouter`, `openai`, `mock` | Active provider selection strategy |
| `GROQ_API_KEY` | Optional | `gsk_...` | `llama-3.3-70b-versatile`, `mixtral-8x7b-32768` | **Groq LPU API** for ultra-fast Llama-3.3 inference |
| `GROQ_BASE_URL` | Optional | `https://api.groq.com/openai/v1` | — | Groq OpenAI-compatible endpoint |
| `NVIDIA_API_KEY` | Optional | `nvapi-...` | `meta/llama-3.3-70b-instruct`, `nvidia/llama-3.1-nemotron-70b-instruct` | **NVIDIA NIM Microservices** enterprise LLM inference |
| `NVIDIA_BASE_URL` | Optional | `https://integrate.api.nvidia.com/v1` | — | NVIDIA NIM OpenAI-compatible endpoint |
| `OPENROUTER_API_KEY` | Optional | `sk-or-v1-...` | `meta-llama/llama-3.3-70b-instruct`, `google/gemini-2.5-flash`, `deepseek/deepseek-r1` | **OpenRouter API Gateway** universal multi-model access |
| `OPENROUTER_BASE_URL` | Optional | `https://openrouter.ai/api/v1` | — | OpenRouter OpenAI-compatible endpoint |
| `OPENAI_API_KEY` | Optional | `sk-proj-...` | `gpt-4o-mini`, `gpt-4o`, `text-embedding-3-small` | **OpenAI API** for GPT-4 models and vector embeddings |
| `OPENAI_BASE_URL` | Optional | `https://api.openai.com/v1` | — | OpenAI API endpoint |
| `CATALYST_API_KEY` | Optional | `...` | `catalyst-llm` | **Zoho Catalyst Native AI** service key |

---

## 2. Core Application & Server Settings (`.env`)

| Variable Name | Type | Required | Configured Value | Description |
| :--- | :---: | :---: | :--- | :--- |
| `APP_ENV` | Private | Yes | `development` / `production` | Environment mode |
| `LOG_LEVEL` | Private | Yes | `INFO` / `DEBUG` | Backend logging verbosity |
| `HOST` | Private | Yes | `0.0.0.0` | Network binding interface |
| `PORT` | Private | Yes | `8000` / `9000` | Local HTTP listener port |
| `DATABASE_URL` | Private | Yes | `sqlite+aiosqlite:///./berunda.db` | SQLAlchemy Async DB connection string |
| `JWT_SECRET` | Secret | Yes | `replace-with-a-random-64-hex-char-string` | JWT token signing key |
| `CATALYST_PROJECT_ID` | Private | Yes | `48591000000013025` | Catalyst project identifier |
| `CATALYST_ENVIRONMENT_ID` | Private | Yes | `60079736152` | Catalyst environment identifier |

---

## 3. Frontend Production Settings (`apps/web/.env.production`)

| Variable Name | Type | Required | Configured Value | Description |
| :--- | :---: | :---: | :--- | :--- |
| `VITE_API_BASE_URL` | Public | Yes | `https://berunda-api-50044292022.development.catalystappsail.in/api/v1` | Production AppSail API base URL |
| `VITE_API_URL` | Public | Yes | `https://berunda-api-50044292022.development.catalystappsail.in` | AppSail domain root |
| `VITE_CATALYST_ENABLED` | Public | Yes | `true` | Enables Catalyst Web SDK initialization |
