from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, DateTime, Float, Text, Boolean,
    ForeignKey, UniqueConstraint, func
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "auth_User"

    UserID = Column(Integer, primary_key=True, autoincrement=True)
    Email = Column(String(255), unique=True, index=True, nullable=False)
    HashedPassword = Column(String(255), nullable=False)
    Role = Column(String(50), nullable=False)
    DistrictID = Column(Integer, ForeignKey("src_District.DistrictID"), nullable=True)
    IsActive = Column(Boolean, default=True, nullable=False)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    UpdatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Session(Base):
    __tablename__ = "auth_Session"

    SessionID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("auth_User.UserID"), nullable=False)
    TokenHash = Column(String(255), index=True, nullable=False)
    ExpiresAt = Column(DateTime(timezone=True), nullable=False)
    RevokedAt = Column(DateTime(timezone=True), nullable=True)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Permission(Base):
    __tablename__ = "auth_Permission"

    PermissionID = Column(Integer, primary_key=True, autoincrement=True)
    Role = Column(String(50), nullable=False)
    Resource = Column(String(255), nullable=False)
    Action = Column(String(50), nullable=False)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class CaseMaster(Base):
    __tablename__ = "src_CaseMaster"
    __table_args__ = (
        UniqueConstraint("CrimeNo", name="uq_crime_no"),
    )

    CaseMasterID = Column(Integer, primary_key=True, autoincrement=True)
    CrimeNo = Column(String(255), unique=True, nullable=False)
    CaseNo = Column(String(255), nullable=True)
    CrimeRegisteredDate = Column(DateTime(timezone=True), nullable=True)
    PoliceStationID = Column(Integer, ForeignKey("src_Unit.UnitID"), nullable=True)
    CaseCategoryID = Column(Integer, nullable=True)
    GravityOffenceID = Column(Integer, ForeignKey("src_GravityOffence.GravityOffenceID"), nullable=True)
    CrimeMajorHeadID = Column(Integer, ForeignKey("src_CrimeHead.CrimeHeadID"), nullable=True)
    CrimeMinorHeadID = Column(Integer, nullable=True)
    CaseStatusID = Column(Integer, ForeignKey("src_CaseStatusMaster.CaseStatusID"), nullable=True)
    IncidentFromDate = Column(DateTime(timezone=True), nullable=True)
    IncidentToDate = Column(DateTime(timezone=True), nullable=True)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    UpdatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class InvOccuranceTime(Base):
    __tablename__ = "src_Inv_OccuranceTime"

    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), primary_key=True)
    BriefFacts = Column(Text, nullable=True)
    Latitude = Column(Float, nullable=True)
    Longitude = Column(Float, nullable=True)


class ComplainantDetails(Base):
    __tablename__ = "src_ComplainantDetails"

    ComplainantID = Column(Integer, primary_key=True, autoincrement=True)
    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False)
    Name = Column(String(255), nullable=True)
    Age = Column(Integer, nullable=True)
    OccupationID = Column(Integer, nullable=True)
    ReligionID = Column(Integer, nullable=True)
    CasteID = Column(Integer, nullable=True)


class Victim(Base):
    __tablename__ = "src_Victim"

    VictimMasterID = Column(Integer, primary_key=True, autoincrement=True)
    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False)
    Name = Column(String(255), nullable=True)
    Age = Column(Integer, nullable=True)
    GenderID = Column(Integer, nullable=True)


class Accused(Base):
    __tablename__ = "src_Accused"

    AccusedMasterID = Column(Integer, primary_key=True, autoincrement=True)
    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False)
    Name = Column(String(255), nullable=True)
    Age = Column(Integer, nullable=True)
    PersonID = Column(Integer, nullable=True)


class ActSectionAssociation(Base):
    __tablename__ = "src_ActSectionAssociation"
    __table_args__ = (
        UniqueConstraint("CaseMasterID", "ActID", "SectionID", name="uq_act_section"),
    )

    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), primary_key=True)
    ActID = Column(Integer, primary_key=True)
    SectionID = Column(Integer, primary_key=True)


class District(Base):
    __tablename__ = "src_District"

    DistrictID = Column(Integer, primary_key=True, autoincrement=True)
    DistrictName = Column(String(255), nullable=False)
    StateID = Column(Integer, nullable=True)


class Unit(Base):
    __tablename__ = "src_Unit"

    UnitID = Column(Integer, primary_key=True, autoincrement=True)
    UnitName = Column(String(255), nullable=False)
    DistrictID = Column(Integer, ForeignKey("src_District.DistrictID"), nullable=True)
    TypeID = Column(Integer, nullable=True)


class CrimeHead(Base):
    __tablename__ = "src_CrimeHead"

    CrimeHeadID = Column(Integer, primary_key=True, autoincrement=True)
    CrimeGroupName = Column(String(255), nullable=False)


class CaseStatusMaster(Base):
    __tablename__ = "src_CaseStatusMaster"

    CaseStatusID = Column(Integer, primary_key=True, autoincrement=True)
    CaseStatusName = Column(String(255), nullable=False)


class GravityOffence(Base):
    __tablename__ = "src_GravityOffence"

    GravityOffenceID = Column(Integer, primary_key=True, autoincrement=True)
    LookupValue = Column(String(255), nullable=False)
