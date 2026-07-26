import pytest
from sqlalchemy import create_engine, inspect
from src.migrations import (
    m0001_initial_schema as migration_001_initial_schema,
)
from src.migrations import (
    m0002_create_indexes as migration_002_create_indexes,
)
from src.migrations import (
    m0003_add_relationships as migration_003_add_relationships,
)


@pytest.fixture
def engine():
    e = create_engine("sqlite:///:memory:", echo=False)
    yield e
    e.dispose()


def test_migration_001_creates_all_tables(engine):
    migration_001_initial_schema.upgrade(engine)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    expected = [
        "src_District", "src_Unit", "src_CrimeHead",
        "src_CaseStatusMaster", "src_GravityOffence",
        "src_CaseMaster", "src_Inv_OccuranceTime",
        "src_ComplainantDetails", "src_Victim", "src_Accused",
        "src_ActSectionAssociation",
        "auth_User", "auth_Session", "auth_Permission",
    ]
    for t in expected:
        assert t in tables, f"Table {t} not found"


def test_migration_001_rollback(engine):
    migration_001_initial_schema.upgrade(engine)
    inspector = inspect(engine)
    assert "src_CaseMaster" in inspector.get_table_names()
    migration_001_initial_schema.downgrade(engine)
    inspector = inspect(engine)
    assert "src_CaseMaster" not in inspector.get_table_names()


def test_migration_002_creates_indexes(engine):
    migration_001_initial_schema.upgrade(engine)
    migration_002_create_indexes.upgrade(engine)
    inspector = inspect(engine)
    indexes = inspector.get_indexes("src_CaseMaster")
    index_names = [idx["name"] for idx in indexes]
    assert "idx_casemaster_crime_no" in index_names
    assert "idx_casemaster_ps_id" in index_names


def test_migration_ordering_001_before_002(engine):
    migration_001_initial_schema.upgrade(engine)
    migration_002_create_indexes.upgrade(engine)
    inspector = inspect(engine)
    cm_indexes = inspector.get_indexes("src_CaseMaster")
    assert any(i["name"] == "idx_casemaster_crime_no" for i in cm_indexes)


def test_migration_002_rollback(engine):
    migration_001_initial_schema.upgrade(engine)
    migration_002_create_indexes.upgrade(engine)
    migration_002_create_indexes.downgrade(engine)
    inspector = inspect(engine)
    all_indexes = []
    for tbl in inspector.get_table_names():
        for idx in inspector.get_indexes(tbl):
            all_indexes.append(idx["name"])
    assert "idx_casemaster_crime_no" not in all_indexes


def test_alembic_style_sequence(engine):
    steps = [
        migration_001_initial_schema,
        migration_002_create_indexes,
        migration_003_add_relationships,
    ]
    for step in steps:
        step.upgrade(engine)

    inspector = inspect(engine)
    assert "auth_User" in inspector.get_table_names()

    for step in reversed(steps):
        step.downgrade(engine)


def test_unique_constraint_on_crime_no(engine):
    migration_001_initial_schema.upgrade(engine)
    conn = engine.connect()
    from sqlalchemy import text
    conn.execute(text("""
        INSERT INTO src_CaseMaster (CrimeNo) VALUES ('UNQ-TEST-001')
    """))
    with pytest.raises(Exception):
        conn.execute(text("""
            INSERT INTO src_CaseMaster (CrimeNo) VALUES ('UNQ-TEST-001')
        """))
    conn.close()


def test_unique_constraint_on_user_email(engine):
    migration_001_initial_schema.upgrade(engine)
    conn = engine.connect()
    from sqlalchemy import text
    conn.execute(text("""
        INSERT INTO auth_User (Email, HashedPassword, Role, IsActive)
        VALUES ('dup@test.com', 'hash', 'admin', 1)
    """))
    with pytest.raises(Exception):
        conn.execute(text("""
            INSERT INTO auth_User (Email, HashedPassword, Role, IsActive)
            VALUES ('dup@test.com', 'hash', 'admin', 1)
        """))
    conn.close()
