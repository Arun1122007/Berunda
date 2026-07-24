#!/usr/bin/env python3
"""
transform_03_normalize_coordinates.py — Coordinate System Normalization
Project Berunda — Karnataka State Police Datathon 2026

Checks that Latitude/Longitude fall within Karnataka bounds.
Flags outliers. Reads *_02.csv -> *_03.csv
"""

import argparse
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent
INPUT_DIR = WORKSPACE_ROOT / "data" / "interim"
OUTPUT_DIR = WORKSPACE_ROOT / "data" / "interim"
LOGS_DIR = WORKSPACE_ROOT / "logs"
VERSION = "1.0.0"

# Approximate bounding box for Karnataka
KA_BOUNDS = {"lat_min": 11.5, "lat_max": 18.5, "lon_min": 74.0, "lon_max": 78.6}


def setup_logging():
    logger = logging.getLogger("transform_03")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(LOGS_DIR / "acquisition.log", encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | TRANS-03 | %(message)s"))
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%H:%M:%S")
    )
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def check_bounds(row):
    lat, lon = row.get("Latitude"), row.get("Longitude")
    if pd.isna(lat) or pd.isna(lon):
        return True  # Can't invalidate if missing
    return (
        KA_BOUNDS["lat_min"] <= lat <= KA_BOUNDS["lat_max"]
        and KA_BOUNDS["lon_min"] <= lon <= KA_BOUNDS["lon_max"]
    )


def main():
    parser = argparse.ArgumentParser(description="Normalize coordinates")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--no-dry-run", action="store_true")
    args = parser.parse_args()
    dry_run = not args.no_dry_run

    logger = setup_logging()
    logger.info("Starting transform_03_normalize_coordinates")

    csv_files = list(INPUT_DIR.glob("*_02.csv"))
    if not csv_files:
        logger.warning(f"No *_02.csv files found in {INPUT_DIR}")
        sys.exit(0)

    transform_date = datetime.now(timezone.utc).isoformat()

    for file_path in csv_files:
        logger.info(f"Processing {file_path.name}")
        df = pd.read_csv(file_path, comment="#")

        df["_transform_version"] = VERSION
        df["_transform_date"] = transform_date

        if "Latitude" in df.columns and "Longitude" in df.columns:
            df["GeoValid"] = df.apply(check_bounds, axis=1)
            invalid_count = (~df["GeoValid"]).sum()
            if invalid_count > 0:
                logger.warning(f"  Flagged {invalid_count} records with out-of-bounds coordinates")
            else:
                logger.info("  All coordinates valid")

        if not dry_run:
            out_name = file_path.name.replace("_02.csv", "_03.csv")
            out_path = OUTPUT_DIR / out_name
            df.to_csv(out_path, index=False)
            logger.info(f"  Saved to {out_path.name}")

    logger.info("transform_03 complete.")


if __name__ == "__main__":
    main()
