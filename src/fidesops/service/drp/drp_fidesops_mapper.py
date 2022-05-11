from typing import Dict

from fidesops.models.privacy_request import PrivacyRequestStatus
from fidesops.schemas.drp_privacy_request import DrpIdentity
from fidesops.schemas.privacy_request import PrivacyRequestDRPStatus
from fidesops.schemas.redis_cache import PrivacyRequestIdentity


class DrpFidesopsMapper:
    """
    Map DRP objects/enums to Fidesops
    """

    @staticmethod
    def map_identity(drp_identity: DrpIdentity) -> PrivacyRequestIdentity:
        """
        Currently, both email and phone_number identity props map 1:1 to the corresponding
        Fidesops identity props in PrivacyRequestIdentity. This may not always be the case.
        This class also allows us to implement custom logic to handle "verified" id props.
        """
        identity_kwargs = {
            "email": drp_identity.email,
            "phone_number": drp_identity.phone_number,
        }
        return PrivacyRequestIdentity(**identity_kwargs)

    @staticmethod
    def map_status(
        status: PrivacyRequestStatus,
    ) -> PrivacyRequestDRPStatus:
        PRIVACY_REQUEST_STATUS_TO_DRP_MAPPING: Dict[
            PrivacyRequestStatus, PrivacyRequestDRPStatus
        ] = {
            PrivacyRequestStatus.pending: PrivacyRequestDRPStatus.open,
            PrivacyRequestStatus.approved: PrivacyRequestDRPStatus.in_progress,
            PrivacyRequestStatus.denied: PrivacyRequestDRPStatus.denied,
            PrivacyRequestStatus.in_processing: PrivacyRequestDRPStatus.in_progress,
            PrivacyRequestStatus.complete: PrivacyRequestDRPStatus.fulfilled,
            PrivacyRequestStatus.paused: PrivacyRequestDRPStatus.in_progress,
            PrivacyRequestStatus.error: PrivacyRequestDRPStatus.expired,
        }
        try:
            return PRIVACY_REQUEST_STATUS_TO_DRP_MAPPING[status]
        except KeyError:
            raise ValueError(f"Request has invalid DRP request status: {status.value}")
