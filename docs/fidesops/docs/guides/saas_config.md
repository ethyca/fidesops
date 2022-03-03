## What is a SaaS configuration schema?

A SaaS connector is defined in two parts, the [Dataset](dataset.md) and the SaaS config. The Dataset describes the data that is available from the connector and the SaaS config describes how to connect and retrieve/update the data in the connector. If you contrast this to a [database connector](database_connectors.md), the ways to retrieve/update data conform to a specification (such as SQL) and are consistent. When accessing data from APIs, each application or even different endpoints within the same application can follow different patterns. It was necessary to have a flexible configuration to be able to define the different access/update patterns.

In short, you can think of the Dataset as the "what" (what data is available from this API) and the SaaS config as the "how" (how to access and erase the data).

#### An example SaaS config

This config defines:

- The domain and authentication requirements for an HTTP client to Mailchimp
- A test request for verifying the connection was set up correctly
- Endpoints to the following resources within the Mailchimp API:
    - GET and UPDATE for the `members` resource
    - GET for the `conversations` resource
    - GET for the `messages` resource

```yaml
saas_config:
  fides_key: mailchimp_connector_example
  name: Mailchimp SaaS Config
  description: A sample schema representing the Mailchimp connector for Fidesops
  version: 0.0.1

  connector_params:
    - name: domain
    - name: username
    - name: api_key

  client_config:
    protocol: https
    host:
      connector_param: domain
    authentication:
      strategy: basic_authentication
      configuration:
        username:
          connector_param: username
        password:
          connector_param: api_key

  test_request:
    path: /3.0/lists
    
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
          data_path: conversation_messages
    - name: conversations
      requests:
        read:
          path: /3.0/conversations
          request_params:
            - name: count
              type: query
              default_value: 1000
            - name: offset
              type: query
              default_value: 0
            - name: placeholder
              type: query
              identity: email
    - name: member
      requests:
        read:
          path: /3.0/search-members
          request_params:
            - name: query
              type: query
              identity: email
          data_path: exact_matches.members
        update:
          path: /3.0/lists/<list_id>/members/<subscriber_hash>
          request_params:
            - name: list_id
              type: path
              references:
                - dataset: mailchimp_connector_example
                  field: member.list_id
                  direction: from
            - name: subscriber_hash
              type: path
              references:
                - dataset: mailchimp_connector_example
                  field: member.id
                  direction: from
```


A SaaS config schema is broken into the following sections:

- Metadata
- Connector params
- Client config
- Test request
- Endpoints

#### Metadata
This includes the following fields:

- `fides_key` Used to uniquely identify the connector, this field is used to link a SaaS config to a dataset.
- `name` A human readable name for the connector.
- `description` Used to add a useful description.
- `version` Used to track different versions of the SaaS config.

#### Connector params
The `connector_params` field is used to describe a list of settings which a user must configure as part of the setup. This section should just include the name of the parameter but not the actual value. These are added as part of the ConnectionConfig [secrets](database_connectors.md#set-the-connectionconfigs-secrets)

```yaml
connector_params:
  - name: host
  - name: username
  - name: password
```

#### Client config
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

#### Test request
Once the base client is defined we can use a `test_request` to verify our hostname and credentials. This is in the form of an idempotent request (usually a read). The testing approach is the same for any [ConnectionConfig test](database_connectors.md#testing-your-connection).
```yaml
test_request:
  path: /status
```
#### Endpoints
This is where we define how we are going to access and update each collection in the corresponding Dataset. The endpoint section contains the following members:

- `name` This name corresponds to a Collection in the corresponding Dataset.
- `requests` A map of read and update requests for this collection. Each collection can define a way to read and a way to update the data. Each request is made up of:
    - `path` A static or dynamic resource path. The dynamic portions of the path are enclosed within angle brackets `<dynamic_value>` and are replaced with values from request_params.
    - `request_params`
        - `name` Used as the key for query param values, or to map this param to a value placeholder in the path.
        - `type` Either "query" or "path".
        - `references` This is the same as reference in the Dataset schema. It is used to define the source of the value for the given request_param.
        - `identity` This denotes the identity value that this request_param should take.

## Example scenarios
#### Dynamic path with dataset references
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
In this example, we define `/3.0/conversations/<conversation_id>/messages` as the resource path for messages and define the path param of `conversation_id` as coming from the `id` field of the `conversations` collection. A separate GET HTTP request will be issued for each `conversations.id` value.

```yaml
# For three conversations with IDs of 1,2,3
GET /3.0/conversations/1/messages
GET /3.0/conversations/2/messages
GET /3.0/conversations/2/messages
```

#### Identity as a query param
```yaml
endpoints:
  - name: member
    requests:
      read:
        path: /3.0/search-members
        request_params:
          - name: query
            type: query
            identity: email
```
In this example, the `email` identity value is used as a query param named "query" and would look like this:
```
GET /3.0/search-members?query=name@email.com
```

#### Data update with a dynamic path
```yaml
endpoints:
  - name: member
    requests:
      update:
        path: /3.0/lists/<list_id>/members/<subscriber_hash>
        request_params:
          - name: list_id
            type: path
            references:
              - dataset: mailchimp_connector_example
                field: member.list_id
                direction: from
          - name: subscriber_hash
            type: path
            references:
              - dataset: mailchimp_connector_example
                field: member.id
                direction: from
```
This example uses two dynamic path variables, one from `member.id` and one from `member.list_id`. Since both of these are references to the `member` collection, we must first issue a data retrieval (which will happen automatically if the `read` request is defined). If a call to `GET /3.0/search-members` returned the following `member` object:
```yaml
{
    "list_id": "123",
    "id": "456",
    "merge_fields": {
      "FNAME": "First",
      "LNAME": "Last"
    }
}
```
Then the update request would be:
```yaml
PUT /3.0/lists/123/members/456

{
    "list_id": "123",
    "id": "456",
    "merge_fields": {
      "FNAME": "MASKED",
      "LNAME": "MASKED"
    }
}
```
and the contents of the body would be masked according the the configured [policy](policies.md).