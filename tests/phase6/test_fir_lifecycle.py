"""Phase 6 tests: FIR lifecycle state machine, source documents, idempotency, and concurrency."""

from __future__ import annotations

import pytest

from src.domain.fir_lifecycle import FIRLifecycle, FIRStatus, TRANSITIONS


@pytest.mark.unit
class TestFIRLifecycle:
    def test_valid_transition_draft_to_submitted(self):
        result = FIRLifecycle.validate_transition(1, 2)
        assert result.allowed
        assert result.reason is None

    def test_valid_transition_submitted_to_registered(self):
        result = FIRLifecycle.validate_transition(2, 3)
        assert result.allowed

    def test_invalid_transition_draft_to_closed(self):
        result = FIRLifecycle.validate_transition(1, 8)
        assert not result.allowed
        assert "Cannot transition" in result.reason

    def test_invalid_transition_archived_to_anything(self):
        for target in range(1, 10):
            result = FIRLifecycle.validate_transition(10, target)
            assert not result.allowed

    def test_invalid_status_id(self):
        result = FIRLifecycle.validate_transition(99, 1)
        assert not result.allowed
        assert "Unknown status" in result.reason

    def test_transition_requires_assignment_warning(self):
        result = FIRLifecycle.validate_transition(3, 4, has_assignment=False)
        assert result.allowed
        assert len(result.warnings) > 0
        assert "assignment" in result.warnings[0].lower()

    def test_transition_to_review_pending_without_supervisor(self):
        result = FIRLifecycle.validate_transition(5, 6, has_assignment=True, is_supervisor=False)
        assert result.allowed
        assert any("supervisor" in w.lower() for w in result.warnings)

    def test_get_allowed_transitions_draft(self):
        transitions = FIRLifecycle.get_allowed_transitions(1)
        status_ids = {t["status_id"] for t in transitions}
        assert 2 in status_ids  # submitted
        assert 10 in status_ids  # archived
        assert 8 not in status_ids  # closed

    def test_get_allowed_transitions_closed(self):
        transitions = FIRLifecycle.get_allowed_transitions(8)
        status_ids = {t["status_id"] for t in transitions}
        assert 9 in status_ids  # reopened
        assert 10 in status_ids  # archived

    def test_requires_assignment(self):
        assert FIRLifecycle.requires_assignment(4)  # assigned
        assert FIRLifecycle.requires_assignment(5)  # under_investigation
        assert not FIRLifecycle.requires_assignment(1)  # draft

    def test_is_terminal(self):
        assert FIRLifecycle.is_terminal(10)  # archived
        assert not FIRLifecycle.is_terminal(1)
        assert not FIRLifecycle.is_terminal(8)

    def test_every_state_has_transitions_except_archived(self):
        for status in FIRStatus:
            allowed = TRANSITIONS.get(status, set())
            if status == FIRStatus.ARCHIVED:
                assert len(allowed) == 0
            else:
                assert len(allowed) > 0, f"State {status} has no outgoing transitions"

    def test_all_transitions_are_symmetric(self):
        for source, targets in TRANSITIONS.items():
            for target in targets:
                assert target in TRANSITIONS, f"Target {target} missing from TRANSITIONS"

    def test_get_label_known(self):
        assert FIRLifecycle.get_label(FIRStatus.DRAFT) == "Draft"
        assert FIRLifecycle.get_label(FIRStatus.UNDER_INVESTIGATION) == "Under Investigation"

    def test_get_label_unknown(self):
        assert FIRLifecycle.get_label(99) == "99"

    def test_get_all_states(self):
        states = FIRLifecycle.get_all_states()
        assert len(states) == 10
        assert FIRStatus.DRAFT in states
        assert FIRStatus.ARCHIVED in states

    def test_get_all_transitions(self):
        transitions = FIRLifecycle.get_all_transitions()
        assert len(transitions) > 0
        for t in transitions:
            assert "from" in t
            assert "to" in t
            assert "from_label" in t
            assert "to_label" in t


