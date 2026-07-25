"""Migration 001: Create initial schema with all tables."""

from sqlalchemy import (
    MetaData, Table, Column, Integer, String, DateTime, Float, Text,
    Boolean, ForeignKey, UniqueConstraint, func
)


def upgrade(engine):
    meta = MetaData()

    Table(
        "src_District", meta,
        Column("DistrictID", Integer, primary_key=True, autoincrement=True),
        Column("DistrictName", String(255), nullable=False),
        Column("StateID", Integer, nullable=True),
    )
    Table(
        "src_Unit", meta,
        Column("UnitID", Integer, primary_key=True, autoincrement=True),
        Column("UnitName", String(255), nullable=False),
        Column("DistrictID", Integer, ForeignKey("src_District.DistrictID"), nullable=True),
        Column("TypeID", Integer, nullable=True),
    )
    Table(
        "src_CrimeHead", meta,
        Column("CrimeHeadID", Integer, primary_key=True, autoincrement=True),
        Column("CrimeGroupName", String(255), nullable=False),
    )
    Table(
        "src_CaseStatusMaster", meta,
        Column("CaseStatusID", Integer, primary_key=True, autoincrement=True),
        Column("CaseStatusName", String(255), nullable=False),
    )
    Table(
        "src_GravityOffence", meta,
        Column("GravityOffenceID", Integer, primary_key=True, autoincrement=True),
        Column("LookupValue", String(255), nullable=False),
    )
    Table(
        "src_CaseMaster", meta,
        Column("CaseMasterID", Integer, primary_key=True, autoincrement=True),
        Column("CrimeNo", String(255), unique=True, nullable=False),
        Column("CaseNo", String(255), nullable=True),
        Column("CrimeRegisteredDate", DateTime(timezone=True), nullable=True),
        Column("PoliceStationID", Integer, ForeignKey("src_Unit.UnitID"), nullable=True),
        Column("CaseCategoryID", Integer, nullable=True),
        Column("GravityOffenceID", Integer, ForeignKey("src_GravityOffence.GravityOffenceID"), nullable=True),
        Column("CrimeMajorHeadID", Integer, ForeignKey("src_CrimeHead.CrimeHeadID"), nullable=True),
        Column("CrimeMinorHeadID", Integer, nullable=True),
        Column("CaseStatusID", Integer, ForeignKey("src_CaseStatusMaster.CaseStatusID"), nullable=True),
        Column("IncidentFromDate", DateTime(timezone=True), nullable=True),
        Column("IncidentToDate", DateTime(timezone=True), nullable=True),
        Column("CreatedAt", DateTime(timezone=True), server_default=func.now(), nullable=False),
        Column("UpdatedAt", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
        UniqueConstraint("CrimeNo", name="uq_crime_no"),
    )
    Table(
        "src_Inv_OccuranceTime", meta,
        Column("CaseMasterID", Integer, ForeignKey("src_CaseMaster.CaseMasterID"), primary_key=True),
        Column("BriefFacts", Text, nullable=True),
        Column("Latitude", Float, nullable=True),
        Column("Longitude", Float, nullable=True),
    )
    Table(
        "src_ComplainantDetails", meta,
        Column("ComplainantID", Integer, primary_key=True, autoincrement=True),
        Column("CaseMasterID", Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False),
        Column("Name", String(255), nullable=True),
        Column("Age", Integer, nullable=True),
        Column("OccupationID", Integer, nullable=True),
        Column("ReligionID", Integer, nullable=True),
        Column("CasteID", Integer, nullable=True),
    )
    Table(
        "src_Victim", meta,
        Column("VictimMasterID", Integer, primary_key=True, autoincrement=True),
        Column("CaseMasterID", Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False),
        Column("Name", String(255), nullable=True),
        Column("Age", Integer, nullable=True),
        Column("GenderID", Integer, nullable=True),
    )
    Table(
        "src_Accused", meta,
        Column("AccusedMasterID", Integer, primary_key=True, autoincrement=True),
        Column("CaseMasterID", Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False),
        Column("Name", String(255), nullable=True),
        Column("Age", Integer, nullable=True),
        Column("PersonID", Integer, nullable=True),
    )
    Table(
        "src_ActSectionAssociation", meta,
        Column("CaseMasterID", Integer, ForeignKey("src_CaseMaster.CaseMasterID"), primary_key=True),
        Column("ActID", Integer, primary_key=True),
        Column("SectionID", Integer, primary_key=True),
        UniqueConstraint("CaseMasterID", "ActID", "SectionID", name="uq_act_section"),
    )
    Table(
        "auth_User", meta,
        Column("UserID", Integer, primary_key=True, autoincrement=True),
        Column("Email", String(255), unique=True, index=True, nullable=False),
        Column("HashedPassword", String(255), nullable=False),
        Column("Role", String(50), nullable=False),
        Column("DistrictID", Integer, ForeignKey("src_District.DistrictID"), nullable=True),
        Column("IsActive", Boolean, default=True, nullable=False),
        Column("CreatedAt", DateTime(timezone=True), server_default=func.now(), nullable=False),
        Column("UpdatedAt", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
    )
    Table(
        "auth_Session", meta,
        Column("SessionID", Integer, primary_key=True, autoincrement=True),
        Column("UserID", Integer, ForeignKey("auth_User.UserID"), nullable=False),
        Column("TokenHash", String(255), index=True, nullable=False),
        Column("ExpiresAt", DateTime(timezone=True), nullable=False),
        Column("RevokedAt", DateTime(timezone=True), nullable=True),
        Column("CreatedAt", DateTime(timezone=True), server_default=func.now(), nullable=False),
    )
    Table(
        "auth_Permission", meta,
        Column("PermissionID", Integer, primary_key=True, autoincrement=True),
        Column("Role", String(50), nullable=False),
        Column("Resource", String(255), nullable=False),
        Column("Action", String(50), nullable=False),
        Column("CreatedAt", DateTime(timezone=True), server_default=func.now(), nullable=False),
    )

    meta.create_all(engine)


def downgrade(engine):
    meta = MetaData()
    meta.reflect(bind=engine)
    tables = [
        "auth_Permission", "auth_Session", "auth_User",
        "src_ActSectionAssociation", "src_Accused", "src_Victim",
        "src_ComplainantDetails", "src_Inv_OccuranceTime",
        "src_CaseMaster", "src_GravityOffence", "src_CaseStatusMaster",
        "src_CrimeHead", "src_Unit", "src_District",
    ]
    for t in tables:
        if t in meta.tables:
            meta.tables[t].drop(engine)
