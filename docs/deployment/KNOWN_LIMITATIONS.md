# Project Berunda — Known Limitations & Feature Status

> **Document ID:** BERUNDA-DEP-011 | **Version:** 1.0  

---

## 1. Environment Limitations

| Feature / Subsystem | Status | Behavior on Catalyst Cloud |
| :--- | :---: | :--- |
| **Core FIR Management** | ✅ Active | Fully operational with 40,823 synthetic cases |
| **Entity Resolution & Link Graph** | ✅ Active | Operational with NetworkX in-process graph analysis |
| **Hotspot Map & Risk Matrix** | ✅ Active | Spatial clustering and risk scoring operational |
| **Celery / Redis Queue** | ⚠️ Fallback | Gracefully degrades to synchronous task execution (no Redis on Catalyst) |
| **Neo4j Graph Database** | ℹ️ Optional | Falls back to in-memory NetworkX graph when Neo4j is unconfigured |
| **Heavy ML Models (spaCy / Presidio)** | ℹ️ Optional | Replaced with pure-Python regex and rule-based extractors for AppSail compatibility |
