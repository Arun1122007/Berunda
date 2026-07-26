# 01 Feature to Data Matrix

This matrix maps every implemented and planned feature in Project Berunda to its persistent data strategy, strictly enforcing the Catalyst-first methodology.

| Feature | User Role | Tables (Data Store) | NoSQL Documents | Stratus Objects | Cache | AI Data | CRUD Operations | Permissions | Status |
| ------- | --------- | ------ | --------------- | --------------- | ----- | ------- | --------------- | ----------- | ------ |
| **Authentication & RBAC** | All | `Employee`, `Rank`, `Designation` | None | None | None | None | R | Public login, private roles | Defined |
| **FIR Case Management** | Police | `CaseMaster`, `Inv_OccurrenceTime`, `CaseCategory`, `GravityOffence`, `CaseStatusMaster` | None | `FIR_Attachments` (Stratus) | None | None | C, R, U | Role-based (IO/Admin) | Defined |
| **Entity Management** | Police | `ComplainantDetails`, `Victim`, `Accused`, `ArrestSurrender`, `ChargesheetDetails` | None | `Evidence_Photos` (Stratus) | None | None | C, R, U | Role-based (IO/Admin) | Defined |
| **Geospatial Hotspots** | Analyst | `Inv_OccurrenceTime` (Lat/Long), `District`, `Unit` | None | None | `Hotspot_Cache` | None | R | Analyst/Admin | Defined |
| **Graph Network Analysis**| Analyst | `CaseMaster`, Junction tables, Entities | None | None | None | None | R | Analyst/Admin | Defined |
| **Anomaly Detection** | Analyst | `CaseMaster`, Audit tables | `Anomaly_Traces` | None | None | QuickML Model Runs | C, R | Analyst/Admin | Defined |
| **Alerts & Notifications**| All | `Notification`, `AlertRule` | None | None | None | None | C, R, U, D | User isolated | Planned |
| **Document Q&A (RAG)** | Analyst | `Document_Metadata` | `Chat_History` | `Uploaded_Pdfs` | `Embeddings_Cache` | QuickML Knowledge Base | C, R, D | User isolated | Defined |
| **Crime Risk Scoring** | Analyst | `CaseMaster`, `Prediction_Runs` | None | None | None | AutoML/QuickML inference | C, R | Analyst/Admin | Defined |
| **Model Fairness Audit** | Admin | `Fairness_Audit_Log` | None | None | None | None | C, R | Admin only | Planned |

## Catalyst Storage Mapping Rules:
1. **Catalyst Data Store**: All structured entities (e.g. Users, FIRs, Complainants, Alerts).
2. **Catalyst Stratus**: All BLOBs, uploaded documents, images, and evidence files.
3. **Catalyst NoSQL**: Only flexible JSON logs like Chat History and Anomaly trace outputs.
4. **Catalyst Cache**: Temporary pre-computed data like high-frequency Hotspot boundaries.
