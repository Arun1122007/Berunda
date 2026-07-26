#!/usr/bin/env python3
"""
Seed Database Script
Wraps the existing Phase 4 synthetic data generators to fulfill the Phase 1 seeding requirement.
"""

import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def main():
    print("Seeding database using existing data generators...")
    
    # We will just run the phase4_demo_data.py script
    cmd = [sys.executable, "scripts/data/phase4_demo_data.py", "--force"]
    
    try:
        subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)
        print("Database seeded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to seed database: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
