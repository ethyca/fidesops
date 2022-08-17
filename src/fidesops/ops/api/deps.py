from typing import Generator

from fideslib.db.session import get_db_engine, get_db_session

from fidesops.ops.common_exceptions import FunctionalityNotConfigured
from fidesops.ops.core.config import config
from fidesops.ops.util.cache import get_cache as get_redis_connection

_engine = None


def get_db() -> Generator:
    """Return our database session"""
    if not config.database.enabled:
        raise FunctionalityNotConfigured(
            "Application database required, but it is currently disabled! Please update your application configuration to enable integration with an application database."
        )
    return _get_session()


def get_db_for_health_check() -> Generator:
    """Gets a database session regardless of whether the application db is disabled, for a health check."""
    return _get_session()


def _get_session() -> Generator:
    """Gets a database session"""
    try:
        global _engine  # pylint: disable=W0603
        if not _engine:
            _engine = get_db_engine(config=config)
        SessionLocal = get_db_session(config, engine=_engine)
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_cache() -> Generator:
    """Return a connection to our redis cache"""
    if not config.redis.enabled:
        raise FunctionalityNotConfigured(
            "Application redis cache required, but it is currently disabled! Please update your application configuration to enable integration with a redis cache."
        )
    yield get_redis_connection()
