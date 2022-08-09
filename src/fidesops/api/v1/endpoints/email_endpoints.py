import logging
from typing import List, Optional

from fastapi import Security, Depends
from fastapi_pagination import Page, Params, paginate
from fastapi_pagination.bases import AbstractPage
from fideslib.exceptions import KeyOrNameAlreadyExists
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_400_BAD_REQUEST, \
    HTTP_204_NO_CONTENT

from fidesops.api import deps
from fidesops.api.v1.scope_registry import EMAIL_CREATE_OR_UPDATE, EMAIL_READ, EMAIL_DELETE
from fidesops.api.v1.urn_registry import V1_URL_PREFIX, EMAIL_CONFIG, EMAIL_SECRETS, EMAIL_BY_KEY
from fidesops.common_exceptions import EmailConfigNotFoundException
from fidesops.models.email import EmailConfig, get_schema_for_secrets
from fidesops.schemas.api import BulkUpdateFailed
from fidesops.schemas.email.email import BulkPutEmailConfigResponse, TestEmailStatusMessage, EmailConnectionTestStatus, \
    EmailConfigRequest, EmailConfigResponse
from fidesops.schemas.email.email_secrets_docs_only import possible_email_secrets
from fidesops.schemas.shared_schemas import FidesOpsKey
from fidesops.service.email.email_crud_service import create_email_config, get_email_configs, get_email_config_by_key
from fidesops.util.api_router import APIRouter
from fidesops.util.oauth_util import verify_oauth_client

router = APIRouter(tags=["email"], prefix=V1_URL_PREFIX)
logger = logging.getLogger(__name__)


@router.patch(
    EMAIL_CONFIG,
    status_code=HTTP_200_OK,
    dependencies=[Security(verify_oauth_client, scopes=[EMAIL_CREATE_OR_UPDATE])],
    response_model=BulkPutEmailConfigResponse,
)
def patch_config(
        *,
        db: Session = Depends(deps.get_db),
        email_configs: conlist(EmailConfigRequest, max_items=50),  # type: ignore
) -> BulkPutEmailConfigResponse:
    """
    Given a list of email config elements, create or update corresponding EmailConfig and EmailConfigUsage objects
    or report failure.
    """
    created_or_updated: List[EmailConfigResponse] = []
    failed: List[BulkUpdateFailed] = []

    logger.info(f"Starting bulk upsert for {len(email_configs)} email configs")
    for config in email_configs:
        try:
            email_config: EmailConfigResponse = create_email_config(db=db, config=config)

        except KeyOrNameAlreadyExists as exc:
            logger.warning(
                f"Create/update failed for storage config {config.key}: {exc}"
            )
            failure = {
                "message": exc.args[0],
                "data": config.dict(),
            }
            failed.append(BulkUpdateFailed(**failure))
            continue
        except Exception as exc:
            logger.warning(
                f"Create/update failed for email config {config.key}: {exc}"
            )
            failed.append(
                BulkUpdateFailed(
                    **{
                        "message": "Error creating or updating email config.",
                        "data": config.dict(),
                    }
                )
            )
        else:
            created_or_updated.append(email_config)

    return BulkPutEmailConfigResponse(succeeded=created_or_updated, failed=failed)


@router.put(
    EMAIL_SECRETS,
    status_code=HTTP_200_OK,
    dependencies=[Security(verify_oauth_client, scopes=[EMAIL_CREATE_OR_UPDATE])],
    response_model=TestEmailStatusMessage,
)
def put_config_secrets(
        config_key: FidesOpsKey,
        *,
        db: Session = Depends(deps.get_db),
        unvalidated_email_secrets: possible_email_secrets,
        verify: Optional[bool] = True,
) -> TestEmailStatusMessage:
    """
    Add or update secrets for storage config.
    """
    logger.info(f"Finding email config with key '{config_key}'")
    email_config = EmailConfig.get_by(db=db, field="key", value=config_key)
    if not email_config:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No email configuration with key {config_key}.",
        )

    try:
        secrets_schema = get_schema_for_secrets(
            service_type=email_config.service_type,
            secrets=unvalidated_email_secrets,
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.args[0],
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=exc.args[0],
        )

    logger.info(f"Updating email config secrets for config with key '{config_key}'")
    try:
        email_config.set_secrets(db=db, email_secrets=secrets_schema.dict())
    except ValueError as exc:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=exc.args[0],
        )

    msg = f"Secrets updated for EmailConfig with key: {config_key}."
    if verify:
        # fixme: impl email authenticator service
        status = True
        # status = secrets_are_valid(secrets_schema, email_config.service_type)
        # if status:
        #     logger.info(f"Email secrets are valid for config with key '{config_key}'")
        # else:
        #     logger.warning(
        #         f"email secrets are invalid for config with key '{config_key}'"
        #     )

        return TestEmailStatusMessage(
            msg=msg,
            test_status=EmailConnectionTestStatus.succeeded
            if status
            else EmailConnectionTestStatus.failed,
        )

    return TestEmailStatusMessage(msg=msg, test_status=None)


@router.get(
    EMAIL_CONFIG,
    dependencies=[Security(verify_oauth_client, scopes=[EMAIL_READ])],
    response_model=Page[EmailConfigResponse],
)
def get_configs(
        *, db: Session = Depends(deps.get_db), params: Params = Depends()
) -> AbstractPage[EmailConfigResponse]:
    """
    Retrieves configs for storage.
    """
    logger.info(f"Finding all storage configurations with pagination params {params}")
    return paginate(
        get_email_configs(db=db), params=params
    )


@router.get(
    EMAIL_BY_KEY,
    dependencies=[Security(verify_oauth_client, scopes=[EMAIL_READ])],
    response_model=EmailConfigResponse,
)
def get_config_by_key(
        config_key: FidesOpsKey, *, db: Session = Depends(deps.get_db)
) -> Optional[EmailConfigResponse]:
    """
    Retrieves configs for email by key.
    """
    logger.info(f"Finding email config with key '{config_key}'")

    email_config: Optional[EmailConfigResponse] = get_email_config_by_key(db=db, key=config_key)
    if not email_config:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No email config with key {config_key}.",
        )
    return email_config


@router.delete(
    EMAIL_BY_KEY,
    status_code=HTTP_204_NO_CONTENT,
    dependencies=[Security(verify_oauth_client, scopes=[EMAIL_DELETE])],
)
def delete_config_by_key(
        config_key: FidesOpsKey, *, db: Session = Depends(deps.get_db)
) -> None:
    """
    Deletes email configs by key.
    """
    try:
        delete_config_by_key(db=db, key=config_key)
    except EmailConfigNotFoundException:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No email config with key {config_key}.",
        )
