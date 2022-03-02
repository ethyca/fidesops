# How-To: Connect to SaaS Applications

In this section we'll cover

- What is a SaaS connection?
- What is a SaaS config schema?
- How do you configure a SaaS connection?

## What is a SaaS connection?

A SaaS (Software as a Service) connection is a connection type within Fidesops that allows a user to connect to a SaaS application (e.g., Mailchimp, Stripe, Slack, etc.) and execute data access and erasure requests against that application. These connections use functionality introduced in earlier sections (ConnectionConfigs, Datasets, Policies) but also introduce a new SaaS config specification to define how to connect to specific SaaS applications.

## Supported SaaS applications

The current implementation of the SaaS framework can support any SaaS application that uses these features:

- Basic and bearer authentication
- Data access via HTTP GET requests
- Erasure via HTTP PUT requests

The following features are planned for future releases and will allow for the configuration of broader types of connections:

- OAuth 2.0 authentication
- Pagination based on headers ands response contents
- Retry logic based on status codes and response contents

Full examples of a valid SaaS config and Dataset are currently available for Mailchimp.

## What is a SaaS config schema?

A SaaS connector is defined in two parts, the Dataset and the SaaS config. The Dataset describes the data that is available from a connector and the SaaS config describes how to connect and retrieve/update the data in a connector. If you contrast this to a database connector, the ways to retrieve/update data conform to a specification (such as SQL) and are consistent. When accessing data from APIs, each application or even different endpoints within the same application can follow different patterns. It was necessary to have a flexible configuration to be able to define the different access/update patterns.

In short, you can think of the Dataset as the "what" (what data is available from this API) and the SaaS config as the "how" (how to access and erase the data).

A SaaS config schema is broken into the following sections:

- Metadata
- Connector params
- Client config
- Test Request
- Endpoints

### Metadata
This includes the following fields

- `fides_key` used to uniquely identify the connector
- `name` user-friendly name for the connector
- `description` to add any useful descriptions
- `version` used to track different versions of the SaaS config

### Connector params
The `connector_params` field is used to describe a list of settings which a user must configure as part of the setup. This section should just include the name of the parameter but not the actual value. These are added as part of the ConnectionConfig secrets (which we will cover in a later section).

```yaml
connector_params:
    - name: host
    - name: username
    - name: password
```

### Client config
The `client_config` describes the necessary information to be able to create a base HTTP client. Notice that the values for host, username, and password are not defined here, only references in the form of a `connector_param` which Fidesops uses to insert the actual value from the stored secrets.

```yaml
client_config:
  protocol: https
  host:
    connector_param: host
  authentication:
    strategy: basic_authentication
    configuration:
      username:
        connector_param: username
      password:
        connector_param: password
```

The authentication strategies are swappable. In this example we used the `basic_authentication` strategy which uses a `username` and `password` in the configuration. An alternative to this is to use `bearer_authentication` which looks like this:
```yaml
authentication:
strategy: bearer_authentication
configuration:
  token:
    connector_param: api_key
```

### Test Request
Once the base client is defined we can use a `test_request` to verify our hostname and credentials. This is in the form of an idempotent request (usually a read).
```yaml
test_request:
  path: /status
```
### Endpoints
This is where we define how we are going to access and update each collection in the corresponding Dataset.

```yaml
endpoints:
  - name: messages
    requests:
      read:
        path: /3.0/conversations/<conversation_id>/messages
        request_params:
          - name: conversation_id
            type: path
            references:
              - dataset: mailchimp_connector_example
                field: conversations.id
                direction: from
```