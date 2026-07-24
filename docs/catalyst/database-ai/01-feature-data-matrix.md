# 01 - Feature to Data Matrix

| Feature | User Role | Tables (Data Store) | NoSQL Documents (Catalyst NoSQL) | Stratus Objects | Cache | AI Data (QuickML/Zia) | CRUD Operations | Permissions | Status |
| ------- | --------- | ------------------- | -------------------------------- | --------------- | ----- | --------------------- | --------------- | ----------- | ------ |
| **Authentication & AuthZ** | All Users | `users`, `sessions`, `permissions` | - | - | Rate-limiting counters | - | Read, Create, Update (Tokens) | Anonymous (Login), Authenticated (Refresh) | Planned |
| **FIR Management** | Officer, Admin | `case_master`, `inv_occurance_time`, `complainant_details`, `victim`, `accused`, `arrest_surrender`, `chargesheet_details` | - | FIR PDF Scans, Evidence Images | - | - | Create, Read, Update, Delete | District-scoped access | Planned |
| **Reference Data** | Admin | `act`, `section`, `crime_head`, `state`, `district`, `unit`, `rank` | - | - | Standard lookups | - | Read | Authenticated | Planned |
| **Entity Resolution** | Analyst, Admin | `person_entity`, `person_entity_link`, `vehicle_link` | - | - | - | - | Read, Create, Merge | Analyst-scoped | Planned |
| **Graph Traverse** | Analyst, Admin | `relationship_edge` | - | - | Sub-graph caching | - | Read | Analyst-scoped | Planned |
| **Risk Scoring** | Analyst, Admin | `risk_score`, `risk_score_feature_importance` | - | - | - | Predictions (Zia AutoML / custom model output) | Create (Job), Read | Analyst-scoped | Planned |
| **Hotspot Analysis** | Analyst, Admin | `hotspot_layer` | GeoJSON event streams | - | Aggregated cluster cache | - | Read | Analyst-scoped | Planned |
| **Anomaly Detection** | Analyst, Admin | `anomaly_alert` | - | - | - | Prediction/Classification outputs | Read, Update (Acknowledge) | Analyst-scoped | Planned |
| **RAG (Case Search)** | Officer, Analyst | `ai_conversation`, `ai_message`, `rag_corpus_chunk` | Raw embeddings/trace context | Uploaded corpus PDFs | - | QuickML Knowledge Base chunks, Prompt completions | Create, Read | Authenticated | Planned |
| **AI Governance** | Admin | `ai_usage_record`, `prompt_version`, `ai_feedback` | - | - | - | LLM traces, feedback logs | Create, Read | Admin-only | Planned |
| **Fairness Audit** | Admin | `fairness_check_result` | - | - | - | Bias evaluation outputs | Create (Job), Read | Admin-only | Planned |
| **System Audit** | Admin | `audit_log`, `data_provenance_record` | High-volume raw audit events | - | - | - | Create, Read | Admin-only | Planned |

## Notes
- **Catalyst Data Store** will handle all core relational data (e.g. Users, FIRs, Entities).
- **Catalyst Stratus** will handle unstructured files (PDFs, Images, Model artifacts).
- **Catalyst QuickML** will handle RAG and prompt generation.
- **Catalyst NoSQL** will be used selectively for high-volume, semi-structured data like incoming GeoJSON streams or raw audit logs before being aggregated into the Data Store.
