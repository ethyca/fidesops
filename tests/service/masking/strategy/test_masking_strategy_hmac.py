from fidesops.schemas.masking.masking_secrets import MaskingSecretCache, SecretType
from fidesops.service.masking.strategy.masking_strategy_hmac import HmacMaskingStrategy, HMAC
from fidesops.schemas.masking.masking_configuration import HmacMaskingConfiguration
from ....test_helpers.cache_secrets_helper import clear_cache_secrets, cache_secret

request_id = "1345134"


def test_hmac_sha_256():
    configuration = HmacMaskingConfiguration(
        algorithm="SHA-256"
    )
    masker = HmacMaskingStrategy(configuration)
    expected = "df1e66dc2262ae3336f36294811f795b075900287e0a1add7974eacea8a52970"

    secret_key = MaskingSecretCache(
        secret="test_key", masking_strategy=HMAC, secret_type=SecretType.key
    )
    cache_secret(secret_key, request_id)
    secret_salt = MaskingSecretCache(
        secret="test_salt", masking_strategy=HMAC, secret_type=SecretType.salt
    )
    cache_secret(secret_salt, request_id)

    masked = masker.mask("my_data", request_id)
    assert expected == masked
    clear_cache_secrets(request_id)


def test_mask_sha512():
    configuration = HmacMaskingConfiguration(algorithm="SHA-512")
    masker = HmacMaskingStrategy(configuration)
    expected = (
        "2d6805864fdee15f4c6a0e809fada0db3043d0e219383b8395b1dae797db680bb0446bcddf71f633f3a6e8970a6952"
        "7b47f304563f4f061d01712cfe34fc449e"
    )

    secret_key = MaskingSecretCache(
        secret="test_key", masking_strategy=HMAC, secret_type=SecretType.key
    )
    cache_secret(secret_key, request_id)
    secret_salt = MaskingSecretCache(
        secret="test_salt", masking_strategy=HMAC, secret_type=SecretType.salt
    )
    cache_secret(secret_salt, request_id)

    masked = masker.mask("my_data", request_id)
    assert expected == masked
    clear_cache_secrets(request_id)


def test_mask_sha256_default():
    configuration = HmacMaskingConfiguration()
    masker = HmacMaskingStrategy(configuration)
    expected = "df1e66dc2262ae3336f36294811f795b075900287e0a1add7974eacea8a52970"

    secret_key = MaskingSecretCache(
        secret="test_key", masking_strategy=HMAC, secret_type=SecretType.key
    )
    cache_secret(secret_key, request_id)
    secret_salt = MaskingSecretCache(
        secret="test_salt", masking_strategy=HMAC, secret_type=SecretType.salt
    )
    cache_secret(secret_salt, request_id)

    masked = masker.mask("my_data", request_id)
    assert expected == masked
    clear_cache_secrets(request_id)


def test_mask_arguments_null():
    configuration = HmacMaskingConfiguration()
    masker = HmacMaskingStrategy(configuration)
    expected = None

    secret_key = MaskingSecretCache(
        secret="test_key", masking_strategy=HMAC, secret_type=SecretType.key
    )
    cache_secret(secret_key, request_id)
    secret_salt = MaskingSecretCache(
        secret="test_salt", masking_strategy=HMAC, secret_type=SecretType.salt
    )
    cache_secret(secret_salt, request_id)

    masked = masker.mask(None, request_id)
    assert expected == masked
    clear_cache_secrets(request_id)
