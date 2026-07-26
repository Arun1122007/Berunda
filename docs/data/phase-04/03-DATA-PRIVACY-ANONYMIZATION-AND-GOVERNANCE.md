# Data Privacy, Anonymization, and Governance

## 1. Classification
All data generated and processed in Phase 4 is classified as **SYNTHETIC (PUBLIC / LOW RISK)**.

## 2. Mandatory Guardrails
- **Victim Data**: Real victim names, demographics, or exact locations MUST NOT be ingested.
- **Authentication**: Real police login credentials MUST NOT be used. Dummy hash strings are employed for `Demo_Officer_1`, etc.
- **Operational Data**: No real active investigations are simulated. All case narratives are entirely fabricated via LLMs/Faker.
- **Traceability in Output**: Every generated CSV explicitly contains a `synthetic` flag or `SYNTHETIC_` prefix in the filename to prevent accidental ingestion into production environments down the line.

## 3. Privacy Tests (Validation)
Validation scripts must check for the presence of the string `synthetic: true` (or equivalent boolean fields) inside the generated databases.

## 4. Source Control Policy
- No real data is committed to Git.
- `data/raw` containing anything pulled from the web must remain in `.gitignore`.
