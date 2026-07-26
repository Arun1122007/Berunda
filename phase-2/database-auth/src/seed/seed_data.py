from datetime import datetime, timezone

from sqlalchemy.orm import Session as SASession

from ..auth.password import hash_password
from ..models import (
    Accused,
    CaseMaster,
    CaseStatusMaster,
    ComplainantDetails,
    CrimeHead,
    District,
    GravityOffence,
    InvOccuranceTime,
    Unit,
    User,
    Victim,
)


def seed_database(db: SASession) -> None:
    _seed_districts(db)
    _seed_units(db)
    _seed_crime_heads(db)
    _seed_case_statuses(db)
    _seed_gravity_offences(db)
    _seed_users(db)
    _seed_demo_cases(db)
    db.commit()


def _seed_districts(db: SASession) -> None:
    existing = db.query(District).count()
    if existing > 0:
        return
    db.add_all([
        District(DistrictID=1, DistrictName="Bengaluru Urban", StateID=1),
        District(DistrictID=2, DistrictName="Bengaluru Rural", StateID=1),
    ])
    db.flush()


def _seed_units(db: SASession) -> None:
    existing = db.query(Unit).count()
    if existing > 0:
        return
    db.add_all([
        Unit(UnitID=1, UnitName="MG Road Police Station", DistrictID=1, TypeID=1),
        Unit(UnitID=2, UnitName="Whitefield Police Station", DistrictID=1, TypeID=1),
        Unit(UnitID=3, UnitName="Devanahalli Police Station", DistrictID=2, TypeID=1),
        Unit(UnitID=4, UnitName="Nelamangala Police Station", DistrictID=2, TypeID=1),
    ])
    db.flush()


def _seed_crime_heads(db: SASession) -> None:
    existing = db.query(CrimeHead).count()
    if existing > 0:
        return
    db.add_all([
        CrimeHead(CrimeHeadID=1, CrimeGroupName="Theft"),
        CrimeHead(CrimeHeadID=2, CrimeGroupName="Assault"),
        CrimeHead(CrimeHeadID=3, CrimeGroupName="Burglary"),
    ])
    db.flush()


def _seed_case_statuses(db: SASession) -> None:
    existing = db.query(CaseStatusMaster).count()
    if existing > 0:
        return
    db.add_all([
        CaseStatusMaster(CaseStatusID=1, CaseStatusName="Under Investigation"),
        CaseStatusMaster(CaseStatusID=2, CaseStatusName="Charge Sheeted"),
        CaseStatusMaster(CaseStatusID=3, CaseStatusName="Closed"),
    ])
    db.flush()


def _seed_gravity_offences(db: SASession) -> None:
    existing = db.query(GravityOffence).count()
    if existing > 0:
        return
    db.add_all([
        GravityOffence(GravityOffenceID=1, LookupValue="Heinous"),
        GravityOffence(GravityOffenceID=2, LookupValue="Non-Heinous"),
        GravityOffence(GravityOffenceID=3, LookupValue="Minor"),
    ])
    db.flush()


def _seed_users(db: SASession) -> None:
    existing = db.query(User).count()
    if existing > 0:
        return
    db.add_all([
        User(
            UserID=1, Email="admin@berunda.gov",
            HashedPassword=hash_password("admin123"),
            Role="admin", DistrictID=1, IsActive=True,
        ),
        User(
            UserID=2, Email="officer@ksp.gov.in",
            HashedPassword=hash_password("officer123"),
            Role="officer", DistrictID=1, IsActive=True,
        ),
    ])
    db.flush()


def _seed_demo_cases(db: SASession) -> None:
    existing = db.query(CaseMaster).count()
    if existing > 0:
        return

    now = datetime.now(timezone.utc)

    case1 = CaseMaster(
        CaseMasterID=1, CrimeNo="BNG-CITY-001-2026",
        CaseNo="FIR/001/2026", CrimeRegisteredDate=now,
        PoliceStationID=1, CaseCategoryID=1,
        GravityOffenceID=2, CrimeMajorHeadID=1,
        CrimeMinorHeadID=1, CaseStatusID=1,
        IncidentFromDate=now, IncidentToDate=now,
    )
    case2 = CaseMaster(
        CaseMasterID=2, CrimeNo="BNG-CITY-002-2026",
        CaseNo="FIR/002/2026", CrimeRegisteredDate=now,
        PoliceStationID=2, CaseCategoryID=1,
        GravityOffenceID=1, CrimeMajorHeadID=2,
        CrimeMinorHeadID=2, CaseStatusID=2,
        IncidentFromDate=now, IncidentToDate=now,
    )
    case3 = CaseMaster(
        CaseMasterID=3, CrimeNo="BNG-RURAL-001-2026",
        CaseNo="FIR/003/2026", CrimeRegisteredDate=now,
        PoliceStationID=3, CaseCategoryID=2,
        GravityOffenceID=3, CrimeMajorHeadID=3,
        CrimeMinorHeadID=3, CaseStatusID=1,
        IncidentFromDate=now, IncidentToDate=now,
    )
    db.add_all([case1, case2, case3])
    db.flush()

    db.add_all([
        InvOccuranceTime(
            CaseMasterID=1,
            BriefFacts="Stolen wallet from MG Road footpath",
            Latitude=12.9716, Longitude=77.5946,
        ),
        InvOccuranceTime(
            CaseMasterID=2,
            BriefFacts="Assault reported outside Whitefield mall",
            Latitude=12.9698, Longitude=77.7500,
        ),
        InvOccuranceTime(
            CaseMasterID=3,
            BriefFacts="Burglary at Devanahalli residence",
            Latitude=13.2468, Longitude=77.7107,
        ),
    ])
    db.flush()

    db.add_all([
        ComplainantDetails(
            ComplainantID=1, CaseMasterID=1,
            Name="Ravi Kumar", Age=34, OccupationID=1,
            ReligionID=1, CasteID=1,
        ),
        ComplainantDetails(
            ComplainantID=2, CaseMasterID=2,
            Name="Sneha Patel", Age=28, OccupationID=2,
            ReligionID=2, CasteID=2,
        ),
        ComplainantDetails(
            ComplainantID=3, CaseMasterID=3,
            Name="Venkatesh Gowda", Age=45, OccupationID=3,
            ReligionID=1, CasteID=3,
        ),
    ])
    db.flush()

    db.add_all([
        Victim(VictimMasterID=1, CaseMasterID=1, Name="Ravi Kumar", Age=34, GenderID=1),
        Victim(VictimMasterID=2, CaseMasterID=2, Name="Sneha Patel", Age=28, GenderID=2),
        Victim(VictimMasterID=3, CaseMasterID=3, Name="Venkatesh Gowda", Age=45, GenderID=1),
    ])
    db.flush()

    db.add_all([
        Accused(AccusedMasterID=1, CaseMasterID=1, Name="Unknown Person", Age=0, PersonID=None),
        Accused(AccusedMasterID=2, CaseMasterID=2, Name="Arun S", Age=30, PersonID=1),
        Accused(AccusedMasterID=3, CaseMasterID=3, Name="Manjunath K", Age=42, PersonID=2),
    ])
    db.flush()
