import logging
from typing import Any, Dict, List, Union

from fastapi import APIRouter, Body, Depends, Security
from fastapi_pagination import (
    Page,
    Params,
)
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.sqlalchemy import paginate

from fidesops.db.base_class import get_key_from_data
from fidesops.models.connectionconfig import ConnectionConfig
from fidesops.schemas.policy import PolicyWebhookUpdateResponse
from fidesops.schemas.shared_schemas import FidesOpsKey
from pydantic import conlist
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from fidesops.api import deps
from fidesops.api.v1 import scope_registry as scopes
from fidesops.api.v1 import urn_registry as urls
from fidesops.common_exceptions import (
    DataCategoryNotSupported,
    PolicyValidationError,
    RuleValidationError,
    RuleTargetValidationError,
    KeyOrNameAlreadyExists,
    WebhookOrderException,
)
from fidesops.models.client import ClientDetail
from fidesops.models.policy import (
    ActionType,
    Policy,
    Rule,
    RuleTarget,
    PolicyPreWebhook,
    PolicyPostWebhook,
)
from fidesops.models.storage import StorageConfig
from fidesops.schemas import policy as schemas
from fidesops.schemas.api import BulkUpdateFailed
from fidesops.util.oauth_util import verify_oauth_client


router = APIRouter(tags=["Policy"], prefix=urls.V1_URL_PREFIX)

logger = logging.getLogger(__name__)


@router.get(
    urls.POLICY_LIST,
    status_code=200,
    response_model=Page[schemas.PolicyResponse],
    dependencies=[Security(verify_oauth_client, scopes=[scopes.POLICY_READ])],
)
def get_policy_list(
    *,
    db: Session = Depends(deps.get_db),
    params: Params = Depends(),
) -> AbstractPage[Policy]:
    """
    Return a paginated list of all Policy records in this system
    """
    logger.info(f"Finding all policies with pagination params '{params}'")
    policies = Policy.query(db=db)
    return paginate(policies, params=params)


@router.get(
    urls.POLICY_DETAIL,
    status_code=200,
    response_model=schemas.PolicyResponse,
    dependencies=[Security(verify_oauth_client, scopes=[scopes.POLICY_READ])],
)
def get_policy(
    *,
    policy_key: FidesOpsKey,
    db: Session = Depends(deps.get_db),
) -> schemas.PolicyResponse:
    """
    Return a single Policy
    """
    logger.info(f"Finding policy with key '{policy_key}'")
    policy = Policy.get_by(db=db, field="key", value=policy_key)
    if not policy:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No Policy found for key {policy_key}.",
        )

    return policy


@router.patch(
    urls.POLICY_LIST,
    status_code=200,
    response_model=schemas.BulkPutPolicyResponse,
)
def create_or_update_policies(
    *,
    client: ClientDetail = Security(
        verify_oauth_client,
        scopes=[scopes.POLICY_CREATE_OR_UPDATE],
    ),
    db: Session = Depends(deps.get_db),
    data: conlist(schemas.Policy, max_items=50) = Body(...),  # type: ignore
) -> schemas.BulkPutPolicyResponse:
    """
    Given a list of policy data elements, create or update corresponding Policy objects
    or report failure
    """
    created_or_updated: List[Policy] = []
    failed: List[BulkUpdateFailed] = []
    logger.info(f"Starting bulk upsert for {len(data)} policies")

    for policy_schema in data:
        policy_data: Dict[str, Any] = dict(policy_schema)
        try:
            policy = Policy.create_or_update(
                db=db,
                data={
                    "name": policy_data["name"],
                    "key": policy_data.get("key"),
                    "client_id": client.id,
                },
            )
        except KeyOrNameAlreadyExists as exc:
            logger.warning("Create/update failed for policy: %s", exc)
            failure = {
                "message": exc.args[0],
                "data": policy_data,
            }
            failed.append(BulkUpdateFailed(**failure))
            continue
        except PolicyValidationError as exc:
            logger.warning("Create/update failed for policy: %s", exc)
            failure = {
                "message": "This record could not be added because the data provided was invalid.",
                "data": policy_data,
            }
            failed.append(BulkUpdateFailed(**failure))
            continue
        else:
            created_or_updated.append(policy)

    return schemas.BulkPutPolicyResponse(
        succeeded=created_or_updated,
        failed=failed,
    )


