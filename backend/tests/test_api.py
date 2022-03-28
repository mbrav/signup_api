import pytest
from app import models
from app.config import settings
from httpx import AsyncClient
from sqlalchemy.orm import Session


class TestApi:
    """Test Api class"""

    @pytest.mark.asyncio
    async def test_api_root(self, async_client: AsyncClient) -> None:
        response = await async_client.get(f'{settings.API_V1_STR}/')
        assert response.status_code == 200
        assert 'response' in response.json()

    @pytest.mark.asyncio
    async def test_create_signup(
        self,
        db_session: Session,
        async_client: AsyncClient,
        new_signup: dict
    ) -> None:

        response = await async_client.post(
            f'{settings.API_V1_STR}/signups', json=new_signup)

        # created_signup = await models.Signup.get(
        #     db_session, last_name=new_signup['last_name'], raise_404=False)

        assert response.status_code == 201
        # assert response.status_code == response
        # assert created_signup
        # assert new_signup.items() <= created_signup.items()
