# Contract Mismatches — Phase 2 Integration Audit

**Document ID:** BERUNDA-CONTRACT-MISMATCH-001 | **Version:** 1.0 | **Status:** FINAL
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-25

---

## Mismatch 1: Error Response Missing `requestId`

- **Frontend expectation:** The frontend-backend contract (`docs/contracts/frontend-backend-contract.md`) and error contract (`docs/contracts/error-contract.md`) specify an error response shape of `{"error": {"code": "...", "message": "...", "detail": {...}, "requestId": "..."}}`. The frontend `ApiClient` also captures `correlationId` and expects it in error responses.

- **Backend behavior:** The global exception handler in `src/main.py:288-293` returns `{"error": {"code": "...", "message": "...", "detail": ...}}`. The `requestId` (correlation ID) is set on `request.state.correlation_id` by the `CorrelationIDMiddleware` but is **never injected into the error response body**. The correlation ID is only available as a response header (`X-Request-ID`) but not in the JSON error body.

- **Contract definition:** `docs/contracts/error-contract.md` line 18: `"requestId": "550e8400-e29b-41d4-a716-446655440000"` is a required field in every error response.

- **Resolution:** Update `src/main.py` global exception handler to include `requestId` from `request.state.correlation_id` in the error response body:
  ```python
  content = {
      "error": {
          "code": code,
          "message": message,
          **({"detail": detail} if detail else {}),
          "requestId": cid,
      }
  }
  ```

---

## Mismatch 2: Error Response Wrapping — `detail` vs Direct `error` Payload

- **Frontend expectation:** The `api-client.ts` line 47 parses `error.message` from the response body. The contract shows `{"error": {"code": "...", "message": "...", "detail": {...}}}`. The frontend throws `ApiError` with `error.message` as the message.

- **Backend behavior:** The global exception handler wraps errors in `{"error": {...}}`. However, FastAPI's default 422 validation errors from Pydantic return a FastAPI-standard `{"detail": [...]}` array, **not** the `{"error": {...}}` format. This means validation errors (422) from Pydantic schema validation have a different shape than business-logic errors.

- **Contract definition:** `docs/contracts/error-contract.md` defines a single unified error format `{"error": {"code": "...", "message": "...", "detail": {...}, "requestId": "..."}}` for all error responses.

- **Resolution:** Add a custom validation exception handler in `src/main.py` to convert Pydantic `RequestValidationError` into the unified `{"error": {...}}` format:
  ```python
  from fastapi.exceptions import RequestValidationError
  @app.exception_handler(RequestValidationError)
  async def validation_exception_handler(request, exc):
      return JSONResponse(
          status_code=422,
          content={
              "error": {
                  "code": "VALIDATION_ERROR",
                  "message": "Input validation failed",
                  "detail": {"fields": exc.errors()},
                  "requestId": getattr(request.state, "correlation_id", None),
              }
          },
      )
  ```

---

## Mismatch 3: Pagination Field Names — `page_size` vs `pageSize`

- **Frontend expectation:** The frontend `CaseListResponse` type (`apps/web/src/types/api.ts` line 40) defines the pagination field as `pageSize` (camelCase).

- **Backend behavior:** The backend `FIRListResponse` schema (`src/schemas/fir.py` line 59) defines the field as `page_size` (snake_case). Due to the `APIBase` alias generator in `src/schemas/base.py`, this is correctly serialized as `pageSize` via the `_camelize` function. **No actual mismatch at runtime**, but the source-of-truth schemas use different naming conventions.

- **Contract definition:** `docs/contracts/api-contracts.md` section "Pagination Rules" specifies the response includes `items`, `total`, `page`, `page_size`. The contract uses `snake_case` but the frontend expects `camelCase`.

- **Resolution:** This is **resolved at runtime** by Pydantic's alias generator. No code change needed. Recommend updating `docs/contracts/api-contracts.md` to document the wire format as `camelCase`, noting that the backend schemas use `snake_case` internally.

---

## Mismatch 4: `CR-2026-0421` Case Response Type vs Backend

- **Frontend expectation:** `CaseDetail` in `apps/web/src/types/api.ts` lines 43-48 defines `actSections` as `Record<string, unknown>[]` (key-value objects).

- **Backend behavior:** `FIRDetailResponse` in `src/schemas/fir.py` returns `act_sections` as `list[ActSectionResponse]` where each item is a strongly typed Pydantic model with fields `CaseMasterID`, `ActID`, `SectionID`, `ActOrderID`, `SectionOrderID`.

- **Contract definition:** Not explicitly defined in contract docs.

- **Resolution:** Update `CaseDetail.actSections` to a properly typed interface:
  ```typescript
  interface ActSection {
    caseMasterId: number;
    actId: string;
    sectionId: string;
    actOrderId?: number;
    sectionOrderId?: number;
  }
  ```
  Similarly type `ComplainantResponse`, `VictimResponse`, `AccusedResponse` instead of using `Record<string, unknown>[]`.

---

## Mismatch 5: District ID in Registration

- **Frontend expectation:** The registration form may send `districtId` with user registration (as confirmed by `RegisterRequest` having `district_id: int | None`).

- **Backend behavior:** `AuthService.register()` stores `DistrictID` on the User model, which has a FK constraint to `src_District.DistrictID`. If no District exists with the given ID, registration fails with a database integrity error (500) instead of a user-friendly 400/422.

- **Contract definition:** `src/schemas/auth.py:RegisterRequest` lists `district_id` as optional `int | None`.

- **Resolution:** Add validation in `AuthService.register()` to check that the `district_id` references an existing district before attempting insert. Return a proper `ValidationError` (422) or `NotFoundError` (404) if the district doesn't exist.

---

## Mismatch 6: Missing `Case` Status/Domain Type Alignment

- **Frontend expectation:** `domain.ts` defines `CaseMaster` with fields like `caseId`, `firNumber`, `districtId`, `policeStationId`, `crimeTypeId`, `status: CaseStatus` (enum of 7 statuses), `sections: string[]`.

- **Backend behavior:** The backend `FIRResponse` schema uses numeric IDs (`CaseMasterID`, `PoliceStationID`), snake_case fields, and `CaseStatusID` is an integer FK, not a string enum. No section string array is returned at the list level (only at detail level via `ActSectionAssociation`).

- **Contract definition:** Not formally aligned — the `domain.ts` types appear to be aspirational/legacy.

- **Resolution:** Either update `domain.ts` to match the actual API responses, or create a domain mapping layer in the frontend. Deferred to Phase 3.

---

## Mismatch 7: `GET /api/v1/auth/me` Behavior Without Auth

- **Frontend expectation:** The frontend `auth.ts` service calls `getCurrentUser()` which makes a GET to `/auth/me`. If the user is not authenticated, it expects the call to fail and returns `null`.

- **Backend behavior:** The `get_current_user` dependency returns `{"user_id": None, "role": "anonymous"}` when no credentials are provided (see `src/middleware/auth.py:69-73`). The `/me` handler then returns a `UserResponse` with `userId=0`, `email=""`, `role="anonymous"`. It never returns 401.

- **Contract definition:** `docs/contracts/frontend-backend-contract.md` section "Auth Token Flow" step 5 mentions "On 401 → attempt refresh", suggesting `/me` should return 401 when unauthenticated.

- **Resolution:** Change the `/me` endpoint to require authentication by using `require_role()` or `get_current_user` with `auto_error=True`, or alternatively use `Depends(HTTPBearer())` directly so that missing credentials result in a 401.

---

*Phase 2 Integration Contract Audit — Generated 2026-07-25*
