import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import api, db, middleware, models
from app.config import settings
from app.services import GoogleCal, tg_router
from app.utils import create_superuser

models.Base.metadata.create_all(db.engine)


logging.basicConfig(level=logging.INFO)


google_cal = GoogleCal(
    api_key=settings.CAL_API_KEY,
    cal_id=settings.CAL_ID,
)

app = FastAPI(
    title='API service for signups and Telegram integration',
    docs_url='/docs',
    version='0.1.3',
    redoc_url='/redocs',
)

app.include_router(api.api_router, prefix=settings.API_V1_STR)
app.include_router(tg_router, prefix=settings.WEBHOOK_PATH,
                   tags=['Telegram Bot'])

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


@app.on_event('startup')
async def startup_event():
    google_cal.get()

    if settings.FIRST_SUPERUSER:
        await create_superuser(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
