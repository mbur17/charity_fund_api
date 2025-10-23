from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_title: str = Field(
        'QRKot – API для благотворительных проектов', env='APP_TITLE'
    )
    app_description: str = Field(
        'API-сервис для управления благотворительными проектами и донатами.',
        env='APP_DESCRIPTION'
    )
    database_url: str = Field(
        'sqlite+aiosqlite:///./app.db', env='DATABASE_URL'
    )
    secret: str = Field('SECRET', env='SECRET')
    # Google API
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()