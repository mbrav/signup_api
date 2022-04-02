from typing import List, Optional

from pydantic import AnyHttpUrl, BaseSettings, Field, PostgresDsn


class SettingsBase(BaseSettings):
    """
    App Base Settings

    Тo get a new secret key run:
        openssl rand -hex 32

    """

    VERSION: str = Field('0.1.4')

    TESTING: bool = Field(env='TESTING', default=True)
    DEBUG: bool = Field(env='DEBUG', default=False)
    LOGGING: bool = Field(env='LOGGING', default=False)
    LOG_PATH: str = Field(env='LOG_PATH', default='logs/app.log')

    SECRET_KEY: str = Field(env='SECRET_KEY', default='pl3seCh@nGeM3!')
    API_V1_STR: str = Field(env='API_V1_STR', default='/api')

    class Config:
        env_file = '.env'
        env_prefix = ''
        # case_sensitive = True


class DBSettings(SettingsBase):
    """"Database Settings"""

    FIRST_SUPERUSER: str = Field(
        env='FIRST_SUPERUSER', default='admin')
    FIRST_SUPERUSER_PASSWORD: str = Field(
        env='FIRST_SUPERUSER_PASSWORD', default='password')


class PostgresMixin(DBSettings):
    """"Postgres Settings Mixin"""

    POSTGRES_USER: Optional[str] = Field(
        env='POSTGRES_USER', default='postgres')
    POSTGRES_PASSWORD: Optional[str] = Field(
        env='POSTGRES_PASSWORD', default='postgres')
    POSTGRES_SERVER: Optional[str] = Field(
        env='POSTGRES_SERVER', default='db')
    POSTGRES_PORT: Optional[int] = Field(env='POSTGRES_PORT', default=5432)
    POSTGRES_DB: Optional[str] = Field(env='POSTGRES_DB', default='postgres')

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        url = f'postgresql+asyncpg://' \
            f'{self.POSTGRES_USER}:' \
            f'{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:' \
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

    TELEGRAM_BOT_API_KEY: Optional[str] = Field(env='TELEGRAM_BOT_API_KEY')

    WEBHOOK_HOST: Optional[str] = Field(env='WEBHOOK_HOST')
    WEBHOOK_PATH: Optional[str] = Field(env='WEBHOOK_PATH', default='/bot')

    CAL_API_KEY: Optional[str] = Field(env='CAL_API_KEY')
    CAL_ID: Optional[str] = Field(env='CAL_ID')

    @property
    def WEBHOOK_URL(self) -> str:
        url = f'{self.WEBHOOK_HOST}{self.WEBHOOK_PATH}'
        return url


class Settings(
        PostgresMixin,
        AuthServiceMixin,
        ExternalServiceMixin
):
    """Combined Settings with previous settings as mixins"""
    pass


settings = Settings()
