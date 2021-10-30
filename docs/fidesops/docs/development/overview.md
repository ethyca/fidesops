# Development Overview

---

Thanks for contributing to Fidesops! This section of the docs is designed to help you become familiar with how we work, the standards we apply, and how to ensure your contribution is successful.

If you're stuck, don't be shy about asking for help [on GitHub](https://github.com/ethyca/fidesops/issues).

## Getting Started

### Clone Fidesops

To clone fidesops for development, run `git clone https://github.com/ethyca/fidesops.git`.

- Install Docker: https://docs.docker.com/desktop/#download-and-install
- Install Make: `brew install make`
- run `make server` - this spins up the Fastapi server and supporting resources, which you can visit at `http://0.0.0.0:8080`. Check out the docs at `http://0.0.0.0:8000/fidesops/`
- run `make integration-env` to spin up additional postgres, mongo, and mysql databases with test data that you can use to execute privacy requests against
    - Try this out locally with our [Fidesops Postman Collection](../postman/Fidesops.postman_collection.json)
- use `make black`, `make mypy`, and `make pylint` to auto-format code
- use `make check-all` to run the CI checks locally and verify that your code meets project standards
- use `make server-shell` to open a shell on the Docker container, from here you can run useful commands like:
- `ipython` to open a Python shell
- `pytest` to run the tests directly
- `mypy` to run typechecking directly


### Write your code

We have no doubt you can write amazing code! However, we want to help you ensure your code plays nicely with the rest of the Fides ecosystem. Many projects describe code style and documentation as a suggestion; in Fides it's a CI-checked requirement.

* To learn how to style your code, see the [style guide](code_style.md).
* To learn how to document your code, see the [docs guide](documentation.md).
* To learn how to test your code, see the [tests guide](testing.md).
* To learn what format your PR should follow, make sure to follow the [pull request guidelines](pull_requests.md).

### Submit your code

In order to submit code to Fidesops, please:

* [Fork the Fidesops repository](https://help.github.com/en/articles/fork-a-repo)
* [Create a new branch](https://help.github.com/en/desktop/contributing-to-projects/creating-a-branch-for-your-work) on your fork
* [Open a Pull Request](https://help.github.com/en/articles/creating-a-pull-request-from-a-fork) once your work is ready for review
* Once automated tests have passed, a maintainer will review your PR and provide feedback on any changes it requires to be approved. Once approved, your PR will be merged into Fides.

### Congratulations

You're a Fides contributor - welcome to the team! 🎉
