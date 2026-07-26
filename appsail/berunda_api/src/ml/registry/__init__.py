"""ML model registry."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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
    ):
        self.name = name
        self.version = version
        self.model_type = model_type
        self.metrics = metrics or {}
        self.artifact_path = artifact_path
        self.params = params or {}
        self.created_at = datetime.now(timezone.utc).isoformat()
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
            "created_at": self.created_at,
            "version_hash": self.version_hash,
        }


class ArtifactStore:
    """Store and retrieve model artifacts."""

    def __init__(self, base_path: str | Path = "models/"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, model: Any, name: str, version: str) -> str:
        import joblib

        path = self.base_path / name / version
        path.mkdir(parents=True, exist_ok=True)
        artifact_path = path / "model.pkl"
        joblib.dump(model, artifact_path)
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
            "deployed_at": datetime.now(timezone.utc).isoformat(),
        }
        self._save()

    def get_deployment(self, environment: str) -> dict | None:
        return self._deployments.get(environment)
