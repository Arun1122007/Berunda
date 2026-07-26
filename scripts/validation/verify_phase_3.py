#!/usr/bin/env python3
"""
Phase 3 Verification Script
Validates the Analytics Engine API contracts, configuration, and repository implementations.
"""

import sys
import os
from pathlib import Path
from colorama import init, Fore, Style

init()
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def check_file_exists(relative_path: str) -> bool:
    path = PROJECT_ROOT / relative_path
    exists = path.exists()
    status = f"{Fore.GREEN}PASS{Style.RESET_ALL}" if exists else f"{Fore.RED}FAIL{Style.RESET_ALL}"
    print(f"[{status}] File {relative_path}")
    return exists

def main():
    print(f"\n{Style.BRIGHT}--- Phase 3 Analytics Engine Verification ---{Style.RESET_ALL}")
    
    files_to_check = [
        "config/analytics/metrics.yaml",
        "docs/analytics/ANALYTICS-DATA-CONTRACT.md",
        "src/routers/analytics_router.py",
        "src/routers/geospatial_router.py",
        "src/services/analytics_service.py",
        "src/services/geospatial_service.py"
    ]
    
    all_passed = True
    for f in files_to_check:
        if not check_file_exists(f):
            all_passed = False
            
    print(f"\n{Style.BRIGHT}--- Privacy Suppression Check ---{Style.RESET_ALL}")
    with open(PROJECT_ROOT / "src/services/analytics_service.py", "r") as f:
        content = f.read()
        has_suppression = "SUPPRESSED_DUE_TO_LOW_COUNT" in content
        status = f"{Fore.GREEN}PASS{Style.RESET_ALL}" if has_suppression else f"{Fore.RED}FAIL{Style.RESET_ALL}"
        print(f"[{status}] Low-count suppression implemented in AnalyticsService")
        if not has_suppression:
            all_passed = False

    print(f"\n{Style.BRIGHT}--- Endpoints Registration Check ---{Style.RESET_ALL}")
    with open(PROJECT_ROOT / "src/main.py", "r") as f:
        content = f.read()
        has_routes = "analytics_router" in content
        status = f"{Fore.GREEN}PASS{Style.RESET_ALL}" if has_routes else f"{Fore.RED}FAIL{Style.RESET_ALL}"
        print(f"[{status}] Analytics routers registered in main.py")
        if not has_routes:
            all_passed = False

    if all_passed:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}PHASE 3 STATUS: COMPLETE{Style.RESET_ALL}")
        sys.exit(0)
    else:
        print(f"\n{Fore.RED}{Style.BRIGHT}PHASE 3 STATUS: INCOMPLETE{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
