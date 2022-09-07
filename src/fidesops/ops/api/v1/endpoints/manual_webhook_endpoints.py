import logging
from typing import Optional

from fastapi import Depends, Security
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from fidesops.ops.api import deps
from fidesops.ops.api.v1.endpoints.dataset_endpoints import _get_connection_config
from fidesops.ops.api.v1.scope_registry import (
    WEBHOOK_CREATE_OR_UPDATE,
    WEBHOOK_DELETE,
    WEBHOOK_READ,
)
from fidesops.ops.api.v1.urn_registry import ACCESS_MANUAL_WEBHOOK, V1_URL_PREFIX
from fidesops.ops.models.connectionconfig import ConnectionConfig, ConnectionType
from fidesops.ops.models.manual_webhook import AccessManualWebhook
from fidesops.ops.schemas.manual_webhook_schemas import (
    AccessManualWebhookResponse,
    AccessManualWebhooks,
)
from fidesops.ops.util.api_router import APIRouter
from fidesops.ops.util.logger import Pii
from fidesops.ops.util.oauth_util import verify_oauth_client

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Manual Webhooks"], prefix=V1_URL_PREFIX)


def get_access_manual_webhook_or_404(
    connection_config: ConnectionConfig,
) -> AccessManualWebhook:
    """Loads the single AccessManualWebhook associated with the "manual_webhook" ConnectionConfig if it exists."""
    if (
        connection_config.connection_type != ConnectionType.manual_webhook
    ):  # Sanity check
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Can't access manual webhooks for ConnectionConfigs of type '{connection_config.connection_type.value}'",  # type: ignore
        )

    if not connection_config.access_manual_webhook:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No access manual webhook exists for connection config with key '{connection_config.key}'",
        )
    return connection_config.access_manual_webhook


@router.post(
    ACCESS_MANUAL_WEBHOOK,
    status_code=HTTP_201_CREATED,
    dependencies=[Security(verify_oauth_client, scopes=[WEBHOOK_CREATE_OR_UPDATE])],
    response_model=AccessManualWebhookResponse,
)
def create_access_manual_webhook(
    connection_config: ConnectionConfig = Depends(_get_connection_config),
    *,
    db: Session = Depends(deps.get_db),
    request_body: AccessManualWebhooks,
) -> AccessManualWebhookResponse:
    """
    Create an Access Manual Webhook to describe the fields that should be manually uploaded and passed directly to the user
    """
    if connection_config.connection_type != ConnectionType.manual_webhook:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"You can only create manual webhooks for ConnectionConfigs of type '{ConnectionType.manual_webhook.value}'.",
        )

    if connection_config.access_manual_webhook:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"An Access Manual Webhook already exists for ConnectionConfig '{connection_config.key}'.",
        )

    logger.info(
        "Creating access manual webhook for connection config '%s'",
        connection_config.key,
    )

    try:
        webhook = AccessManualWebhook.create(
            db=db,
            data={
                "connection_config_id": connection_config.id,
                "fields": jsonable_encoder(request_body.fields),
            },
        )
    except IntegrityError as exc:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=Pii(str(exc)))

    return webhook


@router.patch(
    ACCESS_MANUAL_WEBHOOK,
    status_code=HTTP_200_OK,
    dependencies=[Security(verify_oauth_client, scopes=[WEBHOOK_CREATE_OR_UPDATE])],
    response_model=AccessManualWebhookResponse,
)
def patch_access_manual_webhook(
    connection_config: ConnectionConfig = Depends(_get_connection_config),
    *,
    db: Session = Depends(deps.get_db),
    request_body: AccessManualWebhooks,
) -> Optional[AccessManualWebhookResponse]:
    """
    Updates the AccessManualWebhook associated with this ConnectionConfig
    """
    access_manual_webhook: AccessManualWebhook = get_access_manual_webhook_or_404(
        connection_config
    )

    access_manual_webhook.fields = jsonable_encoder(request_body.fields)
    access_manual_webhook.save(db=db)

    logger.info(
        "Updated access manual webhook for connection config '%s'",
        connection_config.key,
    )
    return access_manual_webhook


@router.get(
    ACCESS_MANUAL_WEBHOOK,
    status_code=HTTP_200_OK,
    dependencies=[Security(verify_oauth_client, scopes=[WEBHOOK_READ])],
    response_model=AccessManualWebhookResponse,
)
def get_access_manual_webhook(
    connection_config: ConnectionConfig = Depends(_get_connection_config),
) -> Optional[AccessManualWebhookResponse]:
    """
    Gets the Access Manual Webhook associated with this ConnectionConfig.
    """
    access_manual_webhook: AccessManualWebhook = get_access_manual_webhook_or_404(
        connection_config
    )
    logger.info(
        "Retrieved access manual webhook for connection config '%s'",
        connection_config.key,
    )
    return access_manual_webhook


@router.delete(
    ACCESS_MANUAL_WEBHOOK,
    status_code=HTTP_204_NO_CONTENT,
    dependencies=[Security(verify_oauth_client, scopes=[WEBHOOK_DELETE])],
)
def delete_access_manual_webhook(
    connection_config: ConnectionConfig = Depends(_get_connection_config),
    *,
    db: Session = Depends(deps.get_db),
) -> None:
    """
    Deletes the AccessManualWebhook associated with this ConnectionConfig if it exists.
    """
    access_manual_webhook: AccessManualWebhook = get_access_manual_webhook_or_404(
        connection_config
    )

    access_manual_webhook.delete(db)
    logger.info(
        "Deleted access manual webhook for connection config '%s'",
        connection_config.key,
    )
