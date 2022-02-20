import pytest
from main import app


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    return TestClient(app)
