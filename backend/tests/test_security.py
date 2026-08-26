import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.security.auth import get_current_user

# Temporarily remove override to test actual auth
@pytest.fixture(autouse=True)
def remove_auth_override():
    app.dependency_overrides.pop(get_current_user, None)
    yield
    # Restore override for other tests if needed
    app.dependency_overrides[get_current_user] = lambda: "test_user"

def test_unauthenticated_request_rejected():
    with TestClient(app) as client:
        response = client.get("/api/v1/scans/")
        assert response.status_code == 403

def test_authenticated_request_accepted():
    with TestClient(app) as client:
        # Use default token from settings
        headers = {"Authorization": "Bearer demo-token-123"}
        response = client.get("/api/v1/scans/", headers=headers)
        # Note: it might return 200 or something else, but not 403 or 401
        assert response.status_code != 403
        assert response.status_code != 401

def test_invalid_token_rejected():
    with TestClient(app) as client:
        headers = {"Authorization": "Bearer wrong-token"}
        response = client.get("/api/v1/scans/", headers=headers)
        assert response.status_code == 401
