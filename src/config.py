from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    vk_token: str
    giga_auth_key: str
    client_secret: str
    client_id: str
    model_llm: str

    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
