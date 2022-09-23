from datetime import datetime
import logging
import requests
from time import sleep
import uuid
import yaml

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from fidesops.ops.api.v1.scope_registry import SCOPE_REGISTRY
from fidesops.ops.api.v1 import urn_registry as urls

import secrets


class QuickstartBase:

    # FIDESOPS_URL = "http://webserver:8080"
    FIDESOPS_URL = "http://localhost:8080"
    BASE_URL = FIDESOPS_URL + urls.V1_URL_PREFIX
    ROOT_CLIENT_ID = "fidesopsadmin"
    ROOT_CLIENT_SECRET = "fidesopsadminsecret"

    ACCESS_POLICY_KEY = "download"
    ERASURE_POLICY_KEY = "delete"

    # These are external datastores so don't read them from the config
    POSTGRES_SERVER = "host.docker.internal"
    # POSTGRES_SERVER = "postgres_example"
    POSTGRES_USER = "postgres"
    POSTGRES_PASSWORD = "postgres"
    POSTGRES_PORT = 6432
    POSTGRES_DB_NAME = "postgres_example"

    def __init__(self, config={}):
        # Override any config passed in
        for key, value in config.items():
            setattr(self, key, value)

        sleep(2)
        self.check_health()
        self.configure_oauth_client()

    def check_health(self):
        self.connection_retry_count = 0
        url = f"{self.FIDESOPS_URL}{urls.HEALTH}"
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            sleep(2)
            self.connection_retry_count += 1
            if self.connection_retry_count < 4:
                return self.check_health()
            else:
                raise

        if not response.ok:
            raise RuntimeError(
                f"fidesops health check failed! response.status_code={response.status_code}, response.json()={response.json()} at url {url}"
            )

    def get_access_token(self, client_id: str, client_secret: str) -> str:
        """
        Authorize with fidesops via OAuth.
        Returns a valid access token if successful, or throws an error otherwise.
        """
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        url = f"{self.BASE_URL}{urls.TOKEN}"
        response = requests.post(url, data=data)

        if response.ok:
            token = (response.json())["access_token"]
            if token:
                logger.info(f"Completed fidesops oauth login via {url}")
                return token

        raise RuntimeError(
            f"fidesops oauth login failed! response.status_code={response.status_code}, response.json()={response.json()}"
        )

    def create_oauth_client(self, auth_token):
        """
        Create a new OAuth client in fidesops.
        Returns the response JSON if successful, or throws an error otherwise.
        """
        oauth_header = {"Authorization": f"Bearer {auth_token}"}
        response = requests.post(
            f"{self.BASE_URL}{urls.CLIENT}",
            headers=oauth_header,
            json=SCOPE_REGISTRY,
        )

        if response.ok:
            created_client = response.json()
            if created_client["client_id"] and created_client["client_secret"]:
                logger.info("Created fidesops oauth client via /api/v1/oauth/client")
                return created_client["client_id"], created_client["client_secret"]

        raise RuntimeError(
            f"fidesops oauth client creation failed! response.status_code={response.status_code}, response.json()={response.json()}"
        )

    def configure_oauth_client(self):
        """Use the root oauth client to create a new client"""
        root_token = self.get_access_token(
            client_id=self.ROOT_CLIENT_ID,
            client_secret=self.ROOT_CLIENT_SECRET,
        )
        client_id, client_secret = self.create_oauth_client(auth_token=root_token)
        auth_token = self.get_access_token(client_id, client_secret)
        self.auth_header = {"Authorization": f"Bearer {auth_token}"}

    def configure_user(self, username=None, password="Atestpassword1!"):
        """Adds a user with full permissions"""
        if not username:
            username = str(uuid.uuid4())

        response = requests.post(
            f"{self.BASE_URL}{urls.USERS}",
            headers=self.auth_header,
            json={
                "first_name": "Atest",
                "last_name": "User",
                "username": username,
                "password": password,
            },
        )

        if not response.ok:
            raise RuntimeError(
                f"fidesops user creation failed! response.status_code={response.status_code}, response.json()={response.json()}"
            )

        user_id = response.json()["id"]

        user_permissions_url = urls.USER_PERMISSIONS.format(user_id=user_id)
        response = requests.put(
            f"{self.BASE_URL}{user_permissions_url}",
            headers=self.auth_header,
            json={
                "id": user_id,  # TODO: Remove this from the schema
                "scopes": SCOPE_REGISTRY,
            },
        )

        if not response.ok:
            raise RuntimeError(
                f"fidesops user permissions creation failed! response.status_code={response.status_code}, response.json()={response.json()}"
            )
        else:
            logger.info(
                f"Created user with username: {username} and password: {password}"
            )

    def configure_email(self, key="fidesops_email"):
        response = requests.post(
            f"{self.BASE_URL}{urls.EMAIL_CONFIG}",
            headers=self.auth_header,
            json={
                "name": "Fidesops Emails",
                "key": key,  # TODO: Randomise this
                "service_type": "mailgun",
                "details": {
                    "is_eu_domain": False,
                    "api_version": "v3",
                    # TODO: Where do we find this value? Can we be more specific in the docs?
                    "domain": "testmail.ethyca.com",
                },
            },
        )

        if not response.ok:
            if (
                response.json()["detail"]
                != f"Only one email config is supported at a time. Config with key {key} is already configured."
            ):
                raise RuntimeError(
                    f"fidesops email config creation failed! response.status_code={response.status_code}, response.json()={response.json()}"
                )

        # Now add secrets
        email_secrets_path = urls.EMAIL_SECRETS.format(config_key=key)
        response = requests.put(
            f"{self.BASE_URL}{email_secrets_path}",
            headers=self.auth_header,
            json={
                "mailgun_api_key": secrets.MAILGUN_API_KEY,
            },
        )

        if not response.ok:
            raise RuntimeError(
                f"fidesops email config secrets update failed! response.status_code={response.status_code}, response.json()={response.json()}"
            )

        logger.info(response.json()["msg"])

    def create_dataset(self, connection_key, yaml_path):
        with open(yaml_path, "r") as file:
            dataset = yaml.safe_load(file).get("dataset", [])[0]

        dataset_create_data = [dataset]
        dataset_path = urls.DATASETS.format(connection_key=connection_key)
        url = f"{self.BASE_URL}{dataset_path}"
        response = requests.patch(
            url,
            headers=self.auth_header,
            json=dataset_create_data,
        )

        if response.ok:
            datasets = (response.json())["succeeded"]
            if len(datasets) > 0:
                logger.info(f"Created fidesops dataset via {url}")
                return response.json()

        raise RuntimeError(
            f"fidesops dataset creation failed! response.status_code={response.status_code}, response.json()={response.json()}"
        )

    def configure_postgres_connector(self, key="postgres_connector", verify=True):
        connection_create_data = [
            {
                "name": key,
                "key": key,
                "connection_type": "postgres",
                "access": "write",
            },
        ]
        response = requests.patch(
            f"{self.BASE_URL}{urls.CONNECTIONS}",
            headers=self.auth_header,
            json=connection_create_data,
        )

        if not response.ok:
            raise RuntimeError(
                f"fidesops connection creation failed! response.status_code={response.status_code}, response.json()={response.json()}"
            )

        connection_secrets_path = urls.CONNECTION_SECRETS.format(connection_key=key)
        url = f"{self.BASE_URL}{connection_secrets_path}?verify={verify}"
        postgres_secrets_data = {
            "host": self.POSTGRES_SERVER,
            "port": self.POSTGRES_PORT,
            "dbname": self.POSTGRES_DB_NAME,
            "username": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
        }
        response = requests.put(
            url,
            headers=self.auth_header,
            json=postgres_secrets_data,
        )

        if not response.ok:
            raise RuntimeError(
                f"fidesops connection configuration failed! response.status_code={response.status_code}, response.json()={response.json()}"
            )

        if (response.json())["test_status"] == "failed":
            raise RuntimeError(
                f"fidesops connection test failed! response.status_code={response.status_code}, response.json()={response.json()}"
            )

        logger.info(f"Configured fidesops postgres connection secrets for via {url}")

        self.create_dataset(
            connection_key=key,
            yaml_path="data/dataset/postgres_example_test_dataset.yml",
        )

    def configure_mailchimp_connector(self, key=None):
        if not key:
            key = str(uuid.uuid4())

        path = urls.SAAS_CONNECTOR_FROM_TEMPLATE.format(saas_connector_type="mailchimp")
        url = f"{self.BASE_URL}{path}"
        response = requests.post(
            url,
            headers=self.auth_header,
            json={
                "instance_key": f"mailchimp_instance_{key}",
                "secrets": secrets.MAILCHIMP_SECRETS,
                "name": f"Mailchimp Connector {key}",
                "description": "Mailchimp ConnectionConfig description",
                "key": key,
            },
        )

        if not response.ok:
            raise RuntimeError(
                f"fidesops mailchimp connector configuration failed! response.status_code={response.status_code}, response.json()={response.json()}"
            )

    def configure_s3_storage(self, key="s3_storage", policy_key=ACCESS_POLICY_KEY):
        url = f"{self.BASE_URL}{urls.STORAGE_CONFIG}"
        response = requests.patch(
            url,
            headers=self.auth_header,
            json=[
                {
                    "name": key,
                    "key": key,
                    "type": "s3",
                    "format": "json",
                    "details": {
                        "auth_method": "secret_keys",
                        "bucket": "fidesops-demo-10-04-2021",
                        "naming": "request_id",
                        "object_name": "test",
                    },
                },
            ],
        )

        if not response.ok:
            raise RuntimeError(
                f"fidesops storage creation failed! response.status_code={response.status_code}, response.json()={response.json()}"
            )
        else:
            storage = (response.json())["succeeded"]
            if len(storage) > 0:
                logger.info(f"Created fidesops storage with key={key} via {url}")

        storage_secrets_path = urls.STORAGE_SECRETS.format(config_key=key)
        url = f"{self.BASE_URL}{storage_secrets_path}"
        response = requests.put(
            url,
            headers=self.auth_header,
            json={
                "aws_access_key_id": secrets.AWS_ACCESS_KEY_ID,
                "aws_access_secret_id": secrets.AWS_ACCESS_SECRET_ID,
            },
        )

        rule_key = f"{key}_rule"
        rule_create_data = {
            "name": rule_key,
            "key": rule_key,
            "action_type": "access",
            "storage_destination_key": key,
        }

        policy_path = urls.RULE_LIST.format(policy_key=policy_key)
        url = f"{self.BASE_URL}{policy_path}"
        response = requests.patch(
            url,
            headers=self.auth_header,
            json=[rule_create_data],
        )

        if not response.ok:
            raise RuntimeError(
                f"fidesops policy rule creation failed! response.status_code={response.status_code}, response.json()={response.json()}"
            )

        rule_target_path = urls.RULE_TARGET_LIST.format(
            policy_key=self.ACCESS_POLICY_KEY,
            rule_key=rule_key,
        )
        url = f"{self.BASE_URL}{rule_target_path}"
        data_category = "user"
        response = requests.patch(
            url,
            headers=self.auth_header,
            json=[{"data_category": data_category}],
        )

        if response.ok:
            targets = (response.json())["succeeded"]
            if len(targets) > 0:
                logger.info(
                    f"Created fidesops policy rule target for '{data_category}' via {url}"
                )

    def create_policy(self, key, execution_timeframe=45):
        policy_create_data = [
            {
                "name": key,
                "key": key,
                "execution_timeframe": execution_timeframe,
            },
        ]
        response = requests.patch(
            f"{self.BASE_URL}{urls.POLICY_LIST}",
            headers=self.auth_header,
            json=policy_create_data,
        )

        if response.ok:
            policies = (response.json())["succeeded"]
            if len(policies) > 0:
                logger.info(
                    "Created fidesops policy with key=%s via /api/v1/policy", key
                )
                return

        raise RuntimeError(
            f"fidesops policy creation failed! response.status_code={response.status_code}, response.json()={response.json()}"
        )

    def create_access_request(
        self,
        user_email="sean+engdemo@ethyca.com",
        policy_key=ACCESS_POLICY_KEY,
    ):
        response = requests.post(
            f"{self.BASE_URL}{urls.PRIVACY_REQUESTS}",
            json=[
                {
                    "requested_at": str(datetime.utcnow()),
                    "policy_key": policy_key,
                    "identity": {"email": user_email},
                },
            ],
        )

        if not response.ok:
            raise RuntimeError(
                f"fidesops privacy request creation failed! response.status_code={response.status_code}, response.json()={response.json()}"
            )

        created_privacy_requests = (response.json())["succeeded"]
        if len(created_privacy_requests) > 0:
            logger.info(
                f"Created fidesops privacy request for email={user_email} via /api/v1/privacy-request"
            )
