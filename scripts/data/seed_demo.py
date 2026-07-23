# ruff: noqa: E501
"""Seed demo data into Berunda for hackathon demonstration.

Creates lookup tables, sample FIRs with planted patterns:
  1. Repeat offender — one person as accused in 4 cases under different names
  2. Linked vehicle — same vehicle across 3 cases
  3. Hotspot — 2-week crime spike in Bengaluru Urban (theft)

Usage:
    python scripts/data/seed_demo.py
    python scripts/data/seed_demo.py --db-url postgresql+asyncpg://user:pass@localhost:5432/berunda
"""

from __future__ import annotations

import argparse
import asyncio
from datetime import date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.models.int_models import (
    PersonEntity,
    PersonEntityLink,
    RelationshipEdge,
    VehicleLink,
)
from src.models.src_models import (
    Accused,
    Act,
    ActSectionAssociation,
    CaseCategory,
    CaseMaster,
    CaseStatusMaster,
    ComplainantDetails,
    Court,
    CrimeHead,
    CrimeHeadActSection,
    CrimeSubHead,
    Designation,
    District,
    Employee,
    GravityOffence,
    InvOccuranceTime,
    OccupationMaster,
    Rank,
    ReligionMaster,
    Section,
    State,
    Unit,
    UnitType,
)

DB_URL = "postgresql+asyncpg://berunda:berunda@localhost:5432/berunda"

LOOKUP_DATA: dict = {}

