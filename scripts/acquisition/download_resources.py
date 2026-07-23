#!/usr/bin/env python3
"""
download_resources.py — Resource Acquisition Script
Project Berunda — Karnataka State Police Datathon 2026

Downloads resources into quarantine/ following all safety rules.
On success, promotes validated files to data/raw/.

Standard flags: --dry-run, --resource-id, --priority, --max-file-size,
                --max-total-size, --resume, --force
"""

import argparse
import csv
import hashlib
import json
import logging
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package required. Install with: pip install requests")
    sys.exit(2)

# ── Constants ────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent
QUARANTINE_DIR = WORKSPACE_ROOT / "quarantine"
RAW_DIR = WORKSPACE_ROOT / "data" / "raw"
MANIFESTS_DIR = WORKSPACE_ROOT / "manifests"

DEFAULT_MAX_FILE_SIZE = 200 * 1024 * 1024   # 200 MB
DEFAULT_MAX_TOTAL_SIZE = 1024 * 1024 * 1024  # 1 GB
MAX_RETRIES = 5
BACKOFF_BASE = 2
CONNECT_TIMEOUT = 30
DOWNLOAD_TIMEOUT = 300

USER_AGENT = "ProjectBerunda-AcquisitionAgent/1.0 (KSP-Datathon-2026)"

DOMAIN_ALLOWLIST = {
    "hack2skill.com", "catalyst.zoho.com", "help.catalyst.zoho.com",
    "ncrb.gov.in", "data.gov.in", "ksp.karnataka.gov.in",
    "ndap.niti.gov.in", "overpass-api.de", "bhuvan.nrsc.gov.in",
    "censusindia.gov.in", "open-meteo.com", "indiacode.nic.in",
    "bprd.nic.in", "github.com", "js.cytoscape.org", "pypi.org",
    "npmjs.com", "owasp.org", "nist.gov", "geojson.org",
    "networkx.org", "neo4j.com",
}

DOWNLOADABLE_METHODS = {"AUTO-DIRECT-DOWNLOAD"}

SKIP_METHODS = {
    "MANUAL-AUTHORIZED": "Requires human action",
    "AUTO-BROWSER-WITH-USER-SESSION": "Requires authenticated browser session",
    "SEMI-AUTOMATED": "Requires human confirmation of access method",
    "DO-NOT-ACQUIRE": "Explicitly excluded from acquisition",
    "FUTURE-RESTRICTED": "Restricted — not acquired under this blueprint",
    "AUTO-API": "Use dedicated API scripts instead",
    "AUTO-GIT": "Use clone_repositories.py instead",
}


# ── Logging ──────────────────────────────────────────────────

def setup_logging(workspace_root: Path) -> logging.Logger:
    log_dir = workspace_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "acquisition.log"

    logger = logging.getLogger("berunda.acquisition")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | DOWNLOAD | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z"
    ))

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S"
    ))

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


# ── Utilities ────────────────────────────────────────────────

def sha256_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def is_domain_allowed(url: str) -> bool:
    try:
        hostname = urlparse(url).hostname or ""
        for allowed in DOMAIN_ALLOWLIST:
            if hostname == allowed or hostname.endswith("." + allowed):
                return True
        return False
    except Exception:
        return False


def validate_path_in_workspace(path: Path, workspace: Path) -> bool:
    try:
        path.resolve().relative_to(workspace.resolve())
        return True
    except ValueError:
        return False


def load_manifest(manifest_path: Path) -> list[dict]:
    if not manifest_path.exists():
        return []
    with open(manifest_path, encoding="utf-8") as f:
        return json.load(f)


def update_download_manifest(manifests_dir: Path, entry: dict):
    csv_path = manifests_dir / "download_manifest.csv"
    fieldnames = [
        "rsrc_id", "url", "http_status", "bytes_received",
        "timestamp", "local_path", "checksum_sha256"
    ]
    file_exists = csv_path.exists() and csv_path.stat().st_size > 0
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)


def append_provenance(manifests_dir: Path, entry: dict):
    jsonl_path = manifests_dir / "provenance.jsonl"
    with open(jsonl_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def append_failure_log(manifests_dir: Path, resource_id: str, reason: str, next_action: str):
    csv_path = manifests_dir / "failure_log.csv"
    fieldnames = ["resource_id", "attempted_date", "failure_reason", "next_action"]
    file_exists = csv_path.exists() and csv_path.stat().st_size > 0
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "resource_id": resource_id,
            "attempted_date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "failure_reason": reason,
            "next_action": next_action,
        })


# ── Download Engine ──────────────────────────────────────────

