# Functional Validation Report

**Project:** Berunda — AI-Native Crime Intelligence Platform
**Date:** {{DATE}}
**Run ID:** {{RUN_ID}}

---

## Summary

| Category | Passed | Failed | Skipped | Status |
|----------|--------|--------|---------|--------|
| Acceptance Criteria | {{AC_PASSED}} | {{AC_FAILED}} | {{AC_SKIPPED}} | {{AC_STATUS}} |
| Main User Journey | {{JOURNEY_PASSED}} | {{JOURNEY_FAILED}} | {{JOURNEY_SKIPPED}} | {{JOURNEY_STATUS}} |
| Invalid Input (422) | {{INVALID_PASSED}} | {{INVALID_FAILED}} | {{INVALID_SKIPPED}} | {{INVALID_STATUS}} |
| Unauthorized (401) | {{UNAUTH_PASSED}} | {{UNAUTH_FAILED}} | {{UNAUTH_SKIPPED}} | {{UNAUTH_STATUS}} |
| Forbidden (403) | {{FORBIDDEN_PASSED}} | {{FORBIDDEN_FAILED}} | {{FORBIDDEN_SKIPPED}} | {{FORBIDDEN_STATUS}} |
| Not Found (404) | {{NOTFOUND_PASSED}} | {{NOTFOUND_FAILED}} | {{NOTFOUND_SKIPPED}} | {{NOTFOUND_STATUS}} |
| **Overall** | **{{TOTAL_PASSED}}** | **{{TOTAL_FAILED}}** | **{{TOTAL_SKIPPED}}** | **{{OVERALL_STATUS}}** |

---

## Detail: Acceptance Criteria

| Check | Result | Detail |
|-------|--------|--------|
{{AC_DETAILS}}

## Detail: Main User Journey

| Step | Result | Detail |
|------|--------|--------|
{{JOURNEY_DETAILS}}

## Detail: Invalid Input Validation

| Test | Status | Detail |
|------|--------|--------|
{{INVALID_DETAILS}}

## Detail: Unauthorized Access

| Endpoint | Status | Detail |
|----------|--------|--------|
{{UNAUTH_DETAILS}}

## Detail: Forbidden Access

| Endpoint | Status | Detail |
|----------|--------|--------|
{{FORBIDDEN_DETAILS}}

## Detail: Not Found

| Test | Path | Status |
|------|------|--------|
{{NOTFOUND_DETAILS}}

---

## Failed Item Details

{{FAILED_DETAILS}}

---

## Recommendations

{{RECOMMENDATIONS}}
