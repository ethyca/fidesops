"""Contains the nox sessions used during CI checks."""
import nox
from constants_nox import (
    CI_ARGS,
    COMPOSE_SERVICE_NAME,
    RUN_NO_DEPS,
    START_APP,
    WITH_TEST_CONFIG,
)
from docker_nox import build
from utils_nox import teardown

@nox.session()
def ci_suite(session: nox.Session) -> None:
    """
    Runs all of the CI checks, except for 'pytest_external'.

    Excludes 'pytest_external' so that no additional secrets/tooling are required.
    """
    teardown(session)
    build(session, "test")
    black(session)
    isort(session)
    xenon(session)
    mypy(session)
    pylint(session)
    check_install(session)
    pytest(session, "unit")
    pytest(session, "integration")


# Static Checks
@nox.session()
def black(session: nox.Session) -> None:
    """Run the 'black' style linter."""
    command = (
        *RUN_NO_DEPS,
        "black",
        "--check",
        "src",
        "tests",
        "noxfiles",
    )
    session.run(*command, external=True)


@nox.session()
def isort(session: nox.Session) -> None:
    """Run the 'isort' import linter."""
    command = (*RUN_NO_DEPS, "isort", "src", "tests", "noxfiles", "--check")
    session.run(*command, external=True)


@nox.session()
def mypy(session: nox.Session) -> None:
    """Run the 'mypy' static type checker."""
    command = (*RUN_NO_DEPS, "mypy")
    session.run(*command, external=True)


@nox.session()
def pylint(session: nox.Session) -> None:
    """Run the 'pylint' code linter."""
    command = (*RUN_NO_DEPS, "pylint", "src", "noxfiles")
    session.run(*command, external=True)


@nox.session()
def xenon(session: nox.Session) -> None:
    """Run 'xenon' code complexity monitoring."""
    command = (
        "xenon",
        "noxfiles",
        "src",
        "tests",
        "--max-absolute B",
        "--max-modules B",
        "--max-average A",
        "--ignore 'data, docs'",
        "--exclude src/fidesops/_version.py",
    )
    session.run(*command, external=True)


@nox.session()
def check_install(session: nox.Session) -> None:
    """Check that fidesops is installed."""
    session.install(".")
    run_command = ("fidesops", *(WITH_TEST_CONFIG), "--version")
    session.run(*run_command)


# Pytest
@nox.session()
@nox.parametrize(
    "mark",
    [
        nox.param("unit", id="unit"),
        nox.param("integration", id="integration"),
        nox.param("not external", id="not-external"),
    ],
)
def pytest(session: nox.Session, mark: str) -> None:
    """Runs tests."""
    session.notify("teardown")
    session.run(*START_APP, external=True)
    run_command = (
        *RUN_NO_DEPS,
        "pytest",
        "-x",
        "-m",
        mark,
    )
    session.run(*run_command, external=True)


@nox.session()
def pytest_integration_external(session: nox.Session) -> None:
    """Run all tests that rely on the third-party databases and services."""
    session.notify("teardown")
    run_command = (
        "docker-compose",
        "run",
        "-e",
        "ANALYTICS_OPT_OUT",
        "-e",
        "REDSHIFT_TEST_URI",
        "-e",
        "SNOWFLAKE_TEST_URI",
        "-e",
        "REDSHIFT_TEST_DB_SCHEMA",
        "-e",
        "BIGQUERY_KEYFILE_CREDS",
        "-e",
        "BIGQUERY_DATASET",
        "--rm",
        CI_ARGS,
        COMPOSE_SERVICE_NAME,
        "pytest",
        "-m",
        "integration_external",
    )
    session.run(*run_command, external=True)


@nox.session()
def pytest_saas(session: nox.Session) -> None:
    """Run all tests that rely on the third-party databases and services."""
    session.notify("teardown")
    run_command = (
        "docker-compose",
        "run",
        "-e",
        "ANALYTICS_OPT_OUT",
        "-e",
        "VAULT_ADDR",
        "-e",
        "VAULT_NAMESPACE",
        "-e",
        "VAULT_TOKEN",
        "--rm",
        CI_ARGS,
        COMPOSE_SERVICE_NAME,
        "pytest",
        "-m",
        "integration_saas",
    )
    session.run(*run_command, external=True)
