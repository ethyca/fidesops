# pylint: disable=W0611
# Import all the models, so that Base has them before being
# imported by Alembic
from fidesops.db.base_class import Base  # type: ignore
from fidesops.models.audit_log import AuditLog
from fidesops.models.authentication_request import AuthenticationRequest
from fidesops.models.client import ClientDetail
from fidesops.models.connectionconfig import ConnectionConfig
from fidesops.models.datasetconfig import DatasetConfig
from fidesops.models.fidesops_user import FidesopsUser
from fidesops.models.fidesops_user_permissions import FidesopsUserPermissions
from fidesops.models.policy import Policy, Rule, RuleTarget
from fidesops.models.privacy_request import PrivacyRequest
from fidesops.models.storage import StorageConfig
