from typing import Union

from fidesops.schemas.base_class import DocsOnlySchema
from fidesops.schemas.storage.storage import (
    StorageSecretsLocal,
    StorageSecretsS3,
    StorageSecretsOnetrust,
)


class StorageSecretsS3Docs(StorageSecretsS3, DocsOnlySchema):
    """The secrets required to connect to S3, for documentation"""


class StorageSecretsOnetrustDocs(StorageSecretsOnetrust, DocsOnlySchema):
    """The secrets required to send results to Onetrust, for documentation"""


possible_storage_secrets = Union[StorageSecretsS3Docs, StorageSecretsOnetrustDocs]