def download_file(
    url: str,
    dest_path: Path,
    logger: logging.Logger,
    max_file_size: int = DEFAULT_MAX_FILE_SIZE,
    connect_timeout: int = CONNECT_TIMEOUT,
    download_timeout: int = DOWNLOAD_TIMEOUT,
    resume: bool = False,
) -> dict:
    headers = {"User-Agent": USER_AGENT}
    start_byte = 0
    mode = "wb"

    if resume and dest_path.exists():
        start_byte = dest_path.stat().st_size
        headers["Range"] = f"bytes={start_byte}-"
        mode = "ab"
        logger.info(f"  Resuming from byte {start_byte}")

    session = requests.Session()
    session.stream = True

    response = session.get(
        url,
        headers=headers,
        stream=True,
        timeout=(connect_timeout, download_timeout),
        allow_redirects=True,
    )

    if response.history:
        chain = " -> ".join(r.url for r in response.history)
        logger.debug(f"  Redirect chain: {chain} -> {response.url}")

    response.raise_for_status()

    content_length = response.headers.get("Content-Length")
    if content_length and int(content_length) > max_file_size:
        return {
            "success": False,
            "http_status": response.status_code,
            "bytes_received": 0,
            "checksum": "",
            "error": f"File size {int(content_length)} exceeds max {max_file_size} bytes",
        }

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    bytes_received = start_byte
    hasher = hashlib.sha256()

    with open(dest_path, mode) as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                bytes_received += len(chunk)
                if bytes_received > max_file_size:
                    return {
                        "success": False,
                        "http_status": response.status_code,
                        "bytes_received": bytes_received,
                        "checksum": "",
                        "error": f"Download exceeded max size {max_file_size} bytes",
                    }
                f.write(chunk)
                hasher.update(chunk)

    if resume and start_byte > 0:
        checksum = sha256_file(dest_path)
    else:
        checksum = hasher.hexdigest()

    sha_path = dest_path.with_name(dest_path.name + ".sha256")
    sha_path.write_text(f"{checksum}  {dest_path.name}\n", encoding="utf-8")

    return {
        "success": True,
        "http_status": response.status_code,
        "bytes_received": bytes_received,
        "checksum": checksum,
        "error": "",
    }


def download_with_retry(
    url: str,
    dest_path: Path,
    logger: logging.Logger,
    max_file_size: int = DEFAULT_MAX_FILE_SIZE,
    connect_timeout: int = CONNECT_TIMEOUT,
    download_timeout: int = DOWNLOAD_TIMEOUT,
    resume: bool = False,
    max_retries: int = MAX_RETRIES,
) -> dict:
    last_error = ""
    http_status = 0
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"  Attempt {attempt}/{max_retries}: {url}")
            result = download_file(
                url, dest_path, logger, max_file_size,
                connect_timeout, download_timeout, resume
            )
            if result["success"]:
                return result
            last_error = result["error"]
            http_status = result["http_status"]
            logger.warning(f"  Attempt {attempt} failed: {last_error}")
        except requests.exceptions.Timeout:
            last_error = f"Timeout (connect={connect_timeout}s, download={download_timeout}s)"
            logger.warning(f"  Attempt {attempt} timed out")
        except requests.exceptions.ConnectionError as e:
            last_error = f"Connection error: {e}"
            logger.warning(f"  Attempt {attempt} connection error")
        except requests.exceptions.HTTPError as e:
            http_status = e.response.status_code
            last_error = f"HTTP {http_status}"
            logger.warning(f"  Attempt {attempt} HTTP {http_status}")
            if http_status < 500 and http_status != 429:
                return {
                    "success": False,
                    "http_status": http_status,
                    "bytes_received": 0, "checksum": "",
                    "error": last_error,
                }
        except Exception as e:
            last_error = f"Unexpected error: {e}"
            logger.error(f"  Attempt {attempt}: {e}")

        if attempt < max_retries:
            backoff = BACKOFF_BASE ** attempt
            logger.info(f"  Waiting {backoff}s before retry...")
            time.sleep(backoff)

    return {
        "success": False,
        "http_status": http_status,
        "bytes_received": 0, "checksum": "",
        "error": f"All {max_retries} attempts failed. Last error: {last_error}",
    }


# ── Main Logic ───────────────────────────────────────────────

