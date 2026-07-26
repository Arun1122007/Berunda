"""Berunda Demo Startup — database initialization, seed data, and startup instructions."""

from __future__ import annotations

import sys
from pathlib import Path

_root = str(Path(__file__).resolve().parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

import asyncio
from datetime import date

import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.models.auth_models import User
from src.models.base import Base
from src.models.src_models import (
    CaseMaster,
    CaseStatusMaster,
    CrimeHead,
    District,
    GravityOffence,
    State,
    Unit,
    UnitType,
)

DB_URL = settings.DATABASE_URL


def db_path() -> Path:
    if "sqlite" in DB_URL:
        rel = DB_URL.removeprefix("sqlite+aiosqlite:///").removeprefix("sqlite:///")
        return Path(_root).parent / rel if not Path(rel).is_absolute() else Path(rel)
    return Path(_root).parent / "berunda.db"


async def ensure_database():
    engine = create_async_engine(DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print(f"[OK] Database ready: {db_path()}")
    return engine


async def seed_data(engine):
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        existing = await session.execute(select(District).limit(1))
        if existing.scalar_one_or_none():
            print("[SKIP] Seed data already exists")
            return

        # ── Lookups ──
        state = State(StateID=1, StateName="Karnataka")
        session.add(state)

        district = District(DistrictID=1, DistrictName="Bengaluru Urban", StateID=1)
        district2 = District(DistrictID=2, DistrictName="Bengaluru Rural", StateID=1)
        session.add_all([district, district2])

        ut = UnitType(UnitTypeID=1, UnitTypeName="Police Station")
        session.add(ut)
        ps1 = Unit(UnitID=1, UnitName="Cubbon Park Police Station", TypeID=1, DistrictID=1)
        ps2 = Unit(UnitID=2, UnitName="Whitefield Police Station", TypeID=1, DistrictID=1)
        session.add_all([ps1, ps2])

        ch = CrimeHead(CrimeHeadID=1, CrimeGroupName="Theft")
        session.add(ch)

        cs = CaseStatusMaster(CaseStatusID=1, CaseStatusName="Under Investigation")
        session.add(cs)

        go = GravityOffence(GravityOffenceID=1, LookupValue="Non-Cognizable")
        session.add(go)

        # ── Users ──
        admin_hash = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()
        admin = User(Email="admin@berunda.gov", HashedPassword=admin_hash, Role="admin", DistrictID=1, IsActive=True)
        officer_hash = bcrypt.hashpw(b"officer123", bcrypt.gensalt()).decode()
        officer = User(Email="officer@ksp.gov.in", HashedPassword=officer_hash, Role="officer", DistrictID=1, IsActive=True)
        analyst_hash = bcrypt.hashpw(b"analyst123", bcrypt.gensalt()).decode()
        analyst = User(Email="analyst@berunda.gov", HashedPassword=analyst_hash, Role="analyst", DistrictID=1, IsActive=True)
        session.add_all([admin, officer, analyst])

        # ── Demo FIRs ──
        cases = [
            CaseMaster(
                CrimeNo="CR-2026-0001", CaseNo="1/2026",
                CrimeRegisteredDate=date(2026, 1, 15),
                PoliceStationID=1, CaseStatusID=1, CrimeMajorHeadID=1,
            ),
            CaseMaster(
                CrimeNo="CR-2026-0002", CaseNo="2/2026",
                CrimeRegisteredDate=date(2026, 2, 20),
                PoliceStationID=1, CaseStatusID=1, CrimeMajorHeadID=1,
            ),
            CaseMaster(
                CrimeNo="CR-2026-0003", CaseNo="3/2026",
                CrimeRegisteredDate=date(2026, 3, 10),
                PoliceStationID=2, CaseStatusID=1, CrimeMajorHeadID=1,
            ),
        ]
        session.add_all(cases)
        await session.commit()

        print("[OK] Seeded: 1 state, 2 districts, 1 unit type, 2 police stations")
        print("[OK] Seeded: 1 crime head, 1 case status, 1 gravity offence")
        print("[OK] Seeded: 3 users (admin/officer/analyst), 3 demo FIRs")

    await engine.dispose()


async def main():
    print("=" * 60)
    print("  Berunda - Demo Startup")
    print("=" * 60)

    engine = await ensure_database()
    await seed_data(engine)

    print()
    print("  Startup Instructions:")
    print("  ---------------------")
    print(f"  1. cd {_root}")
    print('  2. python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000')
    print()
    print("  Demo Credentials:")
    print("  ----------------")
    print("  Admin:   admin@berunda.gov / admin123")
    print("  Officer: officer@ksp.gov.in / officer123")
    print("  Analyst: analyst@berunda.gov / analyst123")
    print()
    print("  Health Check:")
    print("  -------------")
    print("  http://localhost:8000/health")
    print("  http://localhost:8000/api/v1/status")
    print()
    print("  API Login Test:")
    print("  ---------------")
    print('  curl -X POST http://localhost:8000/api/v1/auth/login \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"email": "admin@berunda.gov", "password": "admin123"}\'')
    print()
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
