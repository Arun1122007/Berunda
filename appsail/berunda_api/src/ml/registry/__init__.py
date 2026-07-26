from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from src.shared.logging import get_logger

logger = get_logger(__name__)

_SEMVER_PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def _parse_semver(version: str) -> tuple[int, int, int]:
    match = _SEMVER_PATTERN.match(version)
    if not match:
        raise ValueError(f"Invalid semantic version: {version}. Use 'major.minor.patch'")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def _increment_version(version: str, bump: str = "patch") -> str:
    major, minor, patch = _parse_semver(version)
    if bump == "major":
        return f"{major + 1}.0.0"
    elif bump == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


class ModelVersion:
    """Tracks a single model version with metadata."""

    def __init__(
        self,
        name: str,
        version: str,
        model_type: str,
        metrics: dict | None = None,
        artifact_path: str | None = None,
        params: dict | None = None,
        stage: str = "staging",
    ):
        self.name = name
        self.version = version
        self.model_type = model_type
        self.metrics = metrics or {}
        self.artifact_path = artifact_path
        self.params = params or {}
        self.stage = stage
        self.created_at = datetime.utcnow().isoformat()
        self.version_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        raw = f"{self.name}:{self.version}:{self.created_at}"
        return hashlib.sha256(raw.encode()).hexdigest()[:12]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "model_type": self.model_type,
            "metrics": self.metrics,
            "artifact_path": self.artifact_path,
            "params": self.params,
            "stage": self.stage,
            "created_at": self.created_at,
            "version_hash": self.version_hash,
        }

    @classmethod
    def from_dict(cls, data: dict) -> ModelVersion:
        obj = cls(
            name=data["name"],
            version=data["version"],
            model_type=data.get("model_type", ""),
            metrics=data.get("metrics", {}),
            artifact_path=data.get("artifact_path"),
            params=data.get("params", {}),
            stage=data.get("stage", "staging"),
        )
        obj.created_at = data.get("created_at", obj.created_at)
        obj.version_hash = data.get("version_hash", obj.version_hash)
        return obj


class ArtifactStore:
    """Store and retrieve model artifacts on local filesystem."""

    def __init__(self, base_path: str | Path = "models/"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, model: Any, name: str, version: str) -> str:
        import joblib
        path = self.base_path / name / version
        path.mkdir(parents=True, exist_ok=True)
        artifact_path = path / "model.pkl"
        joblib.dump(model, artifact_path)
            logger.info("Artifact saved", extra={"model_name": name, "model_version": version, "model_path": str(artifact_path)})
        return str(artifact_path)

    def load(self, name: str, version: str) -> Any:
        import joblib
        path = self.base_path / name / version / "model.pkl"
        if not path.exists():
            raise FileNotFoundError(f"Model artifact not found: {path}")
        return joblib.load(path)

    def list_versions(self, name: str) -> list[str]:
        model_dir = self.base_path / name
        if not model_dir.exists():
            return []
        return sorted([d.name for d in model_dir.iterdir() if d.is_dir()])

    def delete(self, name: str, version: str) -> bool:
        import shutil
        path = self.base_path / name / version
        if path.exists():
            shutil.rmtree(path)
            logger.info("Artifact deleted", extra={"name": name, "version": version})
            return True
        return False


class DeploymentTracker:
    """Track which model versions are deployed to which environments."""

    def __init__(self, state_path: str | Path = "models/deployments.json"):
        self.state_path = Path(state_path)
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self._deployments: dict[str, dict] = self._load()

    def _load(self) -> dict:
        if self.state_path.exists():
            return json.loads(self.state_path.read_text())
        return {}

    def _save(self) -> None:
        self.state_path.write_text(json.dumps(self._deployments, indent=2))

    def deploy(self, name: str, version: str, environment: str) -> None:
        self._deployments[environment] = {
            "model_name": name,
            "model_version": version,
            "deployed_at": datetime.utcnow().isoformat(),
        }
        self._save()

    def get_deployment(self, environment: str) -> dict | None:
        return self._deployments.get(environment)

    def list_deployments(self) -> dict[str, dict]:
        return dict(self._deployments)


