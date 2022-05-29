import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from fidesops.core.config import get_config


def test_config_from_default() -> None:
    "Test building a config from default local TOML"
    config = get_config()

    assert config.database.SERVER == "db"
    assert config.redis.HOST == "redis"
    assert config.security.APP_ENCRYPTION_KEY == "OLMkv91j8DHiDAULnK5Lxx3kSCov30b3"


@patch.dict(
    os.environ,
    {
        "FIDESOPS__CONFIG_PATH": "data/config/",
    },
    clear=True,
)
def test_config_from_path() -> None:
    """Test reading config using the FIDESOPS__CONFIG_PATH option."""
    config = get_config()
    assert config.database.SERVER == "testserver"
    assert config.redis.HOST == "testredis"
    assert config.security.APP_ENCRYPTION_KEY == "atestencryptionkeythatisvalidlen"


@patch.dict(
    os.environ,
    {
        "FIDESOPS__DATABASE__SERVER": "envserver",
        "FIDESOPS__REDIS__HOST": "envhost",
    },
    clear=True,
)
def test_config_from_env_vars() -> None:
    """Test overriding config using ENV vars."""
    config = get_config()
    assert config.database.SERVER == "envserver"
    assert config.redis.HOST == "envhost"
    # encryption key should be unchanged
    assert config.security.APP_ENCRYPTION_KEY == "OLMkv91j8DHiDAULnK5Lxx3kSCov30b3"


@pytest.mark.parametrize(
    "app_encryption_key,expected_error",
    [
        ("tooshortkey", "must be exactly 32 characters, received 11"),
        ("muchmuchmuchmuchmuchmuchmuchmuchtoolongkey", "must be exactly 32 characters, received 42"),
        ("atestencryptionkeythatisvalidlen", None),
    ],
)
def test_config_app_encryption_key_validation(app_encryption_key, expected_error) -> None:
    """Test APP_ENCRYPTION_KEY is validated to be exactly 32 characters."""
    with patch.dict(
        os.environ,
        {
            "FIDESOPS__SECURITY__APP_ENCRYPTION_KEY": app_encryption_key,
        },
        clear=True,
    ):
        if expected_error is not None:
            with pytest.raises(ValidationError) as err:
                config = get_config()
            assert expected_error in str(err.value)
        else:
            config = get_config()
            assert config.security.APP_ENCRYPTION_KEY == app_encryption_key

