import json
import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Security
from fidesops.models.datasetconfig import DatasetConfig
from fidesops.schemas.connection_configuration.connection_config import (
    ConnectionConfigurationResponse,
)
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from sqlalchemy.orm import Session


from fidesops.api import deps
from fidesops.api.v1.endpoints.dataset_endpoints import _get_connection_config
from fidesops.api.v1.scope_registry import (
    SAAS_CONFIG_CREATE_OR_UPDATE,
    SAAS_CONFIG_DELETE,
    SAAS_CONFIG_READ,
)

from fidesops.api.v1.urn_registry import (
    SAAS_CONFIG,
    SAAS_CONFIG_VALIDATE,
    V1_URL_PREFIX,
)
from fidesops.core.config import SecuritySettings
from fidesops.models.connectionconfig import ConnectionConfig
from fidesops.schemas.saas.saas_config import (
    SaaSConfig,
    SaaSConfigValidationDetails,
    ValidateSaaSConfigResponse,
)
from fidesops.util.oauth_util import verify_oauth_client


router = APIRouter(tags=["SaaS Configs"], prefix=V1_URL_PREFIX)
logger = logging.getLogger(__name__)


@router.put(
    SAAS_CONFIG_VALIDATE,
    dependencies=[Security(verify_oauth_client, scopes=[SAAS_CONFIG_READ])],
    status_code=200,
    response_model=ValidateSaaSConfigResponse,
)
def validate_saas_config(
    saas_config: SaaSConfig,
) -> ValidateSaaSConfigResponse:
    """
    Run validations against a SaaS config without attempting to save it to the database.

    Checks that:
    - all required fields are present, all field values are valid types
    """

    logger.info(f"Validation successful for SaaS config '{saas_config.fides_key}'!")
    return ValidateSaaSConfigResponse(
        saas_config=saas_config,
        validation_details=SaaSConfigValidationDetails(
            msg=None,
        ),
    )


@router.patch(
    SAAS_CONFIG,
    dependencies=[Security(verify_oauth_client, scopes=[SAAS_CONFIG_CREATE_OR_UPDATE])],
    status_code=200,
    response_model=ConnectionConfigurationResponse,
)
def patch_saas_config(
    saas_config: SaaSConfig,
    db: Session = Depends(deps.get_db),
    connection_config: ConnectionConfig = Depends(_get_connection_config),
) -> ConnectionConfig:
    """
    Given a SaaS config element, update the corresponding ConnectionConfig object
    or report failure
    """
    data = {"key": connection_config.key, "saas_config": saas_config.dict()}
    logger.info(f"Starting upsert for SaaS config '{saas_config.fides_key}'")
    return ConnectionConfig.create_or_update(db, data=data)


@router.get(
    SAAS_CONFIG,
    dependencies=[Security(verify_oauth_client, scopes=[SAAS_CONFIG_READ])],
    response_model=SaaSConfig,
)
def get_saas_config(
    connection_config: ConnectionConfig = Depends(_get_connection_config),
) -> SaaSConfig:
    """Returns the SaaS config for the given connection config."""

    logger.info(f"Finding SaaS config for connection '{connection_config.key}'")
    saas_config = connection_config.saas_config
    if not saas_config:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No SaaS config found for connection '{connection_config.key}'",
        )
    return connection_config.saas_config


@router.delete(
    SAAS_CONFIG,
    dependencies=[Security(verify_oauth_client, scopes=[SAAS_CONFIG_DELETE])],
    status_code=204,
)
def delete_saas_config(
    db: Session = Depends(deps.get_db),
    connection_config: ConnectionConfig = Depends(_get_connection_config),
) -> None:
    """Removes the SaaS config for the given connection config.
    The corresponding dataset and secrets must be deleted before deleting the SaaS config"""

    logger.info(f"Finding SaaS config for connection '{connection_config.key}'")
    saas_config = connection_config.saas_config
    if not saas_config:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No SaaS config found for connection '{connection_config.key}'",
        )

    fides_key = saas_config["fides_key"]
    dataset = DatasetConfig.filter(
        db=db,
        conditions=(
            (DatasetConfig.connection_config_id == connection_config.id)
            & (DatasetConfig.fides_key == fides_key)
        ),
    ).first()

    warnings = []
    if dataset:
        warnings.append(
            f"Must delete the dataset with fides_key '{fides_key}' before deleting this SaaS config."
        )
    if connection_config.secrets:
        warnings.append(
            "Must clear the secrets from this connection config before deleting the SaaS config."
        )

    if warnings:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=" ".join(warnings))

    logger.info(f"Deleting SaaS config for connection '{connection_config.key}'")
    ConnectionConfig.create_or_update(
        db, data={"key": connection_config.key, "saas_config": None}
    )
