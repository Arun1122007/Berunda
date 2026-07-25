"""Manual migration: create all Berunda tables from scratch.

Usage:
    python -c "from phase-2.database-auth.migration_phase2 import upgrade; upgrade('sqlite:///berunda.db')"
    python -c "from migration_phase2 import upgrade; upgrade('postgresql://user:pass@localhost/berunda')"
"""

import sqlalchemy as sa
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.models import Base
from src.models.auth_models import User, Session, Permission
from src.models.src_models import (
    Act, Section, CrimeHead, CrimeSubHead, CrimeHeadActSection,
    CaseCategory, GravityOffence, CaseStatusMaster, Court,
    State, District, Unit, UnitType, Rank, Designation, Employee,
    OccupationMaster, CasteMaster, ReligionMaster,
    CaseMaster, InvOccuranceTime, ComplainantDetails,
    Victim, Accused, ArrestSurrender, ActSectionAssociation, ChargesheetDetails,
)
from src.models.int_models import (
    PersonEntity, PersonEntityLink, RelationshipEdge, VehicleLink,
    RiskScore, RiskScoreFeatureImportance, MoPattern, MoPatternLink,
    AnomalyAlert, HotspotLayer, RAGCorpusChunk,
)
from src.models.gov_models import AuditLog, FairnessCheckResult, DataProvenanceRecord
from src.models.ai_models import (
    AIUsageRecord, PromptVersion, AIConversation, AIMessage, AIFeedback,
)

ALL_TABLES = sorted(Base.metadata.tables.keys())


def upgrade(database_url: str = "sqlite+aiosqlite:///./berunda.db") -> None:
    sync_url = database_url.replace("+aiosqlite", "").replace("+asyncpg", "")
    engine = create_engine(sync_url)
    try:
        Base.metadata.create_all(engine)
        print(f"Created {len(Base.metadata.tables)} tables:")
        for name in ALL_TABLES:
            print(f"  + {name}")
    finally:
        engine.dispose()


def downgrade(database_url: str = "sqlite+aiosqlite:///./berunda.db") -> None:
    sync_url = database_url.replace("+aiosqlite", "").replace("+asyncpg", "")
    engine = create_engine(sync_url)
    try:
        Base.metadata.reflect(engine)
        for name in reversed(ALL_TABLES):
            if name in Base.metadata.tables:
                Base.metadata.tables[name].drop(engine)
                print(f"  - {name}")
    finally:
        engine.dispose()


def get_create_statements(dialect: str = "sqlite") -> list[str]:
    sync_url = {"sqlite": "sqlite:///:memory:", "postgresql": "postgresql:///"}
    engine = create_engine(sync_url.get(dialect, sync_url["sqlite"]))
    try:
        return [
            str(s.compile(engine))
            for s in Base.metadata.sorted_tables
        ]
    finally:
        engine.dispose()


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "upgrade"
    url = sys.argv[2] if len(sys.argv) > 2 else "sqlite:///./berunda.db"
    if cmd == "upgrade":
        upgrade(url)
    elif cmd == "downgrade":
        downgrade(url)
    elif cmd == "sql":
        for stmt in get_create_statements():
            print(stmt + ";\n")
