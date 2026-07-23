#!/usr/bin/env python3
"""
generate_synthetic.py — Synthetic Crime/FIR Data Generator
Project Berunda — Karnataka State Police Datathon 2026

Generates realistic synthetic FIR data with planted patterns for
demonstrating entity resolution, hotspot detection, MO analysis,
anomaly detection, and relationship discovery.

Usage:
    python scripts/data/generate_synthetic.py --tier demo --scenario all
    python scripts/data/generate_synthetic.py --tier smoke --format json
    python scripts/data/generate_synthetic.py --tier stress --seed 123

Output: data/synthetic/SYNTHETIC_{Entity}_{tier}_{seed}.csv
"""

import argparse
import csv
import json
import logging
import math
import random
import sys
import time
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

try:
    from faker import Faker
except ImportError:
    print("ERROR: 'faker' package required. Install with: pip install faker")
    sys.exit(1)

# ── Paths ─────────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent
CONFIG_PATH = SCRIPT_DIR / "synthetic_config.json"
DEFAULT_OUTPUT = WORKSPACE_ROOT / "data" / "synthetic"
LOGS_DIR = WORKSPACE_ROOT / "logs"

# ── Set up root logger before anything ───────────────────────────────────────

LOG = logging.getLogger("berunda.synthetic")
LOG.setLevel(logging.DEBUG)


def _init_logging():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(LOGS_DIR / "acquisition.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | SYNTH | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z"
    ))
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s",
                                       datefmt="%H:%M:%S"))
    LOG.addHandler(fh)
    LOG.addHandler(ch)


_init_logging()

# ── Tier configuration ────────────────────────────────────────────────────────

TIERS = {
    "smoke":  {"cases": 200,   "desc": "Quick smoke test (200 records)"},
    "demo":   {"cases": 2000,  "desc": "Demo dataset (2000 records)"},
    "stress": {"cases": 10000, "desc": "Stress test (10000 records)"},
}

# ── Ground Truth Tracker ──────────────────────────────────────────────────────


