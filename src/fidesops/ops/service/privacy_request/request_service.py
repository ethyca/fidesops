import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from sqlalchemy.orm import Session

from fidesops.ops.core.config import config
from fidesops.ops.models.manual_webhook import AccessManualWebhook
from fidesops.ops.models.policy import ActionType, Policy
from fidesops.ops.models.privacy_request import PrivacyRequest, PrivacyRequestStatus
from fidesops.ops.schemas.drp_privacy_request import DrpPrivacyRequestCreate
from fidesops.ops.schemas.masking.masking_secrets import MaskingSecretCache
from fidesops.ops.schemas.redis_cache import Identity
from fidesops.ops.service.masking.strategy.masking_strategy import MaskingStrategy
from fidesops.ops.service.privacy_request.request_runner_service import (
    queue_privacy_request,
)

logger = logging.getLogger(__name__)


def build_required_privacy_request_kwargs(
    requested_at: Optional[datetime], policy_id: str
) -> Dict[str, Any]:
    """Build kwargs required for creating privacy request

    If identity verification is on, the request will have an initial status of
    "identity_unverified", otherwise, it will have an initial status of "pending".
    """
    status = (
        PrivacyRequestStatus.identity_unverified
        if config.execution.subject_identity_verification_required
        else PrivacyRequestStatus.pending
    )
    return {
        "requested_at": requested_at,
        "policy_id": policy_id,
        "status": status,
    }


def cache_data(
    privacy_request: PrivacyRequest,
    policy: Policy,
    identity: Identity,
    encryption_key: Optional[str],
    drp_request_body: Optional[DrpPrivacyRequestCreate],
) -> None:
    """Cache privacy request data"""
    # Store identity and encryption key in the cache
    logger.info("Caching identity for privacy request %s", privacy_request.id)
    privacy_request.cache_identity(identity)
    privacy_request.cache_encryption(encryption_key)  # handles None already

    # Store masking secrets in the cache
    logger.info("Caching masking secrets for privacy request %s", privacy_request.id)
    erasure_rules = policy.get_rules_for_action(action_type=ActionType.erasure)
    unique_masking_strategies_by_name: Set[str] = set()
    for rule in erasure_rules:
        strategy_name: str = rule.masking_strategy["strategy"]  # type: ignore
        configuration = rule.masking_strategy["configuration"]  # type: ignore
        if strategy_name in unique_masking_strategies_by_name:
            continue
        unique_masking_strategies_by_name.add(strategy_name)
        masking_strategy = MaskingStrategy.get_strategy(strategy_name, configuration)
        if masking_strategy.secrets_required():
            masking_secrets: List[
                MaskingSecretCache
            ] = masking_strategy.generate_secrets_for_cache()
            for masking_secret in masking_secrets:
                privacy_request.cache_masking_secret(masking_secret)
    if drp_request_body:
        privacy_request.cache_drp_request_body(drp_request_body)


def queue_requires_input_requests(db: Session) -> None:
    """
    Queue privacy requests with request status "requires_input" if they are no longer blocked by
    webhooks.
    """
    if not AccessManualWebhook.get_enabled(db):
        for pr in PrivacyRequest.filter(
            db=db,
            conditions=(PrivacyRequest.status == PrivacyRequestStatus.requires_input),
        ):
            logger.info(
                "Queuing privacy request '%s with '%s' status now that manual inputs are no longer required.",
                pr.id,
                pr.status.value,
            )
            pr.status = PrivacyRequestStatus.in_processing
            pr.save(db=db)
            queue_privacy_request(
                privacy_request_id=pr.id,
            )
