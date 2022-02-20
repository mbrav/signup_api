from starlette.middleware.cors import CORSMiddleware

from app import api, config, db, middleware, models

# from app.services import TGbot


models.Base.metadata.create_all(db.engine)
if config.FIRST_SUPERUSER:
    from app.api.deps import create_superuser
    create_superuser(
        username=config.FIRST_SUPERUSER,
        password=config.FIRST_SUPERUSER_PASSWORD)


app = config.app
app.include_router(api.index.router)
app.include_router(api.auth.router)
app.include_router(api.signups.router)


app.add_middleware(middleware.ProcessTimeMiddleware)
if config.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.BACKEND_CORS_ORIGINS,
        # allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


# bot = TGbot(token=config.TELEGRAM_TOKEN)
# bot.run()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=8000,
        debug=True
    )
