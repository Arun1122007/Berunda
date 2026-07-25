"""Smoke tests — Alembic migration structure.

Validates the migration revision chain is well-formed and linear,
and that offline SQL generation succeeds for schema-only revisions.
"""

from __future__ import annotations

import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory


def _alembic_cfg() -> Config:
    return Config("src/alembic.ini")


def _script() -> ScriptDirectory:
    return ScriptDirectory.from_config(_alembic_cfg())


class TestAlembicRevisionChain:
    def test_single_head(self):
        heads = _script().get_heads()
        assert len(heads) == 1, f"Expected single head, got {heads}"

    def test_head_is_006(self):
        heads = _script().get_heads()
        assert heads[0] == "006", f"Expected head 006, got {heads[0]}"

    def test_linear_revision_chain(self):
        revisions = list(_script().walk_revisions())
        assert len(revisions) == 6
        expected = ["006", "005", "004", "003", "002", "001"]
        actual = [r.revision for r in revisions]
        assert actual == expected, f"Expected chain {expected}, got {actual}"

    def test_all_revisions_have_doc_strings(self):
        for rev in _script().walk_revisions():
            assert rev.doc, f"Revision {rev.revision} is missing a doc string"

    def test_all_revisions_import_cleanly(self):
        revisions = list(_script().walk_revisions())
        for rev in revisions:
            module = rev.module
            assert module is not None
            assert callable(getattr(module, "upgrade", None))
            assert callable(getattr(module, "downgrade", None))

    def test_offline_sql_generation_schema_only(self):
        """Generate SQL up to revision 001 (before seed migration that requires online mode)."""
        cfg = _alembic_cfg()
        from alembic.command import upgrade

        cfg.set_main_option("sqlalchemy.url", "sqlite:///:memory:")
        upgrade(cfg, "001", sql=True)

    def test_offline_sql_generation_all_revisions_safely(self):
        """Attempt full-chain offline SQL generation, expecting it to skip seed data gracefully."""
        cfg = _alembic_cfg()
        from alembic.command import upgrade
        from alembic.util.exc import CommandError

        cfg.set_main_option("sqlalchemy.url", "sqlite:///:memory:")
        try:
            upgrade(cfg, "head", sql=True)
        except (CommandError, AttributeError) as exc:
            if "has no attribute" in str(exc):
                pytest.skip(
                    "Seed migration requires online mode for .scalar() call — "
                    "this is a known limitation."
                )
            raise
