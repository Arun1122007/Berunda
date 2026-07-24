#!/usr/bin/env python3
"""
transform_05_build_feature_tables.py — Feature Table Construction
Project Berunda — Karnataka State Police Datathon 2026

Aggregates case data to build feature tables for ML models.
Reads from *_04.csv in interim/ and outputs final files to data/processed/.
"""

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent
INPUT_DIR = WORKSPACE_ROOT / "data" / "interim"
OUTPUT_DIR = WORKSPACE_ROOT / "data" / "processed"
LOGS_DIR = WORKSPACE_ROOT / "logs"
VERSION = "1.0.0"


def setup_logging():
    logger = logging.getLogger("transform_05")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(LOGS_DIR / "acquisition.log", encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | TRANS-05 | %(message)s"))
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%H:%M:%S")
    )
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def process_case_master(file_path, logger, dry_run):
    df = pd.read_csv(file_path, comment="#")
    if "IncidentFromDate" not in df.columns or "DistrictName" not in df.columns:
        return

    df["DateObj"] = pd.to_datetime(df["IncidentFromDate"])
    df["YearMonth"] = df["DateObj"].dt.to_period("M")

    # Aggregation: Count of crimes per district per month
    agg_df = df.groupby(["YearMonth", "DistrictName"]).size().reset_index(name="CrimeCount")

    # Save Feature Table
    out_path = OUTPUT_DIR / "FEATURE_District_Crime_Density.csv"
    if not dry_run:
        agg_df.to_csv(out_path, index=False)
        logger.info(f"  Built feature table: {out_path.name}")

    # Also save the final processed file
    final_out_path = OUTPUT_DIR / file_path.name.replace("_04.csv", "_FINAL.csv")
    if not dry_run:
        df.drop(columns=["DateObj", "YearMonth"], inplace=True, errors="ignore")
        df.to_csv(final_out_path, index=False)
        logger.info(f"  Saved final processed file to {final_out_path.name}")


def main():
    parser = argparse.ArgumentParser(description="Build feature tables")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--no-dry-run", action="store_true")
    args = parser.parse_args()
    dry_run = not args.no_dry_run

    logger = setup_logging()
    logger.info("Starting transform_05_build_feature_tables")

    csv_files = list(INPUT_DIR.glob("*_04.csv"))
    if not csv_files:
        logger.warning(f"No *_04.csv files found in {INPUT_DIR}")
        sys.exit(0)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for file_path in csv_files:
        logger.info(f"Processing {file_path.name}")

        # If this is the CaseMaster file, build features from it
        if "CaseMaster" in file_path.name:
            process_case_master(file_path, logger, dry_run)
        else:
            # Just move other files to processed
            if not dry_run:
                df = pd.read_csv(file_path, comment="#")
                final_out_path = OUTPUT_DIR / file_path.name.replace("_04.csv", "_FINAL.csv")
                df.to_csv(final_out_path, index=False)
                logger.info(f"  Saved final processed file to {final_out_path.name}")

    logger.info("transform_05 complete. Processed data ready in data/processed/")


if __name__ == "__main__":
    main()
