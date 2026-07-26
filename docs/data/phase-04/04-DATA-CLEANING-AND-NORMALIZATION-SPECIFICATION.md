# Data Cleaning and Normalization Specification

## 1. Overview
As part of Phase 4, the raw synthetic data must be sanitized to ensure Catalyst Data Store compatibility and absolute compliance with our privacy rules.

## 2. Implemented Rules
- **Rule 1 (Whitespace)**: All string/object columns are stripped of leading and trailing whitespace.
- **Rule 2 (Synthetic Marker)**: A strict boolean `synthetic` column must exist and evaluate to `true` for every row.

## 3. Data Flow
1. Generated in `scripts/data/generate_synthetic.py`
2. Processed by `scripts/data/clean_data.py` (Rule 1 & 2 applied)
3. Validated by `scripts/data/validate_schemas.py`
4. Output safely stored in `data/synthetic/`
