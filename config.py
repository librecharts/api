from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LibreCharts API"
    update_token: str
    model_config = SettingsConfigDict(env_file=".env")
