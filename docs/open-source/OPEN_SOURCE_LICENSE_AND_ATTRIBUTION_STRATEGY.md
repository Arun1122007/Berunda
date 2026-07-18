# Open Source License and Attribution Strategy

[//]: # (Document ID: BERUNDA-OSS-001 | Version: 1.0 | Status: DRAFT | Classification: PUBLIC | Owner: Berunda Team | Audience: General / Public | Source: Standard templates + OSS best practices | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Recommended License

**MIT License** — recommended for Project Berunda.

Rationale:
- Permissive — allows reuse by Karnataka Police or any government agency without restriction
- Simple — one-page, widely understood
- Compatible with Catalyst deployment (no copyleft obligations)

## 2. Dependency Attributions

| Dependency | License | Usage |
|------------|---------|-------|
| spaCy | MIT | NER extraction |
| NetworkX | BSD-3-Clause | Graph algorithms |
| scikit-learn | BSD-3-Clause | Risk scoring (fallback) |
| Faker | MIT | Synthetic data generation |
| indic-faker | MIT | Kannada name generation (STRETCH) |
| React | MIT | Frontend framework |
| Cytoscape.js | LGPL-2.1 | Graph visualization |
| MapLibre GL | BSD-3-Clause | Geospatial map |
| Recharts | MIT | Analytics charts |
| pytest | MIT | Testing framework |
| Playwright | Apache-2.0 | E2E testing |

## 3. Third-Party Data Attribution

| Data | Source | License | Usage |
|------|--------|---------|-------|
| FIR ER Diagram schema | Karnataka Police (provided by datathon) | Datathon use only | Schema reference |
| Crime distribution statistics | NCRB 2022 Karnataka report | Govt. publication — fair use | Synthetic data distribution reference |
| OpenStreetMap data | OpenStreetMap contributors | ODbL | Geospatial enrichment (STRETCH) |

## 4. License File (MIT)

```text
MIT License

Copyright (c) 2026 Project Berunda Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
