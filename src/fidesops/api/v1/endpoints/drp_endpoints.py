import logging
from typing import Dict, Any, Optional

import jwt
from fastapi import HTTPException, Depends, APIRouter, Request
from requests import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_424_FAILED_DEPENDENCY, HTTP_200_OK, \
    HTTP_400_BAD_REQUEST

from fidesops import common_exceptions
from fidesops.api import deps
from fidesops.api.v1 import urn_registry as urls
from fidesops.core.config import config
from fidesops.models.policy import Policy
from fidesops.models.privacy_request import PrivacyRequest
from fidesops.schemas.drp_privacy_request import DrpPrivacyRequestCreate, DrpIdentity
from fidesops.schemas.redis_cache import PrivacyRequestIdentity
from fidesops.service.drp.drp_fidesops_identity_mapper_service import DrpFidesopsIdentityMapper
from fidesops.service.privacy_request.request_runner_service import PrivacyRequestRunner
from fidesops.service.privacy_request.request_service import build_required_privacy_request_kwargs, cache_data
from fidesops.util.cache import FidesopsRedis

logger = logging.getLogger(__name__)
router = APIRouter(tags=["DRP"], prefix=urls.V1_URL_PREFIX)
EMBEDDED_EXECUTION_LOG_LIMIT = 50


@router.post(
    urls.DRP_EXERCISE,
    status_code=HTTP_200_OK,
    response_model=Dict[str, Any],  # fixme: replace with DrpPrivacyRequestStatus once other PR is merged
)
def create_drp_privacy_request(
        *,
        request: Request,
        cache: FidesopsRedis = Depends(deps.get_cache),
        db: Session = Depends(deps.get_db),
        data: DrpPrivacyRequestCreate,
) -> Dict[str, Any]:
    """
    Given a drp privacy request body, create and execute
    a corresponding Fidesops PrivacyRequest
    """

    jwt_key: str = config.security.DRP_JWT_SECRET
    if jwt_key is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="JWT key must be provided",
        )

    logger.info(f"Finding policy with drp action '{data.exercise}'")
    policy: Optional[Policy] = Policy.get_by(
        db=db,
        field="drp_action",
        value=data.exercise[0],
    )

    if not policy:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No policy found with drp action '{data.exercise}'.",
        )

    privacy_request_kwargs: Dict[str, Any] = build_required_privacy_request_kwargs(None, policy.id)

    try:
        privacy_request: PrivacyRequest = PrivacyRequest.create(db=db, data=privacy_request_kwargs)

        decrypted_identity: DrpIdentity = jwt.decode(data.identity, jwt_key, algorithms="HS256")

        mapped_identity: PrivacyRequestIdentity = DrpFidesopsIdentityMapper.map(drp_identity=decrypted_identity)

        cache_data(privacy_request, policy, mapped_identity, None, data)

        PrivacyRequestRunner(
            cache=cache,
            privacy_request=privacy_request,
        ).submit()

        return {
            "request_id": privacy_request.id,
            "received_at": privacy_request.requested_at,
            "status": "test"  # fixme- replace once other pr is merged
        }

    except common_exceptions.RedisConnectionError as exc:
        logger.error("RedisConnectionError: %s", exc)
        # Thrown when cache.ping() fails on cache connection retrieval
        raise HTTPException(
            status_code=HTTP_424_FAILED_DEPENDENCY,
            detail=exc.args[0],
        )
    except Exception as exc:
        logger.error("Exception: %s", exc)
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="DRP privacy request could not be exercised",
        )
