import base64
from datetime import timezone
from typing import Any, List, Optional

from pydantic import (AnyHttpUrl, BaseSettings, Field, FilePath, PostgresDsn,
                      SecretStr, validator)


class SettingsBase(BaseSettings):
    """
    App Base Settings

    Тo get a new secret key run:
        openssl rand -hex 32

    """

    VERSION: str = Field(env='VERSION', default='0.0.1')

    TESTING: bool = Field(env='TESTING', default=True)
    DEBUG: bool = Field(env='DEBUG', default=False)
    LOGGING: bool = Field(env='LOGGING', default=False)
    LOG_PATH: str = Field(env='LOG_PATH', default='logs/app.log')

    SECRET_KEY: SecretStr = Field(env='SECRET_KEY', default='pl3seCh@nGeM3!')
    API_V1_STR: str = Field(env='API_V1_STR', default='/api')
    TIMEZONE: timezone = Field(timezone.utc)

    SSL_PUBLIC_PATH: Optional[FilePath] = Field(
        env='SSL_PUBLIC_PATH', default=None)

    class Config:
        env_file = '.env'
        env_prefix = ''
        # case_sensitive = True

    @property
    def SSL_PUBLIC(self) -> Optional[Any]:
        if self.SSL_PUBLIC_PATH:
            with open(self.SSL_PUBLIC_PATH) as key:
                string = key.read().encode('utf-8')
                encodedBytes = base64.b64encode(string)
                return str(encodedBytes, 'utf-8')
        return None


class DBSettings(SettingsBase):
    """"Database Settings"""

    FIRST_SUPERUSER: str = Field(
        env='FIRST_SUPERUSER', default='admin')
    FIRST_SUPERUSER_PASSWORD: SecretStr = Field(
        env='FIRST_SUPERUSER_PASSWORD', default='password')


class PostgresMixin(DBSettings):
    """"Postgres Settings Mixin"""

    POSTGRES_USER: str = Field(
        env='POSTGRES_USER', default='postgres')
    POSTGRES_PASSWORD: SecretStr = Field(
        env='POSTGRES_PASSWORD', default='postgres')
    POSTGRES_SERVER: str = Field(
        env='POSTGRES_SERVER', default='db')
    POSTGRES_PORT: int = Field(env='POSTGRES_PORT', default=5432)
    POSTGRES_DB: str = Field(env='POSTGRES_DB', default='postgres')

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        url = f'postgresql+asyncpg://' \
            f'{self.POSTGRES_USER}:' \
            f'{self.POSTGRES_PASSWORD.get_secret_value()}' \
            f'@{self.POSTGRES_SERVER}:' \
            f'{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        return url


class AuthServiceMixin(SettingsBase):
    """Auth Service Settings Mixin"""

    CRYPT_ALGORITHM: str = Field(
        env='CRYPT_ALGORITHM', default='HS256')
    TOKEN_EXPIRE_MINUTES: int = Field(
        env='TOKEN_EXPIRE_MINUTES', default=60*24)
    BACKEND_CORS_ORIGINS: Optional[List[AnyHttpUrl]] = Field(
        env='BACKEND_CORS_ORIGINS')


class ExternalServiceMixin(SettingsBase):
    """External Service Settings Mixin for bots, APIs etc."""

    TELEGRAM_TOKEN: Optional[SecretStr] = Field(env='TELEGRAM_TOKEN')
    TELEGRAM_ADMIN: Optional[int] = Field(
        env='TELEGRAM_ADMIN', default=12345678)

    WEBHOOK_USE: Optional[bool] = Field(env='WEBHOOK_USE', default=False)
    WEBHOOK_HOST: Optional[str] = Field(env='WEBHOOK_HOST')
    WEBHOOK_PORT: Optional[int] = Field(env='WEBHOOK_PORT', default=80)
    WEBHOOK_PATH: Optional[str] = Field(env='WEBHOOK_PATH', default='/bot')

    CAL_API_KEY: Optional[SecretStr] = Field(env='CAL_API_KEY')
    CAL_ID: Optional[SecretStr] = Field(env='CAL_ID')

    @property
    def WEBHOOK_URL(self) -> AnyHttpUrl:
        port = f':{self.WEBHOOK_PORT}' if (self.WEBHOOK_PORT != 80) else ''
        url = f'{self.WEBHOOK_HOST}{port}{self.WEBHOOK_PATH}'
        return url

    @validator('WEBHOOK_PORT')
    def WEBHOOK_PORT_valid(cls, v):
        error = 'Tg webhook can be set up only on ports 80, 88, 443 or 8443'
        assert v in (80, 88, 443, 8443), error
        return v


class Settings(
        PostgresMixin,
        AuthServiceMixin,
        ExternalServiceMixin
):
    """Combined Settings with previous settings as mixins"""
    pass


settings = Settings()
test = settings
