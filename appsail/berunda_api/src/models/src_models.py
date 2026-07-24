"""Source schema models — src_ tables from the FIR ER diagram."""

from __future__ import annotations

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from src.models.base import Base


class Act(Base):
    __tablename__ = "src_Act"

    ActCode = Column(String(10), primary_key=True)
    ActDescription = Column(String(500), nullable=False)
    ShortName = Column(String(100))
    Active = Column(Boolean, default=True)

    sections = relationship("Section", back_populates="act")


class Section(Base):
    __tablename__ = "src_Section"

    ActCode = Column(String(10), ForeignKey("src_Act.ActCode"), primary_key=True)
    SectionCode = Column(String(20), primary_key=True)
    SectionDescription = Column(String(500))
    Active = Column(Boolean, default=True)

    act = relationship("Act", back_populates="sections")


class CrimeHead(Base):
    __tablename__ = "src_CrimeHead"

    CrimeHeadID = Column(Integer, primary_key=True)
    CrimeGroupName = Column(String(200), nullable=False)
    Active = Column(Boolean, default=True)

    sub_heads = relationship("CrimeSubHead", back_populates="crime_head")
    act_sections = relationship("CrimeHeadActSection", back_populates="crime_head")


class CrimeSubHead(Base):
    __tablename__ = "src_CrimeSubHead"

    CrimeSubHeadID = Column(Integer, primary_key=True)
    CrimeHeadID = Column(Integer, ForeignKey("src_CrimeHead.CrimeHeadID"), nullable=False)
    CrimeHeadName = Column(String(200), nullable=False)
    SeqID = Column(Integer)
    Active = Column(Boolean, default=True)

    crime_head = relationship("CrimeHead", back_populates="sub_heads")


class CrimeHeadActSection(Base):
    __tablename__ = "src_CrimeHeadActSection"

    CrimeHeadID = Column(Integer, ForeignKey("src_CrimeHead.CrimeHeadID"), primary_key=True)
    ActCode = Column(String(10), ForeignKey("src_Act.ActCode"), primary_key=True)
    SectionCode = Column(String(10), primary_key=True)

    crime_head = relationship("CrimeHead", back_populates="act_sections")
    act = relationship("Act")


class CaseCategory(Base):
    __tablename__ = "src_CaseCategory"

    CaseCategoryID = Column(Integer, primary_key=True)
    LookupValue = Column(String(10), nullable=False)
    Active = Column(Boolean, default=True)


class GravityOffence(Base):
    __tablename__ = "src_GravityOffence"

    GravityOffenceID = Column(Integer, primary_key=True)
    LookupValue = Column(String(50), nullable=False)
    Active = Column(Boolean, default=True)


class CaseStatusMaster(Base):
    __tablename__ = "src_CaseStatusMaster"

    CaseStatusID = Column(Integer, primary_key=True)
    CaseStatusName = Column(String(100), nullable=False)
    Active = Column(Boolean, default=True)


class State(Base):
    __tablename__ = "src_State"

    StateID = Column(Integer, primary_key=True)
    StateName = Column(String(100), nullable=False, unique=True)
    NationalityID = Column(Integer)
    Active = Column(Boolean, default=True)


class District(Base):
    __tablename__ = "src_District"

    DistrictID = Column(Integer, primary_key=True)
    DistrictName = Column(String(100), nullable=False)
    StateID = Column(Integer, ForeignKey("src_State.StateID"))
    Active = Column(Boolean, default=True)

    state = relationship("State")


class Unit(Base):
    __tablename__ = "src_Unit"

    UnitID = Column(Integer, primary_key=True)
    UnitName = Column(String(200), nullable=False)
    TypeID = Column(Integer, ForeignKey("src_UnitType.UnitTypeID"))
    ParentUnit = Column(Integer)
    NationalityID = Column(Integer)
    StateID = Column(Integer, ForeignKey("src_State.StateID"))
    DistrictID = Column(Integer, ForeignKey("src_District.DistrictID"))
    Active = Column(Boolean, default=True)

    unit_type = relationship("UnitType")
    district = relationship("District")