async def seed_lookups(session: AsyncSession):
    """Seed reference/lookup tables from synthetic_config equivalents."""

    existing = await session.execute(select(State).limit(1))
    if existing.scalar_one_or_none():
        print("Lookup data already seeded; skipping.")
        return

    # ── State ──
    state = State(StateID=1, StateName="Karnataka", NationalityID=1, Active=True)
    session.add(state)

    # ── Districts (31 Karnataka districts) ──
    districts = [
        District(DistrictID=1,  DistrictName="Bagalkote",              StateID=1, Active=True),
        District(DistrictID=2,  DistrictName="Ballari",                StateID=1, Active=True),
        District(DistrictID=3,  DistrictName="Belagavi",               StateID=1, Active=True),
        District(DistrictID=4,  DistrictName="Bengaluru Rural",        StateID=1, Active=True),
        District(DistrictID=5,  DistrictName="Bengaluru Urban",        StateID=1, Active=True),
        District(DistrictID=6,  DistrictName="Bidar",                  StateID=1, Active=True),
        District(DistrictID=7,  DistrictName="Chamarajanagara",        StateID=1, Active=True),
        District(DistrictID=8,  DistrictName="Chikkaballapura",        StateID=1, Active=True),
        District(DistrictID=9,  DistrictName="Chikkamagaluru",         StateID=1, Active=True),
        District(DistrictID=10, DistrictName="Chitradurga",            StateID=1, Active=True),
        District(DistrictID=11, DistrictName="Dakshina Kannada",       StateID=1, Active=True),
        District(DistrictID=12, DistrictName="Davanagere",             StateID=1, Active=True),
        District(DistrictID=13, DistrictName="Dharwad",                StateID=1, Active=True),
        District(DistrictID=14, DistrictName="Gadag",                  StateID=1, Active=True),
        District(DistrictID=15, DistrictName="Hassan",                 StateID=1, Active=True),
        District(DistrictID=16, DistrictName="Haveri",                 StateID=1, Active=True),
        District(DistrictID=17, DistrictName="Kalaburagi",             StateID=1, Active=True),
        District(DistrictID=18, DistrictName="Kodagu",                 StateID=1, Active=True),
        District(DistrictID=19, DistrictName="Kolar",                  StateID=1, Active=True),
        District(DistrictID=20, DistrictName="Koppala",                StateID=1, Active=True),
        District(DistrictID=21, DistrictName="Mandya",                 StateID=1, Active=True),
        District(DistrictID=22, DistrictName="Mysuru",                 StateID=1, Active=True),
        District(DistrictID=23, DistrictName="Raichur",                StateID=1, Active=True),
        District(DistrictID=24, DistrictName="Ramanagara",             StateID=1, Active=True),
        District(DistrictID=25, DistrictName="Shivamogga",             StateID=1, Active=True),
        District(DistrictID=26, DistrictName="Tumakuru",               StateID=1, Active=True),
        District(DistrictID=27, DistrictName="Udupi",                  StateID=1, Active=True),
        District(DistrictID=28, DistrictName="Uttara Kannada",         StateID=1, Active=True),
        District(DistrictID=29, DistrictName="Vijayapura",             StateID=1, Active=True),
        District(DistrictID=30, DistrictName="Yadgiri",                StateID=1, Active=True),
        District(DistrictID=31, DistrictName="Bengaluru City",         StateID=1, Active=True),
    ]
    for d in districts:
        session.add(d)

    # ── Unit Types ──
    unit_types = [
        UnitType(UnitTypeID=1, UnitTypeName="Commissionerate", CityDistState="City"),
        UnitType(UnitTypeID=2, UnitTypeName="Police Station", CityDistState="District"),
        UnitType(UnitTypeID=3, UnitTypeName="District Office", CityDistState="District"),
    ]
    for ut in unit_types:
        session.add(ut)

    # ── Police Stations (sample — one per district) ──
    for i in range(1, 32):
        session.add(Unit(
            UnitID=i, UnitName=f"PS-{i:02d}",
            TypeID=2, DistrictID=i, StateID=1, Active=True,
        ))

    # ── Acts ──
    acts = [
        Act(ActCode="BNS",      ActDescription="Bharatiya Nyaya Sanhita 2023", ShortName="BNS", Active=True),
        Act(ActCode="IT_Act",   ActDescription="Information Technology Act 2000", ShortName="IT Act", Active=True),
        Act(ActCode="NDPS",     ActDescription="Narcotic Drugs and Psychotropic Substances Act", ShortName="NDPS", Active=True),
        Act(ActCode="Arms_Act", ActDescription="Arms Act 1959", ShortName="Arms Act", Active=True),
    ]
    for a in acts:
        session.add(a)

    # ── Sections ──
    sections = [
        Section(ActCode="BNS", SectionCode="101", SectionDescription="Murder", Active=True),
        Section(ActCode="BNS", SectionCode="109", SectionDescription="Attempt to murder", Active=True),
        Section(ActCode="BNS", SectionCode="115", SectionDescription="Voluntarily causing hurt", Active=True),
        Section(ActCode="BNS", SectionCode="137", SectionDescription="Rape", Active=True),
        Section(ActCode="BNS", SectionCode="140", SectionDescription="Kidnapping", Active=True),
        Section(ActCode="BNS", SectionCode="191", SectionDescription="Rioting", Active=True),
        Section(ActCode="BNS", SectionCode="303", SectionDescription="Theft", Active=True),
        Section(ActCode="BNS", SectionCode="305", SectionDescription="Theft in dwelling house", Active=True),
        Section(ActCode="BNS", SectionCode="308", SectionDescription="Extortion", Active=True),
        Section(ActCode="BNS", SectionCode="309", SectionDescription="Robbery", Active=True),
        Section(ActCode="BNS", SectionCode="310", SectionDescription="Dacoity", Active=True),
        Section(ActCode="BNS", SectionCode="316", SectionDescription="Cheating", Active=True),
        Section(ActCode="BNS", SectionCode="329", SectionDescription="Criminal trespass", Active=True),
        Section(ActCode="BNS", SectionCode="331", SectionDescription="Burglary", Active=True),
        Section(ActCode="BNS", SectionCode="336", SectionDescription="Mischief", Active=True),
        Section(ActCode="IT_Act", SectionCode="66", SectionDescription="Computer related offences", Active=True),
        Section(ActCode="IT_Act", SectionCode="67", SectionDescription="Publishing obscene material", Active=True),
        Section(ActCode="NDPS", SectionCode="20", SectionDescription="Cultivation etc.", Active=True),
        Section(ActCode="NDPS", SectionCode="21", SectionDescription="Manufacture etc.", Active=True),
        Section(ActCode="Arms_Act", SectionCode="25", SectionDescription="Arms possession", Active=True),
        Section(ActCode="Arms_Act", SectionCode="27", SectionDescription="Arms use", Active=True),
    ]
    for s in sections:
        session.add(s)

    # ── Crime Heads ──
    crime_heads = [
        CrimeHead(CrimeHeadID=1,  CrimeGroupName="Theft", Active=True),
        CrimeHead(CrimeHeadID=2,  CrimeGroupName="Burglary", Active=True),
        CrimeHead(CrimeHeadID=3,  CrimeGroupName="Robbery", Active=True),
        CrimeHead(CrimeHeadID=4,  CrimeGroupName="Dacoity", Active=True),
        CrimeHead(CrimeHeadID=5,  CrimeGroupName="Murder", Active=True),
        CrimeHead(CrimeHeadID=6,  CrimeGroupName="Attempt to Murder", Active=True),
        CrimeHead(CrimeHeadID=7,  CrimeGroupName="Hurt / Assault", Active=True),
        CrimeHead(CrimeHeadID=8,  CrimeGroupName="Rape / Sexual Assault", Active=True),
        CrimeHead(CrimeHeadID=9,  CrimeGroupName="Kidnapping", Active=True),
        CrimeHead(CrimeHeadID=10, CrimeGroupName="Cheating / Fraud", Active=True),
        CrimeHead(CrimeHeadID=11, CrimeGroupName="Criminal Trespass", Active=True),
        CrimeHead(CrimeHeadID=12, CrimeGroupName="Rioting", Active=True),
        CrimeHead(CrimeHeadID=13, CrimeGroupName="Arson", Active=True),
        CrimeHead(CrimeHeadID=14, CrimeGroupName="Motor Vehicle Theft", Active=True),
        CrimeHead(CrimeHeadID=15, CrimeGroupName="Extortion", Active=True),
        CrimeHead(CrimeHeadID=16, CrimeGroupName="Cyber Crime", Active=True),
        CrimeHead(CrimeHeadID=17, CrimeGroupName="NDPS Violation", Active=True),
        CrimeHead(CrimeHeadID=18, CrimeGroupName="Arms Act Violation", Active=True),
        CrimeHead(CrimeHeadID=19, CrimeGroupName="Missing Person", Active=True),
        CrimeHead(CrimeHeadID=20, CrimeGroupName="Property Damage", Active=True),
    ]
    for ch in crime_heads:
        session.add(ch)

    # ── Crime Sub Heads ──
    for ch in crime_heads:
        session.add(CrimeSubHead(
            CrimeSubHeadID=ch.CrimeHeadID,
            CrimeHeadID=ch.CrimeHeadID,
            CrimeHeadName=ch.CrimeGroupName,
            SeqID=1, Active=True,
        ))

    # ── Crime Head Act/Section Associations ──
    associations = [
        (1, "BNS", "303"), (2, "BNS", "331"), (3, "BNS", "309"),
        (4, "BNS", "310"), (5, "BNS", "101"), (6, "BNS", "109"),
        (7, "BNS", "115"), (8, "BNS", "137"), (9, "BNS", "140"),
        (10, "BNS", "316"), (11, "BNS", "329"), (12, "BNS", "191"),
        (13, "BNS", "336"), (14, "BNS", "303"), (15, "BNS", "308"),
        (16, "IT_Act", "66"), (17, "NDPS", "20"), (18, "Arms_Act", "25"),
        (19, "BNS", "101"), (20, "BNS", "336"),
    ]
    for ch_id, act_code, sec_code in associations:
        session.add(CrimeHeadActSection(CrimeHeadID=ch_id, ActCode=act_code, SectionCode=sec_code))

    # ── Case Categories ──
    for cat in [(1, "FIR"), (2, "UDR"), (3, "PAR"), (4, "Zero FIR")]:
        session.add(CaseCategory(CaseCategoryID=cat[0], LookupValue=cat[1], Active=True))

    # ── Gravity Offences ──
    session.add(GravityOffence(GravityOffenceID=1, LookupValue="Heinous", Active=True))
    session.add(GravityOffence(GravityOffenceID=2, LookupValue="Non-Heinous", Active=True))

    # ── Case Statuses ──
    statuses = [
        CaseStatusMaster(CaseStatusID=1, CaseStatusName="Under Investigation", Active=True),
        CaseStatusMaster(CaseStatusID=2, CaseStatusName="Charge Sheeted", Active=True),
        CaseStatusMaster(CaseStatusID=3, CaseStatusName="Pending Trial", Active=True),
        CaseStatusMaster(CaseStatusID=4, CaseStatusName="Convicted", Active=True),
        CaseStatusMaster(CaseStatusID=5, CaseStatusName="Acquitted", Active=True),
    ]
    for s in statuses:
        session.add(s)

    # ── Ranks & Designations ──
    session.add(Rank(RankID=1, RankName="Police Constable", Hierarchy=1))
    session.add(Rank(RankID=2, RankName="Sub-Inspector", Hierarchy=5))
    session.add(Rank(RankID=3, RankName="Inspector", Hierarchy=7))
    session.add(Designation(DesignationID=1, DesignationName="SHO", SortOrder=1))
    session.add(Designation(DesignationID=2, DesignationName="IO", SortOrder=2))

    # ── Employees ──
    session.add(Employee(
        EmployeeID=1, DistrictID=5, UnitID=1, RankID=3,
        DesignationID=1, KGID="KG001", FirstName="Arun",
        AppointmentDate=date(2020, 1, 1),
    ))
    session.add(Employee(
        EmployeeID=2, DistrictID=5, UnitID=1, RankID=2,
        DesignationID=2, KGID="KG002", FirstName="Kumar",
        AppointmentDate=date(2021, 6, 1),
    ))

    # ── Occupations ──
    for occ in [(1, "Private Employee"), (2, "Government Employee"),
                 (3, "Business"), (4, "Farmer"), (5, "Student"),
                 (6, "Unemployed"), (7, "Retired"), (8, "Other")]:
        session.add(OccupationMaster(OccupationID=occ[0], OccupationName=occ[1], Active=True))

    # ── Religions ──
    for rel in [(1, "Hindu"), (2, "Muslim"), (3, "Christian"), (4, "Sikh"), (5, "Other")]:
        session.add(ReligionMaster(ReligionID=rel[0], ReligionName=rel[1], Active=True))

    # ── Courts ──
    for c in [(1, "JMFC Bengaluru", 5), (2, "CJM Bengaluru", 5),
              (3, "Session Court Bengaluru", 5), (4, "JMFC Mysuru", 22)]:
        session.add(Court(CourtID=c[0], CourtName=c[1], DistrictID=c[2], StateID=1, Active=True))

    await session.commit()
    print(f"Seeded lookup data: {len(districts)} districts, {len(crime_heads)} crime heads.")


