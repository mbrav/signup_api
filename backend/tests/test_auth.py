# from typing import Dict

# import pytest
# from app.config import settings
# from httpx import AsyncClient


# class TestAuth:
#     """Test auth"""

#     def test_service(self, authservice):
#         assert authservice

#     @pytest.mark.asyncio
#     async def test_registration(
#         self,
#         async_client: AsyncClient,
#         new_login: dict
#     ) -> dict:

#         response = await async_client.post(
#             f'{settings.API_V1_STR}/auth/register', json=new_login)
#         json_res = response.json()

#         assert response.status_code == 201
#         assert json_res['username'] == new_login['username']
#         return new_login

#     @pytest.mark.asyncio
#     async def test_token_get(
#         self,
#         async_client: AsyncClient,
#         new_login: dict
#     ) -> dict:
#         test_login = await self.test_registration(async_client, new_login)

#         response = await async_client.post(
#             f'{settings.API_V1_STR}/auth/token', data=test_login)

#         json_res = response.json()
#         assert json_res['access_token']
#         assert json_res['token_type'] == 'bearer'
#         assert response.status_code == 200
#         return json_res

#     @pytest.mark.asyncio
#     async def test_token_use(
#         self,
#         async_client: AsyncClient,
#         new_login: Dict
#     ) -> None:

#         token = await self.test_token_get(async_client, new_login)

#         headers = {
#             'Authorization': f'{token["token_type"]} {token["access_token"]}'
#         }

#         response = await async_client.get(
#             f'{settings.API_V1_STR}/users/me', headers=headers)

#         json_res = response.json()
#         assert json_res['username'] == new_login['username']
#         assert response.status_code != 405
#         assert response.status_code == 200
