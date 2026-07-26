"""Database validation — migrations, constraints, indexes, seed data, sensitive data."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


async def check_clean_migration(db_session: Any = None) -> dict[str, Any]:
    """Fresh database -> run all migrations -> verify table existence."""
    expected_tables = {
        "src_Act", "src_Section", "src_CrimeHead", "src_CrimeSubHead",
        "src_CrimeHeadActSection", "src_CaseCategory", "src_GravityOffence",
        "src_CaseStatusMaster", "src_Court", "src_State", "src_District",
        "src_Unit", "src_UnitType", "src_Rank", "src_Designation",
        "src_Employee", "src_OccupationMaster", "src_CasteMaster",
        "src_ReligionMaster", "src_CaseMaster", "src_Inv_OccuranceTime",
        "src_ComplainantDetails", "src_Victim", "src_Accused",
        "src_ArrestSurrender", "src_ActSectionAssociation",
        "src_ChargesheetDetails", "int_PersonEntity", "int_PersonEntityLink",
        "int_RelationshipEdge", "int_VehicleLink", "int_RiskScore",
        "int_RiskScoreFeatureImportance", "int_MoPattern", "int_MoPatternLink",
        "int_AnomalyAlert", "int_HotspotLayer", "int_RAGCorpusChunk",
        "gov_AuditLog", "gov_FairnessCheckResult", "gov_DataProvenanceRecord",
        "auth_User", "auth_Session", "auth_Permission",
        "ai_AIUsageRecord", "ai_PromptVersion", "ai_AIConversation",
        "ai_AIMessage", "ai_AIFeedback",
    }
    if db_session is None:
        return {"passed": True, "details": "no db session, skipping migration check"}

    try:
        from sqlalchemy import inspect as sa_inspect

        async with db_session() as session:
            conn = await session.connection()
            inspector = await conn.run_sync(sa_inspect)
            existing = set(await conn.run_sync(inspector.get_table_names))
            missing = expected_tables - existing
            return {
                "passed": len(missing) == 0,
                "expected": len(expected_tables),
                "existing": len(existing),
                "missing": sorted(missing),
            }
    except Exception as exc:
        return {"passed": False, "details": str(exc)}


async def check_constraints(db_session: Any = None) -> dict[str, Any]:
    """Verify FK, unique, and NOT NULL constraints are in place."""
    if db_session is None:
        return {"passed": True, "details": "no db session, skipping"}

    expected_fks = {
        "src_Section": ["ActCode"],
        "src_District": ["StateID"],
        "src_CaseMaster": ["PoliceStationID", "CaseCategoryID", "GravityOffenceID", "CaseStatusID"],
        "src_ComplainantDetails": ["CaseMasterID"],
        "src_Accused": ["CaseMasterID"],
        "src_Victim": ["CaseMasterID"],
        "src_Inv_OccuranceTime": ["CaseMasterID"],
    }
    try:
        from sqlalchemy import inspect as sa_inspect

        async with db_session() as session:
            conn = await session.connection()
            inspector = await conn.run_sync(sa_inspect)
            issues = []
            for table, expected_cols in expected_fks.items():
                fks = await conn.run_sync(inspector.get_foreign_keys, table)
                fk_cols = {col for fk in fks for col in fk["constrained_columns"]}
                for col in expected_cols:
                    if col not in fk_cols:
                        issues.append(f"{table}.{col} missing FK")
            return {"passed": len(issues) == 0, "issues": issues}
    except Exception as exc:
        return {"passed": False, "details": str(exc)}


async def check_indexes(db_session: Any = None) -> dict[str, Any]:
    """Verify expected indexes exist."""
    if db_session is None:
        return {"passed": True, "details": "no db session, skipping"}

    expected_indexes = {
        "ix_case_crimeno", "ix_case_regdate", "ix_case_station",
        "ix_case_majorhead", "ix_case_status", "ix_case_station_date",
        "ix_accused_case", "ix_victim_case", "ix_comp_case",
        "ix_arrest_case", "ix_cs_case",
        "ix_pelink_pentity", "ix_pelink_case",
        "ix_reledge_a", "ix_reledge_b", "ix_reledge_case",
        "ix_vlink_case", "ix_vlink_number",
        "ix_audit_user", "ix_audit_timestamp", "ix_audit_entity",
    }
    try:
        from sqlalchemy import inspect as sa_inspect

        async with db_session() as session:
            conn = await session.connection()
            inspector = await conn.run_sync(sa_inspect)
            existing = set()
            for table_name in await conn.run_sync(inspector.get_table_names):
                indexes = await conn.run_sync(inspector.get_indexes, table_name)
                for idx in indexes:
                    existing.add(idx["name"])
            missing = expected_indexes - existing
            return {
                "passed": len(missing) == 0,
                "missing": sorted(missing),
                "existing_count": len(existing),
            }
    except Exception as exc:
        return {"passed": False, "details": str(exc)}


async def check_seed_data(db_session: Any = None) -> dict[str, Any]:
    """Verify seed data count and shape."""
    if db_session is None:
        return {"passed": True, "details": "no db session, skipping"}

    expected_counts = {
        "src_State": 1,
        "src_District": 31,
        "src_Act": 4,
        "src_CrimeHead": 20,
        "src_CaseMaster": 24,
    }
    try:
        import sqlalchemy as sa

        async with db_session() as session:
            issues = []
            for table, expected in expected_counts.items():
                result = await session.execute(sa.text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                if count != expected:
                    issues.append(f"{table}: expected {expected}, got {count}")
            return {"passed": len(issues) == 0, "issues": issues}
    except Exception as exc:
        return {"passed": False, "details": str(exc)}


async def check_reset(db_session: Any = None) -> dict[str, Any]:
    """Verify drop and recreate works."""
    if db_session is None:
        return {"passed": True, "details": "no db session, skipping"}
    try:
        from sqlalchemy import inspect as sa_inspect

        from src.models.base import Base

        async with db_session() as session:
            conn = await session.connection()
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            inspector = await conn.run_sync(sa_inspect)
            tables = await conn.run_sync(inspector.get_table_names)
            return {
                "passed": len(tables) > 0,
                "table_count": len(tables),
            }
    except Exception as exc:
        return {"passed": False, "details": str(exc)}


async def check_sensitive_data(db_session: Any = None) -> dict[str, Any]:
    """Verify no PII in seed data — synthetic markers only."""
    if db_session is None:
        return {"passed": True, "details": "no db session, skipping"}
    pii_patterns = [
        "aadhaar", "aadhar", "pan card", "passport", "bank account",
        "credit card", "upi", " biometric",
    ]
    try:
        import sqlalchemy as sa

        async with db_session() as session:
            tables_with_text = [
                "src_ComplainantDetails", "src_Accused", "src_Victim",
                "src_Inv_OccuranceTime", "int_PersonEntity",
            ]
            issues = []
            for table in tables_with_text:
                result = await session.execute(sa.text(f"SELECT * FROM {table} LIMIT 50"))
                rows = result.all()
                for row in rows:
                    for col in row._fields:
                        val = str(getattr(row, col, "")).lower()
                        for pat in pii_patterns:
                            if pat in val:
                                issues.append(f"{table}.{col} contains potential PII: '{pat}'")
                                break
            return {"passed": len(issues) == 0, "issues": issues}
    except Exception as exc:
        return {"passed": False, "details": str(exc)}
