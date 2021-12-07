import secrets
from enum import Enum
from typing import Optional, List

from fidesops.core.config import config
from fidesops.schemas.masking.masking_configuration import (
    MaskingConfiguration,
    AesEncryptionMaskingConfiguration, HmacMaskingConfiguration,
)
from fidesops.schemas.masking.masking_secrets import MaskingSecret, SecretType
from fidesops.schemas.masking.masking_strategy_description import (
    MaskingStrategyDescription,
    MaskingStrategyConfigurationDescription,
)
from fidesops.service.masking.strategy.format_preservation import FormatPreservation
from fidesops.service.masking.strategy.masking_strategy import MaskingStrategy
from fidesops.util.cache import get_cache, get_masking_secret_cache_key
from fidesops.util.encryption.aes_gcm_encryption_scheme import encrypt
from fidesops.util.encryption.hmac_encryption_scheme import hmac_encrypt_return_bytes

AES_ENCRYPT = "aes_encrypt"


class AesEncryptionMaskingStrategy(MaskingStrategy):
    def __init__(self, configuration: AesEncryptionMaskingConfiguration):
        self.mode = configuration.mode
        self.format_preservation = configuration.format_preservation

    def mask(self, value: Optional[str]) -> str:
        if self.mode == AesEncryptionMaskingConfiguration.Mode.GCM:
            # todo- does it make sense to move into init?
            secret_key: bytes = self._get_secret_key()
            nonce: bytes = self._generate_nonce(value, secret_key)
            # todo- should the same key be used to generate the nonce AND in the aes encrypt function?
            masked: str = encrypt(value, secret_key, nonce)
            if self.format_preservation is not None:
                formatter = FormatPreservation(self.format_preservation)
                return formatter.format(masked)
            return masked
        else:
            raise ValueError(f"aes_mode {self.mode} is not supported")

    def _generate_nonce(self, value: Optional[str], key) -> bytes:
        salt: str = self._get_secret_salt()
        return hmac_encrypt_return_bytes(value, key, salt, HmacMaskingConfiguration.Algorithm.sha_256)

    @staticmethod
    def _get_secret_key() -> bytes:
        cache = get_cache()
        masking_secret_cache_key = get_masking_secret_cache_key(
            # todo- how do I get privacy request id at this level?
            privacy_request_id="",
            masking_strategy=AES_ENCRYPT,
            secret_type=SecretType.key
        )
        secret_key: bytes = cache.get(masking_secret_cache_key)
        if not secret_key:
            # todo- log warning?
            pass
        return secret_key

    @staticmethod
    def _get_secret_salt() -> str:
        cache = get_cache()
        masking_secret_cache_key = get_masking_secret_cache_key(
            # todo- how do I get privacy request id at this level?
            privacy_request_id="",
            masking_strategy=AES_ENCRYPT,
            secret_type=SecretType.salt
        )
        secret_hmac_salt: str = cache.get(masking_secret_cache_key)
        if not secret_hmac_salt:
            # todo- log warning?
            pass
        return secret_hmac_salt

    def generate_secrets(self) -> List[MaskingSecret]:
        masking_secrets = []
        # todo- maybe refactor this out into util helper that takes ({secret_type, bytes vs string format, masking strategy})
        secret_key = secrets.token_bytes(config.security.AES_ENCRYPTION_KEY_LENGTH)
        masking_secrets.append(MaskingSecret(secret=secret_key, masking_strategy=AES_ENCRYPT, secret_type=SecretType.key))
        # the salt will be used in hmac to generate the nonce for aes
        secret_salt = secrets.token_urlsafe(config.security.AES_GCM_NONCE_LENGTH)
        masking_secrets.append(MaskingSecret(secret=secret_salt, masking_strategy=AES_ENCRYPT, secret_type=SecretType.salt))
        return masking_secrets

    @staticmethod
    def get_configuration_model() -> MaskingConfiguration:
        """Used to get the configuration model to configure the strategy"""
        return AesEncryptionMaskingConfiguration

    @staticmethod
    def get_description() -> MaskingStrategyDescription:
        """Returns the description used for documentation. In particular, used by the
        documentation endpoint in masking_endpoints.list_masking_strategies"""
        return MaskingStrategyDescription(
            name=AES_ENCRYPT,
            description="Masks by encrypting the value using AES",
            configurations=[
                MaskingStrategyConfigurationDescription(
                    key="mode", description="Specifies the algorithm mode. Default is GCM if not provided."
                ),
                MaskingStrategyConfigurationDescription(
                    key="format_preservation",
                    description="Option to preserve format in masking, with a provided suffix",
                )
            ],
        )

    @staticmethod
    def data_type_supported(data_type: Optional[str]) -> bool:
        """Determines whether or not the given data type is supported by this masking strategy"""
        supported_data_types = {"string"}
        return data_type in supported_data_types