@router.patch(
    urls.RULE_LIST,
    status_code=200,
    response_model=schemas.BulkPutRuleResponse,
)
def create_or_update_rules(
    *,
    client: ClientDetail = Security(
        verify_oauth_client,
        scopes=[scopes.RULE_CREATE_OR_UPDATE],
    ),
    policy_key: FidesOpsKey,
    db: Session = Depends(deps.get_db),
    input_data: conlist(schemas.RuleCreate, max_items=50) = Body(...),  # type: ignore
) -> schemas.BulkPutRuleResponse:
    """
    Given a list of Rule data elements, create or update corresponding Rule objects
    or report failure
    """
    logger.info(f"Finding policy with key '{policy_key}'")

    policy = Policy.get_by(db=db, field="key", value=policy_key)
    if not policy:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No Policy found for key {policy_key}.",
        )

    created_or_updated: List[Rule] = []
    failed: List[BulkUpdateFailed] = []

    logger.info(
        f"Starting bulk upsert for {len(input_data)} rules on policy {policy_key}"
    )

    for schema in input_data:
        # Validate all FKs in the input data exist
        associated_storage_config_id = None
        if schema.action_type == ActionType.access.value:
            # Only validate the associated StorageConfig on access rules
            storage_destination_key = schema.storage_destination_key
            associated_storage_config: StorageConfig = StorageConfig.get_by(
                db=db,
                field="key",
                value=storage_destination_key,
            )
            if not associated_storage_config:
                logger.warning(
                    f"No storage config found with key {storage_destination_key}"
                )
                failure = {
                    "message": f"A StorageConfig with key {storage_destination_key} does not exist",
                    "data": dict(
                        schema
                    ),  # Be sure to pass the schema out the same way it came in
                }
                failed.append(BulkUpdateFailed(**failure))
                continue
            else:
                associated_storage_config_id = associated_storage_config.id

        masking_strategy_data = None
        if schema.masking_strategy:
            masking_strategy_data = schema.masking_strategy.dict()

        try:
            rule = Rule.create_or_update(
                db=db,
                data={
                    "action_type": schema.action_type,
                    "client_id": client.id,
                    "key": schema.key,
                    "name": schema.name,
                    "policy_id": policy.id,
                    "storage_destination_id": associated_storage_config_id,
                    "masking_strategy": masking_strategy_data,
                },
            )
        except KeyOrNameAlreadyExists as exc:
            logger.warning(
                f"Create/update failed for rule '{schema.key}' on policy {policy_key}: {exc}"
            )
            failure = {
                "message": exc.args[0],
                "data": dict(schema),
            }
            failed.append(BulkUpdateFailed(**failure))
            continue
        except RuleValidationError as exc:
            logger.warning(
                f"Create/update failed for rule '{schema.key}' on policy {policy_key}: {exc}"
            )
            failure = {
                "message": exc.args[0],
                "data": dict(schema),
            }
            failed.append(BulkUpdateFailed(**failure))
            continue
        except ValueError as exc:
            logger.warning(
                f"Create/update failed for rule '{schema.key}' on policy {policy_key}: {exc}"
            )
            failure = {
                "message": exc.args[0],
                "data": dict(schema),
            }
            failed.append(BulkUpdateFailed(**failure))
            continue
        else:
            created_or_updated.append(rule)

    return schemas.BulkPutRuleResponse(succeeded=created_or_updated, failed=failed)


@router.delete(
    urls.RULE_DETAIL,
    status_code=204,
    dependencies=[Security(verify_oauth_client, scopes=[scopes.RULE_DELETE])],
)
def delete_rule(
    *,
    policy_key: FidesOpsKey,
    rule_key: FidesOpsKey,
    db: Session = Depends(deps.get_db),
) -> None:
    """
    Delete a policy rule.
    """
    logger.info(f"Finding policy with key '{policy_key}'")

    policy = Policy.get_by(db=db, field="key", value=policy_key)
    if not policy:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No Policy found for key {policy_key}.",
        )

    logger.info(f"Finding rule with key '{rule_key}'")

    rule = Rule.filter(
        db=db, conditions=(Rule.key == rule_key and Rule.policy_id == policy.id)
    ).first()
    if not rule:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No Rule found for key {rule_key} on Policy {policy_key}.",
        )

    logger.info(f"Deleting rule with key '{rule_key}'")
    rule.delete(db=db)


