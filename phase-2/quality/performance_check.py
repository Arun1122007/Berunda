"""Performance Check — Phase 2 Quality Gate

Analyzes the codebase for common performance anti-patterns:
- N+1 query patterns
- Unbounded database reads
- Missing pagination
- Missing eager loading
- Large payload issues

Run: python phase-2/quality/performance_check.py
"""

from __future__ import annotations

import ast
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SKIP_DIRS = {".venv", "__pycache__", ".git", "node_modules", ".mypy_cache", ".pytest_cache", ".ruff_cache", "venv", "htmlcov"}


class QueryAnalyzer(ast.NodeVisitor):
    """AST visitor that detects SQLAlchemy query patterns."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.findings: list[dict] = []

    def visit_Call(self, node: ast.Call) -> None:
        # Detect unbounded .all() calls
        if isinstance(node.func, ast.Attribute) and node.func.attr == "all":
            parent = getattr(node, "parent", None)
            # Check if the call chain has .limit() or .offset()
            chain = self._get_call_chain(node)
            if "limit" not in chain and "offset" not in chain:
                self.findings.append({
                    "file": self.filepath,
                    "line": node.lineno,
                    "check": "Unbounded .all() — no .limit() before .all()",
                    "severity": "WARN",
                })

        # Detect selectinload / joinedload usage (these are GOOD — prevent N+1)
        if isinstance(node.func, ast.Attribute) and node.func.attr in ("selectinload", "joinedload"):
            pass  # Eager loading is good

        # Detect lazy loading in a loop (potential N+1)
        if isinstance(node.func, ast.Attribute) and node.func.attr in ("options",):
            pass  # .options() with eager loads is good

        # Detect relationship access in for-loops
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        """Check for relationship attribute access inside loops (N+1 pattern)."""
        loop_vars = set()
        if isinstance(node.target, ast.Name):
            loop_vars.add(node.target.id)
            self._check_nested_attribute_access(node, loop_vars)

        self.generic_visit(node)

    def _check_nested_attribute_access(self, node: ast.AST, loop_vars: set) -> None:
        """Look for relationship attribute access on loop variable."""
        for child in ast.walk(node):
            if isinstance(child, ast.Attribute):
                # Check if this is something like `item.relationship.field`
                if isinstance(child.value, ast.Attribute):
                    if isinstance(child.value.value, ast.Name) and child.value.value.id in loop_vars:
                        self.findings.append({
                            "file": self.filepath,
                            "line": child.lineno,
                            "check": "Possible N+1: relationship access on loop variable (missing eager load?)",
                            "severity": "INFO",
                        })

    def _get_call_chain(self, node: ast.Call) -> list[str]:
        """Trace back the method chain to get method names."""
        chain = []
        current: ast.AST = node
        while isinstance(current, ast.Call):
            if isinstance(current.func, ast.Attribute):
                chain.append(current.func.attr)
                current = current.func.value  # type: ignore[assignment]
            else:
                break
        return chain


# ---------------------------------------------------------------------------
# PERFORMANCE CHECK 1 — N+1 Query Patterns
# ---------------------------------------------------------------------------
def check_n_plus_one() -> list[dict]:
    findings = []
    for root, dirs, files in os.walk(REPO_ROOT / "src"):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not fname.endswith(".py"):
                continue
            fp = Path(root) / fname
            try:
                tree = ast.parse(fp.read_text(encoding="utf-8", errors="replace"))
            except SyntaxError:
                continue
            analyzer = QueryAnalyzer(str(fp.relative_to(REPO_ROOT)))
            analyzer.visit(tree)
            findings.extend(analyzer.findings)
    # Check for explicit eager loading in services
    service_dir = REPO_ROOT / "src" / "services"
    router_dir = REPO_ROOT / "src" / "routers"
    for fp in sorted(service_dir.glob("*.py")) + sorted(router_dir.glob("*.py")):
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        # Check for selectinload/joinedload usage
        if "selectinload" in text or "joinedload" in text:
            findings.append({
                "file": str(fp.relative_to(REPO_ROOT)),
                "severity": "INFO",
                "check": "Eager loading used (GOOD — prevents N+1)",
                "detail": f"{fp.name} uses selectinload/joinedload",
            })
    return findings

# ---------------------------------------------------------------------------
# PERFORMANCE CHECK 2 — Unbounded Database Reads
# ---------------------------------------------------------------------------
def check_unbounded_reads() -> list[dict]:
    findings = []
    for root, dirs, files in os.walk(REPO_ROOT / "src"):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not fname.endswith(".py"):
                continue
            fp = Path(root) / fname
            try:
                text = fp.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                # .all() without .limit()
                if ".all()" in line and ".limit(" not in line and re.search(r'\.execute\(.*\)', line):
                    # Check if this is preceded by .limit() on the same or prior line
                    findings.append({
                        "file": str(fp.relative_to(REPO_ROOT)),
                        "line": i,
                        "severity": "INFO",
                        "check": "Unbounded .execute() + .all() — verify limit exists",
                        "snippet": line.strip()[:80],
                    })
    # Specifically verify all list_* methods have pagination
    for fp in sorted((REPO_ROOT / "src").rglob("*.py")):
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for m in re.finditer(r'def list_\w+\(', text):
            start = max(0, m.start() - 200)
            snippet = text[start:m.end() + 300]
            if "limit" not in snippet and "page_size" not in snippet:
                findings.append({
                    "file": str(fp.relative_to(REPO_ROOT)),
                    "line": text[:m.start()].count("\n") + 1,
                    "severity": "WARN",
                    "check": f"list_* method may lack pagination: {m.group()}",
                    "detail": "No 'limit' or 'page_size' parameter found in method body",
                })
    return findings

# ---------------------------------------------------------------------------
# PERFORMANCE CHECK 3 — Missing Indexes on Foreign Keys
# ---------------------------------------------------------------------------
def check_missing_indexes() -> list[dict]:
    findings = []
    models_dir = REPO_ROOT / "src" / "models"
    if not models_dir.exists():
        return findings

    # Collect all FK columns defined in models
    fk_columns = []
    for fp in sorted(models_dir.glob("*.py")):
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for m in re.finditer(r"ForeignKey\(['\"](.+?)['\"]\)", text):
            start_line = text[:m.start()].count("\n") + 1
            # Check if Column also has index=True or if there's an __table_args__ with Index
            context_start = max(0, m.start() - 100)
            context = text[context_start:m.end()]
            if "index=True" not in context:
                fk_columns.append({
                    "file": str(fp.relative_to(REPO_ROOT)),
                    "line": start_line,
                    "fk_target": m.group(1),
                    "severity": "WARN",
                })

    # Check migrations for index creation
    migration_dir = REPO_ROOT / "src" / "alembic" / "versions"
    index_statements = []
    if migration_dir.exists():
        for fp in migration_dir.glob("*.py"):
            text = fp.read_text(encoding="utf-8", errors="replace")
            for m in re.finditer(r'create_index|op\.create_index|sa\.Index\(', text):
                index_statements.append(str(fp.relative_to(REPO_ROOT)))

    for fk in fk_columns:
        if index_statements:
            findings.append({
                "file": fk["file"],
                "line": fk["line"],
                "severity": "INFO",
                "check": f"FK column may need index (target: {fk['fk_target']})",
                "detail": "Indexes found in migrations — verify this FK is covered",
            })
        else:
            findings.append({
                "file": fk["file"],
                "line": fk["line"],
                "severity": "WARN",
                "check": f"FK column without explicit index (target: {fk['fk_target']})",
                "detail": "Consider adding index=True for performance on JOINs",
            })
    return findings

# ---------------------------------------------------------------------------
# PERFORMANCE CHECK 4 — Large Payload Issues
# ---------------------------------------------------------------------------
def check_large_payloads() -> list[dict]:
    findings = []
    # Check for response models that might expose too much data
    for root, dirs, files in os.walk(REPO_ROOT / "src"):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not fname.endswith(".py"):
                continue
            fp = Path(root) / fname
            try:
                text = fp.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                # Check for large file/image uploads without limit
                if re.search(r'UploadFile|File\(', line) and "max_length" not in line and "max_size" not in line:
                    findings.append({
                        "file": str(fp.relative_to(REPO_ROOT)),
                        "line": i,
                        "severity": "INFO",
                        "check": "File upload without explicit size limit",
                        "snippet": line.strip()[:80],
                    })
    # Check request body size limits
    main_py = REPO_ROOT / "src" / "main.py"
    if main_py.exists():
        text = main_py.read_text(encoding="utf-8")
        if "max_request_size" not in text and "body_limit" not in text:
            findings.append({
                "file": "src/main.py",
                "severity": "INFO",
                "check": "No explicit request body size limit",
                "detail": "FastAPI defaults to ~4MB; consider adding middleware for large payload protection",
            })
    return findings

# ---------------------------------------------------------------------------
# PERFORMANCE CHECK 5 — Cache Usage
# ---------------------------------------------------------------------------
def check_cache_usage() -> list[dict]:
    findings = []
    service_dir = REPO_ROOT / "src" / "services"
    if not service_dir.exists():
        return findings
    for fp in sorted(service_dir.glob("*.py")):
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        has_cache = "_cache" in text
        has_get = "cache.get" in text or "cache.set" in text
        if has_cache and has_get:
            findings.append({
                "file": str(fp.relative_to(REPO_ROOT)),
                "severity": "INFO",
                "check": "Cache layer used (GOOD)",
                "detail": f"{fp.name} implements cache.get/set",
            })
        elif "list_" in text or "get_" in text:
            # Service handles list/get but no caching
            findings.append({
                "file": str(fp.relative_to(REPO_ROOT)),
                "severity": "INFO",
                "check": "Consider adding caching",
                "detail": f"{fp.name} has data methods but no cache integration",
            })
    return findings


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------
def run_all_checks() -> list[dict]:
    all_findings: list[dict] = []

    print("=" * 72)
    print("  BERUNDA — PERFORMANCE CHECK (Phase 2 Quality Gate)")
    print("=" * 72)

    print("\n[1/5] Checking for N+1 query patterns...")
    n1 = check_n_plus_one()
    for f in n1:
        if "N+1" in f["check"] or "Eager" in f["check"]:
            all_findings.append(f)
    n1_issues = [f for f in n1 if "Eager" not in f["check"] and "N+1" in f["check"]]
    n1_good = [f for f in n1 if "Eager" in f["check"]]
    print(f"  Eager loading verified: {len(n1_good)} files")
    if n1_issues:
        for f in n1_issues:
            print(f"  [{f['severity']}] {f['file']}:{f.get('line', '?')} — {f['check']}")
    else:
        print("  No N+1 patterns detected.")

    print("\n[2/5] Checking for unbounded database reads...")
    unbounded = check_unbounded_reads()
    for f in unbounded:
        all_findings.append(f)
        print(f"  [{f['severity']}] {f['file']}:{f.get('line', '?')} — {f['check']}")

    print("\n[3/5] Checking for missing indexes on foreign keys...")
    indexes = check_missing_indexes()
    for f in indexes:
        all_findings.append(f)
        print(f"  [{f['severity']}] {f['file']}:{f['line']} — {f['check']}")

    print("\n[4/5] Checking for large payload issues...")
    payloads = check_large_payloads()
    for f in payloads:
        all_findings.append(f)
        print(f"  [{f['severity']}] {f['file']}:{f.get('line', '?')} — {f['check']}")

    print("\n[5/5] Checking cache usage...")
    cache = check_cache_usage()
    for f in cache:
        all_findings.append(f)
        sev = f.get("severity", "INFO")
        print(f"  [{sev}] {f['file']} — {f['check']}")

    # Summary
    severity_count = {"WARN": 0, "INFO": 0}
    for f in all_findings:
        sev = f.get("severity", "INFO")
        if sev in severity_count:
            severity_count[sev] += 1

    print("\n" + "=" * 72)
    print("  PERFORMANCE CHECK SUMMARY")
    print("=" * 72)
    for sev, count in severity_count.items():
        print(f"  {sev:10s}: {count}")
    print(f"  {'TOTAL':10s}: {len(all_findings)}")

    warnings = severity_count.get("WARN", 0)
    if warnings == 0:
        print("\n  OUTCOME: PASS — No performance warnings")
    else:
        print(f"\n  OUTCOME: PASS WITH {warnings} WARNINGS — Review suggested")
    print("=" * 72)
    return all_findings


if __name__ == "__main__":
    run_all_checks()
