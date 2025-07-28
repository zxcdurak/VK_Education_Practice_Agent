from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    vk_token: str
    giga_auth_key: str
    clientSecret: str
    clientID: str
    model_LLM: str

    model_config = SettingsConfigDict(env_file="../.env")

settings = Settings()
