import sys
from pathlib import Path

_root = str(Path(__file__).parent.parent)
if _root not in sys.path: sys.path.insert(0, _root)

from src.domain.rules import (
    CrimeNumberRule,
    DistrictScopeRule,
    GravityOffenceRule,
    RoleHierarchyRule,
)


class TestCrimeNumberRule:
    def test_valid_crime_number(self):
        assert CrimeNumberRule.validate("24/001234") is None

    def test_valid_crime_number_short_year(self):
        assert CrimeNumberRule.validate("24/1234") is None

    def test_empty_string_returns_error(self):
        error = CrimeNumberRule.validate("")
        assert error is not None
        assert "empty" in error.lower()

    def test_whitespace_only_returns_error(self):
        error = CrimeNumberRule.validate("   ")
        assert error is not None

    def test_none_returns_error(self):
        error = CrimeNumberRule.validate(None)
        assert error is not None

    def test_invalid_format_no_slash(self):
        error = CrimeNumberRule.validate("24123456")
        assert error is not None

    def test_invalid_format_letters(self):
        error = CrimeNumberRule.validate("ab/123456")
        assert error is not None

    def test_uniqueness_true(self):
        assert CrimeNumberRule.is_unique(["24/001", "24/002"], "24/003") is True

    def test_uniqueness_false(self):
        assert CrimeNumberRule.is_unique(["24/001", "24/002"], "24/001") is False


class TestDistrictScopeRule:
    def test_admin_can_access_any(self):
        assert DistrictScopeRule.can_access("D001", None, "admin") is True
        assert DistrictScopeRule.can_access("D002", "D001", "admin") is True

    def test_analyst_can_access_any(self):
        assert DistrictScopeRule.can_access("D001", "D002", "analyst") is True

    def test_officer_can_access_own(self):
        assert DistrictScopeRule.can_access("D001", "D001", "officer") is True

    def test_officer_cannot_access_other(self):
        assert DistrictScopeRule.can_access("D002", "D001", "officer") is False

    def test_officer_no_district_false(self):
        assert DistrictScopeRule.can_access("D001", None, "officer") is False

    def test_unknown_role_cannot_access(self):
        assert DistrictScopeRule.can_access("D001", "D001", "viewer") is False

    def test_filter_query_returns_dict(self):
        result = DistrictScopeRule.filter_query(["D001", "D002"])
        assert result == {"district_id_in": ["D001", "D002"]}


class TestRoleHierarchyRule:
    def test_admin_has_admin_role(self):
        assert RoleHierarchyRule.has_role("admin", "admin") is True

    def test_admin_has_analyst_role(self):
        assert RoleHierarchyRule.has_role("admin", "analyst") is True

    def test_analyst_does_not_have_admin(self):
        assert RoleHierarchyRule.has_role("analyst", "admin") is False

    def test_officer_has_officer_role(self):
        assert RoleHierarchyRule.has_role("officer", "officer") is True

    def test_viewer_does_not_have_officer(self):
        assert RoleHierarchyRule.has_role("viewer", "officer") is False

    def test_can_assign_admin_can_assign_analyst(self):
        assert RoleHierarchyRule.can_assign_role("admin", "analyst") is True

    def test_cannot_assign_same_role(self):
        assert RoleHierarchyRule.can_assign_role("admin", "admin") is False

    def test_cannot_assign_higher_role(self):
        assert RoleHierarchyRule.can_assign_role("officer", "admin") is False

    def test_is_admin_returns_true(self):
        assert RoleHierarchyRule.is_admin("admin") is True

    def test_is_admin_returns_false(self):
        assert RoleHierarchyRule.is_admin("officer") is False


class TestGravityOffenceRule:
    def test_valid_gravity_ids(self):
        for g in ["minor", "moderate", "serious", "heinous"]:
            assert GravityOffenceRule.validate(g) is None

    def test_invalid_gravity_id(self):
        error = GravityOffenceRule.validate("critical")
        assert error is not None

    def test_serious_requires_approval(self):
        assert GravityOffenceRule.requires_supervisory_approval("serious") is True

    def test_heinous_requires_approval(self):
        assert GravityOffenceRule.requires_supervisory_approval("heinous") is True

    def test_minor_no_approval(self):
        assert GravityOffenceRule.requires_supervisory_approval("minor") is False

    def test_moderate_no_approval(self):
        assert GravityOffenceRule.requires_supervisory_approval("moderate") is False

    def test_heinous_is_high_risk(self):
        assert GravityOffenceRule.is_high_risk("heinous") is True

    def test_serious_is_not_high_risk(self):
        assert GravityOffenceRule.is_high_risk("serious") is False

    def test_minor_is_not_high_risk(self):
        assert GravityOffenceRule.is_high_risk("minor") is False
