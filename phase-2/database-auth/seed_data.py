"""Seed all lookups and initial users for the Berunda platform.

Usage:
    python -c "from seed_data import seed_all; seed_all()"
    python -c "from seed_data import seed_all; from sqlalchemy import create_engine; from sqlalchemy.orm import Session; engine = create_engine('sqlite:///berunda.db'); seed_all(Session(bind=engine))"
"""

import bcrypt
from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.orm import Session as SASession

from src.config import settings
from src.models.auth_models import User, Session as AuthSession, Permission
from src.models.src_models import (
    Act, Section, CrimeHead, CrimeSubHead, CrimeHeadActSection,
    CaseCategory, GravityOffence, CaseStatusMaster, State, District,
    Unit, UnitType, Court, Employee, Rank, Designation,
    OccupationMaster, ReligionMaster, CasteMaster,
)

KARNATAKA_STATE_ID = 1

DISTRICTS = [
    (1, "Bengaluru Urban"),
    (2, "Bengaluru Rural"),
    (3, "Mysuru"),
    (4, "Belagavi"),
    (5, "Dakshina Kannada"),
    (6, "Kalaburagi"),
    (7, "Tumakuru"),
    (8, "Shivamogga"),
    (9, "Hubballi-Dharwad"),
    (10, "Ballari"),
]

POLICE_STATIONS = {
    1: ["MG Road PS", "Whitefield PS", "Koramangala PS", "Jayanagar PS"],
    2: ["Devanahalli PS", "Nelamangala PS", "Doddaballapura PS"],
    3: ["Kuvempunagar PS", "Vijayanagar PS", "Nazarbad PS"],
    4: ["Belagavi City PS", "Tilakwadi PS", "Camp PS"],
    5: ["Mangaluru City PS", "Ullal PS", "Bunder PS"],
    6: ["Kalaburagi City PS", "Shahabad PS"],
    7: ["Tumakuru City PS", "Gubbi PS"],
    8: ["Shivamogga City PS", "Bhadravati PS"],
    9: ["Hubballi PS", "Dharwad PS"],
    10: ["Ballari City PS", "Kampli PS"],
}

CASE_STATUSES = [
    (1, "Under Investigation"),
    (2, "Chargesheet Filed"),
    (3, "Trial"),
    (4, "Closed"),
    (5, "Acquitted"),
    (6, "Convicted"),
]

CASE_CATEGORIES = [(1, "FIR"), (2, "UDR"), (3, "PAR"), (4, "Zero FIR")]

CRIME_HEADS = [
    (1, "Property Offences"),
    (2, "Violent Crimes"),
    (3, "Cyber Crimes"),
    (4, "Drugs / NDPS"),
    (5, "Arms Act Violation"),
    (6, "Economic Offences"),
    (7, "Missing Person"),
    (8, "Other"),
]

CRIME_SUB_HEADS = [
    (1, 1, "Theft"),
    (2, 1, "Burglary"),
    (3, 1, "Robbery"),
    (4, 1, "Dacoity"),
    (5, 2, "Murder"),
    (6, 2, "Attempt to Murder"),
    (7, 2, "Hurt / Assault"),
    (8, 2, "Rape / Sexual Assault"),
    (9, 2, "Kidnapping"),
    (10, 3, "Hacking"),
    (11, 3, "Online Fraud"),
    (12, 4, "NDPS Cultivation"),
    (13, 4, "NDPS Possession"),
    (14, 5, "Arms Possession"),
    (15, 6, "Cheating / Fraud"),
    (16, 6, "Counterfeiting"),
]

ACTS = [
    ("BNS", "Bharatiya Nyaya Sanhita 2023", "BNS"),
    ("IPC", "Indian Penal Code 1860", "IPC"),
    ("IT_Act", "Information Technology Act 2000", "IT Act"),
    ("NDPS", "Narcotic Drugs and Psychotropic Substances Act 1985", "NDPS"),
    ("Arms_Act", "Arms Act 1959", "Arms Act"),
]

