"""Pytest fixtures for database and auth testing.

Usage:
    from test_fixtures import sample_users, sample_district_data, sample_fir_data
"""

import pytest


@pytest.fixture
def sample_users() -> dict:
    """Return dict of sample user data for admin, officer, analyst roles."""
    return {
        "admin": {
            "Email": "admin@berunda.gov",
            "Password": "Admin@123",
            "HashedPassword": None,  # set at runtime
            "Role": "admin",
            "DistrictID": 1,
            "IsActive": True,
        },
        "officer": {
            "Email": "officer@ksp.karnataka.gov.in",
            "Password": "Officer@123",
            "HashedPassword": None,
            "Role": "officer",
            "DistrictID": 1,
            "IsActive": True,
        },
        "analyst": {
            "Email": "analyst@berunda.gov",
            "Password": "Analyst@123",
            "HashedPassword": None,
            "Role": "analyst",
            "DistrictID": 1,
            "IsActive": True,
        },
    }


@pytest.fixture
def sample_district_data() -> dict:
    """Return dict of district reference data."""
    return {
        "state": {"StateID": 1, "StateName": "Karnataka", "NationalityID": 1},
        "districts": [
            {"DistrictID": 1, "DistrictName": "Bengaluru Urban", "StateID": 1},
            {"DistrictID": 2, "DistrictName": "Bengaluru Rural", "StateID": 1},
            {"DistrictID": 3, "DistrictName": "Mysuru", "StateID": 1},
        ],
        "police_stations": [
            {"UnitID": 1, "UnitName": "MG Road PS", "TypeID": 1, "DistrictID": 1},
            {"UnitID": 2, "UnitName": "Whitefield PS", "TypeID": 1, "DistrictID": 1},
            {"UnitID": 3, "UnitName": "Kuvempunagar PS", "TypeID": 1, "DistrictID": 3},
        ],
    }


@pytest.fixture
def sample_fir_data() -> dict:
    """Return a minimal FIR record dict suitable for test creation."""
    return {
        "CrimeNo": "TEST-FIR-001",
        "CaseNo": "FIR/TEST/001/2026",
        "CrimeRegisteredDate": "2026-01-15T10:30:00Z",
        "PoliceStationID": 1,
        "CaseCategoryID": 1,
        "GravityOffenceID": 2,
        "CrimeMajorHeadID": 1,
        "CrimeMinorHeadID": 1,
        "CaseStatusID": 1,
        "IncidentFromDate": "2026-01-15T20:00:00Z",
        "IncidentToDate": "2026-01-15T21:00:00Z",
        "occurrence": {
            "BriefFacts": "Test FIR: stolen wallet",
            "Latitude": 12.9716,
            "Longitude": 77.5946,
        },
        "complainant": {
            "ComplainantName": "Test Complainant",
            "AgeYear": 30,
            "OccupationID": 1,
            "ReligionID": 1,
            "CasteID": 1,
        },
        "victim": {
            "VictimName": "Test Victim",
            "AgeYear": 30,
            "GenderID": 1,
        },
        "accused": {
            "AccusedName": "Test Accused",
            "AgeYear": 35,
        },
    }


@pytest.fixture
def sample_password_data() -> dict:
    """Return sample passwords for policy validation testing."""
    return {
        "valid": "Test@1234",
        "too_short": "Ab1!",
        "no_upper": "test@1234",
        "no_lower": "TEST@1234",
        "no_digit": "Test@Test",
        "no_special": "Test1234",
    }
