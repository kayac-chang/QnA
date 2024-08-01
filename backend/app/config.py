from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SUPABASE_DB_CONNECTION: str
    SUPABASE_API_URL: str
    SUPABASE_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
