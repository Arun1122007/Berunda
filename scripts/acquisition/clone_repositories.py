#!/usr/bin/env python3
"""
clone_repositories.py — Repository Acquisition Script
Project Berunda — Karnataka State Police Datathon 2026

Shallow clones Git repos into repositories/<owner>__<repo>/
with commit pinning, license detection, and secrets scanning.

Standard flags: --dry-run, --resource-id, --priority, --max-file-size,
                --max-total-size, --resume, --force
"""

import argparse
import csv
import logging
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent
REPOS_DIR = WORKSPACE_ROOT / "repositories"
MANIFESTS_DIR = WORKSPACE_ROOT / "manifests"

MAX_RETRIES = 5
BACKOFF_BASE = 2
CLONE_TIMEOUT = 300

GIT_RESOURCES = {
    "RSRC-050": {
        "url": "https://github.com/alephdata/followthemoney",
        "name": "FollowTheMoney schema",
        "classification": "REFERENCE",
    },
    "RSRC-052": {
        "url": "https://github.com/keplergl/kepler.gl",
        "name": "Kepler.gl",
        "classification": "REFERENCE",
    },
    "RSRC-065": {
        "url": "https://github.com/maplibre/maplibre-gl-js",
        "name": "MapLibre GL JS",
        "classification": "REFERENCE",
    },
}

SECRETS_PATTERNS = [
    re.compile(r'(?i)(api[_-]?key|apikey)\s*[:=]\s*[\'"][a-zA-Z0-9]{16,}'),
    re.compile(r'(?i)(secret|password|passwd|pwd)\s*[:=]\s*[\'"][^\s\'"]{8,}'),
    re.compile(r"(?i)bearer\s+[a-zA-Z0-9\-._~+/]+=*"),
    re.compile(r"(?i)(aws_access_key_id|aws_secret_access_key)\s*=\s*\S+"),
    re.compile(r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----"),
    re.compile(r"ghp_[a-zA-Z0-9]{36}"),
    re.compile(r"gho_[a-zA-Z0-9]{36}"),
]


# ── Logging ──────────────────────────────────────────────────


def setup_logging() -> logging.Logger:
    log_dir = WORKSPACE_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "acquisition.log"

    logger = logging.getLogger("berunda.clone")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)-8s | CLONE | %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z"
        )
    )

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%H:%M:%S")
    )

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


# ── Git helpers ──────────────────────────────────────────────


def run_git(
    args: list[str], cwd: str | None = None, timeout: int = CLONE_TIMEOUT
) -> tuple[int, str, str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except FileNotFoundError:
        return -1, "", "git not found"


def get_clone_dir(url: str) -> Path:
    parts = url.rstrip("/").split("/")
    owner = parts[-2] if len(parts) >= 2 else "unknown"
    repo = parts[-1] if parts else "unknown"
    return REPOS_DIR / f"{owner}__{repo}"


# ── License detection ────────────────────────────────────────


def find_license(repo_path: Path) -> tuple[str, str]:
    license_names = [
        "LICENSE",
        "LICENSE.md",
        "LICENSE.txt",
        "LICENCE",
        "LICENCE.md",
        "LICENCE.txt",
        "COPYING",
        "COPYING.md",
    ]
    for name in license_names:
        lpath = repo_path / name
        if lpath.exists():
            try:
                content = lpath.read_text(encoding="utf-8", errors="ignore")[:2000].lower()
                if "mit license" in content or "permission is hereby granted" in content:
                    return "MIT", name
                if "apache license" in content and "version 2.0" in content:
                    return "Apache-2.0", name
                if "bsd" in content and "3-clause" in content:
                    return "BSD-3-Clause", name
                if "bsd" in content and "2-clause" in content:
                    return "BSD-2-Clause", name
                if "gnu general public license" in content:
                    if "version 3" in content:
                        return "GPL-3.0", name
                    if "version 2" in content:
                        return "GPL-2.0", name
                    return "GPL", name
                if "isc license" in content:
                    return "ISC", name
                if "mozilla public license" in content:
                    return "MPL-2.0", name
                return "UNKNOWN", name
            except Exception:
                continue
    return "NONE", ""


# ── Dependency detection ────────────────────────────────────


def find_dependency_files(repo_path: Path) -> list[str]:
    candidates = [
        "package.json",
        "requirements.txt",
        "setup.py",
        "setup.cfg",
        "pyproject.toml",
        "Pipfile",
        "Cargo.toml",
        "go.mod",
        "pom.xml",
        "build.gradle",
        "Gemfile",
        "composer.json",
    ]
    return [name for name in candidates if (repo_path / name).exists()]


# ── Secrets scan ─────────────────────────────────────────────


def scan_for_secrets(repo_path: Path, logger: logging.Logger) -> list[str]:
    findings = []
    skip_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv", ".gitignore"}
    skip_exts = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".ico",
        ".woff",
        ".woff2",
        ".ttf",
        ".eot",
        ".svg",
        ".mp4",
        ".webm",
        ".zip",
        ".tar",
        ".gz",
        ".jar",
        ".class",
        ".pyc",
        ".exe",
        ".dll",
        ".so",
        ".dylib",
        ".bin",
    }

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for fname in files:
            fpath = Path(root) / fname
            if fpath.suffix.lower() in skip_exts:
                continue
            try:
                if fpath.stat().st_size > 1_000_000:
                    continue
            except OSError:
                continue
            try:
                content = fpath.read_text(encoding="utf-8", errors="ignore")
                for i, pattern in enumerate(SECRETS_PATTERNS):
                    matches = pattern.findall(content)
                    if matches:
                        rel_path = fpath.relative_to(repo_path)
                        findings.append(f"PATTERN[{i}] in {rel_path}: {len(matches)} match(es)")
                        if len(findings) >= 50:
                            logger.warning("Secrets scan: hit 50-finding limit, stopping")
                            return findings
            except Exception:
                continue

    return findings


