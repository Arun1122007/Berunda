#!/usr/bin/env python3
"""
validate_resources.py — Resource Validation Script
Project Berunda — Karnataka State Police Datathon 2026

Implements Section I Quality Gates. A resource does not leave
quarantine/ until it passes every applicable gate.
"""

import argparse
import csv
import hashlib
import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent
QUARANTINE_DIR = WORKSPACE_ROOT / "quarantine"
RAW_DIR = WORKSPACE_ROOT / "data" / "raw"
MANIFESTS_DIR = WORKSPACE_ROOT / "manifests"
LOGS_DIR = WORKSPACE_ROOT / "logs"

# ── Logging ──────────────────────────────────────────────────

def setup_logging() -> logging.Logger:
    log_file = LOGS_DIR / "acquisition.log"
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("berunda.validate")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | VALIDATE | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z"
    ))

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s",
                                       datefmt="%H:%M:%S"))

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


# ── Quality Gate Functions ───────────────────────────────────

def gate_file_integrity(filepath: Path, expected_checksum: str | None, logger: logging.Logger) -> tuple[bool, str]:
    """Gate: file exists, is non-empty, and checksum matches if provided."""
    if not filepath.exists():
        return False, f"File not found: {filepath.name}"
    if filepath.stat().st_size == 0:
        return False, "File is empty (0 bytes)"

    actual_hash = hashlib.sha256(filepath.read_bytes()).hexdigest()

    if expected_checksum and expected_checksum != actual_hash:
        return False, f"Checksum mismatch: expected {expected_checksum[:16]}..., got {actual_hash[:16]}..."

    return True, f"OK ({filepath.stat().st_size} bytes, sha256:{actual_hash[:16]}...)"


def gate_archive_integrity(filepath: Path, logger: logging.Logger) -> tuple[bool, str]:
    """Gate: archive extracts cleanly (zip, tar, gz)."""
    ext = filepath.suffix.lower()
    if ext == ".zip":
        import zipfile
        try:
            with zipfile.ZipFile(filepath, 'r') as z:
                bad = z.testzip()
                if bad:
                    return False, f"Corrupt entry in zip: {bad}"
            return True, f"ZIP OK ({len(z.namelist())} entries)"
        except zipfile.BadZipFile as e:
            return False, f"Bad ZIP: {e}"
    elif ext in (".gz", ".tgz"):
        import gzip
        try:
            with gzip.open(filepath, 'rb') as f:
                f.read(1024)
            return True, "GZIP OK"
        except Exception as e:
            return False, f"Bad GZIP: {e}"
    elif ext == ".tar":
        import tarfile
        try:
            with tarfile.open(filepath, 'r') as t:
                t.getmembers()
            return True, "TAR OK"
        except Exception as e:
            return False, f"Bad TAR: {e}"

    return True, "Not an archive — skipped"


def gate_csv_parse(filepath: Path, logger: logging.Logger) -> tuple[bool, str]:
    """Gate: CSV/TSV parses without error, report column count."""
    ext = filepath.suffix.lower()
    if ext not in (".csv", ".tsv"):
        return True, "Not CSV/TSV — skipped"

    try:
        delimiter = "\t" if ext == ".tsv" else ","
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f, delimiter=delimiter)
            headers = next(reader, None)
            if not headers:
                return False, "CSV is empty (no header row)"

            row_count = 0
            col_count = len(headers)
            for row in reader:
                row_count += 1

        return True, f"CSV OK ({col_count} columns, {row_count} data rows)"
    except Exception as e:
        return False, f"CSV parse error: {e}"


