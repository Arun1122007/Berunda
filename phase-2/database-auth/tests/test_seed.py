import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SASession

from src.models import (
    Base, District, Unit, CrimeHead, CaseStatusMaster,
    GravityOffence, User, CaseMaster, InvOccuranceTime,
    ComplainantDetails, Victim, Accused,
)
from src.seed.seed_data import seed_database


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    session = SASession(bind=engine)
    yield session
    session.close()
    engine.dispose()


def test_seed_districts(db_session):
    seed_database(db_session)
    assert db_session.query(District).count() == 2


def test_seed_units(db_session):
    seed_database(db_session)
    assert db_session.query(Unit).count() == 4


def test_seed_crime_heads(db_session):
    seed_database(db_session)
    heads = db_session.query(CrimeHead).all()
    names = {h.CrimeGroupName for h in heads}
    assert names == {"Theft", "Assault", "Burglary"}


def test_seed_case_statuses(db_session):
    seed_database(db_session)
    assert db_session.query(CaseStatusMaster).count() == 3


def test_seed_gravity_offences(db_session):
    seed_database(db_session)
    assert db_session.query(GravityOffence).count() == 3


def test_seed_users(db_session):
    seed_database(db_session)
    users = db_session.query(User).all()
    emails = {u.Email for u in users}
    assert "admin@berunda.gov" in emails
    assert "officer@ksp.gov.in" in emails
    assert len(users) == 2


def test_seed_users_have_admin_role(db_session):
    seed_database(db_session)
    admin = db_session.query(User).filter(User.Email == "admin@berunda.gov").first()
    assert admin.Role == "admin"


def test_seed_users_have_officer_role(db_session):
    seed_database(db_session)
    officer = db_session.query(User).filter(User.Email == "officer@ksp.gov.in").first()
    assert officer.Role == "officer"


def test_seed_case_masters(db_session):
    seed_database(db_session)
    assert db_session.query(CaseMaster).count() == 3


def test_seed_occurrence_times(db_session):
    seed_database(db_session)
    assert db_session.query(InvOccuranceTime).count() == 3


def test_seed_complainants(db_session):
    seed_database(db_session)
    assert db_session.query(ComplainantDetails).count() == 3


def test_seed_victims(db_session):
    seed_database(db_session)
    assert db_session.query(Victim).count() == 3


def test_seed_accused(db_session):
    seed_database(db_session)
    assert db_session.query(Accused).count() == 3


def test_seed_idempotent(db_session):
    seed_database(db_session)
    first_count = db_session.query(District).count()
    seed_database(db_session)
    second_count = db_session.query(District).count()
    assert first_count == second_count


def test_seed_relationships(db_session):
    seed_database(db_session)
    case = db_session.query(CaseMaster).first()
    assert case.occurrence_time is not None
    assert len(case.complainants) > 0
    assert len(case.victims) > 0
    assert len(case.accused) > 0
