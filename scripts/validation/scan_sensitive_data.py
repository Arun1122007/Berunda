#!/usr/bin/env python3
"""
scan_sensitive_data.py — PII / Secrets Scanner
Project Berunda — Karnataka State Police Datathon 2026

Scans files for patterns indicating real PII or leaked credentials.
Section I quality gate: nothing that looks like a real name/phone/ID
pattern in anything meant to be aggregate or synthetic.
"""

import argparse
import json
import logging
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent
LOGS_DIR = WORKSPACE_ROOT / "logs"

# ── PII Patterns ─────────────────────────────────────────────

PII_PATTERNS = {
    "Aadhaar (12 digits)": re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"),
    "Indian Phone (+91)": re.compile(r"\b(?:\+91[\s-]?|91[\s-]?|0)?[6-9]\d{9}\b"),
    "Email Address": re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"),
    "PAN Card": re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"),
    "Indian Passport": re.compile(r"\b[A-Z]\d{7}\b"),
    "Vehicle Registration (KA)": re.compile(r"\bKA[\s-]?\d{2}[\s-]?[A-Z]{1,2}[\s-]?\d{4}\b"),
    "Credit Card (16 digits)": re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"),
    "IFSC Code": re.compile(r"\b[A-Z]{4}0[A-Z0-9]{6}\b"),
    "Bank Account (long number)": re.compile(r"\b\d{9,18}\b"),
}

SECRETS_PATTERNS = {
    "API Key assignment": re.compile(r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"][a-zA-Z0-9]{16,}"),
    "Password assignment": re.compile(r"(?i)(password|passwd|pwd|secret)\s*[:=]\s*['\"][^\s'\"]{8,}"),
    "Bearer Token": re.compile(r"(?i)bearer\s+[a-zA-Z0-9\-._~+/]+=*"),
    "AWS Key": re.compile(r"(?:AKIA|ABIA|ACCA|ASIA)[A-Z0-9]{16}"),
    "Private Key Header": re.compile(r"-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----"),
    "GitHub Token": re.compile(r"gh[ps]_[a-zA-Z0-9]{36}"),
    "Slack Token": re.compile(r"xox[baprs]-[a-zA-Z0-9-]+"),
    "Generic Secret": re.compile(r"(?i)(?:secret|token|credential)\s*[:=]\s*['\"][^\s'\"]{8,}"),
}

# File extensions to skip
BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".bmp", ".webp",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".mp4", ".webm", ".avi", ".mov",
    ".zip", ".tar", ".gz", ".bz2", ".7z", ".rar",
    ".jar", ".class", ".pyc", ".pyo", ".exe", ".dll", ".so",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx",
    ".parquet", ".feather", ".arrow", ".hdf5",
    ".sqlite", ".db",
    ".sha256",
}


def setup_logging() -> logging.Logger:
    log_file = LOGS_DIR / "acquisition.log"
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("berunda.sensitive_scan")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | PII-SCAN | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z"
    ))
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s",
                                       datefmt="%H:%M:%S"))
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def scan_file(filepath: Path, logger: logging.Logger) -> dict:
    """Scan a single file for PII and secrets patterns."""
    findings = {"pii": {}, "secrets": {}, "total_matches": 0}

    if filepath.suffix.lower() in BINARY_EXTENSIONS:
        return findings

    if filepath.stat().st_size > 10_000_000:  # Skip files > 10MB
        logger.debug(f"  Skipping large file: {filepath.name} ({filepath.stat().st_size} bytes)")
        return findings

    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        logger.debug(f"  Could not read {filepath.name}: {e}")
        return findings

    # PII scan
    for name, pattern in PII_PATTERNS.items():
        matches = pattern.findall(content)
        if matches:
            # Filter out likely false positives
            unique_matches = set(matches)
            if len(unique_matches) > 0:
                findings["pii"][name] = {
                    "count": len(matches),
                    "unique": len(unique_matches),
                    "samples": list(unique_matches)[:3],  # Max 3 samples
                }
                findings["total_matches"] += len(matches)

    # Secrets scan
    for name, pattern in SECRETS_PATTERNS.items():
        matches = pattern.findall(content)
        if matches:
            findings["secrets"][name] = {
                "count": len(matches),
                # Don't log actual secret values!
                "note": "Potential credential — verify manually",
            }
            findings["total_matches"] += len(matches)

    return findings


