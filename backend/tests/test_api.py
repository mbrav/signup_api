from app import models
from app.config import settings
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestApi:
    """Test Api class"""

    def test_api_root(self, client: TestClient) -> None:
        response = client.get(f'{settings.API_V1_STR}/')
        assert response.status_code == 200
        assert 'response' in response.json()

    def test_create_signup(
        self,
        db: Session,
        client: TestClient,
        new_signup: dict
    ) -> None:

        res = client.post(f'{settings.API_V1_STR}/signups', json=new_signup)

        created_user = db.query(
            models.Signup).filter(
            models.Signup.first_name == new_signup['first_name']).first()

        assert res.status_code == 201
        assert created_user
