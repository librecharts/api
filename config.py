from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LibreCharts API"
    password: str
    update_token: str
    sentry_uri: str
    model_config = SettingsConfigDict(env_file=".env")
