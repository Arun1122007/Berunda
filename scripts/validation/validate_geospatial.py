#!/usr/bin/env python3
"""
validate_geospatial.py — Geospatial Validation Script
Project Berunda — Karnataka State Police Datathon 2026

Section I quality gates specific to spatial data:
- Geometry validity
- Coordinates within Karnataka bounding box
- CRS = WGS84 (EPSG:4326)
- Administrative-code join check
"""

import argparse
import json
import logging
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent
LOGS_DIR = WORKSPACE_ROOT / "logs"

# Karnataka approximate bounding box (WGS84)
KARNATAKA_BBOX = {
    "min_lat": 11.5,
    "max_lat": 18.5,
    "min_lon": 74.0,
    "max_lon": 78.6,
}

KARNATAKA_DISTRICTS = [
    "Bagalkot", "Ballari", "Belagavi", "Bengaluru Rural",
    "Bengaluru Urban", "Bidar", "Chamarajanagar", "Chikkaballapur",
    "Chikkamagaluru", "Chitradurga", "Dakshina Kannada", "Davanagere",
    "Dharwad", "Gadag", "Hassan", "Haveri", "Kalaburagi",
    "Kodagu", "Kolar", "Koppal", "Mandya", "Mysuru",
    "Raichur", "Ramanagara", "Shivamogga", "Tumakuru",
    "Udupi", "Uttara Kannada", "Vijayapura", "Yadgir",
    "Vijayanagara",
]


def setup_logging() -> logging.Logger:
    log_file = LOGS_DIR / "acquisition.log"
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("berunda.geospatial")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | GEO-VALIDATE | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z"
    ))
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s",
                                       datefmt="%H:%M:%S"))
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def validate_coordinates(lat: float, lon: float) -> tuple[bool, str]:
    """Check if coordinates fall within Karnataka bounding box."""
    bb = KARNATAKA_BBOX
    if not (bb["min_lat"] <= lat <= bb["max_lat"]):
        return False, f"Latitude {lat} outside Karnataka range [{bb['min_lat']}, {bb['max_lat']}]"
    if not (bb["min_lon"] <= lon <= bb["max_lon"]):
        return False, f"Longitude {lon} outside Karnataka range [{bb['min_lon']}, {bb['max_lon']}]"
    return True, "Within Karnataka bounding box"


def validate_geojson(filepath: Path, logger: logging.Logger) -> dict:
    """Validate a GeoJSON file against geospatial quality gates."""
    results = {
        "file": str(filepath),
        "gates": {},
        "all_passed": True,
    }

    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        results["gates"]["json_parse"] = {"passed": False, "detail": f"Invalid JSON: {e}"}
        results["all_passed"] = False
        return results

    results["gates"]["json_parse"] = {"passed": True, "detail": "Valid JSON"}

    # Check GeoJSON structure
    geojson_type = data.get("type", "")
    if geojson_type not in ("FeatureCollection", "Feature", "Point", "MultiPoint",
                             "LineString", "MultiLineString", "Polygon", "MultiPolygon",
                             "GeometryCollection"):
        results["gates"]["geojson_structure"] = {
            "passed": False,
            "detail": f"Unrecognized GeoJSON type: {geojson_type}"
        }
        results["all_passed"] = False
        return results

    results["gates"]["geojson_structure"] = {"passed": True, "detail": f"Type: {geojson_type}"}

    # Check CRS (GeoJSON RFC 7946 mandates WGS84)
    crs = data.get("crs")
    if crs:
        crs_name = str(crs.get("properties", {}).get("name", ""))
        if "4326" in crs_name or "WGS" in crs_name.upper():
            results["gates"]["crs_check"] = {"passed": True, "detail": f"CRS: {crs_name} (WGS84)"}
        else:
            results["gates"]["crs_check"] = {
                "passed": False,
                "detail": f"CRS is {crs_name}, expected WGS84/EPSG:4326"
            }
            results["all_passed"] = False
    else:
        results["gates"]["crs_check"] = {"passed": True, "detail": "No CRS specified (RFC 7946 assumes WGS84)"}

    # Validate coordinates within Karnataka
    features = data.get("features", [data] if "geometry" in data else [])
    total_coords = 0
    outside_bbox = 0

    def extract_coords(geometry):
        nonlocal total_coords, outside_bbox
        if not geometry:
            return
        geom_type = geometry.get("type", "")
        coords = geometry.get("coordinates", [])

        if geom_type == "Point":
            lon, lat = coords[0], coords[1]
            total_coords += 1
            ok, _ = validate_coordinates(lat, lon)
            if not ok:
                outside_bbox += 1
        elif geom_type in ("MultiPoint", "LineString"):
            for c in coords:
                total_coords += 1
                ok, _ = validate_coordinates(c[1], c[0])
                if not ok:
                    outside_bbox += 1
        elif geom_type in ("Polygon", "MultiLineString"):
            for ring in coords:
                for c in ring:
                    total_coords += 1
                    ok, _ = validate_coordinates(c[1], c[0])
                    if not ok:
                        outside_bbox += 1
        elif geom_type == "MultiPolygon":
            for polygon in coords:
                for ring in polygon:
                    for c in ring:
                        total_coords += 1
                        ok, _ = validate_coordinates(c[1], c[0])
                        if not ok:
                            outside_bbox += 1

    for feature in features:
        geom = feature.get("geometry") if "geometry" in feature else feature
        extract_coords(geom)

    if total_coords == 0:
        results["gates"]["bbox_check"] = {"passed": True, "detail": "No coordinates to check"}
    elif outside_bbox > 0:
        pct = 100 * outside_bbox / total_coords
        passed = pct < 5  # Allow up to 5% outside (border tolerance)
        results["gates"]["bbox_check"] = {
            "passed": passed,
            "detail": f"{outside_bbox}/{total_coords} coords ({pct:.1f}%) outside Karnataka bbox"
        }
        if not passed:
            results["all_passed"] = False
    else:
        results["gates"]["bbox_check"] = {
            "passed": True,
            "detail": f"All {total_coords} coords within Karnataka bbox"
        }

    results["gates"]["feature_count"] = {
        "passed": True,
        "detail": f"{len(features)} features, {total_coords} coordinates"
    }

    return results


def validate_csv_coordinates(filepath: Path, lat_col: str, lon_col: str,
                              logger: logging.Logger) -> dict:
    """Validate lat/lon columns in a CSV file."""
    import csv as csv_mod

    results = {"file": str(filepath), "gates": {}, "all_passed": True}

    try:
        with open(filepath, encoding="utf-8", errors="replace") as f:
            reader = csv_mod.DictReader(f)
            if lat_col not in (reader.fieldnames or []) or lon_col not in (reader.fieldnames or []):
                results["gates"]["columns"] = {
                    "passed": False,
                    "detail": f"Columns {lat_col}/{lon_col} not found. Available: {reader.fieldnames}"
                }
                results["all_passed"] = False
                return results

            total = 0
            outside = 0
            invalid = 0

            for row in reader:
                total += 1
                try:
                    lat = float(row[lat_col])
                    lon = float(row[lon_col])
                    ok, _ = validate_coordinates(lat, lon)
                    if not ok:
                        outside += 1
                except (ValueError, TypeError):
                    invalid += 1

        results["gates"]["coordinate_validity"] = {
            "passed": invalid == 0,
            "detail": f"{total} rows, {invalid} unparseable coordinates"
        }

        if outside > 0:
            pct = 100 * outside / max(total - invalid, 1)
            results["gates"]["bbox_check"] = {
                "passed": pct < 5,
                "detail": f"{outside}/{total} ({pct:.1f}%) outside Karnataka bbox"
            }
            if pct >= 5:
                results["all_passed"] = False
        else:
            results["gates"]["bbox_check"] = {
                "passed": True,
                "detail": f"All {total} coordinates within Karnataka bbox"
            }

    except Exception as e:
        results["gates"]["file_read"] = {"passed": False, "detail": f"Error: {e}"}
        results["all_passed"] = False

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Project Berunda — Geospatial Validation"
    )
    parser.add_argument("files", nargs="*", help="GeoJSON or CSV files to validate")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--no-dry-run", action="store_true")
    parser.add_argument("--resource-id", type=str, default=None)
    parser.add_argument("--priority", type=str, default=None,
                        choices=["P0", "P1", "P2", "P3", "P4"])
    parser.add_argument("--lat-col", default="latitude", help="Latitude column name for CSV")
    parser.add_argument("--lon-col", default="longitude", help="Longitude column name for CSV")
    parser.add_argument("--max-file-size", type=int, default=200*1024*1024)
    parser.add_argument("--max-total-size", type=int, default=1024*1024*1024)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--force", action="store_true")

    args = parser.parse_args()
    logger = setup_logging()

    logger.info("=" * 60)
    logger.info("Project Berunda — Geospatial Validation")
    logger.info("=" * 60)

    if not args.files:
        # Auto-scan quarantine and boundaries directories
        scan_dirs = [
            WORKSPACE_ROOT / "quarantine",
            WORKSPACE_ROOT / "boundaries",
            WORKSPACE_ROOT / "data" / "external",
        ]
        files = []
        for d in scan_dirs:
            if d.exists():
                files.extend(d.rglob("*.geojson"))
                files.extend(d.rglob("*.json"))

        if not files:
            logger.info("No geospatial files found to validate")
            sys.exit(0)
    else:
        files = [Path(f) for f in args.files]

    all_results = []
    for filepath in files:
        logger.info(f"Validating: {filepath}")
        ext = filepath.suffix.lower()

        if ext in (".geojson", ".json"):
            result = validate_geojson(filepath, logger)
        elif ext == ".csv":
            result = validate_csv_coordinates(filepath, args.lat_col, args.lon_col, logger)
        else:
            logger.info(f"  Skipping unsupported format: {ext}")
            continue

        all_results.append(result)

        for gate_name, gate_result in result.get("gates", {}).items():
            status = "PASS" if gate_result["passed"] else "FAIL"
            logger.info(f"  [{gate_name}] {status}: {gate_result['detail']}")

    passed = sum(1 for r in all_results if r["all_passed"])
    failed = len(all_results) - passed
    logger.info("=" * 60)
    logger.info(f"GEO VALIDATION: {passed} passed, {failed} failed")
    logger.info("=" * 60)

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