# ── Inventory update ─────────────────────────────────────────


def update_repo_inventory(manifests_dir: Path, entry: dict):
    csv_path = manifests_dir / "repository_inventory.csv"
    fieldnames = [
        "rsrc_id",
        "repo_url",
        "clone_path",
        "pinned_commit",
        "license_spdx",
        "classification",
        "dependency_file",
        "secrets_scan_result",
    ]
    file_exists = csv_path.exists() and csv_path.stat().st_size > 50
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)


# ── Clone logic ──────────────────────────────────────────────


def clone_repository(
    resource_id: str,
    repo_info: dict,
    logger: logging.Logger,
    dry_run: bool,
    force: bool,
) -> bool:
    url = repo_info["url"]
    name = repo_info["name"]
    classification = repo_info["classification"]
    clone_dir = get_clone_dir(url)

    if clone_dir.exists() and not force:
        logger.info(f"[{resource_id}] SKIP — already cloned: {clone_dir.name}")
        return True

    if dry_run:
        logger.info(f"[{resource_id}] DRY-RUN — would clone: {url}")
        logger.info(f"         -> {clone_dir}")
        return True

    logger.info(f"[{resource_id}] CLONING: {name} | {url}")
    logger.info(f"         Dest: {clone_dir}")

    REPOS_DIR.mkdir(parents=True, exist_ok=True)

    if clone_dir.exists() and force:
        logger.warning(f"[{resource_id}] Force mode — removing existing clone")
        shutil.rmtree(clone_dir)

    # Clone with retry
    clone_success = False
    for attempt in range(1, MAX_RETRIES + 1):
        logger.info(f"  Attempt {attempt}/{MAX_RETRIES}")
        rc, _stdout, stderr = run_git(["clone", "--depth", "1", url, str(clone_dir)])
        if rc == 0:
            clone_success = True
            break
        logger.warning(f"  Attempt {attempt} failed: {stderr or 'unknown error'}")
        if attempt < MAX_RETRIES:
            backoff = BACKOFF_BASE**attempt
            logger.info(f"  Waiting {backoff}s before retry...")
            time.sleep(backoff)

    if not clone_success:
        logger.error(f"[{resource_id}] Clone failed after {MAX_RETRIES} attempts")
        return False

    # Pin commit
    rc, commit_hash, _ = run_git(["rev-parse", "HEAD"], cwd=str(clone_dir))
    if rc != 0:
        commit_hash = "UNKNOWN"
    run_git(["tag", f"berunda-pin-{resource_id}", "HEAD"], cwd=str(clone_dir))
    logger.info(f"[{resource_id}] Pinned at commit: {commit_hash}")

    # License
    spdx, license_file = find_license(clone_dir)
    logger.info(f"[{resource_id}] License: {spdx} ({license_file})")

    # Dependencies
    dep_files = find_dependency_files(clone_dir)
    if dep_files:
        logger.info(f"[{resource_id}] Dependency files: {dep_files}")

    # Secrets scan
    logger.info(f"[{resource_id}] Running secrets scan...")
    findings = scan_for_secrets(clone_dir, logger)
    scan_result = "CLEAN" if not findings else f"ALERT: {len(findings)} finding(s)"
    if findings:
        logger.warning(f"[{resource_id}] Secrets scan: {scan_result}")
        for f in findings[:10]:
            logger.warning(f"  {f}")
    else:
        logger.info(f"[{resource_id}] Secrets scan: CLEAN")

    # Update inventory
    update_repo_inventory(
        MANIFESTS_DIR,
        {
            "rsrc_id": resource_id,
            "repo_url": url,
            "clone_path": str(clone_dir.relative_to(WORKSPACE_ROOT)).replace("\\", "/"),
            "pinned_commit": commit_hash,
            "license_spdx": spdx,
            "classification": classification,
            "dependency_file": ";".join(dep_files),
            "secrets_scan_result": scan_result,
        },
    )

    logger.info(f"[{resource_id}] SUCCESS — cloned, pinned, scanned")
    return True


