from fidesops.schemas.drp_privacy_request import DrpIdentity
from fidesops.schemas.redis_cache import PrivacyRequestIdentity


class DrpFidesopsIdentityMapper:
    """
    Currently, both email and phone_number identity props map 1:1 to the corresponding
    Fidesops identity props in PrivacyRequestIdentity. This may not always be the case.
    This class also allows us to implement custom logic to handle "verified" id props.
    """

    @staticmethod
    def map(drp_identity: DrpIdentity) -> PrivacyRequestIdentity:
        # Fidesops doesn't support executing privacy requests with other DRP identity props at this time.
        identity_kwargs = {"email": drp_identity.email, "phone_number": drp_identity.phone_number}
        return PrivacyRequestIdentity(**identity_kwargs)
