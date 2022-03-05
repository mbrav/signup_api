from starlette.middleware.cors import CORSMiddleware

from app import api, db, middleware, models
from app.config import app, settings
from app.services import GoogleCal
from app.utils import create_superuser

google_cal = GoogleCal(
    api_key=settings.CAL_API_KEY,
    cal_id=settings.CAL_ID,
)

app.include_router(api.api_router, prefix=settings.API_V1_STR)


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

models.Base.metadata.create_all(db.engine)


@app.on_event("startup")
async def startup_event():
    google_cal.get()
    if settings.FIRST_SUPERUSER:
        await create_superuser(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD)
    if __name__ == '__main__':
        import uvicorn
        await uvicorn.run(
            app,
            host='0.0.0.0',
            port=8000,
            debug=True
        )
