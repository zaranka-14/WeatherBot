from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings
from secret_token import token


class Settings(BaseSettings):
    bot_token: SecretStr = token
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
