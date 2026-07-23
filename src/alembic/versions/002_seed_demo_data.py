# ruff: noqa: E501, E731
"""seed demo data for hackathon demonstration.

Revision ID: 002
Revises: 001
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

import sqlalchemy as sa

from alembic import op

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    # ── Skip if already seeded ──
    existing = conn.execute(sa.text("SELECT 1 FROM src_State LIMIT 1")).scalar()
    if existing:
        print("Data already seeded; skipping.")
        return

    # ── State ──
    conn.execute(
        sa.text(
            "INSERT INTO src_State (StateID, StateName, NationalityID, Active) VALUES (1, 'Karnataka', 1, true)"
        )
    )

    # ── Districts ──
    districts = [
        (1, "Bagalkote"),
        (2, "Ballari"),
        (3, "Belagavi"),
        (4, "Bengaluru Rural"),
        (5, "Bengaluru Urban"),
        (6, "Bidar"),
        (7, "Chamarajanagara"),
        (8, "Chikkaballapura"),
        (9, "Chikkamagaluru"),
        (10, "Chitradurga"),
        (11, "Dakshina Kannada"),
        (12, "Davanagere"),
        (13, "Dharwad"),
        (14, "Gadag"),
        (15, "Hassan"),
        (16, "Haveri"),
        (17, "Kalaburagi"),
        (18, "Kodagu"),
        (19, "Kolar"),
        (20, "Koppala"),
        (21, "Mandya"),
        (22, "Mysuru"),
        (23, "Raichur"),
        (24, "Ramanagara"),
        (25, "Shivamogga"),
        (26, "Tumakuru"),
        (27, "Udupi"),
        (28, "Uttara Kannada"),
        (29, "Vijayapura"),
        (30, "Yadgiri"),
        (31, "Bengaluru City"),
    ]
    for did, dname in districts:
        conn.execute(
            sa.text(
                "INSERT INTO src_District (DistrictID, DistrictName, StateID, Active) VALUES (:id, :name, 1, true)"
            ),
            {"id": did, "name": dname},
        )

    # ── Unit Types ──
    conn.execute(
        sa.text(
            "INSERT INTO src_UnitType (UnitTypeID, UnitTypeName, CityDistState) VALUES (1, 'Commissionerate', 'City')"
        )
    )
    conn.execute(
        sa.text(
            "INSERT INTO src_UnitType (UnitTypeID, UnitTypeName, CityDistState) VALUES (2, 'Police Station', 'District')"
        )
    )
    conn.execute(
        sa.text(
            "INSERT INTO src_UnitType (UnitTypeID, UnitTypeName, CityDistState) VALUES (3, 'District Office', 'District')"
        )
    )

    # ── Police Stations ──
    for i in range(1, 32):
        conn.execute(
            sa.text("""
            INSERT INTO src_Unit (UnitID, UnitName, TypeID, DistrictID, StateID, Active)
            VALUES (:id, :name, 2, :did, 1, true)"""),
            {"id": i, "name": f"PS-{i:02d}", "did": i},
        )

    # ── Acts ──
    conn.execute(
        sa.text(
            "INSERT INTO src_Act (ActCode, ActDescription, ShortName, Active) VALUES ('BNS', 'Bharatiya Nyaya Sanhita 2023', 'BNS', true)"
        )
    )
    conn.execute(
        sa.text(
            "INSERT INTO src_Act (ActCode, ActDescription, ShortName, Active) VALUES ('IT_Act', 'Information Technology Act 2000', 'IT Act', true)"
        )
    )
    conn.execute(
        sa.text(
            "INSERT INTO src_Act (ActCode, ActDescription, ShortName, Active) VALUES ('NDPS', 'Narcotic Drugs and Psychotropic Substances Act', 'NDPS', true)"
        )
    )
    conn.execute(
        sa.text(
            "INSERT INTO src_Act (ActCode, ActDescription, ShortName, Active) VALUES ('Arms_Act', 'Arms Act 1959', 'Arms Act', true)"
        )
    )

    # ── Sections ──
    sections = [
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
        ("IT_Act", "66", "Computer related offences"),
        ("IT_Act", "67", "Publishing obscene material"),
        ("NDPS", "20", "Cultivation etc."),
        ("NDPS", "21", "Manufacture etc."),
        ("Arms_Act", "25", "Arms possession"),
        ("Arms_Act", "27", "Arms use"),
    ]
    for act, code, desc in sections:
        conn.execute(
            sa.text(
                "INSERT INTO src_Section (ActCode, SectionCode, SectionDescription, Active) VALUES (:act, :code, :desc, true)"
            ),
            {"act": act, "code": code, "desc": desc},
        )

    # ── Crime Heads ──
    for cid, cname in [
        (1, "Theft"),
        (2, "Burglary"),
        (3, "Robbery"),
        (4, "Dacoity"),
        (5, "Murder"),
        (6, "Attempt to Murder"),
        (7, "Hurt / Assault"),
        (8, "Rape / Sexual Assault"),
        (9, "Kidnapping"),
        (10, "Cheating / Fraud"),
        (11, "Criminal Trespass"),
        (12, "Rioting"),
        (13, "Arson"),
        (14, "Motor Vehicle Theft"),
        (15, "Extortion"),
        (16, "Cyber Crime"),
        (17, "NDPS Violation"),
        (18, "Arms Act Violation"),
        (19, "Missing Person"),
        (20, "Property Damage"),
    ]:
        conn.execute(
            sa.text(
                "INSERT INTO src_CrimeHead (CrimeHeadID, CrimeGroupName, Active) VALUES (:id, :name, true)"
            ),
            {"id": cid, "name": cname},
        )
        conn.execute(
            sa.text(
                "INSERT INTO src_CrimeSubHead (CrimeSubHeadID, CrimeHeadID, CrimeHeadName, SeqID, Active) VALUES (:id, :id, :name, 1, true)"
            ),
            {"id": cid, "name": cname},
        )

    ch_assoc = [
        (1, "BNS", "303"),
        (2, "BNS", "331"),
        (3, "BNS", "309"),
        (4, "BNS", "310"),
        (5, "BNS", "101"),
        (6, "BNS", "109"),
        (7, "BNS", "115"),
        (8, "BNS", "137"),
        (9, "BNS", "140"),
        (10, "BNS", "316"),
        (11, "BNS", "329"),
        (12, "BNS", "191"),
        (13, "BNS", "336"),
        (14, "BNS", "303"),
        (15, "BNS", "308"),
        (16, "IT_Act", "66"),
        (17, "NDPS", "20"),
        (18, "Arms_Act", "25"),
        (19, "BNS", "101"),
        (20, "BNS", "336"),
    ]
    for ch_id, act, sec in ch_assoc:
        conn.execute(
            sa.text(
                "INSERT INTO src_CrimeHeadActSection (CrimeHeadID, ActCode, SectionCode) VALUES (:cid, :act, :sec)"
            ),
            {"cid": ch_id, "act": act, "sec": sec},
        )

    # ── Case Categories ──
    for cid, val in [(1, "FIR"), (2, "UDR"), (3, "PAR"), (4, "Zero FIR")]:
        conn.execute(
            sa.text(
                "INSERT INTO src_CaseCategory (CaseCategoryID, LookupValue, Active) VALUES (:id, :val, true)"
            ),
            {"id": cid, "val": val},
        )

    # ── Gravity Offences, Case Statuses ──
    conn.execute(
        sa.text(
            "INSERT INTO src_GravityOffence (GravityOffenceID, LookupValue, Active) VALUES (1, 'Heinous', true)"
        )
    )
    conn.execute(
        sa.text(
            "INSERT INTO src_GravityOffence (GravityOffenceID, LookupValue, Active) VALUES (2, 'Non-Heinous', true)"
        )
    )
    for sid, sname in [
        (1, "Under Investigation"),
        (2, "Charge Sheeted"),
        (3, "Pending Trial"),
        (4, "Convicted"),
        (5, "Acquitted"),
    ]:
        conn.execute(
            sa.text(
                "INSERT INTO src_CaseStatusMaster (CaseStatusID, CaseStatusName, Active) VALUES (:id, :name, true)"
            ),
            {"id": sid, "name": sname},
        )

    # ── Ranks, Designations ──
    conn.execute(
        sa.text(
            "INSERT INTO src_Rank (RankID, RankName, Hierarchy) VALUES (1, 'Police Constable', 1)"
        )
    )
    conn.execute(
        sa.text("INSERT INTO src_Rank (RankID, RankName, Hierarchy) VALUES (2, 'Sub-Inspector', 5)")
    )
    conn.execute(
        sa.text("INSERT INTO src_Rank (RankID, RankName, Hierarchy) VALUES (3, 'Inspector', 7)")
    )
    conn.execute(
        sa.text(
            "INSERT INTO src_Designation (DesignationID, DesignationName, SortOrder) VALUES (1, 'SHO', 1)"
        )
    )
    conn.execute(
        sa.text(
            "INSERT INTO src_Designation (DesignationID, DesignationName, SortOrder) VALUES (2, 'IO', 2)"
        )
    )

    # ── Employees ──
    conn.execute(
        sa.text(
            "INSERT INTO src_Employee (EmployeeID, DistrictID, UnitID, RankID, DesignationID, KGID, FirstName, AppointmentDate) VALUES (1, 5, 1, 3, 1, 'KG001', 'Arun', '2020-01-01')"
        )
    )
    conn.execute(
        sa.text(
            "INSERT INTO src_Employee (EmployeeID, DistrictID, UnitID, RankID, DesignationID, KGID, FirstName, AppointmentDate) VALUES (2, 5, 1, 2, 2, 'KG002', 'Kumar', '2021-06-01')"
        )
    )

    # ── Occupations, Religions, Courts ──
    for oid, oname in [
        (1, "Private Employee"),
        (2, "Government Employee"),
        (3, "Business"),
        (4, "Farmer"),
        (5, "Student"),
        (6, "Unemployed"),
        (7, "Retired"),
        (8, "Other"),
    ]:
        conn.execute(
            sa.text(
                "INSERT INTO src_OccupationMaster (OccupationID, OccupationName, Active) VALUES (:id, :name, true)"
            ),
            {"id": oid, "name": oname},
        )
    for rid, rname in [(1, "Hindu"), (2, "Muslim"), (3, "Christian"), (4, "Sikh"), (5, "Other")]:
        conn.execute(
            sa.text(
                "INSERT INTO src_ReligionMaster (ReligionID, ReligionName, Active) VALUES (:id, :name, true)"
            ),
            {"id": rid, "name": rname},
        )
    for cid, cname, did in [
        (1, "JMFC Bengaluru", 5),
        (2, "CJM Bengaluru", 5),
        (3, "Session Court Bengaluru", 5),
        (4, "JMFC Mysuru", 22),
    ]:
        conn.execute(
            sa.text(
                "INSERT INTO src_Court (CourtID, CourtName, DistrictID, StateID, Active) VALUES (:id, :name, :did, 1, true)"
            ),
            {"id": cid, "name": cname, "did": did},
        )

    # ── Sample FIR Cases ──
    base = date(2026, 1, 1)

    def _ts(days: int) -> datetime:
        return datetime.combine(base + timedelta(days=days), datetime.min.time())

    case_data = [
        # Repeat offender cases (CM 1-4)
        (1, "KA-01-001", 0, 12.97, 77.59, "Theft of mobile phone"),
        (2, "KA-01-002", 30, 12.98, 77.60, "Theft of wallet"),
        (3, "KA-01-003", 60, 12.99, 77.61, "Theft of bicycle"),
        (4, "KA-02-001", 90, 12.96, 77.58, "Theft of jewellery"),
        # Vehicle-linked cases (CM 5-7)
        (5, "KA-01-005", 120, 12.95, 77.58, "Bajaj 2024 theft"),
        (6, "KA-01-006", 135, 12.96, 77.57, "Chain snatching"),
        (7, "KA-01-007", 150, 12.94, 77.60, "Vehicle theft"),
        # Hotspot spike (CM 10-14)
        (10, "KA-01-HS-001", 45, 12.97, 77.59, "Theft during commute"),
        (11, "KA-01-HS-002", 48, 12.97, 77.59, "Theft at bus stop"),
        (12, "KA-01-HS-003", 51, 12.97, 77.59, "Mobile theft"),
        (13, "KA-01-HS-004", 54, 12.97, 77.59, "Pickpocketing"),
        (14, "KA-01-HS-005", 57, 12.97, 77.59, "Bag snatching"),
        # Extra cases (CM 15-24)
        (15, "KA-01-010", 90, 12.90, 77.50, "Murder near market"),
        (16, "KA-01-011", 97, 12.95, 77.55, "Assault case"),
        (17, "KA-03-001", 104, 13.00, 77.60, "Cyber fraud"),
        (18, "KA-04-001", 111, 12.85, 77.45, "Vehicle theft Belagavi"),
        (19, "KA-05-001", 118, 12.80, 77.40, "Burglary in shop"),
        (20, "KA-09-001", 125, 12.75, 77.35, "Kidnapping case"),
        (21, "KA-06-001", 132, 13.05, 77.65, "Property damage"),
        (22, "KA-07-001", 139, 13.10, 77.70, "NDPS seizure"),
        (23, "KA-08-001", 146, 13.15, 77.75, "Robbery highway"),
        (24, "KA-01-012", 153, 12.92, 77.52, "Rioting incident"),
    ]
    for cm_id, crime_no, day_offset, lat, lon, brief in case_data:
        major = (
            1
            if "Theft" in brief or "Mobile" in brief or "Pickpocket" in brief or "Bag" in brief
            else 14
            if "Vehicle" in brief
            else 5
            if "Murder" in brief
            else 7
            if "Assault" in brief
            else 16
            if "Cyber" in brief
            else 2
            if "Burglary" in brief
            else 9
            if "Kidnapping" in brief
            else 20
            if "Property" in brief
            else 17
            if "NDPS" in brief
            else 3
            if "Robbery" in brief
            else 12
            if "Rioting" in brief
            else 10
            if "Chain" in brief
            else 1
        )
        conn.execute(
            sa.text("""
            INSERT INTO src_CaseMaster (CaseMasterID, CrimeNo, CaseNo, CrimeRegisteredDate, PoliceStationID,
                CaseCategoryID, GravityOffenceID, CrimeMajorHeadID, CrimeMinorHeadID, CaseStatusID)
            VALUES (:id, :crime_no, :case_no, :date, 5, 1, :grav, :major, :minor, 1)"""),
            {
                "id": cm_id,
                "crime_no": crime_no,
                "case_no": f"FIR/{crime_no}",
                "date": base + timedelta(days=day_offset),
                "grav": 2 if major != 5 else 1,
                "major": major,
                "minor": major,
            },
        )
        conn.execute(
            sa.text("""
            INSERT INTO src_Inv_OccuranceTime (CaseMasterID, IncidentFromDate, Latitude, Longitude, BriefFacts)
            VALUES (:id, :ts, :lat, :lon, :brief)"""),
            {
                "id": cm_id,
                "ts": _ts(day_offset).replace(hour=20),
                "lat": lat,
                "lon": lon,
                "brief": brief,
            },
        )

    # ── Complainants ──
    for i, cm_id in enumerate(
        [1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    ):
        conn.execute(
            sa.text("""INSERT INTO src_ComplainantDetails
            (ComplainantID, CaseMasterID, ComplainantName, AgeYear)
            VALUES (:cid, :cmid, :name, :age)"""),
            {
                "cid": i + 1,
                "cmid": cm_id,
                "name": f"Complainant {cm_id}",
                "age": 30 + (i % 10),
            },
        )

    # ── Accused ──
    accused_names = [
        "Ramesh K",
        "R Kumar",
        "Ramesh Shetty",
        "R Shetty",
        "Unknown A",
        "Unknown B",
        "Unknown C",
        "Hotspot S1",
        "Hotspot S2",
        "Hotspot S3",
        "Hotspot S4",
        "Hotspot S5",
        "Suspect 15",
        "Suspect 16",
        "Suspect 17",
        "Suspect 18",
        "Suspect 19",
        "Suspect 20",
        "Suspect 21",
        "Suspect 22",
        "Suspect 23",
        "Suspect 24",
    ]
    for i, (cm_id, aname) in enumerate(
        zip(
            [1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
            accused_names,
        )
    ):
        conn.execute(
            sa.text(
                "INSERT INTO src_Accused (AccusedMasterID, CaseMasterID, AccusedName, AgeYear) VALUES (:aid, :cmid, :name, :age)"
            ),
            {
                "aid": i + 1,
                "cmid": cm_id,
                "name": aname,
                "age": 30 + (i % 10),
            },
        )

    # ── Act/Section Associations ──
    for cm_id in [1, 2, 3, 4, 10, 11, 12, 13, 14]:
        conn.execute(
            sa.text(
                "INSERT INTO src_ActSectionAssociation (CaseMasterID, ActID, SectionID) VALUES (:cmid, 'BNS', '303')"
            ),
            {"cmid": cm_id},
        )
    for cm_id in [5, 6, 7]:
        conn.execute(
            sa.text(
                "INSERT INTO src_ActSectionAssociation (CaseMasterID, ActID, SectionID) VALUES (:cmid, 'BNS', '303')"
            ),
            {"cmid": cm_id},
        )
    for cm_id, act, sec in [
        (15, "BNS", "101"),
        (16, "BNS", "115"),
        (17, "IT_Act", "66"),
        (18, "BNS", "303"),
        (19, "BNS", "331"),
        (20, "BNS", "140"),
        (21, "BNS", "336"),
        (22, "NDPS", "20"),
        (23, "BNS", "309"),
        (24, "BNS", "191"),
    ]:
        conn.execute(
            sa.text(
                "INSERT INTO src_ActSectionAssociation (CaseMasterID, ActID, SectionID) VALUES (:cmid, :act, :sec)"
            ),
            {"cmid": cm_id, "act": act, "sec": sec},
        )

    # ── PersonEntity & Links ──
    conn.execute(
        sa.text(
            "INSERT INTO int_PersonEntity (PersonEntityID, CanonicalName, Gender, PrimaryDistrictID) VALUES (1, 'Ramesh Kumar', 'M', 5)"
        )
    )
    for pe_id, src_rec, cm_id, conf in [
        (1, 1, 1, 0.95),
        (1, 2, 2, 0.85),
        (1, 3, 3, 0.80),
        (1, 4, 4, 0.75),
    ]:
        conn.execute(
            sa.text("""INSERT INTO int_PersonEntityLink
            (PersonEntityID, SourceTable, SourceRecordID, CaseMasterID, Confidence)
            VALUES (:pe, 'src_Accused', :src, :cm, :conf)"""),
            {"pe": pe_id, "src": src_rec, "cm": cm_id, "conf": conf},
        )

    conn.execute(
        sa.text(
            "INSERT INTO int_PersonEntity (PersonEntityID, CanonicalName, Gender, PrimaryDistrictID) VALUES (2, 'Unknown Vehicle Suspect', 'M', 5)"
        )
    )
    for pe_id, src_rec, cm_id in [(2, 5, 5), (2, 6, 6), (2, 7, 7)]:
        conn.execute(
            sa.text("""INSERT INTO int_PersonEntityLink
            (PersonEntityID, SourceTable, SourceRecordID, CaseMasterID, Confidence)
            VALUES (:pe, 'src_Accused', :src, :cm, 0.50)"""),
            {"pe": pe_id, "src": src_rec, "cm": cm_id},
        )

    for i in range(3, 8):
        conn.execute(
            sa.text(
                "INSERT INTO int_PersonEntity (PersonEntityID, CanonicalName, Gender, PrimaryDistrictID) VALUES (:id, :name, :g, 5)"
            ),
            {"id": i, "name": f"Entity {i}", "g": "M" if i % 2 == 0 else "F"},
        )
        conn.execute(
            sa.text("""INSERT INTO int_PersonEntityLink
            (PersonEntityID, SourceTable, SourceRecordID, CaseMasterID, Confidence)
            VALUES (:pe, 'src_Accused', :src, :cm, 0.90)"""),
            {"pe": i, "src": 10 + i, "cm": 15 + i - 3},
        )

    # ── RelationshipEdges ──
    conn.execute(
        sa.text(
            "INSERT INTO int_RelationshipEdge (PersonEntityA, PersonEntityB, RelationshipType, SourceCaseID, Confidence) VALUES (1, 2, 'shared_vehicle', 5, 0.60)"
        )
    )
    conn.execute(
        sa.text(
            "INSERT INTO int_RelationshipEdge (PersonEntityA, PersonEntityB, RelationshipType, SourceCaseID, Confidence) VALUES (1, 3, 'co_accused', 15, 0.85)"
        )
    )
    conn.execute(
        sa.text(
            "INSERT INTO int_RelationshipEdge (PersonEntityA, PersonEntityB, RelationshipType, SourceCaseID, Confidence) VALUES (3, 4, 'co_accused', 16, 0.80)"
        )
    )
    conn.execute(
        sa.text(
            "INSERT INTO int_RelationshipEdge (PersonEntityA, PersonEntityB, RelationshipType, SourceCaseID, Confidence) VALUES (4, 5, 'co_accused', 17, 0.75)"
        )
    )

    # ── VehicleLinks ──
    for cm_id in [5, 6, 7]:
        conn.execute(
            sa.text(
                "INSERT INTO int_VehicleLink (VehicleNumber, CaseMasterID, Confidence, Source) VALUES ('KA-01-MQ-1234', :cmid, 0.95, 'witness')"
            ),
            {"cmid": cm_id},
        )

    print("Seed data migration complete: 24 cases, 7 entities, lookup tables.")


def downgrade() -> None:
    conn = op.get_bind()
    tables = [
        "int_VehicleLink",
        "int_RelationshipEdge",
        "int_PersonEntityLink",
        "int_PersonEntity",
        "src_ActSectionAssociation",
        "src_ChargesheetDetails",
        "src_ArrestSurrender",
        "src_Accused",
        "src_Victim",
        "src_ComplainantDetails",
        "src_Inv_OccuranceTime",
        "src_CaseMaster",
        "src_Court",
        "src_ReligionMaster",
        "src_OccupationMaster",
        "src_Employee",
        "src_Designation",
        "src_Rank",
        "src_Unit",
        "src_UnitType",
        "src_District",
        "src_State",
        "src_CaseStatusMaster",
        "src_GravityOffence",
        "src_CaseCategory",
        "src_CrimeHeadActSection",
        "src_CrimeSubHead",
        "src_CrimeHead",
        "src_Section",
        "src_Act",
    ]
    for table in reversed(tables):
        conn.execute(sa.text(f"DELETE FROM {table}"))
    print("Seed data reverted.")
