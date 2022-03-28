import logging
import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import api, db, middleware, models
from app.config import settings
# from app.services import GoogleCal, tg_router
from app.utils import create_superuser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# google_cal = GoogleCal(
#     api_key=settings.CAL_API_KEY,
#     cal_id=settings.CAL_ID,
# )

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(FILE_DIR)
with open(f'{REPO_DIR}/README.md') as f:
    description = f.read()

app = FastAPI(
    title='API service for signups and Telegram integration',
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
# app.include_router(tg_router, prefix=settings.WEBHOOK_PATH,
#                    tags=['Telegram Bot'])

app.add_middleware(middleware.ProcessTimeMiddleware)
# app.add_middleware(middleware.ClientLookupMiddleware)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


async def start_db():
    async with db.engine.begin() as conn:
        if settings.TESTING:
            await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)
    await db.engine.dispose()


@app.on_event('startup')
async def startup_event():
    logger.info('FastAPI starting up...')
    # google_cal.get()
    await start_db()
    if settings.FIRST_SUPERUSER:
        await create_superuser(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD)


@app.on_event('shutdown')
async def shutdown_event():
    logger.info('FastAPI shutting down...')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
