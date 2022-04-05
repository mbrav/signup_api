import config
from api import db, middleware, models
from api.routes import router

# from api.services import TGbot

models.Base.metadata.create_all(db.engine)

app = config.app
app.include_router(router)
app.add_middleware(middleware.ProcessTimeMiddleware)


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
