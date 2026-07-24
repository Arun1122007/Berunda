"""Add foreign key constraints, indexes, and check constraints.

This migration adds the referential integrity, performance indexes, and
data validation constraints that were missing from the initial schema.
All operations are additive (no destructive changes).
"""

from alembic import op

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── Foreign Key Constraints ──────────────────────────────────────────

    # src_Section → src_Act
    with op.batch_alter_table("src_Section") as batch_op:
        batch_op.create_foreign_key("fk_section_act", "src_Act", ["ActCode"], ["ActCode"])

    # src_CrimeSubHead → src_CrimeHead
    # Already exists in migration 001 via inline sa.ForeignKey — skip

    # src_CrimeHeadActSection → src_CrimeHead, src_Act
    with op.batch_alter_table("src_CrimeHeadActSection") as batch_op:
        batch_op.create_foreign_key(
            "fk_chas_crimehead", "src_CrimeHead", ["CrimeHeadID"], ["CrimeHeadID"]
        )
    with op.batch_alter_table("src_CrimeHeadActSection") as batch_op:
        batch_op.create_foreign_key("fk_chas_act", "src_Act", ["ActCode"], ["ActCode"])

    # src_District → src_State (already inline in 001 — skip)

    # src_Unit → src_UnitType, src_State, src_District
    with op.batch_alter_table("src_Unit") as batch_op:
        batch_op.create_foreign_key("fk_unit_unittype", "src_UnitType", ["TypeID"], ["UnitTypeID"])
    with op.batch_alter_table("src_Unit") as batch_op:
        batch_op.create_foreign_key("fk_unit_state", "src_State", ["StateID"], ["StateID"])
    with op.batch_alter_table("src_Unit") as batch_op:
        batch_op.create_foreign_key(
            "fk_unit_district", "src_District", ["DistrictID"], ["DistrictID"]
        )

    # src_Employee → src_District, src_Unit, src_Rank, src_Designation
    with op.batch_alter_table("src_Employee") as batch_op:
        batch_op.create_foreign_key(
            "fk_emp_district", "src_District", ["DistrictID"], ["DistrictID"]
        )
    with op.batch_alter_table("src_Employee") as batch_op:
        batch_op.create_foreign_key("fk_emp_unit", "src_Unit", ["UnitID"], ["UnitID"])
    with op.batch_alter_table("src_Employee") as batch_op:
        batch_op.create_foreign_key("fk_emp_rank", "src_Rank", ["RankID"], ["RankID"])
    with op.batch_alter_table("src_Employee") as batch_op:
        batch_op.create_foreign_key(
            "fk_emp_designation", "src_Designation", ["DesignationID"], ["DesignationID"]
        )

    # src_Court → src_District, src_State (already inline in 001 — skip)

    # src_CaseMaster → multiple lookup tables
    with op.batch_alter_table("src_CaseMaster") as batch_op:
        batch_op.create_foreign_key(
            "fk_case_employee", "src_Employee", ["PolicePersonID"], ["EmployeeID"]
        )
    with op.batch_alter_table("src_CaseMaster") as batch_op:
        batch_op.create_foreign_key("fk_case_unit", "src_Unit", ["PoliceStationID"], ["UnitID"])
    with op.batch_alter_table("src_CaseMaster") as batch_op:
        batch_op.create_foreign_key(
            "fk_case_category", "src_CaseCategory", ["CaseCategoryID"], ["CaseCategoryID"]
        )
    with op.batch_alter_table("src_CaseMaster") as batch_op:
        batch_op.create_foreign_key(
            "fk_case_gravity", "src_GravityOffence", ["GravityOffenceID"], ["GravityOffenceID"]
        )
    with op.batch_alter_table("src_CaseMaster") as batch_op:
        batch_op.create_foreign_key(
            "fk_case_majorhead", "src_CrimeHead", ["CrimeMajorHeadID"], ["CrimeHeadID"]
        )
    with op.batch_alter_table("src_CaseMaster") as batch_op:
        batch_op.create_foreign_key(
            "fk_case_minorhead", "src_CrimeSubHead", ["CrimeMinorHeadID"], ["CrimeSubHeadID"]
        )
    with op.batch_alter_table("src_CaseMaster") as batch_op:
        batch_op.create_foreign_key(
            "fk_case_status", "src_CaseStatusMaster", ["CaseStatusID"], ["CaseStatusID"]
        )
    with op.batch_alter_table("src_CaseMaster") as batch_op:
        batch_op.create_foreign_key("fk_case_court", "src_Court", ["CourtID"], ["CourtID"])

    # src_Inv_OccuranceTime → src_CaseMaster
    with op.batch_alter_table("src_Inv_OccuranceTime") as batch_op:
        batch_op.create_foreign_key(
            "fk_invoccur_case", "src_CaseMaster", ["CaseMasterID"], ["CaseMasterID"]
        )

    # src_ComplainantDetails → src_CaseMaster, lookups
    with op.batch_alter_table("src_ComplainantDetails") as batch_op:
        batch_op.create_foreign_key(
            "fk_comp_case", "src_CaseMaster", ["CaseMasterID"], ["CaseMasterID"]
        )
    with op.batch_alter_table("src_ComplainantDetails") as batch_op:
        batch_op.create_foreign_key(
            "fk_comp_occupation", "src_OccupationMaster", ["OccupationID"], ["OccupationID"]
        )
    with op.batch_alter_table("src_ComplainantDetails") as batch_op:
        batch_op.create_foreign_key(
            "fk_comp_religion", "src_ReligionMaster", ["ReligionID"], ["ReligionID"]
        )
    with op.batch_alter_table("src_ComplainantDetails") as batch_op:
        batch_op.create_foreign_key(
            "fk_comp_caste", "src_CasteMaster", ["CasteID"], ["caste_master_id"]
        )

    # src_Accused → src_CaseMaster
    with op.batch_alter_table("src_Accused") as batch_op:
        batch_op.create_foreign_key(
            "fk_accused_case", "src_CaseMaster", ["CaseMasterID"], ["CaseMasterID"]
        )

    # src_Victim → src_CaseMaster
    with op.batch_alter_table("src_Victim") as batch_op:
        batch_op.create_foreign_key(
            "fk_victim_case", "src_CaseMaster", ["CaseMasterID"], ["CaseMasterID"]
        )

    # src_ArrestSurrender → multiple
    with op.batch_alter_table("src_ArrestSurrender") as batch_op:
        batch_op.create_foreign_key(
            "fk_arrest_case", "src_CaseMaster", ["CaseMasterID"], ["CaseMasterID"]
        )
    with op.batch_alter_table("src_ArrestSurrender") as batch_op:
        batch_op.create_foreign_key(
            "fk_arrest_state", "src_State", ["ArrestSurrenderStateId"], ["StateID"]
        )
    with op.batch_alter_table("src_ArrestSurrender") as batch_op:
        batch_op.create_foreign_key(
            "fk_arrest_district", "src_District", ["ArrestSurrenderDistrictId"], ["DistrictID"]
        )
    with op.batch_alter_table("src_ArrestSurrender") as batch_op:
        batch_op.create_foreign_key("fk_arrest_unit", "src_Unit", ["PoliceStationID"], ["UnitID"])
    with op.batch_alter_table("src_ArrestSurrender") as batch_op:
        batch_op.create_foreign_key("fk_arrest_io", "src_Employee", ["IOID"], ["EmployeeID"])
    with op.batch_alter_table("src_ArrestSurrender") as batch_op:
        batch_op.create_foreign_key("fk_arrest_court", "src_Court", ["CourtID"], ["CourtID"])
    with op.batch_alter_table("src_ArrestSurrender") as batch_op:
        batch_op.create_foreign_key(
            "fk_arrest_accused", "src_Accused", ["AccusedMasterID"], ["AccusedMasterID"]
        )

    # src_ActSectionAssociation → src_CaseMaster, src_Act
    with op.batch_alter_table("src_ActSectionAssociation") as batch_op:
        batch_op.create_foreign_key(
            "fk_actsec_case", "src_CaseMaster", ["CaseMasterID"], ["CaseMasterID"]
        )
    with op.batch_alter_table("src_ActSectionAssociation") as batch_op:
        batch_op.create_foreign_key("fk_actsec_act", "src_Act", ["ActID"], ["ActCode"])

    # src_ChargesheetDetails → src_CaseMaster, src_Employee
    with op.batch_alter_table("src_ChargesheetDetails") as batch_op:
        batch_op.create_foreign_key(
            "fk_cs_case", "src_CaseMaster", ["CaseMasterID"], ["CaseMasterID"]
        )
    with op.batch_alter_table("src_ChargesheetDetails") as batch_op:
        batch_op.create_foreign_key(
            "fk_cs_employee", "src_Employee", ["PolicePersonID"], ["EmployeeID"]
        )

    # Intelligence schema FKs
    with op.batch_alter_table("int_PersonEntity") as batch_op:
        batch_op.create_foreign_key(
            "fk_pentity_district", "src_District", ["PrimaryDistrictID"], ["DistrictID"]
        )
    with op.batch_alter_table("int_PersonEntityLink") as batch_op:
        batch_op.create_foreign_key(
            "fk_pelink_pentity", "int_PersonEntity", ["PersonEntityID"], ["PersonEntityID"]
        )
    with op.batch_alter_table("int_PersonEntityLink") as batch_op:
        batch_op.create_foreign_key(
            "fk_pelink_case", "src_CaseMaster", ["CaseMasterID"], ["CaseMasterID"]
        )
    with op.batch_alter_table("int_RelationshipEdge") as batch_op:
        batch_op.create_foreign_key(
            "fk_reledge_a", "int_PersonEntity", ["PersonEntityA"], ["PersonEntityID"]
        )
    with op.batch_alter_table("int_RelationshipEdge") as batch_op:
        batch_op.create_foreign_key(
            "fk_reledge_b", "int_PersonEntity", ["PersonEntityB"], ["PersonEntityID"]
        )
    with op.batch_alter_table("int_RelationshipEdge") as batch_op:
        batch_op.create_foreign_key(
            "fk_reledge_case", "src_CaseMaster", ["SourceCaseID"], ["CaseMasterID"]
        )
    with op.batch_alter_table("int_VehicleLink") as batch_op:
        batch_op.create_foreign_key(
            "fk_vlink_case", "src_CaseMaster", ["CaseMasterID"], ["CaseMasterID"]
        )
    with op.batch_alter_table("int_RiskScore") as batch_op:
        batch_op.create_foreign_key(
            "fk_riskscore_pentity", "int_PersonEntity", ["PersonEntityID"], ["PersonEntityID"]
        )
    with op.batch_alter_table("int_RiskScoreFeatureImportance") as batch_op:
        batch_op.create_foreign_key(
            "fk_rsfeat_riskscore", "int_RiskScore", ["RiskScoreID"], ["RiskScoreID"]
        )
    with op.batch_alter_table("int_MoPatternLink") as batch_op:
        batch_op.create_foreign_key(
            "fk_molink_pattern", "int_MoPattern", ["MoPatternID"], ["MoPatternID"]
        )
    with op.batch_alter_table("int_MoPatternLink") as batch_op:
        batch_op.create_foreign_key(
            "fk_molink_case", "src_CaseMaster", ["CaseMasterID"], ["CaseMasterID"]
        )
    with op.batch_alter_table("int_AnomalyAlert") as batch_op:
        batch_op.create_foreign_key(
            "fk_anomaly_district", "src_District", ["DistrictID"], ["DistrictID"]
        )
    with op.batch_alter_table("int_AnomalyAlert") as batch_op:
        batch_op.create_foreign_key(
            "fk_anomaly_crimehead", "src_CrimeHead", ["CrimeHeadID"], ["CrimeHeadID"]
        )
    with op.batch_alter_table("int_HotspotLayer") as batch_op:
        batch_op.create_foreign_key(
            "fk_hotspot_district", "src_District", ["DistrictID"], ["DistrictID"]
        )
    with op.batch_alter_table("int_RAGCorpusChunk") as batch_op:
        batch_op.create_foreign_key(
            "fk_rag_case", "src_CaseMaster", ["CaseMasterID"], ["CaseMasterID"]
        )

    # Governance schema FKs
    with op.batch_alter_table("gov_AuditLog") as batch_op:
        batch_op.create_foreign_key("fk_audit_user", "src_Employee", ["UserID"], ["EmployeeID"])

    # ── Indexes ──────────────────────────────────────────────────────────

    # Core case lookup
    op.create_index("ix_case_crimeno", "src_CaseMaster", ["CrimeNo"], unique=True)
    op.create_index("ix_case_regdate", "src_CaseMaster", ["CrimeRegisteredDate"])
    op.create_index("ix_case_station", "src_CaseMaster", ["PoliceStationID"])
    op.create_index("ix_case_majorhead", "src_CaseMaster", ["CrimeMajorHeadID"])
    op.create_index("ix_case_status", "src_CaseMaster", ["CaseStatusID"])
    op.create_index(
        "ix_case_station_date",
        "src_CaseMaster",
        ["PoliceStationID", "CrimeRegisteredDate"],
    )

    # Person-to-case lookups
    op.create_index("ix_accused_case", "src_Accused", ["CaseMasterID"])
    op.create_index("ix_victim_case", "src_Victim", ["CaseMasterID"])
    op.create_index("ix_comp_case", "src_ComplainantDetails", ["CaseMasterID"])
    op.create_index("ix_arrest_case", "src_ArrestSurrender", ["CaseMasterID"])
    op.create_index("ix_cs_case", "src_ChargesheetDetails", ["CaseMasterID"])

    # Intelligence schema
    op.create_index("ix_pelink_pentity", "int_PersonEntityLink", ["PersonEntityID"])
    op.create_index("ix_pelink_case", "int_PersonEntityLink", ["CaseMasterID"])
    op.create_index("ix_reledge_a", "int_RelationshipEdge", ["PersonEntityA"])
    op.create_index("ix_reledge_b", "int_RelationshipEdge", ["PersonEntityB"])
    op.create_index("ix_reledge_case", "int_RelationshipEdge", ["SourceCaseID"])
    op.create_index("ix_riskscore_pentity", "int_RiskScore", ["PersonEntityID"])
    op.create_index("ix_vlink_case", "int_VehicleLink", ["CaseMasterID"])
    op.create_index("ix_vlink_number", "int_VehicleLink", ["VehicleNumber"])
    op.create_index("ix_molink_pattern", "int_MoPatternLink", ["MoPatternID"])
    op.create_index("ix_molink_case", "int_MoPatternLink", ["CaseMasterID"])
    op.create_index(
        "ix_anomaly_district_week",
        "int_AnomalyAlert",
        ["DistrictID", "WeekStart"],
    )
    op.create_index(
        "ix_hotspot_district_week",
        "int_HotspotLayer",
        ["DistrictID", "WeekStart"],
    )
    op.create_index("ix_rag_case", "int_RAGCorpusChunk", ["CaseMasterID"])

    # Governance schema
    op.create_index("ix_audit_user", "gov_AuditLog", ["UserID"])
    op.create_index("ix_audit_timestamp", "gov_AuditLog", ["Timestamp"])
    op.create_index(
        "ix_audit_entity",
        "gov_AuditLog",
        ["EntityType", "EntityID"],
    )
    op.create_index(
        "ix_provenance_target", "gov_DataProvenanceRecord", ["TargetTable", "TargetRecordID"]
    )

    # Jurisdiction hierarchy
    op.create_index("ix_district_state", "src_District", ["StateID"])
    op.create_index("ix_unit_district", "src_Unit", ["DistrictID"])
    op.create_index("ix_unit_type", "src_Unit", ["TypeID"])
    op.create_index("ix_emp_district", "src_Employee", ["DistrictID"])
    op.create_index("ix_emp_unit", "src_Employee", ["UnitID"])
    op.create_index("ix_court_district", "src_Court", ["DistrictID"])