@router.patch(
    urls.RULE_TARGET_LIST,
    status_code=200,
    response_model=schemas.BulkPutRuleTargetResponse,
)
def create_or_update_rule_targets(
    *,
    client: ClientDetail = Security(
        verify_oauth_client, scopes=[scopes.RULE_CREATE_OR_UPDATE]
    ),
    policy_key: FidesOpsKey,
    rule_key: FidesOpsKey,
    db: Session = Depends(deps.get_db),
    input_data: conlist(schemas.RuleTarget, max_items=50) = Body(...),  # type: ignore
) -> schemas.BulkPutRuleTargetResponse:
    """
    Given a list of Rule data elements, create corresponding Rule objects
    or report failure
    """
    logger.info(f"Finding policy with key '{policy_key}'")
    policy = Policy.get_by(db=db, field="key", value=policy_key)
    if not policy:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No Policy found for key {policy_key}.",
        )

    logger.info(f"Finding rule with key '{rule_key}'")
    rule = Rule.filter(
        db=db, conditions=(Rule.key == rule_key and Rule.policy_id == policy.id)
    ).first()
    if not rule:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No Rule found for key {rule_key} on Policy {policy_key}.",
        )

    created_or_updated = []
    failed = []
    logger.info(
        f"Starting bulk upsert for {len(input_data)} rule targets on rule {rule_key}"
    )
    for schema in input_data:
        try:
            target = RuleTarget.create_or_update(
                db=db,
                data={
                    "name": schema.name,
                    "key": schema.key,
                    "data_category": schema.data_category,
                    "rule_id": rule.id,
                    "client_id": client.id,
                },
            )
        except KeyOrNameAlreadyExists as exc:
            logger.warning(
                f"Create/update failed for rule target {schema.key} on rule {rule_key}: {exc}"
            )
            failure = {
                "message": exc.args[0],
                "data": dict(schema),
            }
            failed.append(BulkUpdateFailed(**failure))
            continue
        except (
            DataCategoryNotSupported,
            PolicyValidationError,
            RuleTargetValidationError,
        ) as exc:
            logger.warning(
                f"Create/update failed for rule target {schema.key} on rule {rule_key}: {exc}"
            )
            failure = {
                "message": exc.args[0],
                "data": dict(schema),
            }
            failed.append(BulkUpdateFailed(**failure))
            continue
        except IntegrityError as exc:
            logger.warning(
                f"Create/update failed for rule target {schema.key} on rule {rule_key}: {exc}"
            )
            failure = {
                "message": f"DataCategory {schema.data_category} is already specified on Rule with ID {rule.id}",
                "data": dict(schema),
            }
            failed.append(BulkUpdateFailed(**failure))
        else:
            created_or_updated.append(target)

    return schemas.BulkPutRuleTargetResponse(
        succeeded=created_or_updated,
        failed=failed,
    )


@router.delete(
    urls.RULE_TARGET_DETAIL,
    status_code=204,
    dependencies=[Security(verify_oauth_client, scopes=[scopes.RULE_DELETE])],
)
def delete_rule_target(
    *,
    policy_key: FidesOpsKey,
    rule_key: FidesOpsKey,
    rule_target_key: FidesOpsKey,
    db: Session = Depends(deps.get_db),
) -> None:
    """
    Delete the rule target.
    """
    logger.info(f"Finding policy with key '{policy_key}'")

    policy = Policy.get_by(db=db, field="key", value=policy_key)
    if not policy:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No Policy found for key {policy_key}.",
        )

    logger.info(f"Finding rule with key '{rule_key}'")
    rule = Rule.filter(
        db=db, conditions=(Rule.key == rule_key and Rule.policy_id == policy.id)
    ).first()
    if not rule:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No Rule found for key {rule_key} on Policy {policy_key}.",
        )

    logger.info(f"Finding rule target with key '{rule_target_key}'")
    target = RuleTarget.filter(
        db=db,
        conditions=(
            RuleTarget.key == rule_target_key and RuleTarget.rule_id == rule.id
        ),
    ).first()
    if not target:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No RuleTarget found for key {rule_target_key} at Rule {rule_key} on Policy {policy_key}.",
        )

    logger.info(f"Deleting rule target with key '{rule_target_key}'")

    target.delete(db=db)


