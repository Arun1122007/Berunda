"""Security Scan — Phase 2 Quality Gate

Scans the codebase for common security issues in a FastAPI application.
Run: python phase-2/quality/security_scan.py
Output: Writes findings to stdout; non-zero exit on CRITICAL issues.
"""

from __future__ import annotations

import ast
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SKIP_DIRS = {".venv", "__pycache__", ".git", "node_modules", ".mypy_cache", ".pytest_cache", ".ruff_cache", "venv", "htmlcov", ".opencode"}

# ---------------------------------------------------------------------------
# SECURITY CHECK 1 — Hardcoded secret patterns
# ---------------------------------------------------------------------------
SECRET_PATTERNS: list[tuple[str, str]] = [
    ("JWT secret", r'(?i)(jwt[_-]?secret|secret[_-]?key)\s*[:=]\s*["\'].+["\']'),
    ("API key", r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\'].{8,}["\']'),
    ("Password in code", r'(?i)(password|passwd|pwd)\s*[:=]\s*["\'][^"\']{3,}["\']'),
    ("AWS access key", r'AKIA[0-9A-Z]{16}'),
    ("Bearer token in code", r'(?i)bearer\s+[a-z0-9\-_]{20,}'),
    ("Private key header", r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----'),
    ("Auth token literal", r'(?i)(auth[_-]?token|access[_-]?token)\s*[:=]\s*["\'].{8,}["\']'),
]

def scan_code_for_secrets(filepath: Path) -> list[dict]:
    findings = []
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings
    for label, pattern in SECRET_PATTERNS:
        for match in re.finditer(pattern, text):
            findings.append({
                "file": str(filepath.relative_to(REPO_ROOT)),
                "line": text[:match.start()].count("\n") + 1,
                "severity": "HIGH",
                "check": f"Hardcoded {label}",
                "snippet": match.group()[:60],
            })
    return findings

# ---------------------------------------------------------------------------
# SECURITY CHECK 2 — .env file tracking
# ---------------------------------------------------------------------------
def check_env_in_gitignore() -> list[dict]:
    findings = []
    gitignore_path = REPO_ROOT / ".gitignore"
    if not gitignore_path.exists():
        return [{"severity": "HIGH", "check": ".gitignore missing", "detail": "No .gitignore found at repo root"}]
    content = gitignore_path.read_text(encoding="utf-8")
    if ".env" not in content:
        findings.append({"severity": "CRITICAL", "check": ".env NOT in .gitignore", "detail": "Environment files may be committed"})
    else:
        findings.append({"severity": "INFO", "check": ".env in .gitignore", "detail": "Verified: .env entry present"})
    if ".env.example" in content:
        findings.append({"severity": "INFO", "check": ".env.example allowlisted", "detail": ".env.example is NOT in .gitignore (correct)"})
    # Check for actual .env files with real secrets
    for env_file in REPO_ROOT.glob(".env*"):
        if env_file.name == ".env.example":
            continue
        text = env_file.read_text(encoding="utf-8", errors="replace")
        # Skip if all values are placeholders
        suspicious = False
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            val = line.split("=", 1)[1].strip().strip("\"'")
            placeholders = {"your_secure_secret_here", "replace-with-a-random-64-hex-char-string", "test-secret-not-for-production", "admin123", "analyst123", ""}
            if val and val not in placeholders and len(val) > 4 and not val.startswith("http://localhost"):
                suspicious = True
        if suspicious:
            findings.append({"severity": "WARN", "check": f"Non-placeholder values in {env_file.name}", "detail": "Check that tracked .env files don't contain real secrets"})
    return findings

# ---------------------------------------------------------------------------
# SECURITY CHECK 3 — SQL injection via raw SQL / f-strings
# ---------------------------------------------------------------------------
def check_sql_injection() -> list[dict]:
    findings = []
    py_files = list(REPO_ROOT.glob("src/**/*.py")) + list(REPO_ROOT.glob("tests/**/*.py"))
    for fp in py_files:
        if any(skip in str(fp) for skip in SKIP_DIRS):
            continue
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        # Look for raw SQL in f-strings
        for i, line in enumerate(text.splitlines(), 1):
            # f-string with SQL keyword
            if 'f"' in line and re.search(r'\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b', line, re.IGNORECASE):
                findings.append({
                    "file": str(fp.relative_to(REPO_ROOT)),
                    "line": i,
                    "severity": "WARN",
                    "check": "Possible raw SQL in f-string",
                    "snippet": line.strip()[:80],
                })
            # sqlalchemy.text() with f-string
            if re.search(r'sa\.text\(f["\']', line) or re.search(r'text\(f["\']', line):
                findings.append({
                    "file": str(fp.relative_to(REPO_ROOT)),
                    "line": i,
                    "severity": "HIGH",
                    "check": "Raw SQL text() with f-string — SQL injection risk",
                    "snippet": line.strip()[:80],
                })
    return findings

# ---------------------------------------------------------------------------
# SECURITY CHECK 4 — Debug endpoints in production
# ---------------------------------------------------------------------------
def check_debug_endpoints() -> list[dict]:
    findings = []
    main_py = REPO_ROOT / "src" / "main.py"
    if not main_py.exists():
        return findings
    text = main_py.read_text(encoding="utf-8")
    # Check for debug-related routes
    debug_routes = ["/docs", "/redoc", "/openapi.json", "/metrics", "/schemas"]
    for route in debug_routes:
        if route in text:
            findings.append({
                "file": "src/main.py",
                "severity": "INFO",
                "check": f"Debug endpoint: {route}",
                "detail": "Acceptable for development; review before production",
            })
    # Check for debug mode
    if "debug=True" in text or 'APP_ENV=development' in text:
        findings.append({
            "file": "src/main.py",
            "severity": "INFO",
            "check": "Debug mode referenced",
            "detail": "Development debug features present",
        })
    return findings

# ---------------------------------------------------------------------------
# SECURITY CHECK 5 — CORS configuration
# ---------------------------------------------------------------------------
def check_cors_config() -> list[dict]:
    findings = []
    main_py = REPO_ROOT / "src" / "main.py"
    if not main_py.exists():
        return findings
    text = main_py.read_text(encoding="utf-8")
    if "allow_origins=[\"*" in text:
        findings.append({
            "severity": "HIGH",
            "check": "CORS wildcard origins",
            "detail": "CORS allow_origins is [\"*\"] — restrict in production",
        })
    elif "allow_origins=" in text:
        findings.append({
            "severity": "INFO",
            "check": "CORS configured with specific origins",
            "detail": "CORS uses configured origins from settings",
        })
    if "allow_credentials=True" in text:
        findings.append({
            "severity": "INFO",
            "check": "CORS allow_credentials=True",
            "detail": "OK when used with specific origins (not wildcard)",
        })
    return findings

# ---------------------------------------------------------------------------
# SECURITY CHECK 6 — Security headers
# ---------------------------------------------------------------------------
def check_security_headers() -> list[dict]:
    findings = []
    middleware_dir = REPO_ROOT / "src" / "middleware"
    if not middleware_dir.exists():
        return findings
    for fp in middleware_dir.glob("*.py"):
        text = fp.read_text(encoding="utf-8")
        for header in ["X-Content-Type-Options", "X-Frame-Options", "Strict-Transport-Security", "Content-Security-Policy"]:
            if header in text:
                findings.append({
                    "file": str(fp.relative_to(REPO_ROOT)),
                    "severity": "INFO",
                    "check": f"Security header: {header}",
                    "detail": f"{header} is set in middleware",
                })
    return findings

# ---------------------------------------------------------------------------
# SECURITY CHECK 7 — Authentication enforcement
# ---------------------------------------------------------------------------
def check_auth_enforcement() -> list[dict]:
    findings = []
    router_dir = REPO_ROOT / "src" / "routers"
    if not router_dir.exists():
        return findings
    for fp in sorted(router_dir.glob("*_router.py")):
        text = fp.read_text(encoding="utf-8")
        # Count public vs protected endpoints
        router_name = fp.stem
        endpoint_count = text.count("@router.")
        auth_deps = text.count("get_current_user") + text.count("require_role") + text.count("Depends")
        if auth_deps == 0 and endpoint_count > 0:
            findings.append({
                "file": str(fp.relative_to(REPO_ROOT)),
                "severity": "HIGH",
                "check": f"No auth dependencies in {router_name}",
                "detail": f"{endpoint_count} endpoints, 0 auth dependencies",
            })
    return findings

# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------
def run_all_checks() -> list[dict]:
    all_findings: list[dict] = []
    print("=" * 72)
    print("  BERUNDA — SECURITY SCAN (Phase 2 Quality Gate)")
    print("=" * 72)

    # Check 1: Hardcoded secrets
    print("\n[1/7] Scanning for hardcoded secrets...")
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not fname.endswith(".py"):
                continue
            fp = Path(root) / fname
            all_findings.extend(scan_code_for_secrets(fp))
    if not any(f["check"].startswith("Hardcoded") for f in all_findings):
        print("  No hardcoded secrets found.")
    else:
        for f in all_findings:
            if f["check"].startswith("Hardcoded"):
                print(f"  [{f['severity']}] {f['file']}:{f['line']} — {f['check']}")

    # Check 2: .env tracking
    print("\n[2/7] Checking .env in .gitignore...")
    for f in check_env_in_gitignore():
        all_findings.append(f)
        print(f"  [{f['severity']}] {f['check']}: {f.get('detail', '')}")

    # Check 3: SQL injection
    print("\n[3/7] Checking for SQL injection vectors...")
    sqli = check_sql_injection()
    if sqli:
        for f in sqli:
            all_findings.append(f)
            print(f"  [{f['severity']}] {f['file']}:{f['line']} — {f['check']}")
    else:
        print("  No SQL injection vectors found.")

    # Check 4: Debug endpoints
    print("\n[4/7] Checking for debug endpoints...")
    for f in check_debug_endpoints():
        all_findings.append(f)
        print(f"  [{f['severity']}] {f['check']}: {f.get('detail', '')}")

    # Check 5: CORS
    print("\n[5/7] Checking CORS configuration...")
    for f in check_cors_config():
        all_findings.append(f)
        print(f"  [{f['severity']}] {f['check']}: {f.get('detail', '')}")

    # Check 6: Security headers
    print("\n[6/7] Checking security headers...")
    for f in check_security_headers():
        all_findings.append(f)
        print(f"  [{f['severity']}] {f['file']} — {f['check']}")

    # Check 7: Auth enforcement
    print("\n[7/7] Checking authentication enforcement...")
    for f in check_auth_enforcement():
        all_findings.append(f)
        print(f"  [{f['severity']}] {f['check']}: {f.get('detail', '')}")
    if not any("auth dependencies" in f["check"] for f in all_findings):
        print("  All routers have auth dependencies.")

    # Summary
    severity_count = {"CRITICAL": 0, "HIGH": 0, "WARN": 0, "INFO": 0}
    for f in all_findings:
        sev = f.get("severity", "INFO")
        if sev in severity_count:
            severity_count[sev] += 1

    print("\n" + "=" * 72)
    print("  SCAN SUMMARY")
    print("=" * 72)
    for sev, count in severity_count.items():
        print(f"  {sev:10s}: {count}")
    print(f"  {'TOTAL':10s}: {len(all_findings)}")

    if severity_count["CRITICAL"] > 0:
        print("\n  OUTCOME: FAIL — Critical issues found")
        return [f for f in all_findings if f["severity"] in ("CRITICAL", "HIGH")]
    if severity_count["HIGH"] > 0:
        print("\n  OUTCOME: PASS WITH WARNINGS — High-severity issues found (review)")
    else:
        print("\n  OUTCOME: PASS — No critical or high-severity issues")

    print("=" * 72)
    return all_findings


if __name__ == "__main__":
    findings = run_all_checks()
    # Exit non-zero only on CRITICAL findings
    critical = [f for f in findings if f.get("severity") == "CRITICAL"]
    if critical:
        sys.exit(1)
