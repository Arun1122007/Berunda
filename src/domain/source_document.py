"""FIR Source Document Preservation — original source text/PDF is never overwritten."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class SourceType(str, Enum):
    MANUAL_TEXT = "manual_text"
    UPLOADED_PDF = "uploaded_pdf"
    UPLOADED_DOC = "uploaded_doc"
    SYNTHETIC = "synthetic"
    IMPORTED = "imported"


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class FIRSource:
    source_id: int | None = None
    case_master_id: int | None = None
    source_type: SourceType = SourceType.MANUAL_TEXT
    original_text: str | None = None
    storage_object_ref: str | None = None
    original_filename: str | None = None
    display_filename: str | None = None
    content_type: str | None = None
    file_size: int | None = None
    checksum: str | None = None
    uploaded_by_user_id: int | None = None
    uploaded_at: datetime | None = None
    processing_status: ProcessingStatus = ProcessingStatus.PENDING
    is_synthetic: bool = False
    source_version: int = 1

    def to_dict(self) -> dict:
        return {
            "source_id": self.source_id,
            "case_master_id": self.case_master_id,
            "source_type": self.source_type.value,
            "original_text": self.original_text,
            "storage_object_ref": self.storage_object_ref,
            "original_filename": self.original_filename,
            "display_filename": self.display_filename,
            "content_type": self.content_type,
            "file_size": self.file_size,
            "checksum": self.checksum,
            "uploaded_by_user_id": self.uploaded_by_user_id,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
            "processing_status": self.processing_status.value,
            "is_synthetic": self.is_synthetic,
            "source_version": self.source_version,
        }


def validate_source_metadata(
    source_type: str,
    original_text: str | None = None,
    filename: str | None = None,
    content_type: str | None = None,
    file_size: int | None = None,
) -> list[str]:
    errors: list[str] = []

    if source_type not in [t.value for t in SourceType]:
        errors.append(f"Invalid source type: {source_type}")

    if source_type in ("uploaded_pdf", "uploaded_doc") and not filename:
        errors.append("Filename is required for uploaded documents")

    if source_type == "manual_text" and not original_text:
        errors.append("Original text is required for manual entries")

    if file_size is not None and file_size > 50 * 1024 * 1024:
        errors.append("File size exceeds maximum of 50 MB")

    return errors
