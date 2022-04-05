[![FastAPI and Pytest CI](https://github.com/mbrav/signup_api/actions/workflows/fastapi.yml/badge.svg)](https://github.com/mbrav/signup_api/actions/workflows/fastapi.yml)

## FastAPI signup_api

An asynchronous Fast API service for signups and Telegram integration

### Run in Docker

With docker-compose installed, do:

```bash
docker-compose up
```

Go to [0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) for SwaggerUI

### Run with Python locally

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
$ poetry install
```

Run server:

```bash
$ python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1 --reload
```

Advanced config:

```bash
$ python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2 --ssl-keyfile ~/ssl/keys/server.key --ssl-certfile ~/ssl/certs/server.crt
```

Go to [0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) for SwaggerUI
