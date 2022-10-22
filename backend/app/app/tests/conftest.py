from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from redis import Redis
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from app.api.deps import get_db
from app.core.config import settings
from app.db.base import Base
from app.main import app, shutdown_event, startup_event
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers

from .utils.overrides import override_get_db
from .utils.test_db import SQLALCHEMY_DATABASE_URL, TestingSessionLocal, engine

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def db() -> Generator:
    if not database_exists(SQLALCHEMY_DATABASE_URL):
        create_database(SQLALCHEMY_DATABASE_URL)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield TestingSessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient, db) -> Dict[str, str]:
    return get_superuser_token_headers(client, db)


@pytest.fixture(scope="module")
def normal_user_token_headers(
    client: TestClient, db: Session
) -> Dict[str, str]:  # pragma: no cover
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )


# Seperate redis database for the tests
@pytest.fixture
async def redis_test_database():
    await startup_event(db=1)
    yield
    await shutdown_event()


@pytest.fixture
def redis_connection():
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)


@pytest.fixture
def clear_cache(redis_connection):  # pragma: no cover
    def _clear_cache():
        redis_connection.flushdb()

    _clear_cache()
    return _clear_cache


@pytest.fixture()
def rating_obj():
    return {"stars": 5, "source_lang": "en", "target_lang": "de"}
