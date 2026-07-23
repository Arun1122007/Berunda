from __future__ import annotations

from src.models import (
    Act,
    AuditLog,
    Base,
    CaseMaster,
    PersonEntity,
    RelationshipEdge,
    Section,
)


class TestModelDefinitions:
    def test_base_metadata_present(self):
        assert hasattr(Base, "metadata")

    def test_case_master_has_expected_columns(self):
        cols = [c.name for c in CaseMaster.__table__.columns]
        assert "CaseMasterID" in cols
        assert "CrimeNo" in cols
        assert "CaseNo" in cols
        assert "PoliceStationID" in cols

    def test_person_entity_has_expected_columns(self):
        cols = [c.name for c in PersonEntity.__table__.columns]
        assert "PersonEntityID" in cols
        assert "CanonicalName" in cols
        assert "PrimaryDistrictID" in cols

    def test_relationship_edge_has_expected_columns(self):
        cols = [c.name for c in RelationshipEdge.__table__.columns]
        assert "RelationshipEdgeID" in cols
        assert "PersonEntityA" in cols
        assert "PersonEntityB" in cols
        assert "RelationshipType" in cols

    def test_audit_log_has_expected_columns(self):
        cols = [c.name for c in AuditLog.__table__.columns]
        assert "AuditLogID" in cols
        assert "Action" in cols
        assert "EntityType" in cols
        assert "Timestamp" in cols

    def test_act_primary_key(self):
        pk = [c.name for c in Act.__table__.primary_key.columns]
        assert "ActCode" in pk

    def test_section_composite_key(self):
        pk = [c.name for c in Section.__table__.primary_key.columns]
        assert "ActCode" in pk
        assert "SectionCode" in pk

    def test_total_model_count(self):
        from src.models import __all__ as all_models

        assert len(all_models) >= 30
