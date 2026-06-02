from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    app_name: str = "App"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Config()
