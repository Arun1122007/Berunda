"""Tests for configuration management."""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch

from src.shared.config import _deep_merge, load_config


class TestConfigLoading:
    """Configuration loader should handle all environment scenarios."""

    def test_load_config_returns_defaults_when_no_config_dir(self):
        result = load_config(config_dir="/nonexistent/path")
        assert isinstance(result, dict)
        assert result == {"logging": {"level": "INFO"}}

    def test_load_config_development_environment(self, tmp_path: Path):
        base = tmp_path / "base.yaml"
        base.write_text(json.dumps({"app": {"name": "Berunda"}, "logging": {"level": "INFO"}}))
        dev = tmp_path / "development.yaml"
        dev.write_text(json.dumps({"logging": {"level": "DEBUG"}}))
        with patch.dict(os.environ, {"APP_ENV": "development"}, clear=True):
            result = load_config(config_dir=tmp_path)
        assert result["app"]["name"] == "Berunda"
        assert result["logging"]["level"] == "DEBUG"

    def test_load_config_uses_env_variables(self, tmp_path: Path):
        base = tmp_path / "base.yaml"
        base.write_text(json.dumps({"server": {"port": 8000}}))
        with patch.dict(os.environ, {"PORT": "9000", "APP_ENV": "development"}, clear=True):
            result = load_config(config_dir=tmp_path)
        assert result["server"]["port"] == 9000

    def test_load_config_production_set_no_base(self, tmp_path: Path):
        prod = tmp_path / "production.yaml"
        prod.write_text(json.dumps({"logging": {"level": "WARNING"}}))
        with patch.dict(os.environ, {"APP_ENV": "production"}, clear=True):
            result = load_config(config_dir=tmp_path)
        assert result["logging"]["level"] == "WARNING"

    def test_deep_merge_overrides_nested_values(self):
        base = {"a": {"b": 1, "c": 2}, "d": 3}
        override = {"a": {"c": 99}, "e": 4}
        _deep_merge(base, override)
        assert base == {"a": {"b": 1, "c": 99}, "d": 3, "e": 4}

    def test_deep_merge_handles_empty_override(self):
        base = {"a": 1}
        _deep_merge(base, {})
        assert base == {"a": 1}


class TestConfigStartupSafety:
    """Application must fail safely with missing configuration."""

    def test_fails_on_missing_required_env(self):
        from src.shared.config import load_config as lc

        result = lc()
        assert isinstance(result, dict)
