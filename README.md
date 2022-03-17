[![FastAPI and Pytest CI](https://github.com/mbrav/signup_api/actions/workflows/fastapi.yml/badge.svg)](https://github.com/mbrav/signup_api/actions/workflows/fastapi.yml)

## FastAPI signup_api

An asynchronous Fast API service for signups and Telegram integration.

### Intent

As of now, this project is an experimental ground that uses [FastAPI](https://fastapi.tiangolo.com/) as a base framework with the following stack:

-   Integration with [SQLAlchemy's](https://www.sqlalchemy.org/) new ORM statement paradigm to be implemented in [v2.0](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html);
-   Asynchronous PostgreSQL databse via [asyncpg](https://github.com/MagicStack/asyncpg), one of the fastest and high performant Database Client Libraries for python/asyncio;
-   Integration with Telegram library [aiogram](https://github.com/aiogram/aiogram) using its upcoming [v3.0 version](https://docs.aiogram.dev/en/dev-3.x/) with webhooks as an integration method with FastAPI;
-   A token authorization system using the [argon2 password hashing algorithm](https://github.com/P-H-C/phc-winner-argon2), the password-hashing function that won the [Password Hashing Competition (PHC)](https://www.password-hashing.net/);
-   Asynchronous pytests using [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio) and [httpx](https://www.python-httpx.org/) libraries instead of the synchronous requests library;
-   Vue.js 3.2 basic frontend with potential future experimentation with [vite](https://vitejs.dev/) and [vuetify](https://github.com/vuetifyjs/vuetify) framework.

### Run FastAPI backend in Docker

With docker-compose installed, do:

```bash
docker-compose up
```

Go to [0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) for SwaggerUI
