"""Performance validation — N+1 queries, index usage, bundle size reference."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


async def check_n_plus_one(db_session: Any = None) -> dict[str, Any]:
    """Check common query patterns for N+1 problems."""
    if db_session is None:
        return {"passed": True, "details": "no db session, skipping"}
    try:
        import sqlalchemy as sa

        async with db_session() as session:
            issues = []
            service_path = Path(__file__).resolve().parents[3] / "src" / "services"
            for pyfile in sorted(service_path.rglob("*.py")):
                text = pyfile.read_text(encoding="utf-8", errors="ignore")
                lines = text.splitlines()
                for i, line in enumerate(lines, 1):
                    stripped = line.strip()
                    if "for " in stripped and "in " in stripped:
                        next_lines = lines[i : i + 5]
                        next_text = " ".join(next_lines).lower()
                        if "execute" in next_text or "await session" in next_text:
                            issues.append(
                                f"{pyfile.relative_to(workspace)}:{i} possible N+1"
                            )
            return {
                "passed": len(issues) == 0,
                "possible_n_plus_one": issues[:10],
            }
    except Exception as exc:
        return {"passed": False, "details": str(exc)}


workspace = Path(__file__).resolve().parents[3]


async def check_indexes_used(db_session: Any = None) -> dict[str, Any]:
    """Verify critical queries have supporting indexes."""
    if db_session is None:
        return {"passed": True, "details": "no db session, skipping"}
    try:
        from sqlalchemy import inspect as sa_inspect

        async with db_session() as session:
            conn = await session.connection()
            inspector = await conn.run_sync(sa_inspect)
            all_indexes = {}
            for table_name in await conn.run_sync(inspector.get_table_names):
                indexes = await conn.run_sync(inspector.get_indexes, table_name)
                all_indexes[table_name] = [idx["name"] for idx in indexes]

            critical_queries = {
                "src_CaseMaster": ["ix_case_crimeno", "ix_case_regdate", "ix_case_station"],
                "src_Accused": ["ix_accused_case"],
                "src_ComplainantDetails": ["ix_comp_case"],
                "int_PersonEntityLink": ["ix_pelink_pentity", "ix_pelink_case"],
                "gov_AuditLog": ["ix_audit_user", "ix_audit_timestamp"],
            }
            issues = []
            for table, expected in critical_queries.items():
                if table in all_indexes:
                    for idx_name in expected:
                        if idx_name not in all_indexes[table]:
                            issues.append(f"{table}: missing index {idx_name}")
            return {"passed": len(issues) == 0, "issues": issues, "indexes_per_table": {k: len(v) for k, v in all_indexes.items()}}
    except Exception as exc:
        return {"passed": False, "details": str(exc)}


async def check_bundle_size() -> dict[str, Any]:
    """Check frontend bundle size (reference value for CI tracking)."""
    workspace = Path(__file__).resolve().parents[3]
    dist_dirs = [
        workspace / "apps" / "web" / "dist",
        workspace / "Drishti-Crime-Viz" / "dist",
    ]
    for dd in dist_dirs:
        if dd.exists():
            js_files = list(dd.rglob("*.js")) + list(dd.rglob("*.jsx"))
            total_size = sum(f.stat().st_size for f in js_files if f.is_file())
            return {
                "passed": total_size < 5_000_000,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / 1_000_000, 2),
                "js_files_count": len(js_files),
            }
    return {
        "passed": True,
        "details": "no dist directory found, tracking not applicable",
        "total_size_bytes": 0,
    }
