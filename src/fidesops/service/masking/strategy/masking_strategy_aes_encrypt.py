import secrets
from typing import Optional, List

from fidesops.schemas.masking.masking_configuration import (
    MaskingConfiguration,
    AesEncryptionMaskingConfiguration, HmacMaskingConfiguration,
)
from fidesops.schemas.masking.masking_secrets import MaskingSecret
from fidesops.schemas.masking.masking_strategy_description import (
    MaskingStrategyDescription,
    MaskingStrategyConfigurationDescription,
)
from fidesops.service.masking.strategy.format_preservation import FormatPreservation
from fidesops.service.masking.strategy.masking_strategy import MaskingStrategy
from fidesops.service.masking.strategy.masking_strategy_factory import get_strategy
from fidesops.util.cache import get_cache, get_masking_secret_cache_key
from fidesops.util.encryption.aes_gcm_encryption_scheme import encrypt


AES_ENCRYPT = "aes_encrypt"
secret_types = {"key"}


class AesEncryptionMaskingStrategy(MaskingStrategy):
    def __init__(self, configuration: AesEncryptionMaskingConfiguration):
        self.mode = configuration.mode
        self.format_preservation = configuration.format_preservation

    def mask(self, value: Optional[str]) -> str:
        if self.mode == AesEncryptionMaskingConfiguration.Mode.GCM:
            secret_key: bytes = self._get_secret_key()
            nonce = self._generate_nonce(value)
            masked: str = encrypt(value, secret_key, nonce)
            if self.format_preservation is not None:
                formatter = FormatPreservation(self.format_preservation)
                return formatter.format(masked)
            return masked
        else:
            raise ValueError(f"aes_mode {self.mode} is not supported")

    @staticmethod
    def _generate_nonce(value: Optional[str]) -> bytes:
        hmac_strategy: MaskingStrategy = get_strategy(
            AES_ENCRYPT, {}
        )
        # todo- return bytes instead of str
        return hmac_strategy.mask(value)

    @staticmethod
    def _get_secret_key() -> bytes:
        cache = get_cache()
        masking_secret_cache_key = get_masking_secret_cache_key(
            # todo- how do I get privacy request id at this level?
            privacy_request_id="",
            masking_strategy=AES_ENCRYPT,
            secret_type="key"
        )
        secret_key: bytes = cache.get(masking_secret_cache_key)
        if not secret_key:
            # todo- log warning?
            pass
        return secret_key

    def generate_secrets(self) -> List[MaskingSecret]:
        masking_secrets = []
        for secret_type in secret_types:
            secret = secrets.token_bytes()  #  todo- add length
            masking_secrets.append(MaskingSecret(secret=secret, masking_strategy=AES_ENCRYPT, secret_type=secret_type))
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
