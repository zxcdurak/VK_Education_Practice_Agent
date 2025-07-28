from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    vk_token: str
    giga_auth_key: str
    clientSecret: str
    clientID: str
    
    model_config = ConfigDict(env_file=".env")

settings = Settings()
