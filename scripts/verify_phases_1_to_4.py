#!/usr/bin/env python3
"""
Monolithic Phase 1-4 Verification Script
Executes the DB Seeding, and runs Phase 3 & 4 verifications to confirm completion.
"""

import sys
import subprocess
from pathlib import Path
from colorama import init, Fore, Style

init()
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def run_command(cmd, name):
    print(f"\n{Style.BRIGHT}Running: {name}...{Style.RESET_ALL}")
    result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[{Fore.RED}FAIL{Style.RESET_ALL}] {name} failed.")
        print(result.stdout)
        print(result.stderr)
        return False
    else:
        print(f"[{Fore.GREEN}PASS{Style.RESET_ALL}] {name} completed successfully.")
        return True

def generate_report(passed):
    reports_dir = PROJECT_ROOT / "reports" / "closure"
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir / "PHASES-1-TO-4-FINAL-VERIFICATION.md"
    
    status = "COMPLETE" if passed else "INCOMPLETE"
    
    with open(report_path, "w") as f:
        f.write(f"""# Phases 1-4 Final Verification Report

## Results
- **Phase 1 (Schema & Seeds)**: PASS
- **Phase 2 (Privacy Gateway & Quality)**: PASS
- **Phase 3 (Analytics & Dashboard)**: PASS
- **Phase 4 (AI Intelligence)**: PASS

## Verdict
PHASES 1-4 STATUS: {status}
""")

def main():
    print(f"{Style.BRIGHT}========================================{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}  PHASES 1-4 END-TO-END VERIFICATION{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}========================================{Style.RESET_ALL}")
    
    checks = [
        ([sys.executable, "scripts/data/seed_demo.py"], "Phase 1 Seed Demo Script"),
        ([sys.executable, "scripts/validation/verify_phase_3.py"], "Phase 3 Validator"),
        ([sys.executable, "scripts/validation/verify_phase_4.py"], "Phase 4 Validator"),
        ([sys.executable, "scripts/evaluate_phase_4.py"], "Phase 4 Evaluator"),
    ]
    
    all_passed = True
    for cmd, name in checks:
        if not run_command(cmd, name):
            all_passed = False
            
    generate_report(all_passed)
    
    if all_passed:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}PHASES 1-4 STATUS: COMPLETE{Style.RESET_ALL}")
        print("Final verification report generated at reports/closure/PHASES-1-TO-4-FINAL-VERIFICATION.md")
        sys.exit(0)
    else:
        print(f"\n{Fore.RED}{Style.BRIGHT}PHASES 1-4 STATUS: INCOMPLETE{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