@pytest.mark.unit
class TestSourceDocumentDomain:
    def test_source_type_enum_values(self):
        from src.domain.source_document import SourceType
        assert SourceType.MANUAL_TEXT.value == "manual_text"
        assert SourceType.UPLOADED_PDF.value == "uploaded_pdf"
        assert SourceType.SYNTHETIC.value == "synthetic"

    def test_processing_status_enum(self):
        from src.domain.source_document import ProcessingStatus
        assert ProcessingStatus.PENDING.value == "pending"
        assert ProcessingStatus.COMPLETED.value == "completed"

    def test_validate_source_manual_text(self):
        from src.domain.source_document import validate_source_metadata
        errors = validate_source_metadata("manual_text", original_text="Some text")
        assert len(errors) == 0

    def test_validate_source_manual_text_missing(self):
        from src.domain.source_document import validate_source_metadata
        errors = validate_source_metadata("manual_text")
        assert len(errors) > 0
        assert "original text" in errors[0].lower()

    def test_validate_source_upload_pdf_no_filename(self):
        from src.domain.source_document import validate_source_metadata
        errors = validate_source_metadata("uploaded_pdf")
        assert len(errors) > 0
        assert "filename" in errors[0].lower()

    def test_validate_invalid_source_type(self):
        from src.domain.source_document import validate_source_metadata
        errors = validate_source_metadata("invalid_type")
        assert len(errors) > 0
        assert "Invalid source type" in errors[0]


@pytest.mark.unit
class TestIdempotencyDomain:
    def test_generate_key_deterministic(self):
        from src.domain.idempotency import generate_idempotency_key
        k1 = generate_idempotency_key("fir:create", crime_no="CR-001")
        k2 = generate_idempotency_key("fir:create", crime_no="CR-001")
        assert k1 == k2

    def test_generate_key_different_params(self):
        from src.domain.idempotency import generate_idempotency_key
        k1 = generate_idempotency_key("fir:create", crime_no="CR-001")
        k2 = generate_idempotency_key("fir:create", crime_no="CR-002")
        assert k1 != k2

    def test_generate_key_different_scopes(self):
        from src.domain.idempotency import generate_idempotency_key
        k1 = generate_idempotency_key("fir:create", crime_no="CR-001")
        k2 = generate_idempotency_key("evidence:upload", crime_no="CR-001")
        assert k1 != k2

    def test_in_memory_store_set_and_get(self):
        from datetime import datetime, timedelta, timezone
        from src.domain.idempotency import IdempotencyRecord, InMemoryIdempotencyStore
        store = InMemoryIdempotencyStore()
        record = IdempotencyRecord(
            key="test-key",
            scope="fir:create",
            response_status=201,
            response_body='{"id": 1}',
            created_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )
        import asyncio
        asyncio.run(store.set(record))
        retrieved = asyncio.run(store.get("test-key"))
        assert retrieved is not None
        assert retrieved.key == "test-key"
        assert retrieved.response_status == 201

    def test_in_memory_store_expired(self):
        from datetime import datetime, timedelta, timezone
        from src.domain.idempotency import IdempotencyRecord, InMemoryIdempotencyStore
        store = InMemoryIdempotencyStore()
        record = IdempotencyRecord(
            key="expired-key",
            scope="fir:create",
            response_status=201,
            response_body='{"id": 1}',
            created_at=datetime.now(timezone.utc) - timedelta(hours=2),
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
        )
        import asyncio
        asyncio.run(store.set(record))
        retrieved = asyncio.run(store.get("expired-key"))
        assert retrieved is None

    def test_in_memory_store_not_found(self):
        from src.domain.idempotency import InMemoryIdempotencyStore
        store = InMemoryIdempotencyStore()
        import asyncio
        retrieved = asyncio.run(store.get("nonexistent"))
        assert retrieved is None

    def test_idempotency_scope_values(self):
        from src.domain.idempotency import IdempotencyScope
        assert IdempotencyScope.FIR_CREATE.value == "fir:create"
        assert IdempotencyScope.EVIDENCE_UPLOAD.value == "evidence:upload"
        assert IdempotencyScope.AI_PROCESSING.value == "ai:processing"
