#!/usr/bin/env python3
"""
Phase 4 Verification Script
Validates the AI/NLP Intelligence Layer architecture, prompt registries, and privacy features.
"""

import sys
from pathlib import Path
from colorama import init, Fore, Style
import re

init()
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def check_file_exists(relative_path: str) -> bool:
    path = PROJECT_ROOT / relative_path
    exists = path.exists()
    status = f"{Fore.GREEN}PASS{Style.RESET_ALL}" if exists else f"{Fore.RED}FAIL{Style.RESET_ALL}"
    print(f"[{status}] File {relative_path}")
    return exists

def main():
    print(f"\n{Style.BRIGHT}--- Phase 4 AI/NLP Intelligence Verification ---{Style.RESET_ALL}")
    
    files_to_check = [
        "config/ai/prompts.yaml",
        "config/ai/models.yaml",
        "src/routers/ai_intelligence_router.py",
        "src/services/ai_provider.py",
        "src/services/privacy_gateway.py",
        "src/services/ai_task_service.py"
    ]
    
    all_passed = True
    for f in files_to_check:
        if not check_file_exists(f):
            all_passed = False
            
    print(f"\n{Style.BRIGHT}--- Privacy Gateway Logic Check ---{Style.RESET_ALL}")
    try:
        from src.services.privacy_gateway import PrivacyGateway
        
        test_string = "My email is test@police.gov.in and my number is 9876543210."
        masked, token_map = PrivacyGateway.apply_privacy_mask(test_string)
        
        if "[EMAIL_0]" in masked and "[PHONE_0]" in masked and "test@police.gov.in" in token_map.values():
            print(f"[{Fore.GREEN}PASS{Style.RESET_ALL}] PII tokenization works correctly.")
        else:
            print(f"[{Fore.RED}FAIL{Style.RESET_ALL}] Tokenization logic failed.")
            all_passed = False
            
        restored = PrivacyGateway.restore_privacy_mask(masked, token_map)
        if restored == test_string:
            print(f"[{Fore.GREEN}PASS{Style.RESET_ALL}] PII restoration works correctly.")
        else:
            print(f"[{Fore.RED}FAIL{Style.RESET_ALL}] Restoration logic failed.")
            all_passed = False
            
    except Exception as e:
        print(f"[{Fore.RED}FAIL{Style.RESET_ALL}] Failed to test Privacy Gateway: {e}")
        all_passed = False

    print(f"\n{Style.BRIGHT}--- Endpoints Registration Check ---{Style.RESET_ALL}")
    with open(PROJECT_ROOT / "src/main.py", "r") as f:
        content = f.read()
        has_routes = "app.include_router(ai_intelligence_router.router)" in content
        status = f"{Fore.GREEN}PASS{Style.RESET_ALL}" if has_routes else f"{Fore.RED}FAIL{Style.RESET_ALL}"
        print(f"[{status}] AI routers registered in main.py")
        if not has_routes:
            all_passed = False

    if all_passed:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}PHASE 4 STATUS: COMPLETE{Style.RESET_ALL}")
        sys.exit(0)
    else:
        print(f"\n{Fore.RED}{Style.BRIGHT}PHASE 4 STATUS: INCOMPLETE{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
