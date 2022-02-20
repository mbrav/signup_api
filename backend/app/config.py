import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

env_path = Path('.env')
load_dotenv(dotenv_path=env_path)


TESTING = os.getenv('TESTING', True)
DEBUG = os.getenv('DEBUG')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', None)

DATABASE_URL = 'sqlite:///./api.db'

SECRET = os.getenv('SECRET', 'HS256')
CRYPT_ALGORITHM = os.getenv('CRYPT_ALGORITHM', 'HS256')
TOKEN_EXPIRE_MINUTES = os.getenv('TOKEN_EXPIRE_MINUTES', 15)


BACKEND_CORS_ORIGINS = os.getenv('BACKEND_CORS_ORIGINS', '').split()

if not TESTING:
    DB_USER = os.getenv('DB_USER', None)
    DB_PASSWORD = os.getenv('DB_PASSWORD', None)
    DB_HOST = os.getenv('DB_HOST', None)
    DB_PORT = os.getenv('DB_PORT', None)
    DB_NAME = os.getenv('DB_NAME', None)
    DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4'

    logger_level = logging.INFO
    if DEBUG:
        logger_level = logging.DEBUG

    formatter = logging.Formatter(
        '%(levelname)s:%(name)s %(asctime)s: %(message)s')
    handler = logging.handlers.RotatingFileHandler('logs/app.log',
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
    version='0.1.0',
    redoc_url='/redocs'
)