def gate_json_parse(filepath: Path, logger: logging.Logger) -> tuple[bool, str]:
    """Gate: JSON/JSONL parses without error."""
    ext = filepath.suffix.lower()
    if ext == ".json":
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return True, f"JSON OK (array, {len(data)} items)"
            elif isinstance(data, dict):
                return True, f"JSON OK (object, {len(data)} keys)"
            return True, "JSON OK"
        except json.JSONDecodeError as e:
            return False, f"JSON parse error: {e}"
    elif ext == ".jsonl":
        try:
            count = 0
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        json.loads(line)
                        count += 1
            return True, f"JSONL OK ({count} lines)"
        except json.JSONDecodeError as e:
            return False, f"JSONL parse error at line {count + 1}: {e}"

    return True, "Not JSON — skipped"


def gate_temporal_validity(filepath: Path, logger: logging.Logger) -> tuple[bool, str]:
    """Gate: no impossible future dates in date-like columns."""
    ext = filepath.suffix.lower()
    if ext != ".csv":
        return True, "Not CSV — skipped"

    date_pattern = re.compile(r"\b(20\d{2})-(\d{2})-(\d{2})\b")
    future_dates = []
    today = datetime.now().date()

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line_num, line in enumerate(f, 1):
                for match in date_pattern.finditer(line):
                    year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
                    try:
                        from datetime import date
                        d = date(year, month, day)
                        if d > today:
                            future_dates.append(f"line {line_num}: {match.group(0)}")
                    except ValueError:
                        pass  # Invalid date — separate issue

        if future_dates:
            return False, f"Future dates found: {future_dates[:5]}"
        return True, "No future dates detected"
    except Exception as e:
        return False, f"Temporal check error: {e}"


def gate_duplicate_detection(filepath: Path, logger: logging.Logger) -> tuple[bool, str]:
    """Gate: report exact-duplicate rows."""
    ext = filepath.suffix.lower()
    if ext != ".csv":
        return True, "Not CSV — skipped"

    try:
        seen = set()
        duplicates = 0
        total = 0
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                total += 1
                row_key = tuple(row)
                if row_key in seen:
                    duplicates += 1
                else:
                    seen.add(row_key)

        if duplicates > 0:
            return False, f"Found {duplicates} duplicate rows out of {total}"
        return True, f"No duplicates ({total} rows)"
    except Exception as e:
        return False, f"Duplicate check error: {e}"


def gate_missing_values(filepath: Path, logger: logging.Logger) -> tuple[bool, str]:
    """Gate: profile missing/null values per column."""
    ext = filepath.suffix.lower()
    if ext != ".csv":
        return True, "Not CSV — skipped"

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            null_counts = {h: 0 for h in headers}
            total = 0

            for row in reader:
                total += 1
                for h in headers:
                    val = row.get(h, "").strip()
                    if not val or val.lower() in ("null", "none", "na", "n/a", ""):
                        null_counts[h] += 1

        if total == 0:
            return True, "No data rows"

        high_null = {h: f"{c}/{total} ({100*c//total}%)"
                     for h, c in null_counts.items() if c > total * 0.5}

        if high_null:
            return True, f"WARNING — high null columns: {high_null}"
        return True, f"Missing-value profile recorded ({total} rows)"
    except Exception as e:
        return False, f"Missing-value check error: {e}"


def gate_pii_scan(filepath: Path, logger: logging.Logger) -> tuple[bool, str]:
    """Gate: scan for patterns that look like real PII."""
    # Delegate to scan_sensitive_data.py for full scan;
    # this is a lightweight inline check
    pii_patterns = {
        "Aadhaar": re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b"),
        "Phone_IN": re.compile(r"\b(?:\+91|91|0)?[6-9]\d{9}\b"),
        "Email": re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"),
        "PAN": re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"),
    }

    findings = {}
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")[:500_000]
        for name, pattern in pii_patterns.items():
            matches = pattern.findall(content)
            if matches:
                findings[name] = len(matches)

        if findings:
            return False, f"PII patterns detected: {findings}"
        return True, "No PII patterns detected"
    except Exception as e:
        return False, f"PII scan error: {e}"


