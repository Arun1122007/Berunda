"""Domain logic and invariants — FIR domain rules, validation, and business operations.

Layering: domain (no framework dependencies beyond Python stdlib)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


class DomainError(Exception):
    """Base domain error."""

    def __init__(self, message: str, code: str = "DOMAIN_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class InvalidCrimeNoError(DomainError):
    def __init__(self, crime_no: str) -> None:
        super().__init__(
            f"Invalid CrimeNo format: '{crime_no}'. Expected format: CR-YYYY-NNNN",
            code="INVALID_CRIME_NO",
        )


class InvalidDateRangeError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            "IncidentFromDate must be before IncidentToDate",
            code="INVALID_DATE_RANGE",
        )


class FutureIncidentDateError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            "Incident date cannot be in the future",
            code="FUTURE_INCIDENT_DATE",
        )


class MissingRequiredFieldError(DomainError):
    def __init__(self, field: str) -> None:
        super().__init__(
            f"Required field '{field}' is missing",
            code="MISSING_REQUIRED_FIELD",
        )


class BriefFactsTooLongError(DomainError):
    def __init__(self, length: int, max_length: int = 10000) -> None:
        super().__init__(
            f"BriefFacts exceeds maximum length: {length} > {max_length}",
            code="BRIEF_FACTS_TOO_LONG",
        )


class InvalidCoordinatesError(DomainError):
    def __init__(self, lat: float | None, lng: float | None) -> None:
        super().__init__(
            f"Invalid coordinates: lat={lat}, lng={lng}. "
            "Latitude must be between -90 and 90, longitude between -180 and 180.",
            code="INVALID_COORDINATES",
        )


@dataclass(frozen=True)
class CrimeNo:
    """Value object for CrimeNo — validated format CR-YYYY-NNNN."""

    prefix: str  # CR
    year: int
    sequence: int

    @classmethod
    def parse(cls, raw: str) -> CrimeNo:
        if not raw or not isinstance(raw, str):
            raise InvalidCrimeNoError(str(raw))
        parts = raw.split("-")
        if len(parts) != 3:
            raise InvalidCrimeNoError(raw)
        prefix = parts[0]
        if prefix != "CR":
            raise InvalidCrimeNoError(raw)
        try:
            year = int(parts[1])
        except ValueError:
            raise InvalidCrimeNoError(raw)
        try:
            sequence = int(parts[2])
        except ValueError:
            raise InvalidCrimeNoError(raw)
        if len(parts[1]) != 4 or year < 2000 or year > 2100:
            raise InvalidCrimeNoError(raw)
        return cls(prefix=prefix, year=year, sequence=sequence)

    def __str__(self) -> str:
        """Return formatted CrimeNo string."""
        return f"CR-{self.year:04d}-{self.sequence:04d}"


class FIRDomainService:
    """Domain service for FIR business rules and invariants."""

    MAX_BRIEF_FACTS_LENGTH = 10000

    @staticmethod
    def validate_crime_no(crime_no: str) -> CrimeNo:
        """Validate and parse CrimeNo format."""
        return CrimeNo.parse(crime_no)

    @staticmethod
    def validate_incident_dates(
        incident_from: datetime | None,
        incident_to: datetime | None,
    ) -> None:
        """Validate incident date range invariants."""
        if incident_from and incident_to and incident_from > incident_to:
            raise InvalidDateRangeError()

    @staticmethod
    def validate_future_date(incident_date: datetime | None) -> None:
        """Ensure incident date is not in the future."""
        if incident_date:
            now = datetime.now(timezone.utc)
            if incident_date > now:
                raise FutureIncidentDateError()

    @staticmethod
    def validate_required_fields(data: dict[str, Any], required: list[str]) -> None:
        """Validate that all required fields are present and non-null."""
        for field in required:
            if field not in data or data[field] is None or data[field] == "":
                raise MissingRequiredFieldError(field)

    @staticmethod
    def validate_brief_facts(brief_facts: str | None) -> None:
        """Validate BriefFacts length."""
        if brief_facts and len(brief_facts) > FIRDomainService.MAX_BRIEF_FACTS_LENGTH:
            raise BriefFactsTooLongError(len(brief_facts))

    @staticmethod
    def validate_coordinates(latitude: float | None, longitude: float | None) -> None:
        """Validate geographic coordinates."""
        if latitude is not None and (latitude < -90 or latitude > 90):
            raise InvalidCoordinatesError(latitude, longitude)
        if longitude is not None and (longitude < -180 or longitude > 180):
            raise InvalidCoordinatesError(latitude, longitude)

    @staticmethod
    def validate_fir_create_input(data: dict[str, Any]) -> None:
        """Run all validations for FIR creation."""
        FIRDomainService.validate_crime_no(data.get("CrimeNo", ""))
        FIRDomainService.validate_required_fields(data, ["CrimeNo"])
        FIRDomainService.validate_incident_dates(
            data.get("IncidentFromDate"),
            data.get("IncidentToDate"),
        )
        FIRDomainService.validate_brief_facts(data.get("BriefFacts"))
        FIRDomainService.validate_coordinates(
            data.get("Latitude"),
            data.get("Longitude"),
        )
