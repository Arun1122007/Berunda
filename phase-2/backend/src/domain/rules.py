from __future__ import annotations

import re
from typing import Optional


class CrimeNumberRule:
    CRIME_NO_PATTERN = re.compile(r"^\d{2,4}/\d{4,6}$")

    @staticmethod
    def validate(crime_no: str) -> Optional[str]:
        if not crime_no or not crime_no.strip():
            return "Crime number must not be empty"
        if not CrimeNumberRule.CRIME_NO_PATTERN.match(crime_no.strip()):
            return "Crime number must match pattern YY/XXXXX (e.g. 24/001234)"
        return None

    @staticmethod
    def is_unique(sequence: list[str], crime_no: str) -> bool:
        return crime_no not in sequence


class DistrictScopeRule:
    @staticmethod
    def can_access(district_id: str, user_district_id: Optional[str], user_role: str) -> bool:
        if user_role == "admin":
            return True
        if user_role == "analyst" and user_district_id is not None:
            return True
        if user_role == "officer":
            return user_district_id == district_id
        return False

    @staticmethod
    def filter_query(allowed_district_ids: list[str]) -> dict:
        return {"district_id_in": allowed_district_ids}


class RoleHierarchyRule:
    ROLE_LEVELS = {"viewer": 0, "officer": 10, "analyst": 20, "admin": 100}

    @staticmethod
    def has_role(user_role: str, minimum_role: str) -> bool:
        user_level = RoleHierarchyRule.ROLE_LEVELS.get(user_role, -1)
        required_level = RoleHierarchyRule.ROLE_LEVELS.get(minimum_role, -1)
        return user_level >= required_level

    @staticmethod
    def can_assign_role(assigner_role: str, target_role: str) -> bool:
        assigner_level = RoleHierarchyRule.ROLE_LEVELS.get(assigner_role, -1)
        target_level = RoleHierarchyRule.ROLE_LEVELS.get(target_role, -1)
        return assigner_level > target_level

    @staticmethod
    def is_admin(user_role: str) -> bool:
        return user_role == "admin"


class GravityOffenceRule:
    GRAVITY_LEVELS = {"minor": 1, "moderate": 2, "serious": 3, "heinous": 4}

    GRAVITY_DESCRIPTIONS = {
        "minor": "Offences punishable with imprisonment up to 1 year",
        "moderate": "Offences punishable with imprisonment between 1-3 years",
        "serious": "Offences punishable with imprisonment between 3-7 years",
        "heinous": "Offences punishable with imprisonment of 7 years or more",
    }

    @staticmethod
    def validate(gravity_id: str) -> Optional[str]:
        if gravity_id not in GravityOffenceRule.GRAVITY_LEVELS:
            valid = ", ".join(GravityOffenceRule.GRAVITY_LEVELS.keys())
            return f"Invalid gravity offence '{gravity_id}'. Must be one of: {valid}"
        return None

    @staticmethod
    def requires_supervisory_approval(gravity_id: str) -> bool:
        level = GravityOffenceRule.GRAVITY_LEVELS.get(gravity_id, 0)
        return level >= GravityOffenceRule.GRAVITY_LEVELS["serious"]

    @staticmethod
    def is_high_risk(gravity_id: str) -> bool:
        level = GravityOffenceRule.GRAVITY_LEVELS.get(gravity_id, 0)
        return level >= GravityOffenceRule.GRAVITY_LEVELS["heinous"]
