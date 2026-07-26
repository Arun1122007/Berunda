from fastapi import Request
from src.repositories.factory import get_repository_factory

def get_fir_repo(request: Request):
    factory = get_repository_factory(request)
    return factory.get_fir_repository()

def get_auth_repo(request: Request):
    factory = get_repository_factory(request)
    return factory.get_auth_repository()
