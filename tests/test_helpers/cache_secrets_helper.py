from fidesops.schemas.masking.masking_secrets import MaskingSecretGeneration
from fidesops.util.cache import FidesopsRedis, get_cache, get_masking_secret_cache_key


def cache_secret(secret: MaskingSecretGeneration, request_id: str) -> None:
    cache: FidesopsRedis = get_cache()
    cache.set_with_autoexpire(
        get_masking_secret_cache_key(
            request_id,
            masking_strategy=secret.masking_strategy,
            secret_type=secret.secret_type,
        ),
        secret.secret,
    )


def clear_cache_secrets(request_id: str) -> None:
    cache: FidesopsRedis = get_cache()
    cache.delete_keys_by_prefix(f"id-{request_id}-masking-secret)")
