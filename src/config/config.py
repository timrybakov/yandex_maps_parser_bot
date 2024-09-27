from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    auth_token: str
    database_url: str
    redis_url: str
    firefox_url: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )
