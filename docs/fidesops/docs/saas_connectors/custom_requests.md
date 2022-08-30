# Custom SaaS Requests

Fidesops provides the option to override a SaaS connection's default configuration with a custom Python function. Implementing a custom request override allows you to process access or erasure requests which cannot be described by a standard configuration file, or which need more complex post-processing and pagination.

## Define a custom request

To use a request override in your SaaS Config, your request must include a `request_override` field along with the request's `param_values`. 

For more information on building a request and the required fields, see the [SaaS Config guide](saas_config.md).

```yaml
endpoints:
    - name: messages
      requests:
        read:
          request_override: mailchimp_messages_access
          param_values:
            - name: conversation_id
              references:
                - dataset: mailchimp_override_connector_example
                  field: conversations.id
                  direction: from
```

| Field | Description |
|----|----|
| `request_override` | The name of the registered override function. |
| `param_values` | The request parameters. See the [SaaS config](saas_config.md/#param-values-in-more-detail) for options. |
| `grouped_inputs` | *Optional.*  A list of reference fields whose inputs are dependent upon one another. See the [SaaS config](saas_config.md#endpoints) for options. |

The above YAML snippet replaces the usual `read` request fields with the required fields `request_override` and `param_values`. Only `grouped_inputs` is permitted as an optional additional field. 

Including any other fields will result in an invalid request.

## Create and register your override function

The string value of `request_override` is used by fidesops to call a registered function for additional processing. 

```py
#register your function - note the name matches the request_override
@SaaSRequestOverrideFactory.register(
    "mailchimp_messages_access", [SaaSRequestType.READ]
)
def mailchimp_messages_access(
    node: TraversalNode,
    policy: Policy,
    privacy_request: PrivacyRequest,
    input_data: Dict[str, List[Any]],
    secrets: Dict[str, Any],
) -> List[Row]:

    # gather you request params
    conversation_ids = input_data.get("conversation_id")

    # build and execute the request for each input data value
    processed_data = []
    if conversation_ids:
        for conversation_id in conversation_ids:
            try:
                response = get(
                    url=f'https://{secrets["domain"]}/3.0/conversations/{conversation_id}/messages',
                    auth=(secrets["username"], secrets["api_key"]),
                )

            # here we mimic the sort of error handling done in the core framework
            # by the AuthenticatedClient. Extenders can chose to handle errors within
            # their implementation as they wish.
            except Exception as exc:  # pylint: disable=W0703
                if config.dev_mode:  # pylint: disable=R1720
                    raise ConnectionException(
                        f"Operational Error connecting to Mailchimp API with error: {exc}"
                    )
                else:
                    raise ConnectionException(
                        "Operational Error connecting to MailchimpAPI."
                    )
            if not response.ok:
                raise ClientUnsuccessfulException(status_code=response.status_code)

            # unwrap and post-process response
            response_data = pydash.get(response.json(), "conversation_messages")
            filtered_data = pydash.filter_(
                response_data,
                {"from_email": privacy_request.get_cached_identity_data().get("email")},
            )

            # build up final result
            processed_data.extend(filtered_data)

    return processed_data
  ```

    Above is an example Python function to add additional processing to a Mailchimp connector. 