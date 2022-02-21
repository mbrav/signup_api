from starlette.middleware.cors import CORSMiddleware

from app import api, db, middleware, models
from app.config import app, settings

# from app.services import TGbot


models.Base.metadata.create_all(db.engine)
if settings.FIRST_SUPERUSER:
    from app.utils import create_superuser
    create_superuser(
        username=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD)


app.include_router(api.index.router)
app.include_router(api.auth.router)
app.include_router(api.signups.router)


app.add_middleware(middleware.ProcessTimeMiddleware)
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        # allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


# bot = TGbot(token=settings.TELEGRAM_TOKEN)
# bot.run()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=8000,
        debug=True
    )
