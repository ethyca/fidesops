from typing import Union

from fidesops.schemas.base_class import NoValidationSchema
from fidesops.schemas.email.email import EmailServiceSecretsMailgun


class EmailSecretsMailgunDocs(EmailServiceSecretsMailgun, NoValidationSchema):
    """The secrets required to connect to Mailgun, for documentation"""


possible_email_secrets = Union[EmailSecretsMailgunDocs]
