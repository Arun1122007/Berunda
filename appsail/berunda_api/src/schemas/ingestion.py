from __future__ import annotations

from typing import Any

from src.schemas.base import APIBase


class IngestionPreviewRequest(APIBase):
    file_name: str
    file_type: str
    rows: list[dict[str, Any]]
    dry_run: bool = True


class IngestionRowDiagnostic(APIBase):
    row_index: int
    status: str  # "valid", "warning", "error"
    messages: list[str] = []


class IngestionPreviewResponse(APIBase):
    file_name: str
    total_rows: int
    valid_rows: int
    warning_rows: int
    error_rows: int
    diagnostics: list[IngestionRowDiagnostic] = []
    ready_for_commit: bool = True


class IngestionCommitRequest(APIBase):
    file_name: str
    rows: list[dict[str, Any]]
    target_table: str = "case_master"