def gate_synthetic_label(filepath: Path, logger: logging.Logger) -> tuple[bool, str]:
    """Gate: synthetic files must carry an explicit SYNTHETIC marker."""
    if "synthetic" in str(filepath).lower() or "SYNTHETIC" in str(filepath):
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")[:5000]
            markers = ["SYNTHETIC", "synthetic", "GENERATED", "NOT REAL"]
            if any(m in content for m in markers):
                return True, "Synthetic marker found"
            return False, "File appears synthetic but lacks SYNTHETIC marker in content"
        except Exception:
            return False, "Could not read file to check synthetic marker"

    return True, "Not a synthetic file — skipped"


def gate_license_check(resource_id: str, manifests_dir: Path, logger: logging.Logger) -> tuple[bool, str]:
    """Gate: license is recorded in license_inventory.csv."""
    csv_path = manifests_dir / "license_inventory.csv"
    if not csv_path.exists():
        return False, "license_inventory.csv not found"

    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("resource_id") == resource_id:
                    return True, f"License on file: {row.get('license_name', 'UNKNOWN')}"
        return False, f"No license entry for {resource_id}"
    except Exception as e:
        return False, f"License check error: {e}"


# ── Main Validation Logic ────────────────────────────────────

def validate_resource(
    resource_id: str,
    filepath: Path,
    logger: logging.Logger,
    expected_checksum: str | None = None,
) -> dict:
    """Run all applicable quality gates on a single file."""
    results = {}

    gates = [
        ("file_integrity", lambda: gate_file_integrity(filepath, expected_checksum, logger)),
        ("archive_integrity", lambda: gate_archive_integrity(filepath, logger)),
        ("csv_parse", lambda: gate_csv_parse(filepath, logger)),
        ("json_parse", lambda: gate_json_parse(filepath, logger)),
        ("temporal_validity", lambda: gate_temporal_validity(filepath, logger)),
        ("duplicate_detection", lambda: gate_duplicate_detection(filepath, logger)),
        ("missing_values", lambda: gate_missing_values(filepath, logger)),
        ("pii_scan", lambda: gate_pii_scan(filepath, logger)),
        ("synthetic_label", lambda: gate_synthetic_label(filepath, logger)),
        ("license_check", lambda: gate_license_check(resource_id, MANIFESTS_DIR, logger)),
    ]

    all_passed = True
    for gate_name, gate_fn in gates:
        try:
            passed, detail = gate_fn()
            results[gate_name] = {"passed": passed, "detail": detail}
            status = "PASS" if passed else "FAIL"
            log_fn = logger.info if passed else logger.warning
            log_fn(f"  [{gate_name}] {status}: {detail}")
            if not passed:
                all_passed = False
        except Exception as e:
            results[gate_name] = {"passed": False, "detail": f"Exception: {e}"}
            logger.error(f"  [{gate_name}] ERROR: {e}")
            all_passed = False

    results["_all_passed"] = all_passed
    results["_resource_id"] = resource_id
    results["_filepath"] = str(filepath)
    results["_timestamp"] = datetime.now(timezone.utc).isoformat()

    return results


