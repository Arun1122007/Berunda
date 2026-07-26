# Phase 4 Defect Register

| Defect ID | Severity | Dataset | Description | Required Correction | Status |
|-----------|----------|---------|-------------|---------------------|--------|
| `P4D-CRT-001` | ERROR | All in `data/synthetic` | The generated synthetic databases lacked an explicit `synthetic` boolean column. | Run a clean script to append the column. | **CLOSED** |
| `P4D-MAJ-001` | ERROR | `data/evaluation` | Project completely lacked the JSONL datasets required for testing prompt logic and parsing for the AI extraction pipeline. | Generate `fir-extraction-evaluation.jsonl`. | **CLOSED** |
| `P4D-MAJ-002` | ERROR | `data/schemas` | Catalyst Data Store schemas were missing for validation. | Generate `CaseMaster.json`. | **CLOSED** |
