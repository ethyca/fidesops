import logging
from typing import List, Optional

from fideslang.validation import FidesKey
from sqlalchemy.orm import Session

from fidesops.common_exceptions import EmailConfigNotFoundException
from fidesops.models.email import EmailConfig
from fidesops.schemas.email.email import EmailConfigRequest, EmailConfigResponse


logger = logging.getLogger(__name__)


def create_or_update_email_config(db: Session, config: EmailConfigRequest) -> EmailConfigResponse:
    # todo- prevent multiple configs to be added for now
    email_config: EmailConfig = EmailConfig.create_or_update(
        db=db, data={
            "key": config.key,
            "name": config.name,
            "service_type": config.service_type,
            "details": config.details.__dict__
        }
    )
    return EmailConfigResponse(
        name=email_config.name,
        key=email_config.key,
        service_type=email_config.service_type,
        details=email_config.details,
    )


def delete_email_config(db: Session, key: FidesKey) -> None:
    logger.info(f"Finding email config with key '{key}'")
    email_config: EmailConfig = EmailConfig.get_by(db, field="key", value=key)
    if not email_config:
        raise EmailConfigNotFoundException
    logger.info(f"Deleting email config with key '{key}'")
    email_config.delete(db)


def get_email_configs(db: Session) -> Optional[List[EmailConfigResponse]]:
    email_configs_response: Optional[List[EmailConfigResponse]] = []
    email_configs = EmailConfig.query(db=db).order_by(EmailConfig.created_at.desc())
    for config in email_configs:
        email_configs_response.append(EmailConfigResponse(
            name=config.name,
            key=config.key,
            service_type=config.service_type,
            details=config.details
        ))
    return email_configs_response


def get_email_config_by_key(db: Session, key: FidesKey) -> Optional[EmailConfigResponse]:
    config = EmailConfig.get_by(db=db, field="key", value=key)
    return EmailConfigResponse(
        name=config.name,
        key=config.key,
        service_type=config.service_type,
        details=config.details
    )


