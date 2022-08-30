# Custom SaaS Requests

When creating a SaaS connection, fidesops provides the option to override the default configuration with a custom Python function to process an access or erasure request. 

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