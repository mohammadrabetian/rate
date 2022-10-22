from fastapi.testclient import TestClient

from app.core.config import settings


def test_security_not_authorized(client: TestClient, rating_obj: dict) -> None:
    r = client.post(f"{settings.API_V1_STR}/rating/", json=rating_obj)
    assert r.status_code == 401
    assert r.json() == {"detail": "Not authenticated"}
