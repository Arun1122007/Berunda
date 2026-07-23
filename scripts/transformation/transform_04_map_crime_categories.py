#!/usr/bin/env python3
"""
transform_04_map_crime_categories.py — Crime Category Mapping
Project Berunda — Karnataka State Police Datathon 2026

Maps IPC sections to BNS 2023 sections.
Reads *_03.csv -> *_04.csv
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

# Mock IPC to BNS mapping (flagged for legal review)
MOCK_BNS_MAPPING = {
    "Murder": "BNS-103",
    "Rape / Sexual Assault": "BNS-64",
    "Robbery": "BNS-309",
    "Burglary / House Break-in": "BNS-331",
    "Theft": "BNS-303",
    "Rioting": "BNS-191",
    "Cheating / Fraud": "BNS-318",
    "Kidnapping": "BNS-137",
    "Hurt / Assault": "BNS-115",
    "Cyber Crime": "IT-Act-66"
}

def setup_logging():
    logger = logging.getLogger("transform_04")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(LOGS_DIR / "acquisition.log", encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | TRANS-04 | %(message)s"))
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%H:%M:%S"))
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

def map_bns(crime_head):
    if pd.isna(crime_head):
        return "UNKNOWN"
    return MOCK_BNS_MAPPING.get(crime_head, f"BNS-MAPPED-{crime_head[:3].upper()}")

def main():
    parser = argparse.ArgumentParser(description="Map crime categories")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--no-dry-run", action="store_true")
    args = parser.parse_args()
    dry_run = not args.no_dry_run

    logger = setup_logging()
    logger.info("Starting transform_04_map_crime_categories")

    csv_files = list(INPUT_DIR.glob("*_03.csv"))
    if not csv_files:
        logger.warning(f"No *_03.csv files found in {INPUT_DIR}")
        sys.exit(0)

    transform_date = datetime.now(timezone.utc).isoformat()

    for file_path in csv_files:
        logger.info(f"Processing {file_path.name}")
        df = pd.read_csv(file_path, comment='#')

        df["_transform_version"] = VERSION
        df["_transform_date"] = transform_date

        if "CrimeMajorHeadName" in df.columns:
            df["MappedBNSSection"] = df["CrimeMajorHeadName"].apply(map_bns)
            logger.info("  Applied BNS Mapping to CrimeMajorHeadName")

        if not dry_run:
            out_name = file_path.name.replace("_03.csv", "_04.csv")
            out_path = OUTPUT_DIR / out_name
            df.to_csv(out_path, index=False)
            logger.info(f"  Saved to {out_path.name}")

    logger.info("transform_04 complete. [WARNING] REQUIRES HUMAN LEGAL REVIEW OF MAPPING.")

if __name__ == "__main__":
    main()
