# 12 - Gap and Risk Register

| Risk / Gap | Severity | Reason | Owner | Required Action | Blocking Status |
| ---------- | -------- | ------ | ----- | --------------- | --------------- |
| **Missing Zoho Catalyst Credentials** | Critical | We are currently using local models and `LocalMemoryRepository` for testing because we do not have an active Zoho account/credentials configured in the environment. | Dev Team | Provision Zoho Catalyst Project, generate SDK credentials, add to `.env`. | **BLOCKING** for full Staging/Prod deploy. |
| **Unsupported `aiomysql` Dependency** | High | Catalyst Data Store requires ZCQL via SDK, not standard MySQL connectors. | Arch | Replace all direct SQLAlchemy usage with `CatalystDataStoreRepository`. | Non-blocking for local test, Blocking for Prod. |
| **OpenAI vs QuickML Parity** | Medium | QuickML might have different token limits or prompt formatting constraints than OpenAI. | AI Eng | Re-evaluate all prompts against QuickML documentation. | Non-blocking. |
| **Zia AutoML Training Data** | High | Training an Anomaly/Risk model requires substantial labelled historical data. | Data Eng | Extract, clean, and upload training sets to Zia. | Blocking for Risk feature accuracy. |
| **Cost / Quota Management** | Medium | High volume of RAG queries might exceed QuickML tiers. | DevOps | Implement rate-limiting and cache RAG responses. | Non-blocking for launch. |