SECTIONS = [
    ("BNS", "101", "Murder"),
    ("BNS", "109", "Attempt to murder"),
    ("BNS", "115", "Voluntarily causing hurt"),
    ("BNS", "137", "Rape"),
    ("BNS", "140", "Kidnapping"),
    ("BNS", "191", "Rioting"),
    ("BNS", "303", "Theft"),
    ("BNS", "305", "Theft in dwelling house"),
    ("BNS", "308", "Extortion"),
    ("BNS", "309", "Robbery"),
    ("BNS", "310", "Dacoity"),
    ("BNS", "316", "Cheating"),
    ("BNS", "329", "Criminal trespass"),
    ("BNS", "331", "Burglary"),
    ("BNS", "336", "Mischief"),
    ("IPC", "302", "Punishment for murder"),
    ("IPC", "307", "Attempt to murder"),
    ("IPC", "323", "Punishment for voluntarily causing hurt"),
    ("IPC", "376", "Punishment for rape"),
    ("IPC", "379", "Theft"),
    ("IPC", "420", "Cheating and dishonestly inducing delivery of property"),
    ("IT_Act", "66", "Computer related offences"),
    ("IT_Act", "67", "Publishing obscene material in electronic form"),
    ("NDPS", "20", "Cultivation of cannabis plant"),
    ("NDPS", "21", "Manufacture, possession, sale of drugs"),
    ("Arms_Act", "25", "Licence for arms and ammunition"),
    ("Arms_Act", "27", "Punishment for using arms"),
]

CRIME_HEAD_ACT_SECTIONS = [
    (1, "BNS", "303"),
    (1, "IPC", "379"),
    (2, "BNS", "309"),
    (2, "BNS", "310"),
    (3, "IT_Act", "66"),
    (4, "NDPS", "20"),
    (4, "NDPS", "21"),
    (5, "Arms_Act", "25"),
    (6, "BNS", "316"),
    (6, "IPC", "420"),
    (7, "BNS", "101"),
    (7, "IPC", "302"),
    (8, "BNS", "115"),
]


def _hash(pw: str) -> str:
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _idempotent(db: SASession, model, condition: dict) -> bool:
    existing = db.query(model).filter_by(**condition).first()
    return existing is not None


def seed_all(db: SASession | None = None) -> None:
    if db is None:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        engine = create_engine(settings.DATABASE_URL.replace("+aiosqlite", ""))
        session_factory = sessionmaker(bind=engine)
        db = session_factory()
        close_session = True
    else:
        close_session = False

    try:
        _seed_state(db)
        _seed_districts(db)
        _seed_unit_types(db)
        _seed_police_stations(db)
        _seed_case_statuses(db)
        _seed_case_categories(db)
        _seed_crime_heads(db)
        _seed_crime_sub_heads(db)
        _seed_acts(db)
        _seed_sections(db)
        _seed_crime_head_act_sections(db)
        _seed_gravity_offences(db)
        _seed_ranks_and_designations(db)
        _seed_occupations_religions_castes(db)
        _seed_courts(db)
        _seed_employees(db)
        _seed_users(db)
        _seed_permissions(db)
        db.commit()
        print("Seed data committed successfully.")
    except Exception:
        db.rollback()
        raise
    finally:
        if close_session:
            db.close()


def _seed_state(db: SASession) -> None:
    if _idempotent(db, State, {"StateID": KARNATAKA_STATE_ID}):
        return
    db.add(State(StateID=KARNATAKA_STATE_ID, StateName="Karnataka", NationalityID=1, Active=True))


def _seed_districts(db: SASession) -> None:
    if _idempotent(db, District, {"DistrictID": 1}):
        return
    for did, dname in DISTRICTS:
        db.add(District(DistrictID=did, DistrictName=dname, StateID=KARNATAKA_STATE_ID, Active=True))


def _seed_unit_types(db: SASession) -> None:
    if _idempotent(db, UnitType, {"UnitTypeID": 1}):
        return
    db.add_all([
        UnitType(UnitTypeID=1, UnitTypeName="Police Station", CityDistState="District", Hierarchy=3),
        UnitType(UnitTypeID=2, UnitTypeName="Commissionerate", CityDistState="City", Hierarchy=2),
        UnitType(UnitTypeID=3, UnitTypeName="District Office", CityDistState="District", Hierarchy=1),
        UnitType(UnitTypeID=4, UnitTypeName="State HQ", CityDistState="State", Hierarchy=0),
    ])


def _seed_police_stations(db: SASession) -> None:
    if _idempotent(db, Unit, {"UnitID": 1}):
        return
    uid = 1
    for did, stations in POLICE_STATIONS.items():
        for sname in stations:
            db.add(Unit(UnitID=uid, UnitName=sname, TypeID=1, DistrictID=did, StateID=KARNATAKA_STATE_ID, Active=True))
            uid += 1


