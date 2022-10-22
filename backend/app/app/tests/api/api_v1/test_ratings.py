import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.helpers.cache import get_model_version_from_db
from app.core.config import settings
from app.tests.utils.rating import create_random_rating


def test_create_rating(
    client: TestClient, superuser_token_headers: dict, db: Session, rating_obj: dict
) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/rating/",
        headers=superuser_token_headers,
        json=rating_obj,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["stars"] == rating_obj["stars"]
    assert content["model_version"] == get_model_version_from_db(
        source_lang=rating_obj["source_lang"], target_lang=rating_obj["target_lang"]
    )
    assert "id" in content
    assert "user_id" in content


def test_read_rating(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    rating = create_random_rating(db)
    response = client.get(
        f"{settings.API_V1_STR}/rating/{rating.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["stars"] == rating.stars
    assert content["id"] == str(rating.id)
    assert content["user_id"] == str(rating.user_id)
    assert content["model_version"] == rating.model_version
