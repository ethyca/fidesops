import logging
from fastapi import APIRouter, Security

from fidesops.api.v1.scope_registry import ENCRYPTION_EXEC
from fidesops.api.v1.urn_registry import (
    ENCRYPT_AES,
    ENCRYPTION_KEY,
    DECRYPT_AES,
    V1_URL_PREFIX,
)
from fidesops.core.config import config
from fidesops.schemas.encryption_request import (
    AesEncryptionRequest,
    AesEncryptionResponse,
    AesDecryptionResponse,
    AesDecryptionRequest,
)
from fidesops.util import cryptographic_util
from fidesops.util.encryption.aes_gcm_encryption_scheme import (
    encrypt as aes_gcm_encrypt,
)
from fidesops.util.encryption.aes_gcm_encryption_scheme import (
    decrypt as aes_gcm_decrypt,
)
from fidesops.util.oauth_util import verify_oauth_client

router = APIRouter(tags=["Encryption"], prefix=V1_URL_PREFIX)


logger = logging.getLogger(__name__)


@router.get(
    ENCRYPTION_KEY,
    dependencies=[Security(verify_oauth_client, scopes=[ENCRYPTION_EXEC])],
    response_model=str,
)
def get_encryption_key() -> str:
    logger.info("Generating encryption key")
    return cryptographic_util.generate_secure_random_string(
        config.security.AES_ENCRYPTION_KEY_LENGTH
    )


@router.put(
    ENCRYPT_AES,
    dependencies=[Security(verify_oauth_client, scopes=[ENCRYPTION_EXEC])],
    response_model=AesEncryptionResponse,
)
def aes_encrypt(encryption_request: AesEncryptionRequest) -> AesEncryptionResponse:
    logger.info("Starting AES Encryption")
    nonce = cryptographic_util.generate_secure_random_string(
        config.security.AES_GCM_NONCE_LENGTH
    )
    encrypted_value = aes_gcm_encrypt(
        encryption_request.value,
        encryption_request.key,
        nonce.encode(config.security.ENCODING),
    )
    return AesEncryptionResponse(encrypted_value=encrypted_value, nonce=nonce)


@router.put(
    DECRYPT_AES,
    dependencies=[Security(verify_oauth_client, scopes=[ENCRYPTION_EXEC])],
    response_model=AesDecryptionResponse,
)
def aes_decrypt(decryption_request: AesDecryptionRequest) -> AesDecryptionResponse:
    logger.info("Starting AES Decryption")
    decrypted_value = aes_gcm_decrypt(
        decryption_request.value,
        decryption_request.key.encode(config.security.ENCODING),
        decryption_request.nonce.encode(config.security.ENCODING),
    )
    return AesDecryptionResponse(decrypted_value=decrypted_value)
