# Phase 3 Contract Consistency Report — Project Berunda

> **Document ID:** BERUNDA-VERIF3-CONTRACT-001 | **Version:** 1.0 | **Status:** FINAL  
> **Classification:** INTERNAL | **Owner:** Independent Verification Team  
> **Date:** 2026-07-26  

---

## 1. Executive Summary

This report evaluates the consistency of interface contracts across the Project Berunda stack, verifying alignment between database schemas, backend Pydantic models, OpenAPI specifications, and frontend TypeScript definitions.

### Consistency Verdict: PASS (with minor observations)
The core FIR lifecycle contracts, authentication payloads, and error envelopes demonstrate high consistency across boundaries. Frontend forms map accurately to backend Pydantic validators, and error responses adhere to a unified JSON schema.

---

## 2. API Contract Alignment (OpenAPI vs. FastAPI)

- **Reference Specification**: `docs/api/openapi.yaml`
- **Implementation**: `src/main.py` (`custom_openapi` function)
- **Evaluation**: 
  - `src/main.py` explicitly constructs an OpenAPI 3.1.0 schema that incorporates the exact tags, descriptions, contact information, and license metadata defined in the Phase 2 specification.
  - Endpoint path parameters (`/api/v1/fir/{id}`) and HTTP method verbs (`GET`, `POST`, `PUT`, `DELETE`) align 1-to-1 with the OpenAPI contract.
  - Authentication security schemes correctly declare JWT Bearer authorization (`Authorization: Bearer <token>`).

---

## 3. ORM Model vs. Pydantic Schema Consistency

- **Database Models**: `src/models/fir.py` (`CaseMaster`, `PersonEntity`, `InvOccuranceTime`)
- **Validation Schemas**: `src/schemas/fir.py` (`FIRCreate`, `FIRUpdate`, `FIRResponse`)
- **Evaluation**:
  - Field naming conventions use snake_case consistently across Python boundaries (`case_number`, `brief_facts`, `district_id`, `police_station_id`).
  - Required fields in `FIRCreate` (e.g., `brief_facts`, `district_id`) match non-nullable column definitions in the `CaseMaster` SQLAlchemy table.
  - Optional relationship lists (`complainants`, `victims`, `accused`) default to empty lists in Pydantic, matching ORM cascade relationship configurations.

---

## 4. Frontend TypeScript vs. Backend API Consistency

- **TypeScript Definitions**: `apps/web/src/types/` and local interfaces in `apps/web/src/features/cases/`.
- **Backend JSON Payload**: Returned via `FIRResponse.model_dump(mode="json")`.
- **Evaluation**:
  - React creation forms (`CreateCasePage.tsx`) construct payload objects matching `FIRCreate` property keys.
  - Status enums (`DRAFT`, `UNDER_INVESTIGATION`, `CHARGESHEETED`, `CLOSED`) match string literal types in TypeScript.
  - Date and time formatting strings use ISO 8601 strings across both frontend and backend boundaries.

---

## 5. Error Contract & Exception Handling

- **Specification Requirement**: Standardized error envelope without internal stack traces.
- **Backend Implementation**: `src/main.py` (`global_exception_handler`)
- **Contract Schema**:
  ```json
  {
    "error": {
      "code": "VALIDATION_ERROR | AUTH_ERROR | NOT_FOUND | INTERNAL_ERROR",
      "message": "Human readable string",
      "detail": { ...optional structured validation errors... }
    }
  }
  ```
- **Frontend Consumption**: `useApi` custom hooks parse the `.error.message` property to display user-facing alert notifications, ensuring a seamless error reporting UX.

---

## 6. Discrepancy & Observation Register

1. **Observation**: While local SQLite models use string representations for UUIDs (`String(36)`), production PostgreSQL/ZCQL schemas require native UUID column types. Pydantic handles this conversion transparently via `UUID4` type coercion.
2. **Observation**: The pagination envelope in `FIRListResponse` uses `items`, `total`, `page`, and `size`. Frontend list views correctly destructure these properties without structural mismatch.

---

## 7. Conclusion

No breaking contract incompatibilities or field naming mismatches were discovered between the frontend UI layer and the backend REST API.
