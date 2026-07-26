# 11 Production Runbook

## Deployment Steps
1. **Prepare Artifacts:** Run `powershell ./scripts/build_appsail.ps1` to compile the `src/` directory into the AppSail target folder.
2. **Environment Variables:** Define secrets securely within the Catalyst Console. Do not upload `.env` files.
   - Required Variables: `JWT_SECRET`, `FRONTEND_CORS_ORIGIN`.
3. **Deployment:** Run `catalyst deploy` from the root directory.
4. **Data Initialization:** If starting from a fresh environment, run the synthetic importer: `python scripts/database/import_synthetic_data.py --tier demo`.

## Incident Management

### AppSail Out Of Memory (OOM)
- **Symptom:** AppSail returns 502/504 Gateway errors. 
- **Cause:** Large PDF chunking for RAG or extensive pandas dataframe processing in `fairness_service.py` exceeding the 256MB Catalyst free tier limit.
- **Resolution:** Offload the processing to Catalyst Event Functions or stream the dataset directly to Stratus.

### Database Limit Exceeded
- **Symptom:** ZCQL queries fail with "Limit Exceeded" or `insert_row` fails.
- **Cause:** Free tier limits on Row counts or API invocations hit.
- **Resolution:** Implement aggressive caching in Catalyst Cache component to reduce `SELECT` invocations.

### AI Hallucination Surge
- **Symptom:** High alert volumes of hallucination failures from `guardrails_service.py`.
- **Cause:** Upstream changes in QuickML prompt handling or bad data ingested into the RAG Knowledge base.
- **Resolution:** Rebuild the Knowledge base or revert the prompt templates via the Catalyst Serverless console.
