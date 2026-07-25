from pydantic import Field
from pydantic_settings import BaseSettings

class IntegrationSettings(BaseSettings):
    model_config = {"env_prefix": "INT_"}
    base_url: str = Field(default="http://localhost:8000", alias="INT_BASE_URL")
    api_prefix: str = Field(default="/api/v1", alias="INT_API_PREFIX")
    test_admin_email: str = Field(default="admin@berunda.gov", alias="INT_ADMIN_EMAIL")
    test_admin_password: str = Field(default="admin123", alias="INT_ADMIN_PASS")
    test_officer_email: str = Field(default="officer@ksp.gov.in", alias="INT_OFFICER_EMAIL")
    test_officer_password: str = Field(default="officer123", alias="INT_OFFICER_PASS")

settings = IntegrationSettings()