async def seed_cases(session: AsyncSession):
    """Seed sample FIR cases with planted patterns."""

    existing = await session.execute(select(CaseMaster).limit(1))
    if existing.scalar_one_or_none():
        print("Cases already seeded; skipping.")
        return

    base_date = date(2026, 1, 1)

    # ── Planted Pattern 1: Repeat Offender (same person, 4 cases) ──
    repeat_names = [
        ("Ramesh K", 35, "Ramesh Kumar", "KA-01-001"),
        ("R Kumar", 34, "Ramu Kumar", "KA-01-002"),
        ("Ramesh Shetty", 36, "Ramesh Shetty", "KA-01-003"),
        ("R Shetty", 35, "Ranga Shetty", "KA-02-001"),
    ]

    for i, (accused_name, age, complainant, crime_no) in enumerate(repeat_names):
        cm_id = i + 1
        session.add(CaseMaster(
            CaseMasterID=cm_id,
            CrimeNo=crime_no,
            CaseNo=f"FIR/{crime_no}",
            CrimeRegisteredDate=base_date + timedelta(days=i * 30),
            PoliceStationID=5,
            CaseCategoryID=1,
            GravityOffenceID=2,
            CrimeMajorHeadID=1,
            CrimeMinorHeadID=1,
            CaseStatusID=1,
        ))
        session.add(InvOccuranceTime(
            CaseMasterID=cm_id,
            IncidentFromDate=datetime(2026, 1, 1 + i * 30, 20, 0),
            Latitude=12.97 + i * 0.01,
            Longitude=77.59 + i * 0.01,
            BriefFacts=f"Theft of mobile phone. Complainant {complainant} reported the incident.",
        ))
        session.add(ComplainantDetails(
            ComplainantID=i + 1, CaseMasterID=cm_id,
            ComplainantName=complainant, AgeYear=40 + i,
        ))
        session.add(Accused(
            AccusedMasterID=i + 1, CaseMasterID=cm_id,
            AccusedName=accused_name, AgeYear=age,
        ))
        session.add(ActSectionAssociation(
            CaseMasterID=cm_id, ActID="BNS", SectionID="303",
        ))

    # ── Planted Pattern 2: Linked Vehicle (KA-01-MQ-1234 in 3 cases) ──
    vehicle_cases = [
        (5, "KA-01-005", "Bajaj", "Bajaj 2024 theft", 12.95, 77.58),
        (6, "KA-01-006", "Priya", "Bajaj 2024 chain snatching", 12.96, 77.57),
        (7, "KA-01-007", "Suresh", "Bajaj 2024 vehicle theft", 12.94, 77.60),
    ]
    for i, (cm_id, crime_no, complainant, brief, lat, lon) in enumerate(vehicle_cases):
        session.add(CaseMaster(
            CaseMasterID=cm_id,
            CrimeNo=crime_no,
            CaseNo=f"FIR/{crime_no}",
            CrimeRegisteredDate=base_date + timedelta(days=120 + i * 15),
            PoliceStationID=5,
            CaseCategoryID=1,
            GravityOffenceID=2,
            CrimeMajorHeadID=14,
            CrimeMinorHeadID=14,
            CaseStatusID=1,
        ))
        session.add(InvOccuranceTime(
            CaseMasterID=cm_id,
            IncidentFromDate=datetime(2026, 5, 1 + i * 15, 22, 0),
            Latitude=lat, Longitude=lon,
            BriefFacts=brief,
        ))
        session.add(ComplainantDetails(
            ComplainantID=10 + i, CaseMasterID=cm_id,
            ComplainantName=complainant, AgeYear=30 + i * 5,
        ))
        session.add(Accused(
            AccusedMasterID=10 + i, CaseMasterID=cm_id,
            AccusedName=f"Unknown Person {chr(65+i)}", AgeYear=30,
        ))
        session.add(VehicleLink(
            VehicleNumber="KA-01-MQ-1234",
            CaseMasterID=cm_id, Confidence=0.95, Source="witness",
        ))

    # ── Planted Pattern 3: Hotspot — theft spike in Bengaluru Urban ──
    for i in range(5):
        cm_id = 10 + i
        session.add(CaseMaster(
            CaseMasterID=cm_id,
            CrimeNo=f"KA-01-HS-{i+1:03d}",
            CaseNo=f"FIR/KA-01-HS-{i+1:03d}",
            CrimeRegisteredDate=base_date + timedelta(days=45 + i * 3),
            PoliceStationID=5,
            CaseCategoryID=1,
            GravityOffenceID=2,
            CrimeMajorHeadID=1,
            CrimeMinorHeadID=1,
            CaseStatusID=1,
        ))
        session.add(InvOccuranceTime(
            CaseMasterID=cm_id,
            IncidentFromDate=datetime(2026, 2, 15 + i * 3, 19, 30),
            Latitude=12.97, Longitude=77.59,
            BriefFacts="Theft during public transport commute.",
        ))
        session.add(ComplainantDetails(
            ComplainantID=20 + i, CaseMasterID=cm_id,
            ComplainantName=f"Hotspot Complainant {i+1}", AgeYear=25 + i * 3,
        ))
        session.add(Accused(
            AccusedMasterID=20 + i, CaseMasterID=cm_id,
            AccusedName=f"Hotspot Suspect {i+1}", AgeYear=28 + i * 2,
        ))

    # ── Extra random cases for volume (10 more) ──
    extra_details = [
        (15, "KA-01-010", "Murder near market", 5, 5),
        (16, "KA-01-011", "Assault case", 7, 7),
        (17, "KA-03-001", "Cyber fraud", 16, 16),
        (18, "KA-04-001", "Vehicle theft Belagavi", 14, 14),
        (19, "KA-05-001", "Burglary in shop", 2, 2),
        (20, "KA-02-001", "Kidnapping case", 9, 9),
        (21, "KA-06-001", "Property damage", 20, 20),
        (22, "KA-07-001", "NDPS seizure", 17, 17),
        (23, "KA-08-001", "Robbery highway", 3, 3),
        (24, "KA-01-012", "Rioting incident", 12, 12),
    ]
    for i, (cm_id, crime_no, brief, major, minor) in enumerate(extra_details):
        station_id = (i % 31) + 1
        session.add(CaseMaster(
            CaseMasterID=cm_id,
            CrimeNo=crime_no,
            CaseNo=f"FIR/{crime_no}",
            CrimeRegisteredDate=base_date + timedelta(days=90 + i * 7),
            PoliceStationID=station_id,
            CaseCategoryID=1,
            GravityOffenceID=2 if major not in (5,) else 1,
            CrimeMajorHeadID=major,
            CrimeMinorHeadID=minor,
            CaseStatusID=1,
        ))
        session.add(InvOccuranceTime(
            CaseMasterID=cm_id,
            IncidentFromDate=datetime(2026, 4, 1 + i * 7, 18, 0),
            Latitude=12.90 + (i * 0.05),
            Longitude=77.50 + (i * 0.05),
            BriefFacts=brief,
        ))
        session.add(ComplainantDetails(
            ComplainantID=30 + i, CaseMasterID=cm_id,
            ComplainantName=f"Complainant {cm_id}", AgeYear=35,
        ))
        session.add(Accused(
            AccusedMasterID=30 + i, CaseMasterID=cm_id,
            AccusedName=f"Suspect {cm_id}", AgeYear=30,
        ))

    await session.commit()
    print("Seeded 24 sample FIR cases with planted patterns.")


