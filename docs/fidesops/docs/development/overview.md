# Development Overview

---

Thanks for contributing to fidesops! This section of the docs is designed to help you become familiar with how we work, the standards we apply, and how to ensure your contribution is successful.

If you're stuck, don't be shy about asking for help [on GitHub](https://github.com/ethyca/fidesops/issues).

## Getting started with fidesops in Docker

The recommended way to run fidesops is to launch it with Docker and Docker Compose. `Make` commands wrap docker-compose 
commands to give you different functionality.

### System Requirements 

1. Install Docker: https://docs.docker.com/desktop/#download-and-install
2. Install [`nox`](https://nox.thea.codes/en/stable/) 
   1. `pip install nox`
3. [Create a fork of fidesops](https://docs.github.com/en/get-started/quickstart/fork-a-repo) 
4. Clone your fork `git clone https://github.com/<your-fork-location>/fidesops.git`
5. `cd fidesops`

### Available `nox -s` commands
- `build` - Build the Docker containers.
- `push` - Push the Docker image to Dockerhub.
- `ci_suite` - Runs all of the CI checks, except for 'pytest_external'.
- `black` - Run the 'black' style linter.
- `isort` - Run the 'isort' import linter.
- `mypy` - Run the 'mypy' static type checker.
- `pylint` - Run the 'pylint' code linter.
- `xenon` - Run 'xenon' code complexity monitoring.
- `check_install` - Check that fidesops is installed.
- `pytest_unit` - Runs all unit tests except those that talk to integration databases.
- `pytest_integration` - Runs all integration tests, except those on external datastores.
- `pytest_integration_external` - Run all tests that rely on the third-party databases and services.
- `pytest_saas` - Run all saas tests that rely on the third-party databases and services.
- `dev` - Spin up the entire application and open a development shell.
- `dev_with_worker` - Spin up the entire application with a dedicated worker, and open a development shell.
- `quickstart` - runs a quick, five minute quickstart that talks to the fidesops API to execute privacy requests.
- `docs_build` - Build docs from the source code.
- `docs_serve` - spins up just the docs, which you can visit at `http://0.0.0.0:8000/fidesops/`
- `docs_check` - Check that the docs can build.
- `create_user` - Create a super user in the fidesops database.
- `seed_test_data` - Seed test data in the Postgres application database.
- `db(init)` - Run commands against the database.
- `db(reset)` - Run commands against the database.
- `clean` - Clean up docker containers, remove orphans, remove volumes
- `teardown` - Tear down the docker dev environment.

#### Issues 

- MSSQL: Known issues around connecting to MSSQL exist today for Apple M1 users. M1 users that wish to install `pyodbc` locally, please reference the workaround [here](https://github.com/mkleehammer/pyodbc/issues/846).

- Package not found: When running `docker-compose up`, if you get a `importlib.metadata.PackageNotFoundError: fidesops`, do `nox -s dev`,
and then run `pip install -e .`. Verify fidesops is installed with `pip list`.


## Write your code

See the [contributing details](contributing_details.md) guide to get familiar with writing and testing API endpoints, database models, and more. 

We want to help you ensure your code plays nicely with the rest of the fidesops ecosystem. Many projects describe code style and documentation as a suggestion; in fidesops it's a CI-checked requirement.

* To learn how to style your code, see the [style guide](code_style.md).
* To learn how to document your code, see the [docs guide](documentation.md).
* To learn how to test your code, see the [tests guide](testing.md).
* To learn what format your PR should follow, make sure to follow the [pull request guidelines](pull_requests.md).


## Submit your code

In order to submit code to fidesops, please:

* [Fork the fidesops repository](https://help.github.com/en/articles/fork-a-repo)
* Add the original as a remote (I'm naming it `upstream`), to keep your fork in sync
  ```bash
  git remote add upstream https://github.com/ethyca/fidesops.git
  ```
* [Create a new branch](https://help.github.com/en/desktop/contributing-to-projects/creating-a-branch-for-your-work) on your fork
  ```bash
    git checkout main 
    git fetch upstream 
    git merge upstream/main 
    git push origin main 
    git checkout -b my-new-branch
    git push origin my-new-branch 
    ```
* [Open a Pull Request](https://help.github.com/en/articles/creating-a-pull-request-from-a-fork) once your work is ready for review
  * Submit the pull request from *your* repo. Pull requests should be submitted with a clear description of the issue being handled, including links to any external specifications or Github issues. PRs should not be merged by the person submitting them, except in rare and urgent circumstances.
  * Once automated tests have passed, a maintainer will review your PR and provide feedback on any changes it requires to be approved. Once approved, your PR will be merged into fidesops.
  

## Congratulations

You're a fidesops contributor - welcome to the team! 🎉
