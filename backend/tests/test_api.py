import pytest


class TestApi:
    def test_api_root(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert 'response' in response.json()
