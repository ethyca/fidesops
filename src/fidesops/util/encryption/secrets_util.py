import logging
import secrets
from typing import TypeVar, Optional, Set, List

from fidesops.schemas.masking.masking_secrets import (
    MaskingSecretMeta,
    MaskingSecretCache,
)
from fidesops.util.cache import get_masking_secret_cache_key, get_cache

T = TypeVar("T")
logger = logging.getLogger(__name__)


class SecretsUtil:
    @staticmethod
    def get_or_generate_secret(
        privacy_request_id: Optional[str], masking_secret_meta: MaskingSecretMeta[T]
    ) -> T:
        if privacy_request_id is not None:
            secret: T = SecretsUtil._get_secret_from_cache(
                privacy_request_id, masking_secret_meta
            )
            if not secret:
                logger.warning(
                    f"Secret type {masking_secret_meta.secret_type} expected from cache but was not present for masking strategy {masking_secret_meta.masking_strategy}"
                )
            return secret
        else:
            # expected for standalone masking service
            return masking_secret_meta.generate_secret(
                masking_secret_meta.secret_length
            )

    @staticmethod
    def _get_secret_from_cache(
        privacy_request_id: str, masking_secret_meta: MaskingSecretMeta[T]
    ) -> T:
        cache = get_cache()
        masking_secret_cache_key: str = get_masking_secret_cache_key(
            privacy_request_id=privacy_request_id,
            masking_strategy=masking_secret_meta.masking_strategy,
            secret_type=masking_secret_meta.secret_type,
        )
        return cache.get(masking_secret_cache_key)

    @staticmethod
    def generate_secret_string(length: int) -> str:
        return secrets.token_urlsafe(length)

    @staticmethod
    def generate_secret_bytes(length: int) -> bytes:
        return secrets.token_bytes(length)

    @staticmethod
    def build_masking_secrets_for_cache(
        masking_secret_meta: Set[MaskingSecretMeta[T]],
    ) -> List[MaskingSecretCache[T]]:
        masking_secrets = []
        for meta in masking_secret_meta:
            secret: T = meta.generate_secret(meta.secret_length)
            masking_secrets.append(
                MaskingSecretCache[T](
                    secret=secret,
                    masking_strategy=meta.masking_strategy,
                    secret_type=meta.secret_type,
                )
            )
        return masking_secrets
