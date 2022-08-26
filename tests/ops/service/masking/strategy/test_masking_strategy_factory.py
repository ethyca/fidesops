import pytest

from fidesops.ops.common_exceptions import NoSuchStrategyException
from fidesops.ops.service.masking.strategy.masking_strategy_aes_encrypt import (
    AesEncryptionMaskingStrategy,
)
from fidesops.ops.service.masking.strategy.masking_strategy_hash import (
    HashMaskingStrategy,
)
from fidesops.ops.service.masking.strategy.masking_strategy_string_rewrite import (
    StringRewriteMaskingStrategy,
)
from fidesops.ops.service.strategy_factory import strategy


def test_get_strategy_hash():
    hash_strategy = strategy("hash", {})
    assert isinstance(hash_strategy, HashMaskingStrategy)


def test_get_strategy_rewrite():
    config = {"rewrite_value": "val"}
    rewrite_strategy = strategy("string_rewrite", config)
    assert isinstance(rewrite_strategy, StringRewriteMaskingStrategy)


def test_get_strategy_aes_encrypt():
    config = {"mode": "GCM", "key": "keycard", "nonce": "none"}
    aes_encrypt_strategy = strategy("aes_encrypt", config)
    assert isinstance(aes_encrypt_strategy, AesEncryptionMaskingStrategy)


def test_get_strategy_invalid():
    with pytest.raises(NoSuchStrategyException):
        strategy("invalid", {})