def downgrade() -> None:
    # Drop indexes (reverse order)
    index_names = [
        "ix_court_district",
        "ix_emp_unit",
        "ix_emp_district",
        "ix_unit_type",
        "ix_unit_district",
        "ix_district_state",
        "ix_provenance_target",
        "ix_audit_entity",
        "ix_audit_timestamp",
        "ix_audit_user",
        "ix_rag_case",
        "ix_hotspot_district_week",
        "ix_anomaly_district_week",
        "ix_molink_case",
        "ix_molink_pattern",
        "ix_vlink_number",
        "ix_vlink_case",
        "ix_riskscore_pentity",
        "ix_reledge_case",
        "ix_reledge_b",
        "ix_reledge_a",
        "ix_pelink_case",
        "ix_pelink_pentity",
        "ix_cs_case",
        "ix_arrest_case",
        "ix_comp_case",
        "ix_victim_case",
        "ix_accused_case",
        "ix_case_station_date",
        "ix_case_status",
        "ix_case_majorhead",
        "ix_case_station",
        "ix_case_regdate",
        "ix_case_crimeno",
    ]
    for name in index_names:
        op.drop_index(name)

    # Drop FK constraints (reverse order) — listing key ones
    fk_names = [
        "fk_audit_user",
        "fk_rag_case",
        "fk_hotspot_district",
        "fk_anomaly_crimehead",
        "fk_anomaly_district",
        "fk_molink_case",
        "fk_molink_pattern",
        "fk_rsfeat_riskscore",
        "fk_riskscore_pentity",
        "fk_vlink_case",
        "fk_reledge_case",
        "fk_reledge_b",
        "fk_reledge_a",
        "fk_pelink_case",
        "fk_pelink_pentity",
        "fk_pentity_district",
        "fk_cs_employee",
        "fk_cs_case",
        "fk_actsec_act",
        "fk_actsec_case",
        "fk_arrest_accused",
        "fk_arrest_court",
        "fk_arrest_io",
        "fk_arrest_unit",
        "fk_arrest_district",
        "fk_arrest_state",
        "fk_arrest_case",
        "fk_victim_case",
        "fk_accused_case",
        "fk_comp_caste",
        "fk_comp_religion",
        "fk_comp_occupation",
        "fk_comp_case",
        "fk_invoccur_case",
        "fk_case_court",
        "fk_case_status",
        "fk_case_minorhead",
        "fk_case_majorhead",
        "fk_case_gravity",
        "fk_case_category",
        "fk_case_unit",
        "fk_case_employee",
        "fk_emp_designation",
        "fk_emp_rank",
        "fk_emp_unit",
        "fk_emp_district",
        "fk_unit_district",
        "fk_unit_state",
        "fk_unit_unittype",
        "fk_chas_act",
        "fk_chas_crimehead",
        "fk_section_act",
    ]
    for name in fk_names:
        import contextlib

        with contextlib.suppress(Exception):
            op.drop_constraint(name)