class UnitType(Base):
    __tablename__ = "src_UnitType"

    UnitTypeID = Column(Integer, primary_key=True)
    UnitTypeName = Column(String(100), nullable=False)
    CityDistState = Column(String(50))
    Hierarchy = Column(Integer)
    Active = Column(Boolean, default=True)


class Rank(Base):
    __tablename__ = "src_Rank"

    RankID = Column(Integer, primary_key=True)
    RankName = Column(String(100), nullable=False)
    Hierarchy = Column(Integer)
    Active = Column(Boolean, default=True)


class Designation(Base):
    __tablename__ = "src_Designation"

    DesignationID = Column(Integer, primary_key=True)
    DesignationName = Column(String(100), nullable=False)
    Active = Column(Boolean, default=True)
    SortOrder = Column(Integer)


class Employee(Base):
    __tablename__ = "src_Employee"

    EmployeeID = Column(Integer, primary_key=True)
    DistrictID = Column(Integer, ForeignKey("src_District.DistrictID"))
    UnitID = Column(Integer, ForeignKey("src_Unit.UnitID"))
    RankID = Column(Integer, ForeignKey("src_Rank.RankID"))
    DesignationID = Column(Integer, ForeignKey("src_Designation.DesignationID"))
    KGID = Column(String(50))
    FirstName = Column(String(100), nullable=False)
    EmployeeDOB = Column(Date)
    GenderID = Column(Integer)
    BloodGroupID = Column(Integer)
    PhysicallyChallenged = Column(Boolean)
    AppointmentDate = Column(Date)


class OccupationMaster(Base):
    __tablename__ = "src_OccupationMaster"

    OccupationID = Column(Integer, primary_key=True)
    OccupationName = Column(String(100), nullable=False)
    Active = Column(Boolean, default=True)


class CasteMaster(Base):
    __tablename__ = "src_CasteMaster"

    caste_master_id = Column(Integer, primary_key=True)
    caste_master_name = Column(String(100), nullable=False)
    Active = Column(Boolean, default=True)


class ReligionMaster(Base):
    __tablename__ = "src_ReligionMaster"

    ReligionID = Column(Integer, primary_key=True)
    ReligionName = Column(String(100), nullable=False)
    Active = Column(Boolean, default=True)


class Court(Base):
    __tablename__ = "src_Court"

    CourtID = Column(Integer, primary_key=True)
    CourtName = Column(String(200), nullable=False)
    DistrictID = Column(Integer, ForeignKey("src_District.DistrictID"))
    StateID = Column(Integer, ForeignKey("src_State.StateID"))
    Active = Column(Boolean, default=True)


class CaseMaster(Base):
    __tablename__ = "src_CaseMaster"

    CaseMasterID = Column(Integer, primary_key=True)
    CrimeNo = Column(String(), unique=True, nullable=False)
    CaseNo = Column(String())
    CrimeRegisteredDate = Column(Date)
    PolicePersonID = Column(Integer, ForeignKey("src_Employee.EmployeeID"), index=True)
    PoliceStationID = Column(Integer, ForeignKey("src_Unit.UnitID"))
    CaseCategoryID = Column(Integer, ForeignKey("src_CaseCategory.CaseCategoryID"))
    GravityOffenceID = Column(Integer, ForeignKey("src_GravityOffence.GravityOffenceID"))
    CrimeMajorHeadID = Column(Integer, ForeignKey("src_CrimeHead.CrimeHeadID"))
    CrimeMinorHeadID = Column(Integer, ForeignKey("src_CrimeSubHead.CrimeSubHeadID"))
    CaseStatusID = Column(Integer, ForeignKey("src_CaseStatusMaster.CaseStatusID"))
    CourtID = Column(Integer, ForeignKey("src_Court.CourtID"))
    IncidentFromDate = Column(DateTime)
    IncidentToDate = Column(DateTime)

    occurrence = relationship("InvOccuranceTime", uselist=False, back_populates="case")
    complainants = relationship("ComplainantDetails", back_populates="case")
    victims = relationship("Victim", back_populates="case")
    accused = relationship("Accused", back_populates="case")
    arrests = relationship("ArrestSurrender", back_populates="case")
    act_sections = relationship("ActSectionAssociation", back_populates="case")
    chargesheets = relationship("ChargesheetDetails", back_populates="case")


