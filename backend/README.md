[![FastAPI and Pytest CI](https://github.com/mbrav/signup_api/actions/workflows/fastapi.yml/badge.svg)](https://github.com/mbrav/signup_api/actions/workflows/fastapi.yml)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-yellow.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![wakatime](https://wakatime.com/badge/user/54ad05ce-f39b-4fa3-9f2a-6fe4b1c53ba4/project/218dc651-c58d-4dfb-baeb-1f70c7bdf2c1.svg)](https://wakatime.com/badge/user/54ad05ce-f39b-4fa3-9f2a-6fe4b1c53ba4/project/218dc651-c58d-4dfb-baeb-1f70c7bdf2c1)

## Run with Python locally

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

### Run pytest

```bash
$ python -m pytest
```
