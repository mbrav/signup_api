[![FastAPI and Pytest CI](https://github.com/mbrav/signup_api/actions/workflows/fastapi.yml/badge.svg)](https://github.com/mbrav/signup_api/actions/workflows/fastapi.yml)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-yellow.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![wakatime](https://wakatime.com/badge/user/54ad05ce-f39b-4fa3-9f2a-6fe4b1c53ba4/project/218dc651-c58d-4dfb-baeb-1f70c7bdf2c1.svg)](https://wakatime.com/badge/user/54ad05ce-f39b-4fa3-9f2a-6fe4b1c53ba4/project/218dc651-c58d-4dfb-baeb-1f70c7bdf2c1)

## FastAPI signup_api

An 100% asynchronous Fast API service for signups and Telegram integration.

### Intent

As of now, this project is mainly an **architecture design** experimental ground with an abstract end goal in mind, rather than an actual functioning app and therefore would be most useful if used as a starting template example. The project uses [FastAPI](https://fastapi.tiangolo.com/) as a base framework with the following stack:

-   Integration with [SQLAlchemy's](https://www.sqlalchemy.org/) new ORM statement paradigm to be implemented in [v2.0](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html);
-   Asynchronous PostgreSQL databse via [asyncpg](https://github.com/MagicStack/asyncpg), one of the fastest and high performant Database Client Libraries for python/asyncio;
-   Integration with Telegram library [aiogram](https://github.com/aiogram/aiogram) using its upcoming [v3.0 version](https://docs.aiogram.dev/en/dev-3.x/) with webhooks as an integration method with FastAPI;
-   A token authorization system using the [argon2 password hashing algorithm](https://github.com/P-H-C/phc-winner-argon2), the password-hashing function that won the [Password Hashing Competition (PHC)](https://www.password-hashing.net/);
-   Asynchronous task scheduling using [apscheduler](https://github.com/agronholm/apscheduler);
-   Designed to run efficently as possbile on a device such as the Raspberry Pi;
-   Asynchronous pytests using [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio) and [httpx](https://www.python-httpx.org/) libraries instead of the synchronous requests library;
-   Vue.js 3.2 basic frontend with potential future experimentation with [vite](https://vitejs.dev/) and [vuetify](https://github.com/vuetifyjs/vuetify) framework.

### Backend

With docker-compose installed, do:

```bash
docker-compose up
```

Go to [0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) for SwaggerUI

#### Run FastAPI Backend locally

```bash
$ git clone https://github.com/mbrav/signup_api.git
$ cd signup_api
```

Setup a local python environment:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

Install dependencies with poetry:

```bash
$ cd app
$ poetry install
```

Copy .env file:

```bash
$ cp .env.example .env
```

Run server:

```bash
$ python main.py
```

Run server with uvicorn:

```bash
$ python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1 --reload
```

Advanced config:

```bash
$ python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2 --ssl-keyfile ~/ssl/keys/server.key --ssl-certfile ~/ssl/certs/server.crt
```

Go to [0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) for SwaggerUI

#### Run pytest

```bash
$ python -m pytest
```