def _put_webhooks(
    webhook_cls: Union[PolicyPreWebhook, PolicyPostWebhook],
    policy_key: FidesOpsKey,
    db: Session = Depends(deps.get_db),
    webhooks: List[schemas.PolicyWebhookCreate] = Body(...),
) -> List[Union[PolicyPreWebhook, PolicyPostWebhook]]:
    """
    Helper method to be shared between both endpoints that create/update policy webhooks.

    Creates/updates webhooks with the same "order" in which they arrived. This endpoint is all-or-nothing.
    Either all webhooks should be created/updated or none should be updated. Deletes any webhooks not present
    in the webhooks list.
    """
    logger.info(f"Finding policy with key '{policy_key}'")

    policy = Policy.get_by(db=db, field="key", value=policy_key)
    if not policy:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No Policy found for key {policy_key}.",
        )

    keys = [
        get_key_from_data(webhook.dict(), webhook_cls.__name__) for webhook in webhooks
    ]
    # Because resources are dependent on each other for order, we want to make sure that we don't have multiple
    # resources in the request that actually point to the same object.
    if len(keys) != len(set(keys)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Check request body: there are multiple webhooks whose keys resolve to the same value.",
        )

    staged_webhooks = []
    for webhook_index, schema in enumerate(webhooks):
        connection_config_key = schema.connection_config_key
        logger.info(f"Finding ConnectionConfig with key '{connection_config_key}'")
        connection_config: ConnectionConfig = ConnectionConfig.get_by(
            db=db, field="key", value=connection_config_key
        )

        if not connection_config:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"No ConnectionConfig found for key {connection_config_key}.",
            )

        try:
            webhook = webhook_cls.create_or_update(
                db=db,
                data={
                    "key": schema.key,
                    "name": schema.name,
                    "policy_id": policy.id,
                    "connection_config_id": connection_config.id,
                    "direction": schema.direction,
                    "order": webhook_index,  # Add in the order they arrived in the request
                },
            )
            staged_webhooks.append(webhook)
        except KeyOrNameAlreadyExists as exc:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=exc.args[0],
            )

    webhooks_to_remove = webhook_cls.filter(
        db,
        conditions=(
            (
                webhook_cls.key.not_in(
                    [staged_webhook.key for staged_webhook in staged_webhooks]
                )
            )
            & (webhook_cls.policy_id == policy.id)
        ),
    )
    logger.info(
        f"Removing Policy {policy.id }Pre-Execution Webhooks that were not included in request: {[webhook.key for webhook in webhooks_to_remove]}"
    )
    webhooks_to_remove.delete()

    # Committing to database now, as a last step, once we've verified that all the webhooks
    # in the request are free of issues.
    db.commit()
    logger.info(
        f"Creating/updating Policy Pre-Execution Webhooks: {[staged_webhook.key for staged_webhook in staged_webhooks]}"
    )

    return staged_webhooks


@router.put(
    urls.POLICY_WEBHOOKS_PRE,
    status_code=200,
    dependencies=[
        Security(verify_oauth_client, scopes=[scopes.WEBHOOK_CREATE_OR_UPDATE])
    ],
    response_model=List[schemas.PolicyWebhookResponse],
)
def create_or_update_pre_execution_webhooks(
    *,
    policy_key: FidesOpsKey,
    db: Session = Depends(deps.get_db),
    webhooks: conlist(schemas.PolicyWebhookCreate, max_items=50) = Body(...),  # type: ignore
) -> List[PolicyPreWebhook]:
    """
    Create or update Policy Webhooks that run **before** query execution.

    All webhooks must be included in the request in the desired order. Any missing webhooks
    from the request body will be removed.
    """
    return _put_webhooks(PolicyPreWebhook, policy_key, db, webhooks)


@router.put(
    urls.POLICY_WEBHOOKS_POST,
    status_code=200,
    dependencies=[
        Security(verify_oauth_client, scopes=[scopes.WEBHOOK_CREATE_OR_UPDATE])
    ],
    response_model=List[schemas.PolicyWebhookResponse],
)
def create_or_update_post_execution_webhooks(
    *,
    policy_key: FidesOpsKey,
    db: Session = Depends(deps.get_db),
    webhooks: conlist(schemas.PolicyWebhookCreate, max_items=50) = Body(...),  # type: ignore
) -> List[PolicyPostWebhook]:
    """
    Create or update Policy Webhooks that run **after** query execution.

    All webhooks must be included in the request in the desired order. Any missing webhooks
    from the request body will be removed.
    """
    return _put_webhooks(PolicyPostWebhook, policy_key, db, webhooks)


