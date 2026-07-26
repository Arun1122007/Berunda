# Index and Query Support Strategy

> **Document ID:** BERUNDA-PH5-INDEX-001 | **Version:** 1.0

## Index Strategy for Catalyst
Catalyst provides basic indexing (Search Index).
- **CaseMaster**: CaseNo (Unique, Search Index)
- **Employee**: EmployeeID (Unique, Search Index)
- **Unit**: UnitID (Unique, Search Index)
- **AuditLog**: CorrelationID (Search Index)

*Note: Catalyst automatically indexes ROWID and Foreign Key columns.*
