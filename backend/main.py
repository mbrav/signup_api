import logging
import os

from fastapi import FastAPI

from app import api, db, middleware, models, services
from app.config import settings
from app.utils import create_superuser

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(FILE_DIR)
with open(f'{REPO_DIR}/README.md') as f:
    description = f.read()

logger = logging.getLogger()

app = FastAPI(
    title='Fast API service for signups and Telegram integration',
    description=description,
    contact={
        'name': 'mbrav',
        'url': 'https://github.com/mbrav',
        'email': 'mbrav@protonmail.com',
    },
    license_info={
        'name': 'GNU 3.0',
        'url': 'https://www.gnu.org/licenses/gpl-3.0.en.html',
    },
    docs_url='/docs',
    version=settings.VERSION,
    redoc_url='/redocs',
)


app.include_router(api.api_router, prefix=settings.API_V1_STR)
app.include_router(services.tg_router,
                   prefix=settings.WEBHOOK_PATH,
                   tags=['Telegram Bot'])

app.add_middleware(middleware.ProcessTimeMiddleware)

if settings.LOGGING:
    logger_level = logging.INFO
    if settings.DEBUG:
        logger_level = logging.DEBUG

    os.makedirs(os.path.dirname(settings.LOG_PATH), exist_ok=True)

    formatter = logging.Formatter(
        '%(levelname)s:%(name)s %(asctime)s: %(message)s')
    handler = logging.handlers.RotatingFileHandler(
        settings.LOG_PATH,
        delay=0,
        maxBytes=1024*1024*2,
        backupCount=5)
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logger_level)
    logger.addHandler(handler)

    logging.getLogger('sqlalchemy.engine').setLevel(logger_level)
    logging.getLogger('sqlalchemy.pool').setLevel(logger_level)


@app.on_event('startup')
async def startup_database():
    logger.info('FastAPI starting up...')
    async with db.engine.begin() as conn:
        if settings.TESTING:
            await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)
    await db.engine.dispose()
    if settings.FIRST_SUPERUSER:
        await create_superuser(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD)


@app.on_event('startup')
async def start_serices():
    await services.start_scheduler()
    await services.start_calendar()


@app.on_event('shutdown')
async def shutdown_event():
    logger.info('FastAPI shutting down...')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
