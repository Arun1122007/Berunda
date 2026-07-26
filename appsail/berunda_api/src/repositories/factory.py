from __future__ import annotations

import os
from typing import Any

from fastapi import Request

from src.database import get_session_factory
from src.repositories.catalyst_adapter import (
    CatalystAIAssistantRepository,
    CatalystAnomalyRepository,
    CatalystAuditRepository,
    CatalystAuthRepository,
    CatalystEntityRepository,
    CatalystFairnessRepository,
    CatalystFIRRepository,
    CatalystGraphRepository,
    CatalystHotspotRepository,
    CatalystIngestionRepository,
    CatalystOffenderRepository,
    CatalystRAGRepository,
    CatalystRiskRepository,
    CatalystSocioeconomicRepository,
)
from src.repositories.core import (
    AIAssistantRepository,
    AnomalyRepository,
    AuditRepository,
    AuthRepository,
    EntityRepository,
    FairnessRepository,
    FileStorage,
    FIRRepository,
    GraphRepository,
    HotspotRepository,
    IngestionRepository,
    OffenderRepository,
    RAGRepository,
    RepositoryFactory,
    RiskRepository,
    SocioeconomicRepository,
)
from src.repositories.sqlite_adapter import (
    SQLiteAIAssistantRepository,
    SQLiteAnomalyRepository,
    SQLiteAuditRepository,
    SQLiteAuthRepository,
    SQLiteEntityRepository,
    SQLiteFairnessRepository,
    SQLiteFIRRepository,
    SQLiteGraphRepository,
    SQLiteHotspotRepository,
    SQLiteIngestionRepository,
    SQLiteOffenderRepository,
    SQLiteRAGRepository,
    SQLiteRiskRepository,
    SQLiteSocioeconomicRepository,
)


class EnvironmentRepositoryFactory(RepositoryFactory):
    def __init__(self, req: Request, session: Any = None):
        self.req = req
        self.session = session
        self.is_catalyst = (
            "X_ZOHO_CATALYST_LISTEN_PORT" in os.environ
            or os.environ.get("USE_CATALYST") == "true"
        )

    def _make_session(self):
        if self.session is not None:
            return self.session
        factory = get_session_factory()
        return factory()

    def get_fir_repository(self) -> FIRRepository:
        if self.is_catalyst:
            return CatalystFIRRepository(self.req)
        return SQLiteFIRRepository(self._make_session())

    def get_auth_repository(self) -> AuthRepository:
        if self.is_catalyst:
            return CatalystAuthRepository(self.req)
        return SQLiteAuthRepository(self._make_session())

    def get_entity_repository(self) -> EntityRepository:
        if self.is_catalyst:
            return CatalystEntityRepository(self.req)
        return SQLiteEntityRepository(self._make_session())

    def get_audit_repository(self) -> AuditRepository:
        if self.is_catalyst:
            return CatalystAuditRepository(self.req)
        return SQLiteAuditRepository(self._make_session())

    def get_file_storage(self) -> FileStorage:
        if self.is_catalyst:
            from src.repositories.catalyst_adapter import CatalystFileStorage
            return CatalystFileStorage(self.req, os.environ.get("STRATUS_BUCKET", "berunda-dev-docs"))
        return LocalFileStorage(self._make_session())

    def get_ai_assistant_repository(self) -> AIAssistantRepository:
        if self.is_catalyst:
            return CatalystAIAssistantRepository(self.req)
        return SQLiteAIAssistantRepository(self._make_session())

    def get_anomaly_repository(self) -> AnomalyRepository:
        if self.is_catalyst:
            return CatalystAnomalyRepository(self.req)
        return SQLiteAnomalyRepository(self._make_session())

    def get_fairness_repository(self) -> FairnessRepository:
        if self.is_catalyst:
            return CatalystFairnessRepository(self.req)
        return SQLiteFairnessRepository(self._make_session())

    def get_graph_repository(self) -> GraphRepository:
        if self.is_catalyst:
            return CatalystGraphRepository(self.req)
        return SQLiteGraphRepository(self._make_session())

    def get_hotspot_repository(self) -> HotspotRepository:
        if self.is_catalyst:
            return CatalystHotspotRepository(self.req)
        return SQLiteHotspotRepository(self._make_session())

    def get_ingestion_repository(self) -> IngestionRepository:
        if self.is_catalyst:
            return CatalystIngestionRepository(self.req)
        return SQLiteIngestionRepository(self._make_session())

    def get_offender_repository(self) -> OffenderRepository:
        if self.is_catalyst:
            return CatalystOffenderRepository(self.req)
        return SQLiteOffenderRepository(self._make_session())

    def get_rag_repository(self) -> RAGRepository:
        if self.is_catalyst:
            return CatalystRAGRepository(self.req)
        return SQLiteRAGRepository(self._make_session())

    def get_risk_repository(self) -> RiskRepository:
        if self.is_catalyst:
            return CatalystRiskRepository(self.req)
        return SQLiteRiskRepository(self._make_session())

    def get_socioeconomic_repository(self) -> SocioeconomicRepository:
        if self.is_catalyst:
            return CatalystSocioeconomicRepository(self.req)
        return SQLiteSocioeconomicRepository(self._make_session())


def get_repository_factory(request: Request, session: Any = None) -> EnvironmentRepositoryFactory:
    return EnvironmentRepositoryFactory(request, session=session)


class LocalFileStorage(FileStorage):
    def __init__(self, session):
        self.session = session

    async def save_file(self, file_path: str, content: bytes, mime_type: str) -> str:
        import hashlib
        import os as os_module

        os_module.makedirs("data/uploads", exist_ok=True)
        file_hash = hashlib.sha256(content).hexdigest()
        ext = os_module.path.splitext(file_path)[1] or ".bin"
        local_path = f"data/uploads/{file_hash}{ext}"
        with open(local_path, "wb") as f:
            f.write(content)
        return local_path

    async def get_file(self, file_uri: str) -> bytes | None:
        import os as os_module

        if os_module.path.exists(file_uri):
            with open(file_uri, "rb") as f:
                return f.read()
        return None

    async def delete_file(self, file_uri: str) -> bool:
        import os as os_module

        if os_module.path.exists(file_uri):
            os_module.remove(file_uri)
            return True
        return False

    async def file_exists(self, file_uri: str) -> bool:
        import os as os_module

        return os_module.path.exists(file_uri)
