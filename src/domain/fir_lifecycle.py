"""FIR Lifecycle State Machine — explicit status transitions with validation.

States map to src_CaseStatusMaster entries:
  1=draft, 2=submitted, 3=registered, 4=assigned,
  5=under_investigation, 6=review_pending, 7=resolved,
  8=closed, 9=reopened, 10=archived
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum

from src.exceptions import ValidationError


class FIRStatus(IntEnum):
    DRAFT = 1
    SUBMITTED = 2
    REGISTERED = 3
    ASSIGNED = 4
    UNDER_INVESTIGATION = 5
    REVIEW_PENDING = 6
    RESOLVED = 7
    CLOSED = 8
    REOPENED = 9
    ARCHIVED = 10


TRANSITIONS: dict[FIRStatus, set[FIRStatus]] = {
    FIRStatus.DRAFT: {FIRStatus.SUBMITTED, FIRStatus.ARCHIVED},
    FIRStatus.SUBMITTED: {FIRStatus.REGISTERED, FIRStatus.DRAFT},
    FIRStatus.REGISTERED: {FIRStatus.ASSIGNED, FIRStatus.UNDER_INVESTIGATION, FIRStatus.ARCHIVED},
    FIRStatus.ASSIGNED: {FIRStatus.UNDER_INVESTIGATION, FIRStatus.REVIEW_PENDING, FIRStatus.REGISTERED},
    FIRStatus.UNDER_INVESTIGATION: {FIRStatus.REVIEW_PENDING, FIRStatus.ASSIGNED, FIRStatus.RESOLVED},
    FIRStatus.REVIEW_PENDING: {FIRStatus.UNDER_INVESTIGATION, FIRStatus.RESOLVED, FIRStatus.CLOSED},
    FIRStatus.RESOLVED: {FIRStatus.CLOSED, FIRStatus.REOPENED},
    FIRStatus.CLOSED: {FIRStatus.REOPENED, FIRStatus.ARCHIVED},
    FIRStatus.REOPENED: {FIRStatus.UNDER_INVESTIGATION, FIRStatus.CLOSED},
    FIRStatus.ARCHIVED: set(),
}

REQUIRES_ASSIGNMENT: set[FIRStatus] = {
    FIRStatus.ASSIGNED,
    FIRStatus.UNDER_INVESTIGATION,
    FIRStatus.REVIEW_PENDING,
}

REQUIRES_OFFICER: set[FIRStatus] = {
    FIRStatus.SUBMITTED,
    FIRStatus.REGISTERED,
    FIRStatus.ASSIGNED,
    FIRStatus.UNDER_INVESTIGATION,
    FIRStatus.REVIEW_PENDING,
    FIRStatus.RESOLVED,
}

STATUS_LABELS: dict[FIRStatus, str] = {
    FIRStatus.DRAFT: "Draft",
    FIRStatus.SUBMITTED: "Submitted",
    FIRStatus.REGISTERED: "Registered",
    FIRStatus.ASSIGNED: "Assigned",
    FIRStatus.UNDER_INVESTIGATION: "Under Investigation",
    FIRStatus.REVIEW_PENDING: "Review Pending",
    FIRStatus.RESOLVED: "Resolved",
    FIRStatus.CLOSED: "Closed",
    FIRStatus.REOPENED: "Reopened",
    FIRStatus.ARCHIVED: "Archived",
}


@dataclass
class TransitionResult:
    allowed: bool = False
    reason: str | None = None
    warnings: list[str] = field(default_factory=list)


class FIRLifecycle:
    @staticmethod
    def validate_transition(
        current_status_id: int,
        new_status_id: int,
        has_assignment: bool = False,
        is_supervisor: bool = False,
    ) -> TransitionResult:
        try:
            current = FIRStatus(current_status_id)
            target = FIRStatus(new_status_id)
        except ValueError:
            return TransitionResult(allowed=False, reason=f"Unknown status ID: {current_status_id} or {new_status_id}")

        allowed = TRANSITIONS.get(current, set())
        if target not in allowed:
            return TransitionResult(
                allowed=False,
                reason=f"Cannot transition from '{STATUS_LABELS.get(current, str(current))}' to '{STATUS_LABELS.get(target, str(target))}'",
            )

        warnings: list[str] = []

        if target in REQUIRES_ASSIGNMENT and not has_assignment:
            warnings.append("Target status requires an active assignment")

        if target == FIRStatus.REVIEW_PENDING and not is_supervisor:
            warnings.append("Review-pending status typically requires supervisor action")

        return TransitionResult(allowed=True, warnings=warnings)

    @staticmethod
    def get_allowed_transitions(status_id: int) -> list[dict]:
        try:
            current = FIRStatus(status_id)
        except ValueError:
            return []
        allowed = TRANSITIONS.get(current, set())
        return [
            {"status_id": s.value, "label": STATUS_LABELS[s]}
            for s in sorted(allowed, key=lambda x: x.value)
        ]

    @staticmethod
    def requires_assignment(status_id: int) -> bool:
        try:
            return FIRStatus(status_id) in REQUIRES_ASSIGNMENT
        except ValueError:
            return False

    @staticmethod
    def is_terminal(status_id: int) -> bool:
        try:
            return FIRStatus(status_id) == FIRStatus.ARCHIVED
        except ValueError:
            return False

    @staticmethod
    def get_label(status: FIRStatus) -> str:
        return STATUS_LABELS.get(status, str(status))

    @staticmethod
    def get_all_states() -> list[FIRStatus]:
        return list(FIRStatus)

    @staticmethod
    def get_all_transitions() -> list[dict]:
        result = []
        for source, targets in TRANSITIONS.items():
            for target in targets:
                result.append({
                    "from": source.value,
                    "from_label": STATUS_LABELS.get(source, str(source)),
                    "to": target.value,
                    "to_label": STATUS_LABELS.get(target, str(target)),
                })
        return result
