from typing import List, Set

from fidesops.schemas.masking.masking_secrets import MaskingSecretCache, SecretType, MaskingSecretMeta
from fidesops.service.masking.strategy.masking_strategy_hmac import HMAC
from fidesops.util.encryption.secrets_util import SecretsUtil
from ...test_helpers.cache_secrets_helper import cache_secret, clear_cache_secrets

request_id = "12345"


def test_get_secret_from_cache() -> None:
    # build masking secret meta for HMAC key
    masking_meta_key = MaskingSecretMeta[str](
            masking_strategy=HMAC,
            secret_type=SecretType.key,
            generate_secret=SecretsUtil.generate_secret_string,
        )

    # cache secrets for HMAC
    secret_key = MaskingSecretCache[str](
        secret="test_key", masking_strategy=HMAC, secret_type=SecretType.key
    )
    cache_secret(secret_key, request_id)

    result: str = SecretsUtil.get_or_generate_secret(request_id, masking_meta_key)
    assert result == "test_key"
    clear_cache_secrets(request_id)

def test_generate_secret() -> None:
    # build masking secret meta for HMAC key
    masking_meta_key = MaskingSecretMeta[str](
        masking_strategy=HMAC,
        secret_type=SecretType.key,
        generate_secret=SecretsUtil.generate_secret_string,
    )

    result: str = SecretsUtil.get_or_generate_secret(None, masking_meta_key)
    assert result

def test_build_masking_secrets_for_cache() -> None:
    # build masking secret meta for all HMAC secrets
    masking_meta: Set[MaskingSecretMeta] = set()
    masking_meta.add(
        MaskingSecretMeta[str](
            masking_strategy=HMAC,
            secret_type=SecretType.key,
            generate_secret=SecretsUtil.generate_secret_string,
        )
    )
    masking_meta.add(
        MaskingSecretMeta[str](
            masking_strategy=HMAC,
            secret_type=SecretType.salt,
            generate_secret=SecretsUtil.generate_secret_string,
        )
    )
    result: List[MaskingSecretCache] = SecretsUtil.build_masking_secrets_for_cache(masking_meta)
    assert len(result) == 2