def scan_directory(dirpath: Path, logger: logging.Logger) -> list[dict]:
    """Scan all files in a directory tree."""
    results = []
    skip_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv", ".opencode"}

    for root, dirs, files in sorted(dirpath.walk()):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for fname in sorted(files):
            filepath = root / fname
            findings = scan_file(filepath, logger)
            if findings["total_matches"] > 0:
                rel_path = filepath.relative_to(WORKSPACE_ROOT)
                results.append({
                    "file": str(rel_path),
                    "findings": findings,
                })
                logger.warning(f"  ALERT: {rel_path} — {findings['total_matches']} pattern matches")
                for cat in ("pii", "secrets"):
                    for name, detail in findings[cat].items():
                        logger.warning(f"    {cat.upper()}: {name} ({detail.get('count', '?')} matches)")

    return results


def write_security_report(results: list[dict], report_path: Path, logger: logging.Logger):
    """Write SECURITY_AND_PRIVACY_REPORT.md."""
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Security and Privacy Report\n\n",
        f"> **Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n",
        f"> **Scanner:** scan_sensitive_data.py\n\n",
        "---\n\n",
    ]

    if not results:
        lines.append("## Result: ✅ CLEAN\n\n")
        lines.append("No PII or secrets patterns detected in scanned files.\n")
    else:
        lines.append(f"## Result: ⚠️ {len(results)} FILE(S) WITH FINDINGS\n\n")
        lines.append("> [!WARNING]\n> Review each finding below. Not all matches are real PII —\n")
        lines.append("> some may be false positives (e.g., random 12-digit numbers).\n\n")

        for entry in results:
            lines.append(f"### `{entry['file']}`\n\n")
            findings = entry["findings"]

            if findings["pii"]:
                lines.append("**PII Patterns:**\n\n")
                lines.append("| Pattern | Matches | Unique | Samples |\n|---------|---------|--------|---------|\n")
                for name, detail in findings["pii"].items():
                    samples = ", ".join(f"`{s}`" for s in detail.get("samples", []))
                    lines.append(f"| {name} | {detail['count']} | {detail['unique']} | {samples} |\n")
                lines.append("\n")

            if findings["secrets"]:
                lines.append("**Secrets Patterns:**\n\n")
                lines.append("| Pattern | Matches | Note |\n|---------|---------|------|\n")
                for name, detail in findings["secrets"].items():
                    lines.append(f"| {name} | {detail['count']} | {detail['note']} |\n")
                lines.append("\n")

    report_path.write_text("".join(lines), encoding="utf-8")
    logger.info(f"Security report: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Project Berunda — PII and Secrets Scanner"
    )
    parser.add_argument("paths", nargs="*", help="Files or directories to scan")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--no-dry-run", action="store_true")
    parser.add_argument("--resource-id", type=str, default=None)
    parser.add_argument("--priority", type=str, default=None,
                        choices=["P0", "P1", "P2", "P3", "P4"])
    parser.add_argument("--max-file-size", type=int, default=200*1024*1024)
    parser.add_argument("--max-total-size", type=int, default=1024*1024*1024)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--force", action="store_true")

    args = parser.parse_args()
    logger = setup_logging()

    logger.info("=" * 60)
    logger.info("Project Berunda — PII / Secrets Scanner")
    logger.info("=" * 60)

    # Default scan paths
    if not args.paths:
        scan_paths = [
            WORKSPACE_ROOT / "data",
            WORKSPACE_ROOT / "quarantine",
            WORKSPACE_ROOT / "boundaries",
        ]
    else:
        scan_paths = [Path(p) for p in args.paths]

    all_results = []
    for scan_path in scan_paths:
        if not scan_path.exists():
            logger.info(f"Path not found, skipping: {scan_path}")
            continue

        logger.info(f"Scanning: {scan_path}")
        if scan_path.is_dir():
            results = scan_directory(scan_path, logger)
        else:
            findings = scan_file(scan_path, logger)
            if findings["total_matches"] > 0:
                results = [{"file": str(scan_path), "findings": findings}]
            else:
                results = []
        all_results.extend(results)

    # Write report
    report_path = WORKSPACE_ROOT / "reports" / "SECURITY_AND_PRIVACY_REPORT.md"
    write_security_report(all_results, report_path, logger)

    logger.info("=" * 60)
    total_findings = sum(r["findings"]["total_matches"] for r in all_results)
    if total_findings > 0:
        logger.warning(f"SCAN COMPLETE: {total_findings} pattern matches in {len(all_results)} file(s)")
    else:
        logger.info("SCAN COMPLETE: No PII or secrets patterns detected")
    logger.info("=" * 60)

    sys.exit(1 if total_findings > 0 else 0)


if __name__ == "__main__":
    main()
