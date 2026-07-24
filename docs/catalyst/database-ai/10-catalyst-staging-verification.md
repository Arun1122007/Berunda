# 10 - Catalyst Staging Verification

## Pre-requisites
- Catalyst CLI installed and authenticated.
- A dedicated `staging` environment in Zoho Catalyst.

## Deployment Steps
1. Run `catalyst deploy` from the repository root.
2. Verify AppSail deployment succeeds.
3. Verify Catalyst Client (Frontend) deployment succeeds.

## Verification Checklist
- [ ] **Health Endpoint**: Fetch `/health` and verify the `database` connection check returns `True` (indicating Data Store connectivity).
- [ ] **Data Store**: Insert a test FIR via the UI. Verify the record appears in Catalyst Data Store Console.
- [ ] **Stratus (File Store)**: Upload a dummy PDF. Verify the object is stored in Stratus and linked to the FIR.
- [ ] **QuickML Integration**: Submit a test prompt via the RAG interface. Verify the API connects to QuickML and returns a coherent text response.
- [ ] **Zia Integration**: Trigger OCR on the dummy PDF and verify text extraction populates the database.
- [ ] **Cache/NoSQL**: Trigger the rate limiter. Verify 429 status code is returned correctly.

## Rollback Procedure
If verification fails:
1. Revert to the previous Catalyst version via the Catalyst Console.
2. Investigate application logs in Catalyst APM / Log Management.