def process_resource(
    resource: dict,
    logger: logging.Logger,
    dry_run: bool,
    max_file_size: int,
    max_total_size: int,
    total_downloaded: int,
    resume: bool,
    force: bool,
) -> tuple[dict | None, int]:
    rid = resource["rsrc_id"]
    method = resource["method"]
    url = resource["source_url"]
    status = resource.get("status", "missing")
    name = resource["name"]

    if status == "completed" and not force:
        logger.info(f"[{rid}] SKIP — already completed: {name}")
        return None, 0

    if method in SKIP_METHODS:
        logger.info(f"[{rid}] SKIP — {SKIP_METHODS[method]}: {name}")
        return None, 0

    if "pip" in method.lower() or "npm" in method.lower():
        logger.info(f"[{rid}] SKIP — package manager install: {name}")
        return None, 0

    if method not in DOWNLOADABLE_METHODS:
        logger.info(f"[{rid}] SKIP — method '{method}' not handled: {name}")
        return None, 0

    if not url or url in ("n/a", "various", "organizer Resources tab", "UNVERIFIED"):
        logger.warning(f"[{rid}] SKIP — no valid URL: {url}")
        append_failure_log(MANIFESTS_DIR, rid, f"No valid URL: {url}", "Verify URL and retry")
        return None, 0

    if not is_domain_allowed(url):
        logger.warning(f"[{rid}] BLOCKED — domain not on allowlist: {url}")
        append_failure_log(MANIFESTS_DIR, rid,
                           f"Domain not on allowlist: {urlparse(url).hostname}",
                           "Add to allowlist with human approval")
        return None, 0

    if total_downloaded >= max_total_size:
        logger.warning(f"[{rid}] BLOCKED — total download limit reached ({max_total_size} bytes)")
        return None, 0

    # Destination
    date_suffix = datetime.now(timezone.utc).strftime("%Y%m%d")
    parsed = urlparse(url)
    url_filename = Path(parsed.path).name if parsed.path and parsed.path != "/" else ""
    if not url_filename or url_filename == "/":
        url_filename = f"{rid}_resource"
    stem = Path(url_filename).stem
    ext = Path(url_filename).suffix or ".html"
    dest_filename = f"{stem}_{date_suffix}{ext}"
    dest_path = QUARANTINE_DIR / rid / dest_filename

    if not validate_path_in_workspace(dest_path, WORKSPACE_ROOT):
        logger.error(f"[{rid}] SECURITY — path escapes workspace: {dest_path}")
        return None, 0

    raw_dest_dir = RAW_DIR / rid
    raw_dest_path = raw_dest_dir / dest_filename

    if dest_path.exists() and not force:
        existing_checksum = sha256_file(dest_path)
        logger.info(f"[{rid}] SKIP — already in quarantine: {dest_path.name} (sha256: {existing_checksum[:16]}...)")
        return None, 0

    if raw_dest_path.exists() and not force:
        logger.info(f"[{rid}] SKIP — already promoted to raw: {raw_dest_path.name}")
        return None, 0

    if dry_run:
        logger.info(f"[{rid}] DRY-RUN — would download: {url}")
        logger.info(f"         -> {dest_path}")
        return {
            "rsrc_id": rid, "url": url, "http_status": "DRY-RUN",
            "bytes_received": 0,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "local_path": str(dest_path.relative_to(WORKSPACE_ROOT)),
            "checksum_sha256": "",
        }, 0

    # ── DOWNLOAD ──
    logger.info(f"[{rid}] DOWNLOADING: {name} | {url}")
    logger.info(f"         Dest: {dest_path}")

    result = download_with_retry(
        url=url, dest_path=dest_path, logger=logger,
        max_file_size=max_file_size, resume=resume,
    )

    if not result["success"]:
        logger.error(f"[{rid}] FAILED — {result['error']}")
        append_failure_log(MANIFESTS_DIR, rid, result["error"], "Investigate and retry")
        return None, 0

    # Success — log and promote
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    checksum = result["checksum"]
    file_size = result["bytes_received"]
    logger.info(f"[{rid}] SUCCESS — {file_size} bytes, sha256: {checksum}")

    # Promote from quarantine to data/raw/
    raw_dest_dir = RAW_DIR / rid
    raw_dest_dir.mkdir(parents=True, exist_ok=True)
    raw_dest_path = raw_dest_dir / dest_filename

    if raw_dest_path.exists():
        raw_dest_path.unlink()
    shutil.move(str(dest_path), str(raw_dest_path))

    sha_src = dest_path.with_name(dest_path.name + ".sha256")
    sha_dst = raw_dest_path.with_name(raw_dest_path.name + ".sha256")
    if sha_src.exists():
        shutil.move(str(sha_src), str(sha_dst))

    logger.info(f"[{rid}] PROMOTED to: {raw_dest_path}")

    # Update manifests
    append_provenance(MANIFESTS_DIR, {
        "rsrc_id": rid,
        "source_url": url,
        "access_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "checksum_sha256": checksum,
        "transform_applied": None,
        "derived_from": None,
    })

    entry = {
        "rsrc_id": rid,
        "url": url,
        "http_status": result["http_status"],
        "bytes_received": file_size,
        "timestamp": timestamp,
        "local_path": "." + str(raw_dest_path).replace(str(WORKSPACE_ROOT), "").replace("\\", "/"),
        "checksum_sha256": checksum,
    }
    update_download_manifest(MANIFESTS_DIR, entry)
    return entry, file_size


