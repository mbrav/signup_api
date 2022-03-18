import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import api, db, middleware, models
from app.config import settings
from app.services import GoogleCal, tg_router
from app.utils import create_superuser

logging.basicConfig(level=logging.INFO)

google_cal = GoogleCal(
    api_key=settings.CAL_API_KEY,
    cal_id=settings.CAL_ID,
)

app = FastAPI(
    title='API service for signups and Telegram integration',
    docs_url='/docs',
    version='0.1.4',
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
        # allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


async def start_db():
    async with db.engine.begin() as conn:
        # await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)
    await db.engine.dispose()


@app.on_event("startup")
async def startup_event():
    # logger.info("Starting up...")
    # google_cal.get()
    # if settings.FIRST_SUPERUSER:
    #     await create_superuser(
    #         username=settings.FIRST_SUPERUSER,
    #         password=settings.FIRST_SUPERUSER_PASSWORD)
    await start_db()


@app.on_event("shutdown")
async def shutdown_event():
    pass
    # logger.info("Shutting down...")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
