from typing import Optional, List, Set

from fidesops.schemas.masking.masking_configuration import (
    MaskingConfiguration,
    AesEncryptionMaskingConfiguration,
    HmacMaskingConfiguration,
)
from fidesops.schemas.masking.masking_secrets import (
    MaskingSecretCache,
    SecretType,
    MaskingSecretMeta,
    SecretDataType,
)
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
            masking_meta: Set[MaskingSecretMeta] = self._build_masking_secret_meta()
            key: bytes = SecretsUtil.get_or_generate_secret(
                privacy_request_id,
                [meta for meta in masking_meta if meta.secret_type == SecretType.key][
                    0
                ],
            )
            key_hmac: str = SecretsUtil.get_or_generate_secret(
                privacy_request_id,
                [
                    meta
                    for meta in masking_meta
                    if meta.secret_type == SecretType.key_hmac
                ][0],
            )
            nonce: bytes = self._generate_nonce(
                value, key_hmac, privacy_request_id, masking_meta
            )
            masked: str = encrypt(value, key, nonce)
            if self.format_preservation is not None:
                formatter = FormatPreservation(self.format_preservation)
                return formatter.format(masked)
            return masked
        else:
            raise ValueError(f"aes_mode {self.mode} is not supported")

    @staticmethod
    def secrets_required() -> bool:
        return True

    def generate_secrets_for_cache(self) -> List[MaskingSecretCache]:
        masking_meta: Set[MaskingSecretMeta] = self._build_masking_secret_meta()
        return SecretsUtil.build_masking_secrets_for_cache(masking_meta)

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
                    key="mode",
                    description="Specifies the algorithm mode. Default is GCM if not provided.",
                ),
                MaskingStrategyConfigurationDescription(
                    key="format_preservation",
                    description="Option to preserve format in masking, with a provided suffix",
                ),
            ],
        )

    @staticmethod
    def data_type_supported(data_type: Optional[str]) -> bool:
        """Determines whether or not the given data type is supported by this masking strategy"""
        supported_data_types = {"string"}
        return data_type in supported_data_types

    @staticmethod
    def _generate_nonce(
        value: Optional[str],
        key: str,
        privacy_request_id: Optional[str],
        masking_meta: Set[MaskingSecretMeta],
    ) -> bytes:
        salt: str = SecretsUtil.get_or_generate_secret(
            privacy_request_id,
            [meta for meta in masking_meta if meta.secret_type == SecretType.salt_hmac][
                0
            ],
        )
        # fixme: replicate what Vault does - remove lower bytes
        return hmac_encrypt_return_bytes(
            value, key, salt, HmacMaskingConfiguration.Algorithm.sha_256
        )

    @staticmethod
    def _build_masking_secret_meta() -> Set[MaskingSecretMeta]:
        masking_meta: Set[MaskingSecretMeta] = set()
        masking_meta.add(
            MaskingSecretMeta[bytes](
                masking_strategy=AES_ENCRYPT,
                secret_type=SecretType.key,
                generate_secret=SecretsUtil.generate_secret_bytes
            )
        )
        masking_meta.add(
            MaskingSecretMeta[str](
                masking_strategy=AES_ENCRYPT,
                secret_type=SecretType.key_hmac,
                generate_secret=SecretsUtil.generate_secret_string
            )
        )
        masking_meta.add(
            MaskingSecretMeta[str](
                masking_strategy=AES_ENCRYPT,
                secret_type=SecretType.salt_hmac,
                generate_secret=SecretsUtil.generate_secret_string
            )
        )
        return masking_meta