def _patch_webhook(
    *,
    db: Session = Depends(deps.get_db),
    policy_key: FidesOpsKey,
    webhook_key: FidesOpsKey,
    webhook_body: schemas.PolicyWebhookUpdate = Body(...),
    webhook_cls: Union[PolicyPreWebhook, PolicyPostWebhook],
) -> PolicyWebhookUpdateResponse:
    """Helper method to be shared between the endpoints that PATCH a single webhook, either
    Pre-Execution or Post-Execution
    """
    logger.info(f"Finding policy with key '{policy_key}'")
    policy = Policy.get_by(db=db, field="key", value=policy_key)
    if not policy:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No Policy found for key {policy_key}.",
        )

    loaded_webhook = webhook_cls.get_by(db=db, field="key", value=webhook_key)
    if not loaded_webhook:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No {webhook_cls.__class__} found for key {webhook_key}.",
        )

    data = webhook_body.dict(exclude_none=True)

    if data.get("connection_config_key"):
        connection_config: ConnectionConfig = ConnectionConfig.get_by(
            db=db, field="key", value=data["connection_config_key"]
        )

        if not connection_config:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"No ConnectionConfig found for key {data['connection_config_key']}.",
            )
        data["connection_config_id"] = connection_config.id

    # Removing index from incoming data - we'll set this later.
    index = data.pop("order", None)

    try:
        logger.info(f"Updating {webhook_cls.__class__} {webhook_key}")
        loaded_webhook.update(db, data=data)
    except KeyOrNameAlreadyExists as exc:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=exc.args[0],
        )

    if index is not None and index != loaded_webhook.order:
        logger.info(
            f"Reordering {'Pre-Execution' if webhook_cls == PolicyPreWebhook else 'Post-Execution'} Webhooks for Policy {policy_key}"
        )
        try:
            loaded_webhook.reorder_related_webhooks(db=db, new_index=index)
        except WebhookOrderException as exc:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=exc.args[0],
            )
        return PolicyWebhookUpdateResponse(
            resource=loaded_webhook,
            reordered=[
                webhook
                for webhook in webhook_cls.filter(
                    db=db,
                    conditions=(webhook_cls.policy_id == policy.id),
                ).order_by(webhook_cls.order)
            ],
        )

    # Policy Webhooks are not committed by default, so we commit at the end.
    db.commit()
    return PolicyWebhookUpdateResponse(resource=loaded_webhook, reordered=[])


@router.patch(
    urls.POLICY_PRE_WEBHOOK_DETAIL,
    status_code=200,
    dependencies=[
        Security(verify_oauth_client, scopes=[scopes.WEBHOOK_CREATE_OR_UPDATE])
    ],
    response_model=PolicyWebhookUpdateResponse,
)
def update_pre_execution_webhook(
    *,
    db: Session = Depends(deps.get_db),
    policy_key: FidesOpsKey,
    pre_webhook_key: FidesOpsKey,
    webhook_body: schemas.PolicyWebhookUpdate = Body(...),
) -> PolicyWebhookUpdateResponse:
    """PATCH a single Policy Webhook that runs **prior** to executing the Privacy Request.

    Note that updates to the webhook's "order" can affect the order of the other pre-execution webhooks.
    """
    return _patch_webhook(
        db=db,
        policy_key=policy_key,
        webhook_key=pre_webhook_key,
        webhook_body=webhook_body,
        webhook_cls=PolicyPreWebhook,
    )


@router.patch(
    urls.POLICY_POST_WEBHOOK_DETAIL,
    status_code=200,
    dependencies=[
        Security(verify_oauth_client, scopes=[scopes.WEBHOOK_CREATE_OR_UPDATE])
    ],
    response_model=PolicyWebhookUpdateResponse,
)
def update_post_execution_webhook(
    *,
    db: Session = Depends(deps.get_db),
    policy_key: FidesOpsKey,
    post_webhook_key: FidesOpsKey,
    webhook_body: schemas.PolicyWebhookUpdate = Body(...),
) -> PolicyWebhookUpdateResponse:
    """PATCH a single Policy Webhook that runs **after** executing the Privacy Request.

    Note that updates to the webhook's "order" can affect the order of the other post-execution webhooks.
    """
    return _patch_webhook(
        db=db,
        policy_key=policy_key,
        webhook_key=post_webhook_key,
        webhook_body=webhook_body,
        webhook_cls=PolicyPostWebhook,
    )