def _seed_case_statuses(db: SASession) -> None:
    if _idempotent(db, CaseStatusMaster, {"CaseStatusID": 1}):
        return
    for sid, sname in CASE_STATUSES:
        db.add(CaseStatusMaster(CaseStatusID=sid, CaseStatusName=sname, Active=True))


def _seed_case_categories(db: SASession) -> None:
    if _idempotent(db, CaseCategory, {"CaseCategoryID": 1}):
        return
    for cid, val in CASE_CATEGORIES:
        db.add(CaseCategory(CaseCategoryID=cid, LookupValue=val, Active=True))


def _seed_crime_heads(db: SASession) -> None:
    if _idempotent(db, CrimeHead, {"CrimeHeadID": 1}):
        return
    for cid, cname in CRIME_HEADS:
        db.add(CrimeHead(CrimeHeadID=cid, CrimeGroupName=cname, Active=True))


def _seed_crime_sub_heads(db: SASession) -> None:
    if _idempotent(db, CrimeSubHead, {"CrimeSubHeadID": 1}):
        return
    for sid, cid, cname in CRIME_SUB_HEADS:
        db.add(CrimeSubHead(CrimeSubHeadID=sid, CrimeHeadID=cid, CrimeHeadName=cname, SeqID=sid, Active=True))


def _seed_acts(db: SASession) -> None:
    if _idempotent(db, Act, {"ActCode": "BNS"}):
        return
    for code, desc, short in ACTS:
        db.add(Act(ActCode=code, ActDescription=desc, ShortName=short, Active=True))


def _seed_sections(db: SASession) -> None:
    if _idempotent(db, Section, {"ActCode": "BNS", "SectionCode": "101"}):
        return
    for act, code, desc in SECTIONS:
        db.add(Section(ActCode=act, SectionCode=code, SectionDescription=desc, Active=True))


def _seed_crime_head_act_sections(db: SASession) -> None:
    if _idempotent(db, CrimeHeadActSection, {"CrimeHeadID": 1, "ActCode": "BNS"}):
        return
    for ch_id, act, sec in CRIME_HEAD_ACT_SECTIONS:
        db.add(CrimeHeadActSection(CrimeHeadID=ch_id, ActCode=act, SectionCode=sec))


def _seed_gravity_offences(db: SASession) -> None:
    if _idempotent(db, GravityOffence, {"GravityOffenceID": 1}):
        return
    db.add_all([
        GravityOffence(GravityOffenceID=1, LookupValue="Heinous", Active=True),
        GravityOffence(GravityOffenceID=2, LookupValue="Non-Heinous", Active=True),
    ])


def _seed_ranks_and_designations(db: SASession) -> None:
    if _idempotent(db, Rank, {"RankID": 1}):
        return
    db.add_all([
        Rank(RankID=1, RankName="Police Constable", Hierarchy=1, Active=True),
        Rank(RankID=2, RankName="Head Constable", Hierarchy=2, Active=True),
        Rank(RankID=3, RankName="Assistant Sub-Inspector", Hierarchy=3, Active=True),
        Rank(RankID=4, RankName="Sub-Inspector", Hierarchy=4, Active=True),
        Rank(RankID=5, RankName="Inspector", Hierarchy=5, Active=True),
        Rank(RankID=6, RankName="Deputy Superintendent of Police", Hierarchy=6, Active=True),
        Rank(RankID=7, RankName="Superintendent of Police", Hierarchy=7, Active=True),
    ])
    db.add_all([
        Designation(DesignationID=1, DesignationName="SHO", Active=True, SortOrder=1),
        Designation(DesignationID=2, DesignationName="IO", Active=True, SortOrder=2),
        Designation(DesignationID=3, DesignationName="Addl. SP", Active=True, SortOrder=3),
        Designation(DesignationID=4, DesignationName="SP", Active=True, SortOrder=4),
    ])


def _seed_occupations_religions_castes(db: SASession) -> None:
    if _idempotent(db, OccupationMaster, {"OccupationID": 1}):
        return
    for oid, oname in [(1, "Private Employee"), (2, "Government Employee"), (3, "Business"), (4, "Farmer"), (5, "Student"), (6, "Unemployed"), (7, "Retired"), (8, "Other")]:
        db.add(OccupationMaster(OccupationID=oid, OccupationName=oname, Active=True))
    for rid, rname in [(1, "Hindu"), (2, "Muslim"), (3, "Christian"), (4, "Sikh"), (5, "Other")]:
        db.add(ReligionMaster(ReligionID=rid, ReligionName=rname, Active=True))
    for cid, cname in [(1, "General"), (2, "OBC"), (3, "SC"), (4, "ST"), (5, "Other")]:
        db.add(CasteMaster(caste_master_id=cid, caste_master_name=cname, Active=True))


