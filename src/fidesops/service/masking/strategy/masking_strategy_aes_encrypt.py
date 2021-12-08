import secrets
from typing import Optional, List

from fidesops.core.config import config
from fidesops.schemas.masking.masking_configuration import (
    MaskingConfiguration,
    AesEncryptionMaskingConfiguration, HmacMaskingConfiguration,
)
from fidesops.schemas.masking.masking_secrets import MaskingSecretGeneration, SecretType
from fidesops.schemas.masking.masking_strategy_description import (
    MaskingStrategyDescription,
    MaskingStrategyConfigurationDescription,
)
from fidesops.service.masking.strategy.format_preservation import FormatPreservation
from fidesops.service.masking.strategy.masking_strategy import MaskingStrategy
from fidesops.util.encryption.aes_gcm_encryption_scheme import encrypt
from fidesops.util.encryption.hmac_encryption_scheme import hmac_encrypt_return_bytes
from fidesops.util.encryption.secrets_util import SecretsUtil

AES_ENCRYPT = "aes_encrypt"


class AesEncryptionMaskingStrategy(MaskingStrategy):
    def __init__(self, configuration: AesEncryptionMaskingConfiguration):
        self.mode = configuration.mode
        self.format_preservation = configuration.format_preservation

    def mask(self, value: Optional[str], privacy_request_id: Optional[str]) -> str:
        if self.mode == AesEncryptionMaskingConfiguration.Mode.GCM:
            # todo- does it make sense to move into init?
            secret_key: bytes = SecretsUtil.get_secret(privacy_request_id, AES_ENCRYPT, SecretType.key)
            nonce: bytes = self._generate_nonce(value, secret_key)
            # todo- should the same key be used to generate the nonce AND in the aes encrypt function?
            masked: str = encrypt(value, secret_key, nonce)
            if self.format_preservation is not None:
                formatter = FormatPreservation(self.format_preservation)
                return formatter.format(masked)
            return masked
        else:
            raise ValueError(f"aes_mode {self.mode} is not supported")

    @staticmethod
    def _generate_nonce(value: Optional[str], key) -> bytes:
        salt: str = SecretsUtil.get_secret(privacy_request_id, AES_ENCRYPT, SecretType.salt)
        return hmac_encrypt_return_bytes(value, key, salt, HmacMaskingConfiguration.Algorithm.sha_256)

    def generate_secrets(self) -> List[MaskingSecretGeneration]:
        masking_secrets = []
        # todo- refactor this out into util helper that takes ({secret_type, bytes vs string format, masking strategy})
        secret_key = secrets.token_bytes(config.security.AES_ENCRYPTION_KEY_LENGTH)
        masking_secrets.append(MaskingSecretGeneration(secret=secret_key, masking_strategy=AES_ENCRYPT, secret_type=SecretType.key))
        # the salt will be used in hmac to generate the nonce for aes
        secret_salt = secrets.token_urlsafe(config.security.AES_GCM_NONCE_LENGTH)
        masking_secrets.append(MaskingSecretGeneration(secret=secret_salt, masking_strategy=AES_ENCRYPT, secret_type=SecretType.salt))
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