def main():
    parser = argparse.ArgumentParser(
        description="Project Berunda — Resource Acquisition Script",
        epilog="Downloads to quarantine/ first. Promotes to data/raw/ after validation.",
    )
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Show what would be downloaded (default: True)")
    parser.add_argument("--no-dry-run", action="store_true",
                        help="Actually perform downloads")
    parser.add_argument("--resource-id", type=str, default=None,
                        help="Download only this resource ID (e.g., R006)")
    parser.add_argument("--priority", type=str, default=None,
                        choices=["P0", "P1", "P2", "P3", "P4"],
                        help="Download only resources of this priority")
    parser.add_argument("--max-file-size", type=int, default=DEFAULT_MAX_FILE_SIZE,
                        help=f"Max single file size in bytes (default: {DEFAULT_MAX_FILE_SIZE})")
    parser.add_argument("--max-total-size", type=int, default=DEFAULT_MAX_TOTAL_SIZE,
                        help=f"Max total download size in bytes (default: {DEFAULT_MAX_TOTAL_SIZE})")
    parser.add_argument("--resume", action="store_true",
                        help="Resume partially downloaded files")
    parser.add_argument("--force", action="store_true",
                        help="Re-download even if already present")
    parser.add_argument("--workspace", type=str, default=str(WORKSPACE_ROOT),
                        help="Workspace root path")

    args = parser.parse_args()
    dry_run = not args.no_dry_run
    workspace = Path(args.workspace).resolve()
    logger = setup_logging(workspace)

    logger.info("=" * 60)
    logger.info("Project Berunda — Resource Acquisition")
    logger.info(f"Mode: {'DRY-RUN' if dry_run else 'LIVE DOWNLOAD'}")
    logger.info(f"Workspace: {workspace}")
    if args.resource_id:
        logger.info(f"Filter: resource_id = {args.resource_id}")
    if args.priority:
        logger.info(f"Filter: priority = {args.priority}")
    logger.info("=" * 60)

    manifest_path = workspace / "manifests" / "resource_manifest.json"
    resources = load_manifest(manifest_path)
    if not resources:
        logger.error(f"No resources found in {manifest_path}")
        sys.exit(2)

    logger.info(f"Loaded {len(resources)} resources from manifest")

    if args.resource_id:
        resources = [r for r in resources if r["rsrc_id"] == args.resource_id]
    if args.priority:
        resources = [r for r in resources if r["priority"] == args.priority]

    if not resources:
        logger.warning("No resources match the specified filters")
        sys.exit(0)

    logger.info(f"Processing {len(resources)} resource(s)")

    total_downloaded = 0
    results = {"downloaded": 0, "skipped": 0, "failed": 0, "dry_run": 0}

    for resource in resources:
        entry, bytes_added = process_resource(
            resource=resource, logger=logger, dry_run=dry_run,
            max_file_size=args.max_file_size,
            max_total_size=args.max_total_size,
            total_downloaded=total_downloaded,
            resume=args.resume, force=args.force,
        )
        if entry is None:
            results["skipped"] += 1
        elif entry.get("http_status") == "DRY-RUN":
            results["dry_run"] += 1
        elif bytes_added > 0:
            results["downloaded"] += 1
            total_downloaded += bytes_added
        else:
            results["failed"] += 1

    exit_code = 2 if results["failed"] > 0 and results["downloaded"] == 0 else (
        1 if results["failed"] > 0 else 0
    )

    logger.info("=" * 60)
    logger.info("ACQUISITION SUMMARY")
    logger.info(f"  Downloaded:  {results['downloaded']}")
    logger.info(f"  Skipped:     {results['skipped']}")
    logger.info(f"  Failed:      {results['failed']}")
    logger.info(f"  Dry-run:     {results['dry_run']}")
    logger.info(f"  Total bytes: {total_downloaded}")
    logger.info(f"  Exit code:   {exit_code}")
    logger.info("=" * 60)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
