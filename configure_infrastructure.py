"""
...
"""
import os
import sys
from typing import (
    List,
)

DOCKER_WAIT = 5
DOCKERFILE_DATASTORES = [
    "postgres",
    "mysql",
    "mongodb",
    "mssql",
]
EXTERNAL_DATASTORES = [
    "snowflake",
    "redshift",
]
IMAGE_NAME = "fidesops"


def configure_infrastructure(
    run_tests: bool = False,  # Should we run the tests after creating the infra?
    datastores: List[str] = [],  # Which infra should we create? If empty, we create all
) -> None:
    """
    - Create a Docker Compose file path for all datastores specified in `datastores`.
    - Defaults to creating infrastructure for all datastores in `DOCKERFILE_DATASTORES` if none
    are provided.
    - Optionally runs integration tests against those datastores from the container identified
    with `IMAGE_NAME`.
    """

    # Configure docker-compose path
    path: str = "-f docker-compose.yml"
    if len(datastores) == 0:
        os.system(
            f'echo "no datastores specified, configuring infrastructure for all datastores"'
        )
        datastores = DOCKERFILE_DATASTORES + EXTERNAL_DATASTORES
    else:
        os.system(f'echo "datastores specified: {", ".join(datastores)}"')

    for datastore in datastores:
        os.system(f'echo "configuring infrastructure for {datastore}"')
        if datastore in DOCKERFILE_DATASTORES:
            # We only need to locate the docker-compose file if the datastore runs in Docker
            path += f" -f docker-compose.integration-{datastore}.yml"
        elif datastore not in EXTERNAL_DATASTORES:
            # If the specified datastore is not known to us
            os.system(f'echo "Datastore {datastore} is currently not supported"')

    os.system(f'echo "infrastructure path: {path}"')
    os.system(f"docker-compose {path} build")
    os.system(f"docker-compose {path} up -d")
    os.system(f'echo "sleeping for: {DOCKER_WAIT} while infrastructure loads"')
    os.system(f"sleep {DOCKER_WAIT}")

    # Seed datastores with data
    for datastore in datastores:
        setup_path = f"tests/integration_tests/{datastore}-setup.py"
        os.system(
            f'docker-compose {path} run {IMAGE_NAME} python {setup_path} || echo "no custom setup logic found for {datastore}"'
        )

    if run_tests:
        pytest_markers: str = ""
        # Now run the tests
        for datastore in datastores:
            if len(pytest_markers) == 0:
                pytest_markers += f"integration_{datastore}"
            else:
                pytest_markers += f" or integration_{datastore}"

        os.system(f'echo "running pytest for markers: {pytest_markers}"')
        os.system(
            f'docker-compose {path} run {IMAGE_NAME} pytest -m "{pytest_markers}"'
        )

        # Now tear down the infrastructure
        os.system(f"docker-compose {path} down --remove-orphans")
        os.system(f'echo "fin."')


if __name__ == "__main__":
    # Check for Python3 existing
    datastores = []
    run_tests = False
    if len(sys.argv) > 1:
        run_tests = sys.argv[1].split("=") == "true"
        datastores_input = sys.argv[2].split("=")[1].split(",")
        datastores = [ds for ds in datastores_input if ds]

    configure_infrastructure(
        run_tests,
        datastores,
    )
