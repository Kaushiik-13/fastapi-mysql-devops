import time
import pytest
from httpx import Client

BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="session", autouse=True)
def wait_for_api():
    """Wait until API is ready before running tests"""
    for _ in range(20):
        try:
            with Client() as client:
                response = client.get(f"{BASE_URL}/health")
                if response.status_code == 200:
                    return
        except Exception:
            pass
        time.sleep(3)

    raise RuntimeError("API not ready")


def test_health_check():
    with Client() as client:
        response = client.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


def test_create_user():
    payload = {
        "name": "Test User",
        "email": "testuser@example.com"
    }

    with Client() as client:
        response = client.post(f"{BASE_URL}/users", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == payload["email"]
        assert "id" in data


def test_get_users():
    with Client() as client:
        response = client.get(f"{BASE_URL}/users")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
