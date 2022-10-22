from logging import getLogger

import aioredis

from app.cache_keys import MODEL_VERSION_KEY
from app.core.connections import redis_cache

logger = getLogger(__name__)


def get_model_version_from_db(source_lang: str, target_lang: str) -> str:
    # Dummy function
    return "1.2.3"


async def get_model_version_from_cache_backend(
    source_lang: str, target_lang: str
) -> str:
    """Get model_version from cache backend.
    In case of a cache miss the model_version is retrieved from the DB,
    and then stored in the cache.
    The cached value will get invalidated after 24 hours.

    Args:
        source_lang (str)
        target_lang (str)

    Returns:
        str: model_version
    """
    key = MODEL_VERSION_KEY.format(source_lang, target_lang)
    model_version = None
    try:
        model_version: bytes = await redis_cache.get(key=key)
    except aioredis.RedisError as err:
        logger.error("Error in reading value from the cache backend", exc_info=err)

    if not model_version:
        model_version = get_model_version_from_db(
            source_lang=source_lang, target_lang=target_lang
        )
        try:
            await redis_cache.execute(
                "set", key, model_version, "ex", twenty_four := 24 * 3600
            )
            logger.info("New model_version data is cached, %s", model_version)
        except aioredis.RedisError as err:
            logger.error("Error in writing to the cache backend", exc_info=err)
    return (
        model_version.decode("utf-8")
        if isinstance(model_version, bytes)
        else model_version
    )
