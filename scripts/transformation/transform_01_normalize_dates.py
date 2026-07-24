#!/usr/bin/env python3
"""
transform_01_normalize_dates.py — Date/Time Normalization
Project Berunda — Karnataka State Police Datathon 2026

Reads synthetic data, normalizes datetime fields to IST (UTC+5:30) in ISO8601,
adds traceability columns, and writes to data/interim/.
"""

import argparse
import logging
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent
INPUT_DIR = WORKSPACE_ROOT / "data" / "synthetic"
OUTPUT_DIR = WORKSPACE_ROOT / "data" / "interim"
LOGS_DIR = WORKSPACE_ROOT / "logs"

VERSION = "1.0.0"

DATE_COLS = [
    "IncidentFromDate",
    "IncidentToDate",
    "InfoReceivedPSDate",
    "CrimeRegisteredDate",
    "ArrestSurrenderDate",
    "csdate",
    "RecoveryDate",
]


def setup_logging():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("transform_01")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(LOGS_DIR / "acquisition.log", encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | TRANS-01 | %(message)s"))
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%H:%M:%S")
    )
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def normalize_to_ist(dt_str):
    if pd.isna(dt_str) or not dt_str:
        return ""
    try:
        # Assuming input is either ISO without TZ (treat as local/IST) or with TZ
        # If it's already an ISO string from our synthetic generator, it lacks a timezone.
        dt = pd.to_datetime(dt_str)
        if dt.tzinfo is None:
            # Localize to UTC, convert to IST +0530
            # Wait, synthetic generator used datetime.now/random naive datetimes representing IST.
            dt = dt.tz_localize(timezone(timedelta(hours=5, minutes=30)))
        return dt.isoformat()
    except Exception:
        return dt_str


def main():
    parser = argparse.ArgumentParser(description="Normalize dates to IST")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Don't write files")
    parser.add_argument("--no-dry-run", action="store_true", help="Write files to interim/")
    args = parser.parse_args()
    dry_run = not args.no_dry_run

    logger = setup_logging()
    logger.info("Starting transform_01_normalize_dates")

    if not INPUT_DIR.exists():
        logger.error(f"Input dir not found: {INPUT_DIR}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    csv_files = list(INPUT_DIR.glob("*.csv"))
    if not csv_files:
        logger.warning(f"No CSV files found in {INPUT_DIR}")
        sys.exit(0)

    transform_date = datetime.now(timezone.utc).isoformat()

    for file_path in csv_files:
        logger.info(f"Processing {file_path.name}")
        df = pd.read_csv(file_path, comment="#")

        # Add traceability
        if "_source_file" not in df.columns:
            df["_source_file"] = file_path.name
            df["_source_row"] = range(1, len(df) + 1)

        df["_transform_version"] = VERSION
        df["_transform_date"] = transform_date

        # Normalize dates
        for col in DATE_COLS:
            if col in df.columns:
                df[col] = df[col].apply(normalize_to_ist)
                logger.info(f"  Normalized column: {col}")

        if not dry_run:
            out_name = file_path.stem + "_01" + file_path.suffix
            out_path = OUTPUT_DIR / out_name
            df.to_csv(out_path, index=False)
            logger.info(f"  Saved to {out_path.name}")
        else:
            logger.info(f"  DRY-RUN: Would save to {file_path.stem}_01{file_path.suffix}")

    logger.info("transform_01 complete.")


if __name__ == "__main__":
    main()
