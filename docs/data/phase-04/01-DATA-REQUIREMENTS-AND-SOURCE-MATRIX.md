# Data Requirements and Source Matrix

| Dataset ID | Dataset Name | Feature Supported | Req IDs | Sensitivity | Source Type | Completion Status |
|------------|--------------|-------------------|---------|-------------|-------------|-------------------|
| `DATA-REQ-001` | `CaseMaster` | FIR Ingestion / Management (F-001) | R-001 | Synthetic / Low | Python Script (Faker) | **Complete** |
| `DATA-REQ-002` | `PersonEntity` | Entity Resolution (F-003) | R-003 | Synthetic / Low | Python Script (Faker) | **Complete** |
| `DATA-REQ-003` | `RelationshipMaster` | Link Analysis (F-004) | R-004 | Synthetic / Low | Python Script (NetworkX) | **Complete** |
| `DATA-REQ-004` | `FIR_Extraction_Eval` | AI Extraction (F-006) | R-010 | Synthetic / Low | LLM Generated | **Pending** |
| `DATA-REQ-005` | `RelatedCase_Eval` | AI Case Linking (F-007) | R-012 | Synthetic / Low | Configured Pairs | **Pending** |
| `DATA-REQ-006` | `SemanticSearch_Eval`| AI Chatbot / Search (F-008) | R-015 | Synthetic / Low | Prompts / JSONL | **Pending** |
| `DATA-REQ-007` | `UserRoles_Demo` | Auth & RBAC (F-009) | R-020 | Synthetic / Low | Static JSON | **Pending** |