# ── CLI ──────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Project Berunda — Repository Clone Script",
        epilog="Clones into repositories/<owner>__<repo>/",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Show what would be cloned (default: True)",
    )
    parser.add_argument("--no-dry-run", action="store_true", help="Actually perform clones")
    parser.add_argument("--resource-id", type=str, default=None, help="Clone only this resource ID")
    parser.add_argument(
        "--priority",
        type=str,
        default=None,
        choices=["P0", "P1", "P2", "P3", "P4"],
        help="Filter by priority (N/A for git clones)",
    )
    parser.add_argument(
        "--max-file-size",
        type=int,
        default=200 * 1024 * 1024,
        help="Interface consistency (not used for git)",
    )
    parser.add_argument(
        "--max-total-size",
        type=int,
        default=1024 * 1024 * 1024,
        help="Interface consistency (not used for git)",
    )
    parser.add_argument(
        "--resume", action="store_true", help="Interface consistency (not used for git)"
    )
    parser.add_argument("--force", action="store_true", help="Re-clone even if already present")

    args = parser.parse_args()
    dry_run = not args.no_dry_run

    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("Project Berunda — Repository Clone")
    logger.info(f"Mode: {'DRY-RUN' if dry_run else 'LIVE CLONE'}")
    logger.info("=" * 60)

    targets = dict(GIT_RESOURCES)
    if args.resource_id:
        if args.resource_id in targets:
            targets = {args.resource_id: targets[args.resource_id]}
        else:
            logger.warning(f"Resource {args.resource_id} is not a git-cloneable resource")
            sys.exit(0)

    results = {"success": 0, "failed": 0, "skipped": 0}
    for rid, info in targets.items():
        clone_dir = get_clone_dir(info["url"])
        if clone_dir.exists() and not args.force and not dry_run:
            logger.info(f"[{rid}] SKIP — already cloned: {clone_dir.name}")
            results["skipped"] += 1
            continue
        ok = clone_repository(rid, info, logger, dry_run, args.force)
        if ok:
            if dry_run:
                results["skipped"] += 1
            else:
                results["success"] += 1
        else:
            results["failed"] += 1

    exit_code = (
        2
        if results["failed"] > 0 and results["success"] == 0
        else (1 if results["failed"] > 0 else 0)
    )

    logger.info("=" * 60)
    logger.info("CLONE SUMMARY")
    logger.info(f"  Success:  {results['success']}")
    logger.info(f"  Skipped:  {results['skipped']}")
    logger.info(f"  Failed:   {results['failed']}")
    logger.info(f"  Exit code: {exit_code}")
    logger.info("=" * 60)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
