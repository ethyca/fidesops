from typing import TypeVar, Optional

from fidesops.schemas.masking.masking_secrets import SecretType
from fidesops.util.cache import get_masking_secret_cache_key, get_cache

T = TypeVar("T")


class SecretsUtil:
    @staticmethod
    def get_secret(
        privacy_request_id: Optional[str],
        masking_strategy: str,
        secret_type: SecretType,
    ) -> T:
        cache = get_cache()
        masking_secret_cache_key: str = get_masking_secret_cache_key(
            privacy_request_id=privacy_request_id,
            masking_strategy=masking_strategy,
            secret_type=secret_type,
        )
        secret: T = cache.get(masking_secret_cache_key)
        if not secret:
            # todo- log warning?
            pass
        return secret