class GroundTruthTracker:
    """Records planted patterns for downstream validation."""

    def __init__(self):
        self.entries = []

    def record(self, pattern_type: str, description: str, case_ids: list,
               details: dict | None = None):
        self.entries.append({
            "pattern_type": pattern_type,
            "description": description,
            "case_ids": sorted(case_ids),
            "details": details or {},
            "timestamp": datetime.now().isoformat(),
        })

    def to_dict(self) -> dict:
        return {
            "generator": "generate_synthetic.py",
            "version": "1.0.0",
            "generated_at": datetime.now().isoformat(),
            "total_planted_patterns": len(self.entries),
            "patterns": self.entries,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


# ── Config Loader ─────────────────────────────────────────────────────────────


def load_config(path: Path | None = None) -> dict:
    path = path or CONFIG_PATH
    if not path.exists():
        LOG.error("Config file not found: %s", path)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ── Weighted Choice Helpers ───────────────────────────────────────────────────


def weighted_choices(items: list, weights: list | None = None, k: int = 1):
    if weights is None:
        return random.choices(items, k=k)
    return random.choices(items, weights=weights, k=k)


def weighted_choice(items: list, weights: list | None = None):
    return weighted_choices(items, weights, k=1)[0]


# ── Lookup / Reference Data Generator ─────────────────────────────────────────


class LookupDataGenerator:
    """Generates reference/lookup table records."""

    def __init__(self, config: dict, fake: Faker, seed: int):
        self.cfg = config
        self.fake = fake
        self.seed = seed
        self.rng = random.Random(seed)

        # Build station lookup: district_name -> list of station names
        self.stations = self.cfg["police_stations"]
        self.district_station_map: dict[str, list[dict]] = {}
        station_id = 1
        for dist in self.cfg["districts"]:
            dname = dist["name"]
            names = self.stations.get(dname, [f"{dname} PS"])
            entries = []
            for sname in names:
                entries.append({
                    "UnitID": station_id,
                    "UnitName": sname,
                    "DistrictName": dname,
                    "DistrictID": dist["id"],
                    "DistrictCode": dist["code"],
                })
                station_id += 1
            self.district_station_map[dname] = entries

        # Employee (police officer) pool — generate ~2 per station
        self.employees = self._generate_employees()

        # Crime head lookups
        self.crime_heads = self.cfg["crime_heads"]
        self.crime_head_map = {ch["name"]: ch for ch in self.crime_heads}

        self.case_categories = self.cfg["case_categories"]
        self.gravity_offences = self.cfg["gravity_offences"]
        self.case_statuses = self.cfg["case_statuses"]

        # Occupations
        self.occupations = self.cfg["person_names"]["occupations"]
        self.id_proof_types = self.cfg["person_names"]["id_proof_types"]

        # Vehicle types
        self.vehicle_types = self.cfg["vehicle_types"]

        # Evidence types
        self.evidence_types = self.cfg["evidence_types"]

    def _generate_employees(self) -> list[dict]:
        employees = []
        eid = 1
        ranks = ["Constable", "Head Constable", "ASI", "SI", "PSI", "Inspector", "DSP"]
        designations = ["IO", "SHO", "Constable", "ASI", "PI"]
        for station_list in self.district_station_map.values():
            for stn in station_list:
                count = self.rng.randint(2, 3)
                for _ in range(count):
                    gender = self.rng.choice(["M", "F"])
                    first = (self.fake.first_name_male() if gender == "M"
                             else self.fake.first_name_female())
                    last = self.rng.choice(self.cfg["person_names"]["last_names"])
                    emp = {
                        "EmployeeID": eid,
                        "FirstName": f"{first} {last}",
                        "GenderID": 1 if gender == "M" else 2,
                        "RankName": self.rng.choice(ranks),
                        "DesignationName": self.rng.choice(designations),
                        "UnitID": stn["UnitID"],
                        "DistrictID": stn["DistrictID"],
                    }
                    employees.append(emp)
                    eid += 1
        return employees

    def get_stations_for_district(self, district_name: str) -> list[dict]:
        return self.district_station_map.get(district_name, [])

    def get_station_by_id(self, station_id: int) -> dict | None:
        for lst in self.district_station_map.values():
            for s in lst:
                if s["UnitID"] == station_id:
                    return s
        return None

    def get_employee_by_id(self, eid: int) -> dict | None:
        for e in self.employees:
            if e["EmployeeID"] == eid:
                return e
        return None

    def random_employee_for_station(self, station_id: int) -> dict:
        candidates = [e for e in self.employees if e["UnitID"] == station_id]
        return self.rng.choice(candidates) if candidates else self.rng.choice(self.employees)

    def random_station_for_district(self, district_name: str) -> dict:
        stations = self.get_stations_for_district(district_name)
        return self.rng.choice(stations) if stations else None

    def random_district(self) -> dict:
        districts = self.cfg["districts"]
        weights = [d["weight"] for d in districts]
        return weighted_choice(districts, weights)

    def random_crime_head(self) -> dict:
        weights = [ch["weight"] for ch in self.crime_heads]
        return weighted_choice(self.crime_heads, weights)

    def random_case_category(self) -> dict:
        return self.rng.choice(self.case_categories)

    def random_gravity(self) -> dict:
        weights = [g["weight"] for g in self.gravity_offences]
        return weighted_choice(self.gravity_offences, weights)

    def random_case_status(self) -> dict:
        weights = [s["weight"] for s in self.case_statuses]
        return weighted_choice(self.case_statuses, weights)

    def random_vehicle_type(self) -> dict:
        weights = [v["weight"] for v in self.vehicle_types]
        return weighted_choice(self.vehicle_types, weights)


# ── Person Name / Identity Generator ──────────────────────────────────────────


class PersonGenerator:
    """Generates synthetic person identities with demographic balancing."""

    def __init__(self, config: dict, fake: Faker, rng: random.Random):
        self.cfg = config
        self.fake = fake
        self.rng = rng
        self.names_cfg = config["person_names"]
        self.male_first = self.names_cfg["male_first"]
        self.female_first = self.names_cfg["female_first"]
        self.last_names = self.names_cfg["last_names"]
        self.occupations = self.names_cfg["occupations"]
        self.id_proof_types = self.names_cfg["id_proof_types"]
        self.gender_weights = config["gender_distribution"]

        # Track generated person identities for entity resolution
        self.person_id_counter = [0]
        self.generated_persons: list[dict] = []

    def _select_gender(self) -> str:
        r = self.rng.uniform(0, 100)
        mw = self.gender_weights["male_weight"]
        fw = self.gender_weights["female_weight"]
        if r < mw:
            return "M"
        elif r < mw + fw:
            return "F"
        return "T"

    def _generate_name(self, gender: str) -> str:
        if gender == "M":
            first = self.rng.choice(self.male_first)
        elif gender == "F":
            first = self.rng.choice(self.female_first)
        else:
            first = self.rng.choice(self.male_first + self.female_first)
        last = self.rng.choice(self.last_names)
        return f"{first} {last}"

    def _generate_age(self, role: str = "general") -> int:
        ranges = {
            "complainant": (20, 70),
            "victim":      (5, 80),
            "accused":     (18, 60),
            "general":     (15, 75),
        }
        lo, hi = ranges.get(role, ranges["general"])
        return self.rng.randint(lo, hi)

    def generate_person(self, role: str = "general",
                        override_name: str | None = None,
                        override_gender: str | None = None) -> dict:
        gender = override_gender or self._select_gender()
        name = override_name or self._generate_name(gender)
        age = self._generate_age(role)
        person = {
            "synthetic": True,
            "name": name,
            "age": age,
            "gender": gender,
            "id_proof_type": self.rng.choice(self.id_proof_types),
            "id_proof_number": self._generate_id_proof(gender),
            "occupation": self.rng.choice(self.occupations),
            "address": self.fake.address().replace("\n", ", "),
        }
        return person

    def _generate_id_proof(self, gender: str) -> str:
        t = self.rng.choice(self.id_proof_types)
        if t == "Aadhaar":
            return f"{self.rng.randint(1000,9999)} {self.rng.randint(1000,9999)} {self.rng.randint(1000,9999)}"
        elif t == "Voter ID":
            return f"{self.rng.choice('ABCDEFGH')}{self.rng.choice('ABCDEFGH')}{self.rng.randint(1000000,9999999)}"
        elif t == "Driving License":
            return f"KA-{self.rng.randint(1,31):02d}-{self.rng.randint(1000000,9999999)}"
        elif t == "PAN Card":
            return f"{self.rng.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}{self.rng.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}{self.rng.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}{self.rng.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}{self.rng.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}{self.rng.randint(1000,9999)}{self.rng.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}"
        return f"PID-{self.rng.randint(100000, 999999)}"


# ── Case Data Generator ───────────────────────────────────────────────────────


class CaseGenerator:
    """Generates CaseMaster and Inv_OccuranceTime records."""

    def __init__(self, lookup: LookupDataGenerator, person_gen: PersonGenerator,
                 config: dict, rng: random.Random, seed: int):
        self.lookup = lookup
        self.person_gen = person_gen
        self.cfg = config
        self.rng = rng
        self.seed = seed
        self.case_id_counter = [0]
        self.crime_no_serial = defaultdict(int)  # (year, dist_id, stn_id) -> serial
        self.cases: list[dict] = []
        self.occurrences: list[dict] = []

    def next_crime_no(self, year: int, dist_id: int, stn_id: int, cat_code: str = "1") -> tuple[str, str]:
        key = (year, dist_id, stn_id)
        self.crime_no_serial[key] += 1
        serial = self.crime_no_serial[key]
        crime_no = f"{cat_code}{dist_id:04d}{stn_id:04d}{year}{serial:05d}"
        case_no = f"{year}{serial:05d}"
        return crime_no, case_no

    def generate_case(self, district_override: dict | None = None,
                      crime_head_override: dict | None = None,
                      case_status_override: dict | None = None,
                      date_override: date | None = None,
                      lat_lon_override: tuple[float, float] | None = None,
                      brief_facts_override: str | None = None) -> dict:
        self.case_id_counter[0] += 1
        cm_id = self.case_id_counter[0]

        # District
        district = district_override or self.lookup.random_district()
        dname = district["name"]

        # Station
        station = self.lookup.random_station_for_district(dname)
        if station is None:
            all_stations = []
            for lst in self.lookup.district_station_map.values():
                all_stations.extend(lst)
            station = self.rng.choice(all_stations)

        # Crime head
        crime_head = crime_head_override or self.lookup.random_crime_head()

        # Dates
        if date_override:
            incident_from = datetime.combine(date_override, datetime.min.time())
        else:
            incident_from = datetime(
                self.rng.randint(2023, 2025),
                self.rng.randint(1, 12),
                self.rng.randint(1, 28),
                self.rng.randint(0, 23),
                self.rng.randint(0, 59),
            )
        incident_to = incident_from + timedelta(hours=self.rng.randint(0, 4))
        info_received = incident_from + timedelta(
            hours=self.rng.randint(0, 48), minutes=self.rng.randint(0, 59)
        )
        registered_date = info_received.date() if self.rng.random() > 0.3 else (
            info_received + timedelta(days=self.rng.randint(1, 7))
        ).date()

        # Crime number
        crime_no, case_no = self.next_crime_no(
            registered_date.year, district["id"], station["UnitID"]
        )

        # Case category, gravity, status
        cat = case_status_override if case_status_override and isinstance(case_status_override, dict) and "id" in case_status_override else None
        case_category = self.lookup.random_case_category()
        gravity = self.lookup.random_gravity()
        case_status = case_status_override or self.lookup.random_case_status()

        # Officer
        employee = self.lookup.random_employee_for_station(station["UnitID"])

        # Optional: court (for charge-sheeted cases)
        court_id = self.rng.randint(1, 50) if case_status["id"] in (2, 4) else None

        case = {
            "synthetic": True,
            "CaseMasterID": cm_id,
            "CrimeNo": crime_no,
            "CaseNo": case_no,
            "CrimeRegisteredDate": registered_date.isoformat(),
            "PolicePersonID": employee["EmployeeID"],
            "PoliceStationID": station["UnitID"],
            "PoliceStationName": station["UnitName"],
            "DistrictID": district["id"],
            "DistrictName": dname,
            "CaseCategoryID": case_category["id"],
            "CaseCategoryName": case_category["name"],
            "GravityOffenceID": gravity["id"],
            "GravityOffenceName": gravity["name"],
            "CrimeMajorHeadID": crime_head["id"],
            "CrimeMajorHeadName": crime_head["name"],
            "CrimeMinorHeadID": crime_head["id"],
            "CrimeMinorHeadName": crime_head["name"],
            "CaseStatusID": case_status["id"],
            "CaseStatusName": case_status["name"],
            "CourtID": court_id or "",
            "IncidentFromDate": incident_from.isoformat(),
            "IncidentToDate": incident_to.isoformat(),
            "tier": "",
            "scenario_patterns": [],
        }

        # Generate occurrence record (1:1)
        lat_lon = lat_lon_override or self._random_lat_lon(district)
        brief_facts = brief_facts_override or self._generate_brief_facts(
            crime_head, case, employee, station, dname
        )

        occ = {
            "synthetic": True,
            "CaseMasterID": cm_id,
            "IncidentFromDate": incident_from.isoformat(),
            "IncidentToDate": incident_to.isoformat(),
            "InfoReceivedPSDate": info_received.isoformat(),
            "Latitude": round(lat_lon[0], 7),
            "Longitude": round(lat_lon[1], 7),
            "BriefFacts": brief_facts,
        }

        self.cases.append(case)
        self.occurrences.append(occ)
        return case, occ

    def _random_lat_lon(self, district: dict) -> tuple[float, float]:
        bounds = self.cfg["district_geo_bounds"].get(
            district["name"], self.cfg["district_geo_bounds"]["default"]
        )
        lat = self.rng.uniform(bounds["lat_min"], bounds["lat_max"])
        lon = self.rng.uniform(bounds["lon_min"], bounds["lon_max"])
        return lat, lon

    def _generate_brief_facts(self, crime_head: dict, case: dict,
                               employee: dict, station: dict,
                               district_name: str) -> str:
        mo_templates = self.cfg["mo_templates"]
        mo_slots = self.cfg["mo_slots"]
        ch_name = crime_head["name"]

        templates = mo_templates.get(ch_name, [])
        if not templates:
            templates = [f"The accused committed {ch_name} at an unknown location."]

        template = self.rng.choice(templates)
        slots = {}
        for key, values in mo_slots.items():
            slots[key] = self.rng.choice(values)

        # Fill template with random slot values
        narrative = template.format(**slots)

        complainant = self.person_gen.generate_person("complainant")
        accused = self.person_gen.generate_person("accused")

        full = (
            f"SYNTHETIC FIR RECORD — NOT REAL\n\n"
            f"On {case['IncidentFromDate'][:10]} at approximately "
            f"{case['IncidentFromDate'][11:16]} hrs, "
            f"{complainant['name']} s/o {self.rng.choice(self.person_gen.names_cfg['male_first'])} "
            f"{complainant['name'].split()[-1]} r/o {complainant['address']} "
            f"reported to {station['UnitName']} Police Station, {district_name} District "
            f"that on the aforesaid date and time, "
            f"{narrative}\n\n"
            f"Accused identified as {accused['name']}. "
            f"Case registered under {crime_head['name']}. Investigation is in progress."
        )
        return full

    def get_cases(self) -> list[dict]:
        return self.cases

    def get_occurrences(self) -> list[dict]:
        return self.occurrences


# ── Person Entity (Complainant, Victim, Accused) Generator ────────────────────


class PersonEntityGenerator:
    """Generates complainant, victim, and accused records linked to cases."""

    def __init__(self, person_gen: PersonGenerator, rng: random.Random):
        self.person_gen = person_gen
        self.rng = rng

    def generate_for_case(self, case: dict) -> tuple[list, list, list]:
        """Returns (complainants, victims, accused) for a single case."""
        complainants = self._generate_complainants(case)
        victims = self._generate_victims(case)
        accused = self._generate_accused(case)
        return complainants, victims, accused

    def _generate_complainants(self, case: dict) -> list[dict]:
        count = self.rng.randint(1, 2)
        rows = []
        for i in range(count):
            p = self.person_gen.generate_person("complainant")
            rows.append({
                "synthetic": True,
                "ComplainantID": None,
                "CaseMasterID": case["CaseMasterID"],
                "ComplainantName": p["name"],
                "AgeYear": p["age"],
                "GenderID": 1 if p["gender"] == "M" else 2,
                "OccupationName": p["occupation"],
                "Address": p["address"],
                "IDProofType": p["id_proof_type"],
                "IDProofNumber": p["id_proof_number"],
                "case_major_head": case["CrimeMajorHeadName"],
            })
        return rows

    def _generate_victims(self, case: dict) -> list[dict]:
        crime_head = case["CrimeMajorHeadName"]
        if crime_head in ("Missing Person",):
            count = 1
        elif crime_head in ("Murder", "Rape / Sexual Assault", "Kidnapping", "Hurt / Assault"):
            count = self.rng.randint(1, 3)
        else:
            count = self.rng.randint(0, 2)

        rows = []
        for i in range(count):
            p = self.person_gen.generate_person("victim")
            is_police = 1 if self.rng.random() < 0.02 else 0
            rows.append({
                "synthetic": True,
                "VictimMasterID": None,
                "CaseMasterID": case["CaseMasterID"],
                "VictimName": p["name"],
                "AgeYear": p["age"],
                "GenderID": 1 if p["gender"] == "M" else 2,
                "VictimPolice": is_police,
                "Address": p["address"],
                "case_major_head": crime_head,
            })
        return rows

    def _generate_accused(self, case: dict) -> list[dict]:
        crime_head = case["CrimeMajorHeadName"]
        if crime_head in ("Rioting", "Dacoity"):
            count = self.rng.randint(3, 8)
        elif crime_head in ("Murder", "Robbery", "Kidnapping"):
            count = self.rng.randint(1, 5)
        else:
            count = self.rng.randint(1, 3)

        rows = []
        for i in range(count):
            p = self.person_gen.generate_person("accused")
            rows.append({
                "synthetic": True,
                "AccusedMasterID": None,
                "CaseMasterID": case["CaseMasterID"],
                "AccusedName": p["name"],
                "AgeYear": p["age"],
                "GenderID": 1 if p["gender"] == "M" else 2,
                "PersonID": f"A{i + 1}",
                "Address": p["address"],
                "case_major_head": crime_head,
            })
        return rows


# ── Vehicle Link Generator ────────────────────────────────────────────────────


class VehicleLinkGenerator:
    """Generates vehicle-to-case links for ~15% of cases."""

    def __init__(self, config: dict, rng: random.Random):
        self.cfg = config
        self.rng = rng
        self.link_id = [0]
        self.generated_vehicles: list[str] = []

    def generate_vehicle_reg_no(self, district_code: str = "KA") -> str:
        code = self.rng.choice(["01", "02", "03", "04", "05", "09", "19", "25", "27", "35"])
        letters = "".join(self.rng.choices("ABCDEFGH", k=2))
        digits = self.rng.randint(1000, 9999)
        return f"{district_code}-{code}-{letters}-{digits}"

    def generate_for_case(self, case: dict) -> list[dict]:
        if self.rng.random() > 0.15:
            return []
        count = self.rng.randint(1, 2)
        rows = []
        for _ in range(count):
            self.link_id[0] += 1
            vtype = self.rng.choice(self.cfg["vehicle_types"])
            model = self.rng.choice(vtype["models"])
            reg_no = self.generate_vehicle_reg_no()
            self.generated_vehicles.append(reg_no)
            rows.append({
                "synthetic": True,
                "VehicleLinkID": self.link_id[0],
                "VehicleNumber": reg_no,
                "VehicleType": vtype["type"],
                "VehicleModel": model,
                "CaseMasterID": case["CaseMasterID"],
                "Confidence": round(self.rng.uniform(0.7, 1.0), 4),
                "Source": "manual",
            })
        return rows

    def generate_shared_vehicle(self, cases: list[dict]) -> list[dict]:
        """Generate a vehicle shared across multiple cases (planted)."""
        if not cases:
            return []
        self.link_id[0] += 1
        reg_no = self.generate_vehicle_reg_no()
        self.generated_vehicles.append(reg_no)
        vtype = self.rng.choice(self.cfg["vehicle_types"])
        model = self.rng.choice(vtype["models"])
        rows = []
        for case in cases:
            rows.append({
                "synthetic": True,
                "VehicleLinkID": self.link_id[0],
                "VehicleNumber": reg_no,
                "VehicleType": vtype["type"],
                "VehicleModel": model,
                "CaseMasterID": case["CaseMasterID"],
                "Confidence": round(self.rng.uniform(0.8, 1.0), 4),
                "Source": "NER",
            })
        return rows


# ── Chargesheet Generator ─────────────────────────────────────────────────────


class ChargesheetGenerator:
    """Generates chargesheet records for ~40-60% of closed/charge-sheeted cases."""

    def __init__(self, config: dict, lookup: LookupDataGenerator, rng: random.Random):
        self.cfg = config
        self.lookup = lookup
        self.rng = rng
        self.cs_id = [0]

    def generate_for_case(self, case: dict, occurrence: dict) -> list[dict]:
        status_id = case["CaseStatusID"]
        if status_id not in (2, 3):
            return []

        if self.rng.random() > 0.55:
            return []

        self.cs_id[0] += 1
        reg_date = datetime.fromisoformat(case["CrimeRegisteredDate"])
        cs_date = reg_date + timedelta(days=self.rng.randint(30, 180))

        cs_type = weighted_choice(
            ["A", "B", "C"],
            [w["weight"] for w in self.cfg["chargesheet_types"].values()]
        )

        officer = self.lookup.random_employee_for_station(case["PoliceStationID"])

        return [{
            "synthetic": True,
            "CSID": self.cs_id[0],
            "CaseMasterID": case["CaseMasterID"],
            "csdate": cs_date.isoformat(),
            "cstype": cs_type,
            "cstype_desc": self.cfg["chargesheet_types"][cs_type]["description"],
            "PolicePersonID": officer["EmployeeID"],
            "Active": 1,
        }]


# ── Evidence Master Generator ─────────────────────────────────────────────────


class EvidenceGenerator:
    """Generates evidence items linked to cases."""

    def __init__(self, config: dict, rng: random.Random):
        self.cfg = config
        self.rng = rng
        self.ev_id = [0]

    def generate_for_case(self, case: dict) -> list[dict]:
        if self.rng.random() > 0.35:
            return []
        count = self.rng.randint(1, 4)
        rows = []
        for _ in range(count):
            self.ev_id[0] += 1
            ev_type = self.rng.choice(self.cfg["evidence_types"])
            subtype = self.rng.choice(ev_type["subtypes"])
            rows.append({
                "synthetic": True,
                "EvidenceID": self.ev_id[0],
                "CaseMasterID": case["CaseMasterID"],
                "EvidenceTypeID": ev_type["id"],
                "EvidenceTypeName": ev_type["name"],
                "EvidenceSubType": subtype,
                "Description": f"{subtype} recovered in connection with {case['CrimeMajorHeadName']}",
                "RecoveryDate": case["CrimeRegisteredDate"],
                "IsForensic": 1 if ev_type["name"] == "Forensic" else 0,
            })
        return rows


# ── Relationship Master Generator ──────────────────────────────────────────────


class RelationshipGenerator:
    """Generates person-to-person and person-to-case relationship records."""

    def __init__(self, rng: random.Random):
        self.rng = rng
        self.rel_id = [0]

    def generate_from_persons(self, case_id: int, complainants: list,
                               victims: list, accused: list) -> list[dict]:
        rows = []
        # Complainant -> Victim links
        for c in complainants:
            for v in victims:
                self.rel_id[0] += 1
                rows.append({
                    "synthetic": True,
                    "RelationshipID": self.rel_id[0],
                    "CaseMasterID": case_id,
                    "PersonA_Type": "Complainant",
                    "PersonA_Name": c["ComplainantName"],
                    "PersonB_Type": "Victim",
                    "PersonB_Name": v["VictimName"],
                    "RelationshipType": "complainant-victim",
                    "Confidence": round(self.rng.uniform(0.8, 1.0), 4),
                })

        # Accused -> Victim links
        for a in accused:
            for v in victims:
                self.rel_id[0] += 1
                rows.append({
                    "synthetic": True,
                    "RelationshipID": self.rel_id[0],
                    "CaseMasterID": case_id,
                    "PersonA_Type": "Accused",
                    "PersonA_Name": a["AccusedName"],
                    "PersonB_Type": "Victim",
                    "PersonB_Name": v["VictimName"],
                    "RelationshipType": "accused-victim",
                    "Confidence": round(self.rng.uniform(0.7, 1.0), 4),
                })

        # Accused -> Complainant links
        for a in accused:
            for c in complainants:
                if self.rng.random() < 0.3:
                    self.rel_id[0] += 1
                    rows.append({
                        "synthetic": True,
                        "RelationshipID": self.rel_id[0],
                        "CaseMasterID": case_id,
                        "PersonA_Type": "Accused",
                        "PersonA_Name": a["AccusedName"],
                        "PersonB_Type": "Complainant",
                        "PersonB_Name": c["ComplainantName"],
                        "RelationshipType": "accused-complainant",
                        "Confidence": round(self.rng.uniform(0.5, 0.9), 4),
                    })

        return rows


# ── Pattern Injectors ──────────────────────────────────────────────────────────


class PatternInjector:
    """Injects planted patterns for demo scenarios."""

    def __init__(self, config: dict, lookup: LookupDataGenerator,
                 case_gen: CaseGenerator, person_gen: PersonGenerator,
                 person_entity_gen: PersonEntityGenerator,
                 vehicle_gen: VehicleLinkGenerator,
                 chargesheet_gen: ChargesheetGenerator,
                 evidence_gen: EvidenceGenerator,
                 relationship_gen: RelationshipGenerator,
                 rng: random.Random, truth: GroundTruthTracker):
        self.cfg = config
        self.lookup = lookup
        self.case_gen = case_gen
        self.person_gen = person_gen
        self.person_entity_gen = person_entity_gen
        self.vehicle_gen = vehicle_gen
        self.chargesheet_gen = chargesheet_gen
        self.evidence_gen = evidence_gen
        self.relationship_gen = relationship_gen
        self.rng = rng
        self.truth = truth
        self._all_persons_data: list[tuple] = []

    def get_all_person_data(self) -> list[tuple]:
        return self._all_persons_data

    def inject_hotspot(self, target_district: str | None = None,
                       cluster_size: int = 20, radius_km: float = 2.0):
        """Plant a cluster of 15+ incidents within 2km radius in one district."""
        if target_district is None:
            # Pick a district with good geo bounds
            candidates = ["Bengaluru Urban", "Mysuru", "Belagavi", "Dharwad"]
            target_district = self.rng.choice(candidates)

        district = next(
            (d for d in self.cfg["districts"] if d["name"] == target_district),
            self.cfg["districts"][4]
        )
        LOG.info("Injecting hotspot: %s (%d cases, radius=%.1f km)",
                 target_district, cluster_size, radius_km)

        # Center of cluster
        bounds = self.cfg["district_geo_bounds"].get(target_district,
                      self.cfg["district_geo_bounds"]["default"])
        center_lat = self.rng.uniform(bounds["lat_min"] + 0.02, bounds["lat_max"] - 0.02)
        center_lon = self.rng.uniform(bounds["lon_min"] + 0.02, bounds["lon_max"] - 0.02)

        # ~0.02 degrees ≈ 2km
        lat_delta = radius_km * 0.009
        lon_delta = radius_km * 0.009 / math.cos(math.radians(center_lat))

        crime_heads = [ch for ch in self.cfg["crime_heads"]
                       if ch["name"] in ("Theft", "Hurt / Assault", "Robbery")]
        crime_head = self.rng.choice(crime_heads)

        case_ids = []
        for _ in range(cluster_size):
            lat = self.rng.uniform(center_lat - lat_delta, center_lat + lat_delta)
            lon = self.rng.uniform(center_lon - lon_delta, center_lon + lon_delta)
            date_override = date(
                self.rng.randint(2024, 2025),
                self.rng.choice([1, 2, 3, 6, 7, 8, 11, 12]),
                self.rng.randint(1, 28)
            )
            case, occ = self.case_gen.generate_case(
                district_override=district,
                crime_head_override=crime_head,
                lat_lon_override=(lat, lon),
                date_override=date_override,
            )
            case["tier"] = "pattern-hotspot"
            case["scenario_patterns"].append("hotspot")
            occ["BriefFacts"] = (
                f"SYNTHETIC — HOTSPOT PATTERN\n\n"
                f"{occ['BriefFacts']}\n\n"
                f"[HOTSPOT MARKER: Cluster incident within {radius_km}km of "
                f"({center_lat:.4f}, {center_lon:.4f})]"
            )
            case_ids.append(case["CaseMasterID"])

            # Person data
            comps, vics, accs = self.person_entity_gen.generate_for_case(case)
            vehs = self.vehicle_gen.generate_for_case(case)
            cs = self.chargesheet_gen.generate_for_case(case, occ)
            evs = self.evidence_gen.generate_for_case(case)
            rels = self.relationship_gen.generate_from_persons(
                case["CaseMasterID"], comps, vics, accs
            )
            self._all_persons_data.append((comps, vics, accs, vehs, cs, evs, rels))

        self.truth.record(
            pattern_type="hotspot",
            description=f"{cluster_size} incidents within ~{radius_km}km radius "
                        f"in {target_district} district centered at "
                        f"({center_lat:.4f}, {center_lon:.4f})",
            case_ids=case_ids,
            details={
                "district": target_district,
                "cluster_size": cluster_size,
                "radius_km": radius_km,
                "center_lat": round(center_lat, 6),
                "center_lon": round(center_lon, 6),
                "crime_head": crime_head["name"],
            }
        )

    def inject_serial_mo(self, count: int = 6):
        """Plant 5+ cases with matching CrimeHead text and MO patterns."""
        LOG.info("Injecting serial-MO pattern: %d cases", count)

        crime_head = self.rng.choice(
            [ch for ch in self.cfg["crime_heads"]
             if ch["name"] in ("Theft", "Burglary", "Robbery", "Cheating / Fraud")]
        )
        district = self.rng.choice(self.cfg["districts"])
        mo_template = self.rng.choice(self.cfg["mo_templates"].get(
            crime_head["name"], ["committed {crime_head['name']} using {items}"]
        ))
        # Fix template slots with common values
        mo_slots = self.cfg["mo_slots"]
        fixed_slots = {k: self.rng.choice(v) for k, v in mo_slots.items()}
        base_narrative = mo_template.format(**fixed_slots)

        case_ids = []
        for i in range(count):
            name_variant = self.rng.choice(
                ["Venkatesh", "Ramesh", "Suresh", "Manoj", "Rajesh", "Satish"]
            ) + " " + self.rng.choice(
                ["Reddy", "Gowda", "Nayak", "Shetty", "Kumar"]
            )
            date_override = date(
                self.rng.randint(2024, 2025),
                self.rng.choice([3, 4, 5, 6, 7, 8, 9, 10]),
                self.rng.randint(1, 28)
            )
            case, occ = self.case_gen.generate_case(
                district_override=district,
                crime_head_override=crime_head,
                date_override=date_override,
            )
            case["tier"] = "pattern-serial-mo"
            case["scenario_patterns"].append("serial-mo")

            # Construct matching MO narrative
            occ["BriefFacts"] = (
                f"SYNTHETIC — SERIAL MO PATTERN (Case {i+1}/{count})\n\n"
                f"Complainant reported that unknown person(s) {base_narrative} "
                f"The modus operandi matches pattern observed in previous case {case_ids[-1] if case_ids else 'N/A'}. "
                f"[SERIAL MO MARKER: Shared MO signature — {crime_head['name']} / {base_narrative[:60]}...]"
            )

            # Use consistent accused name
            acc = self.person_gen.generate_person("accused",
                                                    override_name=name_variant,
                                                    override_gender="M")
            comps, vics, accs_data = self.person_entity_gen.generate_for_case(case)
            # Override one accused entry
            if accs_data:
                accs_data[0]["AccusedName"] = name_variant
                accs_data[0]["PersonID"] = "A1"

            vehs = self.vehicle_gen.generate_for_case(case)
            cs = self.chargesheet_gen.generate_for_case(case, occ)
            evs = self.evidence_gen.generate_for_case(case)
            rels = self.relationship_gen.generate_from_persons(
                case["CaseMasterID"], comps, vics, accs_data
            )
            self._all_persons_data.append((comps, vics, accs_data, vehs, cs, evs, rels))
            case_ids.append(case["CaseMasterID"])

        self.truth.record(
            pattern_type="serial-mo",
            description=f"{count} cases with matching MO pattern "
                        f"({crime_head['name']}) in {district['name']} district",
            case_ids=case_ids,
            details={
                "crime_head": crime_head["name"],
                "template_snippet": base_narrative[:120],
                "district": district["name"],
                "case_count": count,
                "fixed_accused_name": name_variant,
            }
        )

    def inject_linked_cases(self, count: int = 4):
        """Plant 3+ cases sharing same accused across different districts."""
        LOG.info("Injecting linked-cases pattern: %d cases across districts", count)

        accused_name = self.rng.choice(
            ["Rajesh Kumar", "Suresh Patil", "Venkatesh Gowda", "Manoj Shetty", "Mahesh Hegde"]
        )
        selected_districts = self.rng.sample(self.cfg["districts"], min(count, len(self.cfg["districts"])))
        crime_heads = self.rng.choices(
            [ch for ch in self.cfg["crime_heads"] if ch["name"] in
             ("Theft", "Burglary", "Cheating / Fraud", "Criminal Trespass", "Extortion")],
            k=count
        )

        case_ids = []
        for i in range(count):
            district = selected_districts[i % len(selected_districts)]
            ch = crime_heads[i]
            date_override = date(
                self.rng.randint(2024, 2025),
                self.rng.randint(1, 12),
                self.rng.randint(1, 28)
            )
            case, occ = self.case_gen.generate_case(
                district_override=district,
                crime_head_override=ch,
                date_override=date_override,
            )
            case["tier"] = "pattern-linked-cases"
            case["scenario_patterns"].append("linked-cases")

            occ["BriefFacts"] = (
                f"SYNTHETIC — LINKED CASE PATTERN (Cross-district {i+1}/{count})\n\n"
                f"{occ['BriefFacts'][:200]}...\n\n"
                f"CROSS-REFERENCE: Same accused {accused_name} is involved in "
                f"linked case {case_ids[0] if case_ids else 'N/A'} "
                f"registered at a different police station.\n"
                f"[LINKED CASES MARKER: Cross-district accused match — {accused_name}]"
            )

            comps, vics, accs_data = self.person_entity_gen.generate_for_case(case)
            # Override first accused with shared name
            accs_data.insert(0, {
                "synthetic": True,
                "AccusedMasterID": None,
                "CaseMasterID": case["CaseMasterID"],
                "AccusedName": accused_name,
                "AgeYear": self.rng.randint(25, 50),
                "GenderID": 1,
                "PersonID": "A1",
                "Address": f"Cross-district pattern — same accused as case {case_ids[0] if case_ids else '?'}",
                "case_major_head": ch["name"],
            })

            vehs = self.vehicle_gen.generate_for_case(case)
            cs = self.chargesheet_gen.generate_for_case(case, occ)
            evs = self.evidence_gen.generate_for_case(case)
            rels = self.relationship_gen.generate_from_persons(
                case["CaseMasterID"], comps, vics, accs_data
            )
            self._all_persons_data.append((comps, vics, accs_data, vehs, cs, evs, rels))
            case_ids.append(case["CaseMasterID"])

        self.truth.record(
            pattern_type="linked-cases",
            description=f"{count} cases across {len(selected_districts)} districts "
                        f"sharing same accused '{accused_name}'",
            case_ids=case_ids,
            details={
                "accused_name": accused_name,
                "districts": [d["name"] for d in selected_districts[:count]],
                "case_count": count,
            }
        )

    def inject_anomaly_spike(self):
        """Plant unusual crime type in a low-crime area (anomaly spike)."""
        LOG.info("Injecting anomaly-spike pattern")

        # Pick a low-crime district
        low_weight = sorted(self.cfg["districts"], key=lambda d: d["weight"])
        low_district = self.rng.choice(low_weight[:8])

        # Pick an unusual crime for that area
        spike_crime = self.rng.choice(
            [ch for ch in self.cfg["crime_heads"]
             if ch["name"] in ("Cyber Crime", "NDPS Violation", "Arms Act Violation",
                               "Dacoity", "Extortion")]
        )

        # Generate a tight cluster of cases in one week
        base_date = date(
            self.rng.randint(2024, 2025),
            self.rng.choice([5, 6, 7, 8, 9, 10, 11, 12]),
            self.rng.randint(1, 21)
        )
        spike_count = self.rng.randint(5, 10)

        case_ids = []
        for i in range(spike_count):
            day_offset = self.rng.randint(0, 6)
            d = base_date + timedelta(days=day_offset)
            case, occ = self.case_gen.generate_case(
                district_override=low_district,
                crime_head_override=spike_crime,
                date_override=d,
            )
            case["tier"] = "pattern-anomaly-spike"
            case["scenario_patterns"].append("anomaly-spike")

            occ["BriefFacts"] = (
                f"SYNTHETIC — ANOMALY SPIKE PATTERN\n\n"
                f"{occ['BriefFacts'][:250]}...\n\n"
                f"[ANOMALY SPIKE MARKER: Unusual {spike_crime['name']} "
                f"incident in {low_district['name']} district "
                f"(baseline ~0/week, spike {spike_count} cases in 1 week)]"
            )

            comps, vics, accs_data = self.person_entity_gen.generate_for_case(case)
            vehs = self.vehicle_gen.generate_for_case(case)
            cs = self.chargesheet_gen.generate_for_case(case, occ)
            evs = self.evidence_gen.generate_for_case(case)
            rels = self.relationship_gen.generate_from_persons(
                case["CaseMasterID"], comps, vics, accs_data
            )
            self._all_persons_data.append((comps, vics, accs_data, vehs, cs, evs, rels))
            case_ids.append(case["CaseMasterID"])

        self.truth.record(
            pattern_type="anomaly-spike",
            description=f"{spike_count} {spike_crime['name']} cases in 1 week "
                        f"in {low_district['name']} district (normally low-crime)",
            case_ids=case_ids,
            details={
                "district": low_district["name"],
                "crime_head": spike_crime["name"],
                "spike_count": spike_count,
                "week_start": base_date.isoformat(),
                "baseline": "~0/month for this crime type in this district",
            }
        )


# ── CSV / JSON Output Writers ──────────────────────────────────────────────────


class OutputWriter:
    """Writes generated data to CSV and JSON formats."""

    def __init__(self, output_dir: Path, tier: str, seed: int, fmt: str):
        self.output_dir = output_dir
        self.tier = tier
        self.seed = seed
        self.fmt = fmt
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _make_path(self, entity: str, ext: str) -> Path:
        return self.output_dir / f"SYNTHETIC_{entity}_{self.tier}_{self.seed}.{ext}"

    def write_csv(self, entity: str, records: list[dict]):
        if not records:
            LOG.warning("No records for %s — skipping CSV write", entity)
            return
        path = self._make_path(entity, "csv")
        fieldnames = list(records[0].keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write("# GENERATED SYNTHETIC DATA — NOT REAL FIR RECORDS #\n")
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
        LOG.info("Wrote %d records -> %s", len(records), path)

    def write_json(self, entity: str, records: list[dict]):
        if not records:
            LOG.warning("No records for %s — skipping JSON write", entity)
            return
        path = self._make_path(entity, "json")
        payload = {
            "_synthetic_marker": True,
            "_warning": "GENERATED SYNTHETIC DATA — NOT REAL FIR RECORDS",
            "_entity": entity,
            "_tier": self.tier,
            "_seed": self.seed,
            "_generated_at": datetime.now().isoformat(),
            "_count": len(records),
            "records": records,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        LOG.info("Wrote %d records -> %s", len(records), path)

    def write(self, entity: str, records: list[dict]):
        if self.fmt == "csv":
            self.write_csv(entity, records)
        else:
            self.write_json(entity, records)

    def write_ground_truth(self, truth: GroundTruthTracker):
        path = self._make_path("GROUND_TRUTH", "json")
        with open(path, "w", encoding="utf-8") as f:
            f.write(truth.to_json())
        LOG.info("Wrote ground truth -> %s", path)

    def write_generation_report(self, case_count: int, total_persons: int,
                                 start_time: float):
        path = self._make_path("GENERATION_REPORT", "md")
        elapsed = time.time() - start_time
        content = f"""# Synthetic Data Generation Report

> **Tier:** `{self.tier}`
> **Seed:** `{self.seed}`
> **Format:** `{self.fmt}`
> **Generated:** {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}
> **Duration:** {elapsed:.2f}s

## Summary

| Metric | Value |
|--------|-------|
| Cases (FIRs) | {case_count} |
| Total Persons | {total_persons} |
| Output Directory | `{self.output_dir}` |

## Files Generated

- `{self._make_path("CaseMaster", self.fmt).name}`
- `{self._make_path("Inv_OccuranceTime", self.fmt).name}`
- `{self._make_path("ComplainantDetails", self.fmt).name}`
- `{self._make_path("VictimDetails", self.fmt).name}`
- `{self._make_path("AccusedDetails", self.fmt).name}`
- `{self._make_path("VehicleLink", self.fmt).name}`
- `{self._make_path("ChargesheetDetails", self.fmt).name}`
- `{self._make_path("EvidenceMaster", self.fmt).name}`
- `{self._make_path("RelationshipMaster", self.fmt).name}`
- `{self._make_path("GROUND_TRUTH", "json").name}`

## Ground Truth

Planted pattern details are recorded in `{self._make_path("GROUND_TRUTH", "json").name}`.
Use this file to validate entity resolution, hotspot detection, MO analysis,
and anomaly detection components.
"""
        path.write_text(content, encoding="utf-8")
        LOG.info("Wrote generation report -> %s", path)


# ── Main Orchestrator ─────────────────────────────────────────────────────────


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Project Berunda — Synthetic Crime/FIR Data Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python scripts/data/generate_synthetic.py --tier smoke\n"
            "  python scripts/data/generate_synthetic.py --tier demo --scenario all\n"
            "  python scripts/data/generate_synthetic.py --tier stress --format json --seed 123\n"
        ),
    )
    parser.add_argument(
        "--tier", choices=list(TIERS.keys()), default="demo",
        help=f"Scale tier (default: demo). Options: {', '.join(TIERS.keys())}"
    )
    parser.add_argument(
        "--scenario", choices=["hotspot", "serial-mo", "linked-cases",
                                "anomaly-spike", "all", "none"],
        default="all",
        help="Planted pattern scenario (default: all)"
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for reproducibility (default: 42)"
    )
    parser.add_argument(
        "--format", choices=["csv", "json"], default="csv",
        help="Output format (default: csv)"
    )
    parser.add_argument(
        "--output-dir", type=str, default=str(DEFAULT_OUTPUT),
        help=f"Output directory (default: {DEFAULT_OUTPUT})"
    )
    parser.add_argument(
        "--config", type=str, default=str(CONFIG_PATH),
        help="Path to configuration JSON"
    )
    parser.add_argument(
        "--dry-run", action="store_true", default=False,
        help="Perform a dry run without generating files"
    )
    return parser.parse_args(argv)


def main():
    args = parse_args()
    seed = args.seed
    tier_key = args.tier
    scenario = args.scenario
    fmt = args.format
    output_dir = Path(args.output_dir)
    config_path = Path(args.config)

    tier_info = TIERS[tier_key]
    target_count = tier_info["cases"]
    LOG.info("=" * 60)
    LOG.info("Project Berunda — Synthetic Data Generator")
    LOG.info("Tier: %s (%s)", tier_key, tier_info["desc"])
    LOG.info("Seed: %d | Scenario: %s | Format: %s", seed, scenario, fmt)
    if args.dry_run:
        LOG.info("Mode: DRY-RUN")
    LOG.info("=" * 60)

    start_time = time.time()

    # Load config
    config = load_config(config_path)

    # Seed all RNGs
    random.seed(seed)
    fake = Faker("en_IN")
    fake.seed_instance(seed)
    rng = random.Random(seed)

    # Ground truth tracker
    truth = GroundTruthTracker()

    # Core generators
    lookup = LookupDataGenerator(config, fake, seed)
    person_gen = PersonGenerator(config, fake, rng)
    case_gen = CaseGenerator(lookup, person_gen, config, rng, seed)
    person_entity_gen = PersonEntityGenerator(person_gen, rng)
    vehicle_gen = VehicleLinkGenerator(config, rng)
    chargesheet_gen = ChargesheetGenerator(config, lookup, rng)
    evidence_gen = EvidenceGenerator(config, rng)
    relationship_gen = RelationshipGenerator(rng)

    # Pattern injector
    injector = PatternInjector(
        config, lookup, case_gen, person_gen, person_entity_gen,
        vehicle_gen, chargesheet_gen, evidence_gen, relationship_gen,
        rng, truth
    )

    # ── Phase 1: Inject planted patterns ─────────────────────────────────
    pattern_case_count = 0

    if scenario in ("all", "hotspot"):
        # Scale hotspot size to tier
        hotspot_size = max(15, int(target_count * 0.015))
        injector.inject_hotspot(cluster_size=min(hotspot_size, target_count // 4))
        pattern_case_count += hotspot_size

    if scenario in ("all", "serial-mo"):
        serial_count = max(5, min(8, target_count // 100))
        injector.inject_serial_mo(count=serial_count)
        pattern_case_count += serial_count

    if scenario in ("all", "linked-cases"):
        linked_count = max(3, min(6, target_count // 200))
        injector.inject_linked_cases(count=linked_count)
        pattern_case_count += linked_count

    if scenario in ("all", "anomaly-spike"):
        injector.inject_anomaly_spike()
        pattern_case_count += 8  # average spike count

    # ── Phase 2: Generate background cases ───────────────────────────────
    remaining = target_count - pattern_case_count
    if remaining < 0:
        remaining = 0
        LOG.warning("Pattern cases (%d) exceed target (%d) — using pattern-only",
                     pattern_case_count, target_count)

    LOG.info("Generating %d background cases + %d pattern cases = %d total",
             remaining, pattern_case_count, remaining + pattern_case_count)

    all_complainants: list[dict] = []
    all_victims: list[dict] = []
    all_accused: list[dict] = []
    all_vehicles: list[dict] = []
    all_chargesheets: list[dict] = []
    all_evidence: list[dict] = []
    all_relationships: list[dict] = []

    # Process pattern-planted cases
    for comps, vics, accs, vehs, cs, evs, rels in injector.get_all_person_data():
        _assign_ids("ComplainantDetails", comps, all_complainants)
        _assign_ids("VictimDetails", vics, all_victims)
        _assign_ids("AccusedDetails", accs, all_accused)
        all_vehicles.extend(vehs)
        all_chargesheets.extend(cs)
        all_evidence.extend(evs)
        all_relationships.extend(rels)

    # Generate background cases
    batch_size = max(1, min(500, remaining // 10))
    for i in range(0, remaining, batch_size):
        batch_end = min(i + batch_size, remaining)
        LOG.info("  Background cases: %d / %d", batch_end, remaining)

        for _ in range(i, batch_end):
            case, occ = case_gen.generate_case()
            case["tier"] = "background"
            comps, vics, accs = person_entity_gen.generate_for_case(case)
            vehs = vehicle_gen.generate_for_case(case)
            cs = chargesheet_gen.generate_for_case(case, occ)
            evs = evidence_gen.generate_for_case(case)
            rels = relationship_gen.generate_from_persons(
                case["CaseMasterID"], comps, vics, accs
            )

            _assign_ids("ComplainantDetails", comps, all_complainants)
            _assign_ids("VictimDetails", vics, all_victims)
            _assign_ids("AccusedDetails", accs, all_accused)
            all_vehicles.extend(vehs)
            all_chargesheets.extend(cs)
            all_evidence.extend(evs)
            all_relationships.extend(rels)

    # ── Finalise ─────────────────────────────────────────────────────────
    all_cases = case_gen.get_cases()
    all_occurrences = case_gen.get_occurrences()

    total_persons = len(all_complainants) + len(all_victims) + len(all_accused)
    LOG.info("Generated: %d cases, %d persons, %d vehicles, %d chargesheets, "
             "%d evidence, %d relationships",
             len(all_cases), total_persons, len(all_vehicles),
             len(all_chargesheets), len(all_evidence), len(all_relationships))

    # ── Write output ─────────────────────────────────────────────────────
    if not args.dry_run:
        writer = OutputWriter(output_dir, tier_key, seed, fmt)
        writer.write("CaseMaster", all_cases)
        writer.write("Inv_OccuranceTime", all_occurrences)
        writer.write("ComplainantDetails", all_complainants)
        writer.write("VictimDetails", all_victims)
        writer.write("AccusedDetails", all_accused)
        writer.write("VehicleLink", all_vehicles)
        writer.write("ChargesheetDetails", all_chargesheets)
        writer.write("EvidenceMaster", all_evidence)
        writer.write("RelationshipMaster", all_relationships)
        writer.write_ground_truth(truth)
        writer.write_generation_report(
            len(all_cases), total_persons, start_time
        )
    else:
        LOG.info("[DRY-RUN] Skipping file writing.")

    # Log summary
    elapsed = time.time() - start_time
    LOG.info("=" * 60)
    LOG.info("GENERATION COMPLETE — %.2f seconds", elapsed)
    LOG.info("  Cases: %d", len(all_cases))
    LOG.info("  Persons: %d", total_persons)
    LOG.info("  Vehicles: %d", len(all_vehicles))
    LOG.info("  Chargesheets: %d", len(all_chargesheets))
    LOG.info("  Evidence Items: %d", len(all_evidence))
    LOG.info("  Relationships: %d", len(all_relationships))
    LOG.info("  Patterns Planted: %d", len(truth.entries))
    LOG.info("  Output: %s", output_dir)
    LOG.info("=" * 60)


def _assign_ids(entity_type: str, records: list[dict],
                accumulator: list[dict]):
    """Assign sequential IDs and accumulate records."""
    start_id = len(accumulator) + 1
    id_field = {
        "ComplainantDetails": "ComplainantID",
        "VictimDetails": "VictimMasterID",
        "AccusedDetails": "AccusedMasterID",
    }.get(entity_type)

    for i, rec in enumerate(records):
        if id_field and rec.get(id_field) is None:
            rec[id_field] = start_id + i
        accumulator.append(rec)


if __name__ == "__main__":
    main()