def promote_from_quarantine(filepath: Path, resource_id: str, logger: logging.Logger) -> Path | None:
    """Move a validated file from quarantine/ to data/raw/."""
    dest = RAW_DIR / filepath.name
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    try:
        import shutil
        shutil.move(str(filepath), str(dest))

        # Also move checksum file if it exists
        sha_file = filepath.with_suffix(filepath.suffix + ".sha256")
        if sha_file.exists():
            shutil.move(str(sha_file), str(RAW_DIR / sha_file.name))

        logger.info(f"[{resource_id}] PROMOTED: {filepath.name} → data/raw/")
        return dest
    except Exception as e:
        logger.error(f"[{resource_id}] Promotion failed: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Project Berunda — Resource Validation (Section I Quality Gates)"
    )
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Validate but don't promote from quarantine (default: True)")
    parser.add_argument("--no-dry-run", action="store_true",
                        help="Validate and promote passing files to data/raw/")
    parser.add_argument("--resource-id", type=str, default=None,
                        help="Validate only this resource ID")
    parser.add_argument("--priority", type=str, default=None,
                        choices=["P0", "P1", "P2", "P3", "P4"])
    parser.add_argument("--max-file-size", type=int, default=200*1024*1024,
                        help="(interface consistency)")
    parser.add_argument("--max-total-size", type=int, default=1024*1024*1024,
                        help="(interface consistency)")
    parser.add_argument("--resume", action="store_true", help="(interface consistency)")
    parser.add_argument("--force", action="store_true",
                        help="Re-validate even if already validated")

    args = parser.parse_args()
    dry_run = not args.no_dry_run
    logger = setup_logging()

    logger.info("=" * 60)
    logger.info("Project Berunda — Resource Validation")
    logger.info(f"Mode: {'DRY-RUN (validate only)' if dry_run else 'LIVE (validate + promote)'}")
    logger.info("=" * 60)

    # Find files in quarantine
    if not QUARANTINE_DIR.exists():
        logger.warning("No quarantine/ directory found — nothing to validate")
        sys.exit(0)

    # Scan quarantine subdirectories (one per resource_id)
    validation_results = []

    for subdir in sorted(QUARANTINE_DIR.iterdir()):
        if not subdir.is_dir():
            continue

        resource_id = subdir.name
        if args.resource_id and resource_id != args.resource_id:
            continue

        files = [f for f in subdir.iterdir() if f.is_file() and f.suffix != ".sha256"]
        if not files:
            continue

        for filepath in files:
            logger.info(f"[{resource_id}] Validating: {filepath.name}")

            # Check for companion checksum
            sha_path = filepath.with_suffix(filepath.suffix + ".sha256")
            expected_checksum = None
            if sha_path.exists():
                checksum_line = sha_path.read_text(encoding="utf-8").strip()
                expected_checksum = checksum_line.split()[0] if checksum_line else None

            result = validate_resource(resource_id, filepath, logger, expected_checksum)
            validation_results.append(result)

            if result["_all_passed"] and not dry_run:
                promote_from_quarantine(filepath, resource_id, logger)

    # Write validation report
    report_path = WORKSPACE_ROOT / "reports" / "VALIDATION_REPORT.md"
    write_validation_report(report_path, validation_results, logger)

    # Summary
    passed = sum(1 for r in validation_results if r["_all_passed"])
    failed = sum(1 for r in validation_results if not r["_all_passed"])
    logger.info("=" * 60)
    logger.info(f"VALIDATION SUMMARY: {passed} passed, {failed} failed, {len(validation_results)} total")
    logger.info("=" * 60)

    sys.exit(1 if failed > 0 else 0)


def write_validation_report(report_path: Path, results: list[dict], logger: logging.Logger):
    """Write VALIDATION_REPORT.md from gate results."""
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Validation Report\n",
        f"> **Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n",
        f"> **Files validated:** {len(results)}\n",
        "\n---\n",
    ]

    if not results:
        lines.append("\nNo files found in quarantine/ to validate.\n")
    else:
        for r in results:
            rid = r.get("_resource_id", "?")
            fp = r.get("_filepath", "?")
            status = "✅ ALL PASSED" if r["_all_passed"] else "❌ FAILED"
            lines.append(f"\n## {rid} — {status}\n")
            lines.append(f"**File:** `{fp}`\n\n")
            lines.append("| Gate | Result | Detail |\n|------|--------|--------|\n")

            for key, val in r.items():
                if key.startswith("_"):
                    continue
                icon = "✅" if val["passed"] else "❌"
                lines.append(f"| {key} | {icon} | {val['detail']} |\n")

    report_path.write_text("".join(lines), encoding="utf-8")
    logger.info(f"Validation report: {report_path}")


if __name__ == "__main__":
    main()
