# Connect to SaaS Applications

## What is a SaaS connection?

A SaaS (Software as a Service) connection allows a user to connect to a third-party SaaS application (e.g., Mailchimp, Stripe, Slack, etc.), and include that application in fidesops-managed data access and erasure requests. Additional guides are available on [creating Connections](../guides/database_connectors.md#create-a-connectionconfig-object), defining [Datasets](../guides/datasets.md), and configuring [SaaS applications](saas_config.md).

## Supported SaaS applications

The current Connection framework can support any SaaS application that uses these features:

- Basic auth, bearer auth, OAuth2 (Authorization Code Flow)
- Data access via HTTP requests
- Erasure via HTTP requests
- Pagination based on headers and response contents

[Examples](https://github.com/ethyca/fidesops/tree/main/data/saas) of valid connection and Dataset configurations are currently available for multiple applications.

## Configure a SaaS connector

The fidesops [Postman](../postman/using_postman.md) collection includes the necessary requests to configure a SaaS connector. Additionally, you can view the live, interactive [Swagger](https://swagger.io/docs/) API docs by visiting `/docs` on a running instance of fidesops.

1. Create a Connection of type `saas`
```json title="<code>PATCH api/v1/connection</code>"
[
  {
    "name": "SaaS Application",
    "key": {saas_key},
    "connection_type": "saas",
    "access": "read"
  }
]
```

| Field | Description 
|---|---|
| `name` | A human-readable name for your SaaS application.
| `key` | A string that uniquely identifies this Connection.
| `connection_type` | `saas` to establish a new SaaS Connection.
| `access` | Sets the connection's permissions. 


2. Add a [SaaS Config](saas_config.md) (in JSON format). 
```json title="<code>PATCH api/v1/connection/{saas_key}/saas_config</code>"
{
    "fides_key": "mailchimp_connector_example",
    "name": "Mailchimp SaaS Config",
    "type": "mailchimp",
    "description": "A sample schema representing the Mailchimp connector for fidesops"
    ...
}
```

3. Configure the secrets. The SaaS config must already defined to provide validation for the secrets.
```json title="<code>PUT api/v1/connection/{saas_key}/secret</code>"
{
  "domain": "{mailchimp_domain}",
  "username": "{mailchimp_username}",
  "api_key": "{mailchimp_api_key}"
}
```

4. Add a [Dataset](../guides/datasets.md) (in JSON format).
```json title="<code>PUT api/v1/connection/{saas_key}/dataset</code>"
[
  {
    "fides_key":"mailchimp_connector_example",
    "name":"Mailchimp Dataset",
    "description":"A sample dataset representing the Mailchimp connector for fidesops",
    "collections":[
      {
        "name":"messages"
    ...
      }
  }
]
```

## API constraints
These constraints are enforced by the API validation: 

1. A SaaS connector dataset cannot have any `identities` or `references` in the `fidesops_meta`. These relationships must be defined in the [SaaS config](saas_config.md).
2. SaaS config references can only have a direction of `from`.
3. The `fides_key` between the SaaS config and the Dataset must match to associate the two together.