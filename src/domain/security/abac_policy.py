"""Attribute-Based Access Control (ABAC) Engine for Phase 3 Enterprise Scale.

Evaluates multi-dimensional security policies combining investigator clearance level,
assigned district boundaries, time of access, and case sensitivity flags.
"""
from __future__ import annotations

import logging
from datetime import datetime, time
from typing import Any, Dict, List, Optional

logger = logging.getLogger("berunda.abac")

# Clearance hierarchy: 1=PUBLIC, 2=RESTRICTED, 3=CONFIDENTIAL, 4=SECRET, 5=TOP_SECRET
CLEARANCE_LEVELS: Dict[str, int] = {
    "PUBLIC": 1,
    "RESTRICTED": 2,
    "CONFIDENTIAL": 3,
    "SECRET": 4,
    "TOP_SECRET": 5,
}

ROLE_DEFAULT_CLEARANCE: Dict[str, int] = {
    "public": 1,
    "officer": 3,
    "analyst": 4,
    "admin": 5,
}


class ABACPolicyEngine:
    """Evaluates attribute-based access control policies."""

    @staticmethod
    def evaluate_access(
        user: Dict[str, Any],
        resource: Dict[str, Any],
        action: str,
        env_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Evaluate access request and return authorization decision with audit rationale."""
        env = env_context or {}
        user_role = str(user.get("role", "public")).lower()
        user_clearance = user.get("clearance_level") or ROLE_DEFAULT_CLEARANCE.get(user_role, 1)
        if isinstance(user_clearance, str):
            user_clearance = CLEARANCE_LEVELS.get(user_clearance.upper(), 1)

        res_sensitivity = resource.get("sensitivity_level", "CONFIDENTIAL")
        res_clearance_req = CLEARANCE_LEVELS.get(str(res_sensitivity).upper(), 3)

        # 1. Check clearance level hierarchy
        if user_clearance < res_clearance_req:
            reason = f"User clearance ({user_clearance}) below required sensitivity ({res_clearance_req})."
            logger.warning(f"[ABAC DENY] Action: {action} — {reason}")
            return {"allowed": False, "reason": reason, "policy": "CLEARANCE_HIERARCHY"}

        # 2. Check geographical / district boundary (Admin and SCRB analysts can access statewide)
        user_district = str(user.get("district_id", "")).strip()
        res_district = str(resource.get("district_id", "")).strip()
        if user_role not in ["admin", "analyst"] and user_district and res_district:
            if user_district != res_district and user_district != "STATE_HQ":
                reason = f"Officer jurisdiction ({user_district}) does not match resource district ({res_district})."
                logger.warning(f"[ABAC DENY] Action: {action} — {reason}")
                return {"allowed": False, "reason": reason, "policy": "DISTRICT_BOUNDARY"}

        # 3. Check temporal restrictions (e.g. high sensitivity exports only allowed during shift hours 06:00 to 22:00)
        if action in ["export:report", "bulk:download"] and res_clearance_req >= 4:
            now_time = datetime.now().time()
            start_shift, end_shift = time(6, 0), time(22, 0)
            if not (start_shift <= now_time <= end_shift) and user_role != "admin":
                reason = "High sensitivity data exports restricted to operational shift hours (06:00 - 22:00 IST)."
                logger.warning(f"[ABAC DENY] Action: {action} — {reason}")
                return {"allowed": False, "reason": reason, "policy": "TEMPORAL_RESTRICTION"}

        logger.info(f"[ABAC ALLOW] Action: {action} authorized for User #{user.get('user_id', 'unknown')}")
        return {"allowed": True, "reason": "All ABAC policy attributes satisfied.", "policy": "ALLOW"}
