from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Кошачий благотворительный фонд'
    app_description = 'Сервис для поддержки котиков!'
    database_url: str = 'sqlite+aiosqlite:///./database.db'
    secret: str = 'SECRET'
    default_invested_amount = 0
    min_project_name_length = 1
    max_project_name_length = 100
    min_project_description_length = 1
    project_full_amount_example = 5000
    donation_full_amount_example = 2500
    project_description_example = 'project description for example'
    project_name_example = 'Some food for our cats'
    donation_comment_example = 'Some money for sweet cats'
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
        env_file: str = '.env'


settings = Settings()
