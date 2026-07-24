"""Verify all Python package imports work correctly."""

from __future__ import annotations


class TestPackageImports:
    """Every module should import without error."""

    def test_shared_config_imports(self):
        from src.shared.config import _deep_merge, load_config

        assert callable(load_config)
        assert callable(_deep_merge)

    def test_shared_logging_imports(self):
        from src.shared.logging import StructuredFormatter, get_logger

        assert callable(get_logger)
        assert StructuredFormatter is not None

    def test_shared_validators_imports(self):
        from src.shared.validators import __name__ as name

        assert name == "src.shared.validators"

    def test_shared_utils_imports(self):
        from src.shared.utils import __name__ as name

        assert name == "src.shared.utils"

    def test_main_app_imports(self):
        from src.main import app

        assert app.title == "Berunda API"
        assert app.version == "0.4.0"

    def test_ai_module_imports(self):
        from src.ai import __name__ as name

        assert name == "src.ai"

    def test_ml_module_imports(self):
        from src.ml import __name__ as name

        assert name == "src.ml"

    def test_pipelines_module_imports(self):
        from src.pipelines import __name__ as name

        assert name == "src.pipelines"
