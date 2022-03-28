"""
5 Scopes of Pytest Fixtures

Pytest fixtures have five different scopes: function, class, module, package, and session.
"""

from typing import AsyncGenerator

import pytest
from app import api, db, utils
from app.services import AuthService
from fastapi import FastAPI
from httpx import AsyncClient
from main import app


@pytest.fixture()
async def db_session() -> AsyncGenerator:
    yield db.get_database()


@pytest.fixture()
async def get_app() -> FastAPI:
    return app


@pytest.fixture
async def async_client(get_app, scope='session') -> AsyncGenerator:
    """
    Create a test client connected to the main app instance
    Testing with testclient without async, requires requests
    See https://github.com/tiangolo/fastapi/issues/1273

    from fastapi.testclient import TestClient
    return await AsyncClient(app=app)
    """

    async with AsyncClient(app=get_app, base_url='http://test') as client:
        yield client


@pytest.fixture
async def authservice(scope='session') -> AuthService:
    return api.deps.auth_service


@pytest.fixture
async def new_login(scope='function') -> dict:
    data = {
        'username': utils.random_lower_string(10),
        'password': utils.random_id_string(30),
    }
    return data


@pytest.fixture
async def new_signup(scope='function') -> dict:
    data = {
        'first_name': utils.random_lower_string(10).capitalize(),
        'last_name': utils.random_lower_string(12).capitalize(),
        'phone': utils.random_phone(),
        'email': utils.random_email(),
        'class_id': utils.random_id_string(20),
    }
    return data