def _seed_courts(db: SASession) -> None:
    if _idempotent(db, Court, {"CourtID": 1}):
        return
    db.add_all([
        Court(CourtID=1, CourtName="JMFC Bengaluru", DistrictID=1, StateID=KARNATAKA_STATE_ID, Active=True),
        Court(CourtID=2, CourtName="CJM Bengaluru", DistrictID=1, StateID=KARNATAKA_STATE_ID, Active=True),
        Court(CourtID=3, CourtName="Session Court Bengaluru", DistrictID=1, StateID=KARNATAKA_STATE_ID, Active=True),
        Court(CourtID=4, CourtName="JMFC Mysuru", DistrictID=3, StateID=KARNATAKA_STATE_ID, Active=True),
        Court(CourtID=5, CourtName="JMFC Mangaluru", DistrictID=5, StateID=KARNATAKA_STATE_ID, Active=True),
    ])


def _seed_employees(db: SASession) -> None:
    if _idempotent(db, Employee, {"EmployeeID": 1}):
        return
    db.add_all([
        Employee(EmployeeID=1, DistrictID=1, UnitID=1, RankID=5, DesignationID=1, KGID="KG001", FirstName="Arun", AppointmentDate=datetime(2020, 1, 1, tzinfo=timezone.utc)),
        Employee(EmployeeID=2, DistrictID=1, UnitID=1, RankID=4, DesignationID=2, KGID="KG002", FirstName="Kumar", AppointmentDate=datetime(2021, 6, 1, tzinfo=timezone.utc)),
        Employee(EmployeeID=3, DistrictID=3, UnitID=9, RankID=5, DesignationID=1, KGID="KG003", FirstName="Mahesh", AppointmentDate=datetime(2020, 3, 15, tzinfo=timezone.utc)),
        Employee(EmployeeID=4, DistrictID=3, UnitID=9, RankID=4, DesignationID=2, KGID="KG004", FirstName="Suresh", AppointmentDate=datetime(2021, 9, 1, tzinfo=timezone.utc)),
    ])


def _seed_users(db: SASession) -> None:
    if _idempotent(db, User, {"Email": "admin@berunda.gov"}):
        return

    admin_pw = _hash(settings.INITIAL_ADMIN_PASSWORD or "Admin@123")
    officer_pw = _hash(settings.INITIAL_ANALYST_PASSWORD or "Officer@123")
    analyst_pw = _hash("Analyst@123")

    db.add_all([
        User(Email="admin@berunda.gov", HashedPassword=admin_pw, Role="admin", DistrictID=1, IsActive=True),
        User(Email="officer@ksp.karnataka.gov.in", HashedPassword=officer_pw, Role="officer", DistrictID=1, IsActive=True),
        User(Email="analyst@berunda.gov", HashedPassword=analyst_pw, Role="analyst", DistrictID=1, IsActive=True),
        User(Email="officer.mysuru@ksp.karnataka.gov.in", HashedPassword=officer_pw, Role="officer", DistrictID=3, IsActive=True),
        User(Email="officer.belagavi@ksp.karnataka.gov.in", HashedPassword=officer_pw, Role="officer", DistrictID=4, IsActive=True),
    ])


def _seed_permissions(db: SASession) -> None:
    if _idempotent(db, Permission, {"PermissionID": 1}):
        return

    permissions = [
        ("admin", "users", "read"), ("admin", "users", "write"), ("admin", "users", "delete"),
        ("admin", "cases", "read"), ("admin", "cases", "write"), ("admin", "cases", "delete"),
        ("admin", "reports", "read"), ("admin", "reports", "write"),
        ("admin", "analytics", "read"),
        ("admin", "permissions", "read"), ("admin", "permissions", "write"),
        ("officer", "cases", "read"), ("officer", "cases", "write"),
        ("officer", "reports", "read"),
        ("analyst", "cases", "read"),
        ("analyst", "reports", "read"),
        ("analyst", "analytics", "read"),
    ]
    for i, (role, resource, action) in enumerate(permissions, start=1):
        db.add(Permission(PermissionID=i, Role=role, Resource=resource, Action=action))


if __name__ == "__main__":
    seed_all()
