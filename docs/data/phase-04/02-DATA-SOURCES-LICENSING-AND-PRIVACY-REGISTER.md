# Data Sources, Licensing, and Privacy Register

## 1. Primary Strategy
Project Berunda utilizes a **100% Synthetic Data Strategy** for its MVP and Hackathon evaluation phases. No real Police, Victim, or Suspect information is ingested from external public sources (e.g., NCRB scraping or leaked datasets).

## 2. Licensing Table

| Source | Data Description | License / Terms | Modification | Verdict |
|--------|------------------|-----------------|--------------|---------|
| `Faker` (PyPI) | Synthetic Names/Addresses | MIT | Allowed | **APPROVED** |
| `NetworkX` (PyPI) | Graph topologies | 3-Clause BSD | Allowed | **APPROVED** |
| Custom Generators | AI Evaluation JSONLs | Internal | Allowed | **APPROVED** |
| KSP / CCTNS Portals | Real FIR text | Prohibited by Terms | N/A | **REJECTED (DO NOT USE)** |
| Open-Meteo | Historical Weather Data | CC BY 4.0 | Allowed | **APPROVED** |

## 3. Web Scraping Policy
- **Bypassing CAPTCHAs**: Strictly prohibited.
- **Scraping Real FIRs**: Strictly prohibited due to the risk of ingesting real victim PII. All FIR text is synthetically generated for demonstration.
