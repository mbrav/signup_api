from typing import Dict

from app.config import settings
from app.schemas import UserCreate
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestAuth:
    """Test auth"""

    def test_auth_service(self, authservice):
        assert authservice

    def test_registration(
            self, client: TestClient, new_login: dict) -> None:
        res = client.post(
            f'{settings.API_V1_STR}/users/register', json=new_login)

        json = res.json()
        assert json['username'] == new_login['username']
        assert res.status_code == 201
