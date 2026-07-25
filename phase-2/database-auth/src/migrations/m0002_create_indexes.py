"""Migration 002: Add performance indexes on frequently queried columns."""

from sqlalchemy import MetaData, Table, Index, create_engine


INDEX_DEFINITIONS = [
    {"name": "idx_casemaster_crime_no", "table": "src_CaseMaster", "columns": ["CrimeNo"], "unique": True},
    {"name": "idx_casemaster_ps_id", "table": "src_CaseMaster", "columns": ["PoliceStationID"]},
    {"name": "idx_casemaster_status_id", "table": "src_CaseMaster", "columns": ["CaseStatusID"]},
    {"name": "idx_casemaster_reg_date", "table": "src_CaseMaster", "columns": ["CrimeRegisteredDate"]},
    {"name": "idx_user_email", "table": "auth_User", "columns": ["Email"], "unique": True},
    {"name": "idx_session_token_hash", "table": "auth_Session", "columns": ["TokenHash"]},
    {"name": "idx_session_user_id", "table": "auth_Session", "columns": ["UserID"]},
    {"name": "idx_complainant_casemaster", "table": "src_ComplainantDetails", "columns": ["CaseMasterID"]},
    {"name": "idx_victim_casemaster", "table": "src_Victim", "columns": ["CaseMasterID"]},
    {"name": "idx_accused_casemaster", "table": "src_Accused", "columns": ["CaseMasterID"]},
]


def upgrade(engine):
    meta = MetaData()
    meta.reflect(bind=engine)
    for cfg in INDEX_DEFINITIONS:
        unique = cfg.get("unique", False)
        table = meta.tables[cfg["table"]]
        idx = Index(cfg["name"], *[table.c[col] for col in cfg["columns"]], unique=unique)
        idx.create(engine)


def downgrade(engine):
    for cfg in INDEX_DEFINITIONS:
        try:
            Index(cfg["name"]).drop(engine)
        except Exception:
            pass
