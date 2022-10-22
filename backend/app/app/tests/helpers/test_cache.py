import pytest

from app.api.helpers.cache import (
    get_model_version_from_cache_backend,
    get_model_version_from_db,
)
from app.cache_keys import MODEL_VERSION_KEY
from app.core.connections import redis_cache


@pytest.mark.asyncio
async def test_set_model_version_result_to_cache(redis_connection, redis_test_database):

    await get_model_version_from_cache_backend(source_lang="en", target_lang="de")
    cache_value = await redis_cache.get(MODEL_VERSION_KEY.format("en", "de"))
    assert isinstance(cache_value, bytes)
    redis_connection.flushdb()


@pytest.mark.asyncio
async def test_get_model_version_result_from_cache(
    redis_connection, redis_test_database
):

    await get_model_version_from_cache_backend(source_lang="en", target_lang="de")
    cache_value = await get_model_version_from_cache_backend(
        source_lang="en", target_lang="de"
    )

    assert isinstance(cache_value, str)
    assert cache_value == get_model_version_from_db(source_lang="en", target_lang="de")
    redis_connection.flushdb()
