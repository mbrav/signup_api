
from typing import Generator

import pytest
from app.db import Session
from app.utils import (random_email, random_id_string, random_lower_string,
                       random_phone)
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope='session')
def db() -> Generator:
    yield Session()


@pytest.fixture(scope='module')
def client() -> Generator:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='module')
def new_login() -> dict:
    data = {
        'username': random_lower_string(10),
        'password': random_id_string(30),
    }
    return data


@pytest.fixture(scope='module')
def new_signup() -> dict:
    data = {
        'first_name': random_lower_string(10).capitalize(),
        'last_name': random_lower_string(12).capitalize(),
        'phone': random_phone(),
        'email': random_email(),
        'class_id': random_id_string(20),
    }
    return data


@pytest.fixture(scope='module')
def authservice():
    from app.api.deps import auth_service
    return auth_service
