"""Configuration management — YAML/env-based settings loader with environment-aware overrides."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any


def load_config(config_dir: str | Path | None = None) -> dict[str, Any]:
    """Load configuration from YAML files with environment-aware overrides.

    Reads config/base.yaml as the base, then merges with the environment-
    specific file (config/{env}.yaml). Environment is determined by the
    APP_ENV environment variable (default: 'development').
    """
    import yaml

    if config_dir is None:
        config_dir = Path(__file__).parent.parent.parent.parent / "config"
    config_dir = Path(config_dir)

    if not config_dir.exists():
        return {"logging": {"level": "INFO"}}

    env = os.environ.get("APP_ENV", "development")

    base_path = config_dir / "base.yaml"
    env_path = config_dir / f"{env}.yaml"

    config: dict[str, Any] = {}

    if base_path.exists():
        with open(base_path) as f:
            config = yaml.safe_load(f) or {}

    if env_path.exists():
        with open(env_path) as f:
            env_config = yaml.safe_load(f) or {}
        _deep_merge(config, env_config)

    overlay = {
        "app": {"environment": env},
        "server": {
            "host": os.environ.get("HOST", config.get("server", {}).get("host", "0.0.0.0")),
            "port": int(os.environ.get("PORT", config.get("server", {}).get("port", 8000))),
        },
    }
    _deep_merge(config, overlay)

    return config


def _deep_merge(base: dict, override: dict) -> None:
    """Recursively merge override dict into base dict."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
