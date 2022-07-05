"""Populate saas type to saas config

Revision ID: fc90277bbcde
Revises: ed1b00ff963d
Create Date: 2022-07-05 19:20:59.384767

"""
from typing import List

from alembic import op
from sqlalchemy import text

from fidesops.schemas.saas.saas_config import SaaSType

# revision identifiers, used by Alembic.
revision = "fc90277bbcde"
down_revision = "c7cc36820d4b"
branch_labels = None
depends_on = None


query = text(
    """select datasetconfig.id, dataset from datasetconfig, connectionconfig where connectionconfig.id = datasetconfig.connection_config_id and connectionconfig.connection_type = ConnectionType.saas;
    """
)
update_query = text(
    """update datasetconfig set dataset = jsonb_set(dataset, '{type}', :saas_type) where id = :id"""
)


def upgrade():
    connection = op.get_bind()
    saas_options: List[str] = [saas_type.value for saas_type in SaaSType]
    for id, dataset in connection.execute(query):
        fides_key: str = dataset["fides_key"]
        saas_name: str = dataset["name"]
        try:
            saas_type: str = next(
                (
                    opt
                    for opt in saas_options
                    if any(
                        [
                            fides_key.lower().startswith(opt),
                            saas_name.lower().startswith(opt),
                        ]
                    )
                ),
                "custom",
            )
            connection.execute(update_query, {"saas_type": f'"{saas_type}"', "id": id})
        except Exception:
            # default to using "custom" if something went wrong
            connection.execute(update_query, {"saas_type": f'"custom"', "id": id})


def downgrade():
    connection = op.get_bind()
    for id, dataset in connection.execute(query):
        connection.execute(update_query, {"saas_type": f'"custom"', "id": id})