async def seed_entities(session: AsyncSession):
    """Seed PersonEntity records and links for entity resolution demo."""

    existing = await session.execute(select(PersonEntity).limit(1))
    if existing.scalar_one_or_none():
        print("Entities already seeded; skipping.")
        return

    pe = PersonEntity(
        PersonEntityID=1,
        CanonicalName="Ramesh Kumar",
        Gender="M",
        PrimaryDistrictID=5,
    )
    session.add(pe)

    links = [
        PersonEntityLink(PersonEntityID=1, SourceTable="src_Accused", SourceRecordID=1, CaseMasterID=1, Confidence=0.95),
        PersonEntityLink(PersonEntityID=1, SourceTable="src_Accused", SourceRecordID=2, CaseMasterID=2, Confidence=0.85),
        PersonEntityLink(PersonEntityID=1, SourceTable="src_Accused", SourceRecordID=3, CaseMasterID=3, Confidence=0.80),
        PersonEntityLink(PersonEntityID=1, SourceTable="src_Accused", SourceRecordID=4, CaseMasterID=4, Confidence=0.75),
    ]
    for link in links:
        session.add(link)

    pe2 = PersonEntity(
        PersonEntityID=2,
        CanonicalName="Unknown Vehicle Suspect",
        Gender="M",
        PrimaryDistrictID=5,
    )
    session.add(pe2)

    links2 = [
        PersonEntityLink(PersonEntityID=2, SourceTable="src_Accused", SourceRecordID=10, CaseMasterID=5, Confidence=0.50),
        PersonEntityLink(PersonEntityID=2, SourceTable="src_Accused", SourceRecordID=11, CaseMasterID=6, Confidence=0.50),
        PersonEntityLink(PersonEntityID=2, SourceTable="src_Accused", SourceRecordID=12, CaseMasterID=7, Confidence=0.50),
    ]
    for link in links2:
        session.add(link)

    session.add(RelationshipEdge(
        PersonEntityA=1, PersonEntityB=2,
        RelationshipType="shared_vehicle",
        SourceCaseID=5, Confidence=0.60,
    ))

    # Extra entities for graph demo
    for i in range(3, 8):
        session.add(PersonEntity(
            PersonEntityID=i,
            CanonicalName=f"Entity {i}",
            Gender="M" if i % 2 == 0 else "F",
            PrimaryDistrictID=5,
        ))
        session.add(PersonEntityLink(
            PersonEntityID=i, SourceTable="src_Accused",
            SourceRecordID=30 + i, CaseMasterID=15 + i - 3,
            Confidence=0.90,
        ))

    # Link graph edges
    session.add(RelationshipEdge(PersonEntityA=1, PersonEntityB=3, RelationshipType="co_accused", SourceCaseID=15, Confidence=0.85))
    session.add(RelationshipEdge(PersonEntityA=3, PersonEntityB=4, RelationshipType="co_accused", SourceCaseID=16, Confidence=0.80))
    session.add(RelationshipEdge(PersonEntityA=4, PersonEntityB=5, RelationshipType="co_accused", SourceCaseID=17, Confidence=0.75))

    await session.commit()
    print("Seeded entity resolution data with 7 person entities and relationship graph.")


async def main(db_url: str):
    engine = create_async_engine(db_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session_local = sessionmaker(engine, class_=AsyncSession)
    async with async_session_local() as session:
        await seed_lookups(session)
        await seed_cases(session)
        await seed_entities(session)

    await engine.dispose()
    print("\nSeed complete. 24 cases, 7 entities, and all lookup tables populated.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed demo data for Berunda")
    parser.add_argument("--db-url", default=DB_URL, help="Async database URL")
    args = parser.parse_args()
    asyncio.run(main(args.db_url))
