import logging

from jinja2 import (
    Environment,
    FileSystemLoader,
    Template,
    select_autoescape,
)

from fidesops.ops.common_exceptions import EmailTemplateUnhandledActionType
from fidesops.ops.email_templates.template_names import SUBJECT_IDENTITY_VERIFICATION
from fidesops.ops.schemas.email.email import EmailActionType

logger = logging.getLogger(__name__)

template_env = Environment(
    loader=FileSystemLoader("src/fidesops/ops/email_templates/templates"),
    autoescape=select_autoescape(),
)


def get_email_template(action_type: EmailActionType) -> Template:
    if action_type == EmailActionType.SUBJECT_IDENTITY_VERIFICATION:
        return template_env.get_template(SUBJECT_IDENTITY_VERIFICATION)

    logger.error(f"No corresponding template linked to the {action_type}")
    raise EmailTemplateUnhandledActionType(
        f"No corresponding template linked to the {action_type}"
    )
