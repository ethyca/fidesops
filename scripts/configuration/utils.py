from datetime import datetime
import logging
from sqlite3 import connect
import requests
import yaml

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from fidesops.ops.api.v1.scope_registry import SCOPE_REGISTRY
from fidesops.ops.api.v1 import urn_registry as urls

import secrets


class QuickstartBase():

    FIDESOPS_URL = "http://webserver:8080"
    BASE_URL = FIDESOPS_URL + urls.V1_URL_PREFIX
    ROOT_CLIENT_ID = "fidesopsadmin"
    ROOT_CLIENT_SECRET = "fidesopsadminsecret"

    # These are external datastores so don't read them from the config
    POSTGRES_SERVER = "host.docker.internal"
    POSTGRES_USER = "postgres"
    POSTGRES_PASSWORD = "postgres"
    POSTGRES_PORT = 6432
    POSTGRES_DB_NAME = "postgres_example"

    def __init__(self, config={}):
        # Override any config passed in
        for key, value in config.items():
            setattr(self, key, value)

        self.configure_oauth_client()
        self.configure_user()
        self.configure_email()
        self.configure_postgres_connector()
        self.configure_s3_storage()
        self.configure_mailchimp_connector()
        self.create_access_request()

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
                return created_client

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


    def configure_user(self):
        """Adds a user with full permissions"""
        response = requests.post(
            f"{self.BASE_URL}{urls.USERS}",
            headers=self.auth_header,
            json={
                "first_name": "Atest",
                "last_name": "User",
                "username": "atestuser",  # TODO: Randomise this
                "password": "Atestpassword1!",
            },
        )

        if not response.ok:
            raise RuntimeError(
                f"fidesops user creation failed! response.status_code={response.status_code}, response.json()={response.json()}"
            )

        user_id = response.json()["id"]

        user_permissions_url = urls.USER_PERMISSIONS.format(user_id=user_id)
        response = requests.post(
            f"{self.BASE_URL}{user_permissions_url}",
            headers=self.auth_header,
            json={"scopes": SCOPE_REGISTRY},
        )

        if not response.ok:
            raise RuntimeError(
                f"fidesops user permissions creation failed! response.status_code={response.status_code}, response.json()={response.json()}"
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
                }
            },
        )

        if not response.ok:
            if response.json()["detail"] != f"Only one email config is supported at a time. Config with key {key} is already configured.":
                raise RuntimeError(
                    f"fidesops email config creation failed! response.status_code={response.status_code}, response.json()={response.json()}"
                )

        # Now add secrets
        email_secrets_path = urls.EMAIL_SECRETS.format(key=key)
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
                logger.info(
                    f"Created fidesops dataset via {url}"
                )
                return response.json()

        raise RuntimeError(
            f"fidesops dataset creation failed! response.status_code={response.status_code}, response.json()={response.json()}"
        )

    def configure_postgres_connector(self, key="postgres_connector"):
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

        connection_secrets_path = urls.CONNECTION_SECRETS.format(key=key)
        url = f"{self.BASE_URL}{connection_secrets_path}"
        response = requests.put(
            url,
            headers=self.auth_header,
            json={
                "host": self.POSTGRES_SERVER,
                "post": self.POSTGRES_PORT,
                "dbname": self.POSTGRES_DB_NAME,
                "username": self.POSTGRES_USER,
                "password": self.POSTGRES_PASSWORD,
            },
        )

        if not response.ok:
            raise RuntimeError(
                f"fidesops connection configuration failed! response.status_code={response.status_code}, response.json()={response.json()}"
            )

        if (response.json())["test_status"] == "failed":
            raise RuntimeError(
                f"fidesops connection test failed! response.status_code={response.status_code}, response.json()={response.json()}"
            )

        logger.info(
            f"Configured fidesops postgres connection secrets for via {url}"
        )

        self.create_dataset(
            connection_key=key,
            yaml_path="data/dataset/postgres_example_test_dataset.yml",
        )

    def configure_mailchimp_connector(self):
        path = urls.SAAS_CONNECTOR_FROM_TEMPLATE.format(saas_connector_type="mailchimp")
        url = f"{self.BASE_URL}{path}"
        response = requests.put(
            url,
            headers=self.auth_header,
            json={
                "instance_key": "mailchimp_instance",
                "secrets": secrets.MAILCHIMP_SECRETS,
                "name": "Mailchimp Connector",
                "description": "Mailchimp ConnectionConfig description",
                "key": "mailchimp_connection_config",
            },
        )

        if not response.ok:
            raise RuntimeError(
                f"fidesops mailchimp connector configuration failed! response.status_code={response.status_code}, response.json()={response.json()}"
            )

    def configure_s3_storage(self, key="s3_storage"):
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
                    }
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
                logger.info(
                    f"Created fidesops storage with key={key} via {url}"
                )

        storage_secrets_path = urls.STORAGE_SECRETS.format(config_key=key)
        url = f"{self.BASE_URL}{storage_secrets_path}"
        response = requests.put(
            url,
            headers=self.auth_header,
            json={
                "aws_access_key_id": secrets.AWS_ACCESS_KEY_ID,
                "aws_access_secret_id": secrets.AWS_ACCESS_SECRET_ID,
            }
        )
    
    def create_access_request(self, user_email="sean+engdemo@ethyca.com"):
        response = requests.post(
            f"{self.BASE_URL}{urls.PRIVACY_REQUEST}",
            json=[
                {
                    "requested_at": str(datetime.utcnow()),
                    "policy_key": "download",
                    "identity": {"email": user_email},
                },
            ],
        )

        if response.ok:
            created_privacy_requests = (response.json())["succeeded"]
            if len(created_privacy_requests) > 0:
                logger.info(
                    f"Created fidesops privacy request for email={user_email} via /api/v1/privacy-request"
                )
                return response.json()

        raise RuntimeError(
            f"fidesops privacy request creation failed! response.status_code={response.status_code}, response.json()={response.json()}"
        )
