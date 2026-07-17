# Analytics Feature Catalog

[//]: # (Document ID: BERUNDA-AI-002 | Status: DRAFT | Classification: INTERNAL)

---

## 1. Feature Overview

| Feature ID | Name | Type | Scope | Data Source | Priority |
|-----------|------|------|-------|-------------|----------|
| A-001 | FIR Intake Dashboard | Dashboard | MVP | src_CaseMaster | P1 |
| A-002 | Entity Resolution Console | Interface | MVP | int_PersonEntity + int_PersonEntityLink | P1 |
| A-003 | Relationship Graph Visualization | Interface | MVP | int_RelationshipEdge | P1 |
| A-004 | Geospatial Hotspot Map | Map | MVP | src_CaseMaster (Lat/Long) + int_HotspotLayer | P1 |
| A-005 | Temporal Crime Trends | Chart | MVP | src_CaseMaster (CrimeRegisteredDate) | P1 |
| A-006 | Anomaly Spike Alerts | Alert List | MVP | int_AnomalyAlert | P1 |
| A-007 | Risk Score Explorer | Interface | MVP | int_RiskScore + int_RiskScoreFeatureImportance | P1 |
| A-008 | "Ask Berunda" RAG Q&A | Interface | MVP | int_RAGCorpusChunk + QuickML LLM | P1 |
| A-009 | Jurisdiction Filter | Global Filter | MVP | src_State, src_District, src_Unit | P1 |
| A-010 | Audit Log Viewer | Table | MVP | gov_AuditLog | P1 |
| A-011 | Fairness Check Dashboard | Dashboard | MVP | gov_FairnessCheckResult | P1 |
| A-012 | Crime Head Distribution | Chart | MVP | src_CaseMaster + src_CrimeHead | P2 |
| A-013 | Case Status Breakdown | Chart | MVP | src_CaseMaster + src_CaseStatusMaster | P2 |
| A-014 | Vehicle Link Explorer | Interface | STRETCH | int_VehicleLink | P3 |
| A-015 | MO Pattern Explorer | Interface | STRETCH | int_MoPattern + int_MoPatternLink | P3 |

## 2. Feature Details

### A-001: FIR Intake Dashboard

**Type:** Dashboard  
**Source:** src_CaseMaster  
**Description:** Summary statistics of loaded FIR cases.  
**Metrics:** Total FIRs, by category (FIR/UDR/PAR), by status, by district.  
**Charts:** Bar chart (cases by district), pie chart (case category breakdown).  

### A-002: Entity Resolution Console

**Type:** Interface  
**Source:** int_PersonEntity + int_PersonEntityLink  
**Description:** Table of PersonEntities with link confidence, source records, and manual review status.  
**Actions:** Review pending matches, confirm/reject merge.  
**Filters:** Confidence range, source table, review status.  

### A-003: Relationship Graph Visualization

**Type:** Interface  
**Source:** int_RelationshipEdge + int_PersonEntity  
**Description:** Force-directed node-link graph (Cytoscape.js).  
**Features:** Degree centrality coloring, shortest-path search, click-to-expand.  

### A-004: Geospatial Hotspot Map

**Type:** Map (MapLibre GL)  
**Source:** src_CaseMaster (Lat/Long) + int_HotspotLayer  
**Description:** Hexbin/KDE heatmap layer with district boundaries.  
**Interactions:** Zoom, pan, click hexagon for case count.  

### A-005: Temporal Crime Trends

**Type:** Chart (Recharts)  
**Source:** src_CaseMaster (CrimeRegisteredDate)  
**Description:** Weekly/monthly crime counts with crime head breakdown.  
**Filters:** District, crime head, date range.  

### A-006: Anomaly Spike Alerts

**Type:** Alert List  
**Source:** int_AnomalyAlert  
**Description:** Table of detected anomalies sorted by z-score magnitude.  
**Details:** District, crime head, observed vs expected count, z-score.  

### A-007: Risk Score Explorer

**Type:** Interface  
**Source:** int_RiskScore + int_RiskScoreFeatureImportance  
**Description:** Table of persons with risk scores and feature importance breakdown.  
**Visualization:** Horizontal bar chart of top features by importance.  

### A-008: "Ask Berunda" RAG Q&A

**Type:** Interface  
**Source:** int_RAGCorpusChunk + QuickML LLM  
**Description:** Chat-like interface for natural language queries over case data.  
**Display:** Question → Answer with source citations.  

### A-009: Jurisdiction Filter

**Type:** Global Filter  
**Source:** src_State, src_District, src_Unit  
**Description:** Cascading dropdown filter (State → District → Station) applied to all analytics views.  

### A-010: Audit Log Viewer

**Type:** Table  
**Source:** gov_AuditLog  
**Description:** Searchable, filterable table of all audit log entries.  
**Filters:** User, action, entity type, date range.  

### A-011: Fairness Check Dashboard

**Type:** Dashboard  
**Source:** gov_FairnessCheckResult  
**Description:** Status of latest fairness checks with pass/fail indicators.  

### A-012: Crime Head Distribution

**Type:** Chart  
**Source:** src_CaseMaster + src_CrimeHead  
**Description:** Pie/bar chart of case composition by major crime head.  

### A-013: Case Status Breakdown

**Type:** Chart  
**Source:** src_CaseMaster + src_CaseStatusMaster  
**Description:** Status distribution (Under Investigation, Charge Sheeted, Closed).  

### A-014: Vehicle Link Explorer (STRETCH)

**Type:** Interface  
**Source:** int_VehicleLink  
**Description:** Search by vehicle number to see linked cases.  

### A-015: MO Pattern Explorer (STRETCH)

**Type:** Interface  
**Source:** int_MoPattern + int_MoPatternLink  
**Description:** Browse and search modus operandi patterns.  
