# Meet Fidesops

_A part of the [greater Fides ecosystem](https://github.com/ethyca/fides)._

[![Latest Version][pypi-image]][pypi-url]
[![License][license-image]][license-url]
[![Code style: black][black-image]][black-url]
[![Checked with mypy][mypy-image]][mypy-url]
[![Fides Discord Server][discord-image]][discord-url]

## :zap: Overview

Fidesops (*fee-dez-äps*, combination of the Latin term "Fidēs" + "operations") is an extensible, deployed engine that fulfills any Data Subject Access Request (DSAR) and Right to be Forgotten (RTBF) request by connecting directly to your databases.

- **Programmable Data Privacy.** Fidesops connects and orchestrates calls to all of your databases in order to access, update and delete sensitive data per your policy configuration (TODO this needs a new name) written in [Fideslang](https://github.com/ethyca/fides).

- **DAGs for Datastores.** Fidesops works by integrating all your data store connections into a unified graph - also known as a DAG. We know that sensitive data is stored all around your dynamic ecosystem, so fidesops builds the DAG at runtime.

- **B.Y.O. DSAR Automation Provider.** Fidesops handles the integration to privacy management tools like OneTrust and Transcend to fulfill Data Subject Requests and returns the package back to the DSAR Automation provider.

- **Built to scale.** Lots of databases? Tons of microservices? Large distributed infrastructure? Connect as many databases and services as you'd like, and let fidesops do the heavy lifting (like auth management, failure retry, and error handling).

## :rocket: Quick Start - Access and Erasure Requests

If you're looking for a more detailed introduction to Fidesops, we recommend following [our tutorial here](https://ethyca.github.io/fidesops/tutorial/). 

Run the quickstart in your terminal to give fidesops a test drive:

```bash
cd fidesops
make quickstart
```
This runs fidesops in docker along with the necessary data stores.  It also spins up a test postgres
database and a test mongo database to mimic your application.  This quickstart will walk you through executing privacy
requests against your system by making a series of API requests to fidesops.

Follow these five easy steps:

1. First, you'll start with setting up some basic configuration (press `[enter]` to make each API request):

- Authenticate by creating an Access Token
- Connect to your application's postgres and mongo databases with ConnectionConfigs 
- Describe the types of data you have and their relationships with Datasets 
- Dictate where to upload your results with StorageConfigs (a local folder for now)


2. Next you'll define a Policy to describe what data you care about and how you want to manage it.

- In this example, you'll create an `access` Policy,`example-request-policy`, to get all data with the data category: `user.provided.identifiable`.
  

3. Finally, you can issue a Privacy Request using Policy `example-request-policy` across your test databases for `jane@example.com`:


- The following response was sent to a local folder for this quickstart.  We've collected identifiable user-provided
information for Jane across tables in both the postgres and mongo databases.

```json
{
   "postgres_example_test_dataset:customer": [
      {
         "email": "jane@example.com",
         "name": "Jane Customer"
      }
   ],
   "postgres_example_test_dataset:address": [
      {
         "city": "Example Mountain",
         "house": 1111,
         "state": "TX",
         "street": "Example Place",
         "zip": "54321"
      }
   ],
   "postgres_example_test_dataset:payment_card": [
      {
         "ccn": 373719391,
         "code": 222,
         "name": "Example Card 3"
      }
   ],
   "mongo_test:customer_details": [
      {
         "gender": "female",
         "birthday": "1990-02-28T00:00:00"
      }
   ]
}
```


4. Now you'll create another Policy, `example-erasure-policy`, that describes how to `erase` data with the same category, by replacing values with null.


5. The last step is to issue a Privacy Request using `example-erasure-policy` to remove identifiable user-provided data related to "jane@example.com".

- We'll re-run step #3 again to see what data is remaining for data category `user.provided.identifiable`:

```json
{}
```
This returns an empty dictionary confirming Jane's fields with data category `user.provided.identifiable` have been removed.


You've learned how to use the fidesops API to connect a database and a final storage location, define policies that describe
how to handle user data, and execute access and erasure requests.  But there's a lot more to discover,
so we'd recommend following [the tutorial](https://ethyca.github.io/fidesops/tutorial/) to keep learning.

## :book: Learn More

Fides provides a variety of docs to help guide you to a successful outcome.

We are committed to fostering a safe and collaborative environment, such that all interactions are governed by the [Fides Code of Conduct](https://github.com/ethyca/solon/blob/main/docs/solon/docs/community/code_of_conduct.md).

### Documentation

Full Fidesops documentation is available [here](https://github.com/ethyca/solon/blob/main/docs/solon/docs/).

### Support

Join the conversation on:

- [Discord](https://discord.gg/NfWXEmCsd4)
- [Twitter](https://twitter.com/ethyca)
- Discussions (TODO need to enable)

### Contributing

Read about the Fides [community](https://github.com/ethyca/solon/blob/main/docs/solon/docs/community/github.md) or dive in to the [development guides](https://github.com/ethyca/solon/blob/main/docs/solon/docs/development/overview.md) for information about contributions, documentation, code style, testing and more.

## :balance_scale: License

The Fides ecosystem of tools is licensed under the [Apache Software License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

[pypi-image]: https://img.shields.io/pypi/v/fidesctl.svg
[pypi-url]: https://pypi.python.org/pypi/fidesctl/
[license-image]: https://img.shields.io/:license-Apache%202-blue.svg
[license-url]: https://www.apache.org/licenses/LICENSE-2.0.txt
[black-image]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black/
[mypy-image]: http://www.mypy-lang.org/static/mypy_badge.svg
[mypy-url]: http://mypy-lang.org/
[discord-image]: https://img.shields.io/discord/730474183833813142.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2
[discord-url]: https://discord.gg/NfWXEmCsd4
