"""initial schema — create all model tables."""

import sqlalchemy as sa

from alembic import op

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "gov_DataProvenanceRecord",
        sa.Column("ProvenanceID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("TargetTable", sa.String(), nullable=False),
        sa.Column("TargetRecordID", sa.String(), nullable=False),
        sa.Column("SourceTable", sa.String(), nullable=False),
        sa.Column("SourceRecordID", sa.String(), nullable=False),
        sa.Column("TransformationDescription", sa.Text(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "gov_FairnessCheckResult",
        sa.Column("FairnessCheckID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("CheckType", sa.String(), nullable=False),
        sa.Column("Timestamp", sa.DateTime(), nullable=False),
        sa.Column("Passed", sa.Boolean(), nullable=False),
        sa.Column("Details", sa.Text(), nullable=True),
        sa.Column("CheckedBy", sa.String(), nullable=True),
    )
    op.create_table(
        "int_MoPattern",
        sa.Column("MoPatternID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("PatternName", sa.String(), nullable=False),
        sa.Column("Embedding", sa.Text(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "int_RiskScore",
        sa.Column("RiskScoreID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("PersonEntityID", sa.Integer(), nullable=True),
        sa.Column("Score", sa.Float(), nullable=False),
        sa.Column("ModelVersion", sa.String(), nullable=True),
        sa.Column("FeaturesJSON", sa.Text(), nullable=True),
        sa.Column("ComputedAt", sa.DateTime(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "src_Act",
        sa.Column("ActCode", sa.String(length=10), nullable=False, primary_key=True),
        sa.Column("ActDescription", sa.String(length=500), nullable=False),
        sa.Column("ShortName", sa.String(length=100), nullable=True),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_CaseCategory",
        sa.Column("CaseCategoryID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("LookupValue", sa.String(), nullable=False),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_CaseStatusMaster",
        sa.Column("CaseStatusID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("CaseStatusName", sa.String(), nullable=False),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_CasteMaster",
        sa.Column("caste_master_id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("caste_master_name", sa.String(), nullable=False),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_CrimeHead",
        sa.Column("CrimeHeadID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("CrimeGroupName", sa.String(), nullable=False),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_Designation",
        sa.Column("DesignationID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("DesignationName", sa.String(), nullable=False),
        sa.Column("Active", sa.Boolean(), nullable=True),
        sa.Column("SortOrder", sa.Integer(), nullable=True),
    )
    op.create_table(
        "src_GravityOffence",
        sa.Column("GravityOffenceID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("LookupValue", sa.String(), nullable=False),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_OccupationMaster",
        sa.Column("OccupationID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("OccupationName", sa.String(), nullable=False),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_Rank",
        sa.Column("RankID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("RankName", sa.String(), nullable=False),
        sa.Column("Hierarchy", sa.Integer(), nullable=True),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_ReligionMaster",
        sa.Column("ReligionID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("ReligionName", sa.String(), nullable=False),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_State",
        sa.Column("StateID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("StateName", sa.String(), nullable=False),
        sa.Column("NationalityID", sa.Integer(), nullable=True),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_UnitType",
        sa.Column("UnitTypeID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("UnitTypeName", sa.String(), nullable=False),
        sa.Column("CityDistState", sa.String(), nullable=True),
        sa.Column("Hierarchy", sa.Integer(), nullable=True),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_Section",
        sa.Column("ActCode", sa.String(length=10), nullable=False, primary_key=True),
        sa.Column("SectionCode", sa.String(length=20), nullable=False, primary_key=True),
        sa.Column("SectionDescription", sa.String(length=500), nullable=False),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_Unit",
        sa.Column("UnitID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("UnitName", sa.String(), nullable=False),
        sa.Column("TypeID", sa.Integer(), nullable=True),
        sa.Column("ParentUnit", sa.Integer(), nullable=True),
        sa.Column("NationalityID", sa.Integer(), nullable=True),
        sa.Column("StateID", sa.Integer(), nullable=True),
        sa.Column("DistrictID", sa.Integer(), nullable=True),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_CrimeHeadActSection",
        sa.Column("CrimeHeadID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("ActCode", sa.String(length=10), nullable=False, primary_key=True),
        sa.Column("SectionCode", sa.String(length=20), nullable=False, primary_key=True),
    )
    op.create_table(
        "src_CrimeSubHead",
        sa.Column("CrimeSubHeadID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column(
            "CrimeHeadID", sa.Integer(), sa.ForeignKey("src_CrimeHead.CrimeHeadID"), nullable=True
        ),  # noqa: E501
        sa.Column("CrimeHeadName", sa.String(), nullable=False),
        sa.Column("SeqID", sa.Integer(), nullable=True),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_District",
        sa.Column("DistrictID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("DistrictName", sa.String(), nullable=False),
        sa.Column("StateID", sa.Integer(), sa.ForeignKey("src_State.StateID"), nullable=True),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_Court",
        sa.Column("CourtID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("CourtName", sa.String(), nullable=False),
        sa.Column(
            "DistrictID", sa.Integer(), sa.ForeignKey("src_District.DistrictID"), nullable=True
        ),  # noqa: E501
        sa.Column("StateID", sa.Integer(), sa.ForeignKey("src_State.StateID"), nullable=True),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_Employee",
        sa.Column("EmployeeID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("DistrictID", sa.Integer(), nullable=True),
        sa.Column("UnitID", sa.Integer(), nullable=True),
        sa.Column("RankID", sa.Integer(), nullable=True),
        sa.Column("DesignationID", sa.Integer(), nullable=True),
        sa.Column("KGID", sa.String(), nullable=True),
        sa.Column("FirstName", sa.String(), nullable=False),
        sa.Column("EmployeeDOB", sa.Date(), nullable=True),
        sa.Column("GenderID", sa.Integer(), nullable=True),
        sa.Column("BloodGroupID", sa.Integer(), nullable=True),
        sa.Column("PhysicallyChallenged", sa.Boolean(), nullable=True),
        sa.Column("AppointmentDate", sa.Date(), nullable=True),
    )
    op.create_table(
        "src_CaseMaster",
        sa.Column("CaseMasterID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("CrimeNo", sa.String(), nullable=True),
        sa.Column("CaseNo", sa.String(), nullable=True),
        sa.Column("CrimeRegisteredDate", sa.DateTime(), nullable=True),
        sa.Column("PolicePersonID", sa.Integer(), nullable=True),
        sa.Column("PoliceStationID", sa.Integer(), nullable=True),
        sa.Column("CaseCategoryID", sa.Integer(), nullable=True),
        sa.Column("GravityOffenceID", sa.Integer(), nullable=True),
        sa.Column("CrimeMajorHeadID", sa.Integer(), nullable=True),
        sa.Column("CrimeMinorHeadID", sa.Integer(), nullable=True),
        sa.Column("CaseStatusID", sa.Integer(), nullable=True),
        sa.Column("CourtID", sa.Integer(), nullable=True),
        sa.Column("IncidentFromDate", sa.DateTime(), nullable=True),
        sa.Column("IncidentToDate", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "gov_AuditLog",
        sa.Column("AuditLogID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("UserID", sa.String(), nullable=False),
        sa.Column("Action", sa.String(), nullable=False),
        sa.Column("EntityType", sa.String(), nullable=False),
        sa.Column("EntityID", sa.String(), nullable=False),
        sa.Column("OldValue", sa.Text(), nullable=True),
        sa.Column("NewValue", sa.Text(), nullable=True),
        sa.Column("Timestamp", sa.DateTime(), nullable=True),
        sa.Column("IPAddress", sa.String(), nullable=True),
    )
    op.create_table(
        "int_AnomalyAlert",
        sa.Column("AnomalyAlertID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("DistrictID", sa.Integer(), nullable=True),
        sa.Column("CrimeHeadID", sa.Integer(), nullable=True),
        sa.Column("WeekStart", sa.Date(), nullable=True),
        sa.Column("ObservedCount", sa.Integer(), nullable=False),
        sa.Column("BaselineMean", sa.Float(), nullable=True),
        sa.Column("StdDev", sa.Float(), nullable=True),
        sa.Column("ZScore", sa.Float(), nullable=True),
        sa.Column("AlertLevel", sa.String(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "int_HotspotLayer",
        sa.Column("HotspotLayerID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("DistrictID", sa.Integer(), nullable=True),
        sa.Column("TileX", sa.Integer(), nullable=False),
        sa.Column("TileY", sa.Integer(), nullable=False),
        sa.Column("DensityScore", sa.Float(), nullable=False),
        sa.Column("WeekStart", sa.Date(), nullable=True),
        sa.Column("WeekEnd", sa.Date(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "int_MoPatternLink",
        sa.Column("MoPatternLinkID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("MoPatternID", sa.Integer(), nullable=True),
        sa.Column("CaseMasterID", sa.Integer(), nullable=True),
        sa.Column("SimilarityScore", sa.Float(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "int_PersonEntityLink",
        sa.Column("PersonEntityLinkID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("PersonEntityID", sa.Integer(), nullable=True),
        sa.Column("SourceTable", sa.String(), nullable=False),
        sa.Column("SourceRecordID", sa.String(), nullable=False),
        sa.Column("CaseMasterID", sa.Integer(), nullable=True),
        sa.Column("Confidence", sa.Float(), nullable=True),
        sa.Column("IsReviewed", sa.Boolean(), nullable=True),
        sa.Column("ReviewedBy", sa.String(), nullable=True),
        sa.Column("ReviewedAt", sa.DateTime(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "int_RAGCorpusChunk",
        sa.Column("ChunkID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("CaseMasterID", sa.Integer(), nullable=True),
        sa.Column("ChunkIndex", sa.Integer(), nullable=True),
        sa.Column("ChunkText", sa.Text(), nullable=False),
        sa.Column("Embedding", sa.Text(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "int_RelationshipEdge",
        sa.Column("RelationshipEdgeID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("PersonEntityA", sa.Integer(), nullable=True),
        sa.Column("PersonEntityB", sa.Integer(), nullable=True),
        sa.Column("RelationshipType", sa.String(), nullable=True),
        sa.Column("SourceCaseID", sa.Integer(), nullable=True),
        sa.Column("Confidence", sa.Float(), nullable=True),
        sa.Column("DiscoveredAt", sa.DateTime(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "int_VehicleLink",
        sa.Column("VehicleLinkID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("VehicleNumber", sa.String(), nullable=False),
        sa.Column("CaseMasterID", sa.Integer(), nullable=True),
        sa.Column("Confidence", sa.Float(), nullable=True),
        sa.Column("Source", sa.String(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "int_PersonEntity",
        sa.Column("PersonEntityID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("CanonicalName", sa.String(), nullable=False),
        sa.Column("DOB", sa.Date(), nullable=True),
        sa.Column("Gender", sa.String(), nullable=True),
        sa.Column("PrimaryDistrictID", sa.Integer(), nullable=True),
        sa.Column("RiskScoreID", sa.Integer(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
        sa.Column("UpdatedAt", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "int_RiskScoreFeatureImportance",
        sa.Column("RiskScoreImportanceID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("RiskScoreID", sa.Integer(), nullable=True),
        sa.Column("FeatureName", sa.String(), nullable=False),
        sa.Column("ImportanceValue", sa.Float(), nullable=False),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "src_Accused",
        sa.Column("AccusedMasterID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("CaseMasterID", sa.Integer(), nullable=True),
        sa.Column("AccusedName", sa.String(), nullable=False),
        sa.Column("AgeYear", sa.Integer(), nullable=True),
        sa.Column("GenderID", sa.Integer(), nullable=True),
        sa.Column("PersonID", sa.Integer(), nullable=True),
    )
    op.create_table(
        "src_ActSectionAssociation",
        sa.Column("CaseMasterID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("ActID", sa.String(length=10), nullable=False, primary_key=True),
        sa.Column("SectionID", sa.String(length=20), nullable=False, primary_key=True),
        sa.Column("ActOrderID", sa.Integer(), nullable=True),
        sa.Column("SectionOrderID", sa.Integer(), nullable=True),
    )
    op.create_table(
        "src_ArrestSurrender",
        sa.Column("ArrestSurrenderID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("CaseMasterID", sa.Integer(), nullable=True),
        sa.Column("ArrestSurrenderTypeID", sa.Integer(), nullable=True),
        sa.Column("ArrestSurrenderDate", sa.DateTime(), nullable=True),
        sa.Column("ArrestSurrenderStateId", sa.Integer(), nullable=True),
        sa.Column("ArrestSurrenderDistrictId", sa.Integer(), nullable=True),
        sa.Column("PoliceStationID", sa.Integer(), nullable=True),
        sa.Column("IOID", sa.Integer(), nullable=True),
        sa.Column("CourtID", sa.Integer(), nullable=True),
        sa.Column("AccusedMasterID", sa.Integer(), nullable=True),
        sa.Column("IsAccused", sa.Boolean(), nullable=True),
        sa.Column("IsComplainantAccused", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_ChargesheetDetails",
        sa.Column("CSID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("CaseMasterID", sa.Integer(), nullable=True),
        sa.Column("csdate", sa.DateTime(), nullable=True),
        sa.Column("cstype", sa.String(), nullable=True),
        sa.Column("PolicePersonID", sa.Integer(), nullable=True),
        sa.Column("Active", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "src_ComplainantDetails",
        sa.Column("ComplainantID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("CaseMasterID", sa.Integer(), nullable=True),
        sa.Column("ComplainantName", sa.String(), nullable=False),
        sa.Column("AgeYear", sa.Integer(), nullable=True),
        sa.Column("OccupationID", sa.Integer(), nullable=True),
        sa.Column("ReligionID", sa.Integer(), nullable=True),
        sa.Column("CasteID", sa.Integer(), nullable=True),
        sa.Column("GenderID", sa.Integer(), nullable=True),
    )
    op.create_table(
        "src_Inv_OccuranceTime",
        sa.Column("CaseMasterID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("IncidentFromDate", sa.DateTime(), nullable=True),
        sa.Column("IncidentToDate", sa.DateTime(), nullable=True),
        sa.Column("InfoReceivedPSDate", sa.DateTime(), nullable=True),
        sa.Column("Latitude", sa.Float(), nullable=True),
        sa.Column("Longitude", sa.Float(), nullable=True),
        sa.Column("BriefFacts", sa.Text(), nullable=True),
    )
    op.create_table(
        "src_Victim",
        sa.Column("VictimMasterID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("CaseMasterID", sa.Integer(), nullable=True),
        sa.Column("VictimName", sa.String(), nullable=False),
        sa.Column("AgeYear", sa.Integer(), nullable=True),
        sa.Column("GenderID", sa.Integer(), nullable=True),
        sa.Column("VictimPolice", sa.Boolean(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("src_Victim")
    op.drop_table("src_Inv_OccuranceTime")
    op.drop_table("src_ComplainantDetails")
    op.drop_table("src_ChargesheetDetails")
    op.drop_table("src_ArrestSurrender")
    op.drop_table("src_ActSectionAssociation")
    op.drop_table("src_Accused")
    op.drop_table("int_RiskScoreFeatureImportance")
    op.drop_table("int_PersonEntity")
    op.drop_table("int_VehicleLink")
    op.drop_table("int_RelationshipEdge")
    op.drop_table("int_RAGCorpusChunk")
    op.drop_table("int_PersonEntityLink")
    op.drop_table("int_MoPatternLink")
    op.drop_table("int_HotspotLayer")
    op.drop_table("int_AnomalyAlert")
    op.drop_table("gov_AuditLog")
    op.drop_table("src_CaseMaster")
    op.drop_table("src_Employee")
    op.drop_table("src_Court")
    op.drop_table("src_District")
    op.drop_table("src_CrimeSubHead")
    op.drop_table("src_CrimeHeadActSection")
    op.drop_table("src_Unit")
    op.drop_table("src_Section")
    op.drop_table("src_UnitType")
    op.drop_table("src_State")
    op.drop_table("src_ReligionMaster")
    op.drop_table("src_Rank")
    op.drop_table("src_OccupationMaster")
    op.drop_table("src_GravityOffence")
    op.drop_table("src_Designation")
    op.drop_table("src_CrimeHead")
    op.drop_table("src_CasteMaster")
    op.drop_table("src_CaseStatusMaster")
    op.drop_table("src_CaseCategory")
    op.drop_table("src_Act")
    op.drop_table("int_RiskScore")
    op.drop_table("int_MoPattern")
    op.drop_table("gov_FairnessCheckResult")
    op.drop_table("gov_DataProvenanceRecord")