class InvOccuranceTime(Base):
    __tablename__ = "src_Inv_OccuranceTime"

    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), primary_key=True)
    IncidentFromDate = Column(DateTime)
    IncidentToDate = Column(DateTime)
    InfoReceivedPSDate = Column(DateTime)
    Latitude = Column(Float)
    Longitude = Column(Float)
    BriefFacts = Column(Text)

    case = relationship("CaseMaster", back_populates="occurrence")


class ComplainantDetails(Base):
    __tablename__ = "src_ComplainantDetails"

    ComplainantID = Column(Integer, primary_key=True)
    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False)
    ComplainantName = Column(String(200), nullable=False)
    AgeYear = Column(Integer)
    OccupationID = Column(Integer, ForeignKey("src_OccupationMaster.OccupationID"))
    ReligionID = Column(Integer, ForeignKey("src_ReligionMaster.ReligionID"))
    CasteID = Column(Integer, ForeignKey("src_CasteMaster.caste_master_id"))
    GenderID = Column(Integer)

    case = relationship("CaseMaster", back_populates="complainants")


class Victim(Base):
    __tablename__ = "src_Victim"

    VictimMasterID = Column(Integer, primary_key=True)
    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False)
    VictimName = Column(String(200), nullable=False)
    AgeYear = Column(Integer)
    GenderID = Column(Integer)
    VictimPolice = Column(Boolean)

    case = relationship("CaseMaster", back_populates="victims")


class Accused(Base):
    __tablename__ = "src_Accused"

    AccusedMasterID = Column(Integer, primary_key=True)
    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False)
    AccusedName = Column(String(200), nullable=False)
    AgeYear = Column(Integer)
    GenderID = Column(Integer)
    PersonID = Column(Integer)

    case = relationship("CaseMaster", back_populates="accused")


class ArrestSurrender(Base):
    __tablename__ = "src_ArrestSurrender"

    ArrestSurrenderID = Column(Integer, primary_key=True)
    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False)
    ArrestSurrenderTypeID = Column(Integer)
    ArrestSurrenderDate = Column(Date)
    ArrestSurrenderStateId = Column(Integer, ForeignKey("src_State.StateID"))
    ArrestSurrenderDistrictId = Column(Integer, ForeignKey("src_District.DistrictID"))
    PoliceStationID = Column(Integer, ForeignKey("src_Unit.UnitID"))
    IOID = Column(Integer, ForeignKey("src_Employee.EmployeeID"))
    CourtID = Column(Integer, ForeignKey("src_Court.CourtID"))
    AccusedMasterID = Column(Integer, ForeignKey("src_Accused.AccusedMasterID"))
    IsAccused = Column(Boolean)
    IsComplainantAccused = Column(Boolean)

    case = relationship("CaseMaster", back_populates="arrests")


class ActSectionAssociation(Base):
    __tablename__ = "src_ActSectionAssociation"

    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), primary_key=True)
    ActID = Column(String(10), ForeignKey("src_Act.ActCode"), primary_key=True)
    SectionID = Column(String(10), ForeignKey("src_Section.SectionCode"), primary_key=True)
    ActOrderID = Column(Integer)
    SectionOrderID = Column(Integer)

    case = relationship("CaseMaster", back_populates="act_sections")


class ChargesheetDetails(Base):
    __tablename__ = "src_ChargesheetDetails"

    CSID = Column(Integer, primary_key=True)
    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False)
    csdate = Column(DateTime)
    cstype = Column(String())
    PolicePersonID = Column(Integer, ForeignKey("src_Employee.EmployeeID"))
    Active = Column(Boolean, default=True)

    case = relationship("CaseMaster", back_populates="chargesheets")
