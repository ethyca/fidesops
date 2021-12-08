import secrets
from typing import Optional, List

from fidesops.core.config import config
from fidesops.schemas.masking.masking_configuration import (
    MaskingConfiguration,
    HmacMaskingConfiguration,
)
from fidesops.schemas.masking.masking_secrets import MaskingSecretGeneration, SecretType
from fidesops.schemas.masking.masking_strategy_description import (
    MaskingStrategyDescription,
    MaskingStrategyConfigurationDescription,
)
from fidesops.service.masking.strategy.format_preservation import FormatPreservation
from fidesops.service.masking.strategy.masking_strategy import MaskingStrategy
from fidesops.util.encryption.hmac_encryption_scheme import hmac_encrypt_return_str
from fidesops.util.encryption.secrets_util import SecretsUtil

HMAC = "hmac"


class HmacMaskingStrategy(MaskingStrategy):
    """
    Masks a value by generating a hash using a hash algorithm and a required secret key.  One of the differences
    between this and the HashMaskingStrategy is the required secret key."""

    def __init__(
        self,
        configuration: HmacMaskingConfiguration,
    ):
        self.algorithm = configuration.algorithm
        self.format_preservation = configuration.format_preservation

    def mask(self, value: Optional[str]) -> Optional[str]:
        """
        Returns a hash using the hmac algorithm, generating a hash of the supplied value and the secret hmac_key.
        Returns None if the provided value is None.
        """
        if value is None:
            return None
        key = SecretsUtil.get_secret(privacy_request_id, HMAC, SecretType.key)
        salt = SecretsUtil.get_secret(privacy_request_id, HMAC, SecretType.salt)
        masked: str = hmac_encrypt_return_str(value, key, salt, self.algorithm)
        if self.format_preservation is not None:
            formatter = FormatPreservation(self.format_preservation)
            return formatter.format(masked)
        return masked

    def generate_secrets(self) -> List[MaskingSecretGeneration]:
        secret_types = {SecretType.key, SecretType.salt}
        masking_secrets = []
        for secret_type in secret_types:
            secret = secrets.token_urlsafe(config.security.DEFAULT_ENCRYPTION_BYTE_LENGTH)
            masking_secrets.append(MaskingSecretGeneration(secret=secret, masking_strategy=HMAC, secret_type=secret_type))
        return masking_secrets

    @staticmethod
    def get_configuration_model() -> MaskingConfiguration:
        return HmacMaskingConfiguration

    @staticmethod
    def get_description() -> MaskingStrategyDescription:
        return MaskingStrategyDescription(
            name=HMAC,
            description="Masks the input value by using the HMAC algorithm along with a hashed version of the data "
            "and a secret key.",
            configurations=[
                MaskingStrategyConfigurationDescription(
                    key="algorithm",
                    description="Specifies the hashing algorithm to be used. Can be SHA-256 or "
                    "SHA-512. If not provided, default is SHA-256",
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

