import logging
from typing import List, Optional

from fastapi import FastAPI
from pydantic import AmqpDsn, AnyHttpUrl, BaseSettings, Field


class SettingsBase(BaseSettings):
    """
    App Base Settings

    Тo get a new secret key run:
        openssl rand -hex 32

    """

    TESTING: bool = Field(env='TESTING', default=True)
    DEBUG: bool = Field(env='DEBUG', default=False)
    LOGGING: bool = Field(env='LOGGING', default=False)

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


class MySQLMixin(DBSettings):
    """"MySQL Settings Mixin"""

    MYSQL_USER: Optional[str] = Field(env='MYSQL_USER')
    MYSQL_PASSWORD: Optional[str] = Field(env='MYSQL_PASSWORD')
    MYSQL_HOST: Optional[str] = Field(env='MYSQL_HOST')
    MYSQL_PORT: Optional[str] = Field(env='MYSQL_PORT')
    MYSQL_NAME: Optional[str] = Field(env='MYSQL_NAME')

    @property
    def DATABASE_URL(self) -> str:
        url = f'mysql+pymysql://' \
            f'{self.MYSQL_USER}:' \
            f'{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}/' \
            f'{self.MYSQL_NAME}?charset=utf8mb4'
        return url


class SQLiteMixin(DBSettings):
    """"SQLite Settings Mixin"""

    SQLITE_DATABASE_FILE: str = 'sqlite:///./api.db'
    SQLITE_DATABASE_MEMORY: str = 'sqlite:///:memory:'


class ServiceMixin(SettingsBase):
    """Service Settings Mixin"""

    CRYPT_ALGORITHM: str = Field(
        env='CRYPT_ALGORITHM', default='HS256')
    TOKEN_EXPIRE_MINUTES: int = Field(
        env='TOKEN_EXPIRE_MINUTES', default=60*24)
    BACKEND_CORS_ORIGINS: Optional[List[AnyHttpUrl]] = Field(
        env='BACKEND_CORS_ORIGINS')

    TELEGRAM_TOKEN: Optional[str] = Field(env='TELEGRAM_TOKEN')


class Settings(MySQLMixin, SQLiteMixin, ServiceMixin):
    """Combined Settings with previous settings as mixins"""
    pass


settings = Settings()

if settings.LOGGING:
    logger_level = logging.INFO
    if settings.DEBUG:
        logger_level = logging.DEBUG

    formatter = logging.Formatter(
        '%(levelname)s:%(name)s %(asctime)s: %(message)s')
    handler = logging.handlers.RotatingFileHandler(
        'logs/app.log',
        delay=0,
        maxBytes=1024*1024*2,
        backupCount=5)
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logger_level)
    logger.addHandler(handler)

    # logging.getLogger('sqlalchemy.engine').setLevel(logger_level)
    logging.getLogger('sqlalchemy.pool').setLevel(logger_level)

app = FastAPI(
    title='API service for signups and Telegram integration',
    docs_url='/docs',
    version='0.1.3',
    redoc_url='/redocs'
)
