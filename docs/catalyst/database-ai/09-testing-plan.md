# 09 Testing Plan

## Overview
This document outlines the testing strategy for the Berunda backend, particularly focusing on how to test the dual-repository architecture (SQLite + Catalyst Data Store) and the mocked AI features.

## 1. Unit Tests (Local SQLite)
- **Framework:** `pytest` and `pytest-asyncio`
- **Strategy:** All core application logic (e.g. `fir_service`, `fairness_service`) is tested locally using `SQLiteFIRRepository`. This ensures rapid test execution without network latency.
- **Coverage Goal:** 85% for `src/services/` and `src/routers/`.

## 2. Integration Tests (Catalyst Data Store Mocking)
- **Framework:** `pytest-mock`
- **Strategy:** To test `CatalystFIRRepository` locally, we use `unittest.mock.patch` to mock the `zcatalyst_sdk` responses.
- **Data Validation:** Tests assert that the repository builds the correct ZCQL query strings (e.g., verifying that `WHERE PoliceStationID = 12` is correctly appended).

## 3. End-to-End Tests (Staging Environment)
- **Framework:** `Playwright` and Python `requests`.
- **Strategy:** Post-deployment to Catalyst Staging, automated scripts insert a synthetic FIR, verify it appears on the dashboard, upload a mock PDF, and verify QuickML OCR/Summarization runs.

## 4. AI Feature Testing
- **Strategy:** External QuickML and Zia API calls are heavily cached during CI testing using VCR.py to prevent flaky tests due to LLM latency or network timeouts. Faithfulness and structure compliance are tested using deterministic datasets.