class ModelRegistry:
    """Model registry with versioning, staging, and metadata persistence.

    Supports MLflow backend if available, otherwise uses local filesystem.
    """

    def __init__(
        self,
        base_path: str | Path = "models/registry",
        backend: str = "local",
        mlflow_tracking_uri: str | None = None,
    ):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.backend = backend
        self._registry_path = self.base_path / "registry.json"
        self._registry: dict[str, dict[str, Any]] = self._load_registry()

        if backend == "mlflow":
            self._mlflow_available = self._init_mlflow(mlflow_tracking_uri)
            if not self._mlflow_available:
                logger.warning("MLflow not available, falling back to local backend")
                self.backend = "local"
        else:
            self._mlflow_available = False

    def _init_mlflow(self, tracking_uri: str | None) -> bool:
        try:
            import mlflow
            mlflow.set_tracking_uri(tracking_uri or "http://localhost:5000")
            return True
        except ImportError:
            return False

    def _load_registry(self) -> dict[str, dict[str, Any]]:
        if self._registry_path.exists():
            try:
                return json.loads(self._registry_path.read_text())
            except (json.JSONDecodeError, OSError):
                logger.warning("Corrupt registry file, starting fresh")
        return {}

    def _save_registry(self) -> None:
        self._registry_path.write_text(json.dumps(self._registry, indent=2, default=str))

    def register(
        self,
        name: str,
        model: Any = None,
        metrics: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        model_type: str = "unknown",
        version: str | None = None,
        stage: str = "staging",
        artifact_path: str | None = None,
    ) -> str:
        resolved_version = version or self._next_version(name)
        entry = self._registry.setdefault(name, {"versions": {}, "latest_version": "0.0.0"})

        if resolved_version in entry["versions"]:
            logger.warning("Overwriting existing version", extra={"name": name, "version": resolved_version})

        mv = ModelVersion(
            name=name,
            version=resolved_version,
            model_type=model_type,
            metrics=metrics or {},
            params=params or {},
            stage=stage,
            artifact_path=artifact_path,
        )
        entry["versions"][resolved_version] = mv.to_dict()
        entry["latest_version"] = resolved_version
        self._save_registry()

        if model is not None:
            store = ArtifactStore(self.base_path / "artifacts")
            saved_path = store.save(model, name, resolved_version)
            entry["versions"][resolved_version]["artifact_path"] = saved_path
            self._save_registry()

        if self._mlflow_available and model is not None:
            try:
                import mlflow
                with mlflow.start_run(run_name=f"{name}-{resolved_version}"):
                    if metrics:
                        mlflow.log_metrics(metrics)
                    if params:
                        mlflow.log_params(params)
                    mlflow.sklearn.log_model(model, artifact_path=f"model/{name}")
                logger.info("Logged to MLflow", extra={"model_name": name, "model_version": resolved_version})
            except Exception as exc:
                logger.warning("MLflow logging failed", exc_info=exc)

        logger.info("Model registered", extra={"model_name": name, "model_version": resolved_version})
        return resolved_version

    def load(self, name: str, version: str | None = None) -> tuple[Any, dict[str, Any]]:
        resolved_version = version or self.get_latest_version(name)
        entry = self._registry.get(name)
        if not entry or resolved_version not in entry["versions"]:
            raise ValueError(f"Model '{name}' version '{resolved_version}' not found")

        version_data = entry["versions"][resolved_version]
        artifact_path = version_data.get("artifact_path")
        if artifact_path and Path(artifact_path).exists():
            import joblib
            model = joblib.load(artifact_path)
        else:
            store = ArtifactStore(self.base_path / "artifacts")
            model = store.load(name, resolved_version)
        return model, version_data

    def list_models(self) -> list[dict[str, Any]]:
        result = []
        for name, entry in self._registry.items():
            result.append({
                "name": name,
                "latest_version": entry.get("latest_version", "0.0.0"),
                "version_count": len(entry.get("versions", {})),
                "stages": list(set(v.get("stage", "staging") for v in entry.get("versions", {}).values())),
            })
        return result

    def get_latest_version(self, name: str) -> str:
        entry = self._registry.get(name)
        if not entry:
            raise ValueError(f"Model '{name}' not found in registry")
        return entry.get("latest_version", "")

    def promote_to_production(self, name: str, version: str) -> None:
        entry = self._registry.get(name)
        if not entry or version not in entry["versions"]:
            raise ValueError(f"Version '{version}' not found for model '{name}'")
        entry["versions"][version]["stage"] = "production"
        self._save_registry()
        logger.info("Model promoted to production", extra={"model_name": name, "model_version": version})

    def get_version_details(self, name: str, version: str) -> dict[str, Any]:
        entry = self._registry.get(name)
        if not entry or version not in entry["versions"]:
            raise ValueError(f"Version '{version}' not found for model '{name}'")
        return entry["versions"][version]

    def _next_version(self, name: str) -> str:
        entry = self._registry.get(name)
        if not entry:
            return "1.0.0"
        latest = entry.get("latest_version", "0.0.0")
        return _increment_version(latest, "patch")

    def get_production_model(self, name: str) -> tuple[Any, dict[str, Any]]:
        entry = self._registry.get(name)
        if not entry:
            raise ValueError(f"Model '{name}' not found")
        for version, data in entry.get("versions", {}).items():
            if data.get("stage") == "production":
                return self.load(name, version)
        raise ValueError(f"No production version found for model '{name}'")
