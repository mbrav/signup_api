[![FastAPI and Pytest CI](https://github.com/mbrav/signup_api/actions/workflows/fastapi.yml/badge.svg)](https://github.com/mbrav/signup_api/actions/workflows/fastapi.yml)

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
