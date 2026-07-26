from __future__ import annotations

from collections.abc import AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.repositories.factory import get_repository_factory


def get_fir_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_fir_repository()


def get_auth_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_auth_repository()


def get_entity_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_entity_repository()


def get_audit_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_audit_repository()


def get_ai_assistant_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_ai_assistant_repository()


def get_anomaly_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_anomaly_repository()


def get_fairness_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_fairness_repository()


def get_graph_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_graph_repository()


def get_hotspot_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_hotspot_repository()


def get_ingestion_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_ingestion_repository()


def get_offender_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_offender_repository()


def get_rag_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_rag_repository()


def get_risk_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_risk_repository()


def get_socioeconomic_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_socioeconomic_repository()


def get_file_storage(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_file_storage()


def get_investigation_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_fir_repository()


def get_dashboard_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_fir_repository()


def get_search_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_fir_repository()


def get_related_cases_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_fir_repository()


def get_report_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_fir_repository()


def get_job_repo(request: Request, session: AsyncSession = Depends(get_session)):
    factory = get_repository_factory(request, session=session)
    return factory.get_fir_repository()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session
