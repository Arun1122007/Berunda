"""Tests for ml.registry module."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from src.ml.registry import (
    ArtifactStore,
    DeploymentTracker,
    ModelRegistry,
    ModelVersion,
    _increment_version,
    _parse_semver,
)


class TestSemver:
    def test_parse_valid(self):
        assert _parse_semver("1.2.3") == (1, 2, 3)

    def test_parse_invalid_raises(self):
        with pytest.raises(ValueError):
            _parse_semver("abc")

    def test_increment_patch(self):
        assert _increment_version("1.2.3", "patch") == "1.2.4"

    def test_increment_minor(self):
        assert _increment_version("1.2.3", "minor") == "1.3.0"

    def test_increment_major(self):
        assert _increment_version("1.2.3", "major") == "2.0.0"


class TestModelVersion:
    def test_to_dict(self):
        mv = ModelVersion(name="test", version="1.0.0", model_type="rf")
        d = mv.to_dict()
        assert d["name"] == "test"
        assert d["version"] == "1.0.0"
        assert "version_hash" in d

    def test_from_dict(self):
        original = ModelVersion(name="m1", version="2.0.0", model_type="lr", stage="production")
        data = original.to_dict()
        restored = ModelVersion.from_dict(data)
        assert restored.name == "m1"
        assert restored.stage == "production"

    def test_hash_uniqueness(self):
        v1 = ModelVersion(name="a", version="1.0.0", model_type="rf")
        v2 = ModelVersion(name="b", version="1.0.0", model_type="rf")
        assert v1.version_hash != v2.version_hash


class TestArtifactStore:
    def test_save_and_load(self, tmp_path: Path):
        store = ArtifactStore(str(tmp_path / "models"))
        model = {"a": 1, "b": 2}
        path = store.save(model, "test_model", "1.0.0")
        loaded = store.load("test_model", "1.0.0")
        assert loaded == model
        assert Path(path).exists()

    def test_list_versions(self, tmp_path: Path):
        store = ArtifactStore(str(tmp_path / "models"))
        store.save({"x": 1}, "m", "1.0.0")
        store.save({"y": 2}, "m", "2.0.0")
        versions = store.list_versions("m")
        assert "1.0.0" in versions
        assert "2.0.0" in versions

    def test_load_missing_raises(self, tmp_path: Path):
        store = ArtifactStore(str(tmp_path / "models"))
        with pytest.raises(FileNotFoundError):
            store.load("nonexistent", "1.0.0")


class TestDeploymentTracker:
    def test_deploy_and_get(self, tmp_path: Path):
        tracker = DeploymentTracker(str(tmp_path / "deployments.json"))
        tracker.deploy("m1", "1.0.0", "production")
        dep = tracker.get_deployment("production")
        assert dep is not None
        assert dep["model_name"] == "m1"

    def test_list_deployments(self, tmp_path: Path):
        tracker = DeploymentTracker(str(tmp_path / "deployments.json"))
        tracker.deploy("m1", "1.0.0", "staging")
        assert "staging" in tracker.list_deployments()


class TestModelRegistry:
    def test_register_and_list(self, tmp_path: Path):
        registry = ModelRegistry(str(tmp_path / "registry"), backend="local")
        registry.register("test_model", model={"pkl": "dummy"}, metrics={"acc": 0.9}, params={"lr": 0.01})
        models = registry.list_models()
        names = [m["name"] for m in models]
        assert "test_model" in names

    def test_register_without_model(self, tmp_path: Path):
        registry = ModelRegistry(str(tmp_path / "registry"))
        version = registry.register("meta_only", metrics={"acc": 0.8})
        assert version == "1.0.0"

    def test_load_registered_model(self, tmp_path: Path):
        registry = ModelRegistry(str(tmp_path / "registry"))
        import joblib
        from sklearn.dummy import DummyClassifier
        dummy = DummyClassifier(strategy="most_frequent")
        registry.register("dummy", model=dummy)
        loaded, metadata = registry.load("dummy")
        assert loaded is not None

    def test_get_latest_version(self, tmp_path: Path):
        registry = ModelRegistry(str(tmp_path / "registry"))
        registry.register("m", metrics={"a": 1})
        registry.register("m", metrics={"a": 2})
        assert registry.get_latest_version("m") == "1.0.1"

    def test_promote_to_production(self, tmp_path: Path):
        registry = ModelRegistry(str(tmp_path / "registry"))
        registry.register("m", metrics={"a": 1})
        registry.promote_to_production("m", "1.0.0")
        details = registry.get_version_details("m", "1.0.0")
        assert details["stage"] == "production"

    def test_get_version_details(self, tmp_path: Path):
        registry = ModelRegistry(str(tmp_path / "registry"))
        registry.register("m", metrics={"f1": 0.95})
        details = registry.get_version_details("m", "1.0.0")
        assert details["metrics"]["f1"] == 0.95

    def test_list_models_empty(self, tmp_path: Path):
        registry = ModelRegistry(str(tmp_path / "empty"))
        assert registry.list_models() == []

    def test_get_latest_version_missing_raises(self, tmp_path: Path):
        registry = ModelRegistry(str(tmp_path / "registry"))
        with pytest.raises(ValueError):
            registry.get_latest_version("nonexistent")
