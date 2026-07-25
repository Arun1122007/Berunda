# Performance Baseline Report

**Project:** Berunda — AI-Native Crime Intelligence Platform
**Date:** {{DATE}}
**Run ID:** {{RUN_ID}}

---

## Summary

| Category | Passed | Failed | Skipped | Status |
|----------|--------|--------|---------|--------|
| N+1 Query Detection | {{NPLUS_PASSED}} | {{NPLUS_FAILED}} | {{NPLUS_SKIPPED}} | {{NPLUS_STATUS}} |
| Index Usage | {{INDEXES_PASSED}} | {{INDEXES_FAILED}} | {{INDEXES_SKIPPED}} | {{INDEXES_STATUS}} |
| Bundle Size | {{BUNDLE_PASSED}} | {{BUNDLE_FAILED}} | {{BUNDLE_SKIPPED}} | {{BUNDLE_STATUS}} |
| **Overall** | **{{TOTAL_PASSED}}** | **{{TOTAL_FAILED}}** | **{{TOTAL_SKIPPED}}** | **{{OVERALL_STATUS}}** |

---

## N+1 Query Detection

| Module | Possible N+1 | Detail |
|--------|-------------|--------|
{{NPLUS_DETAILS}}

## Index Usage

| Table | Indexes Found | Missing |
|-------|---------------|---------|
{{INDEXES_DETAILS}}

## Bundle Size

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
{{BUNDLE_DETAILS}}

---

## Baseline Values

| Metric | Value | Previous Baseline | Delta |
|--------|-------|-------------------|-------|
{{BASELINE_VALUES}}

---

## Recommendations

{{RECOMMENDATIONS}}

---

## Trend

{{TREND_CHART}}
