
# Hubspot

## Implementation Summary
Fidesops uses the following Hubspot endpoints to retrieve and delete Personally Identifiable Information (PII) when processing a Data Subject Request (DSR). Right to Access and Right to Delete (Right to Forget) support for each endpoint is noted below.

|Endpoint | Right to Access | Right to Delete |
|----|----|----|
|[Search](https://developers.hubspot.com/docs/api/crm/search) | Yes | No |
|[Contacts](https://developers.hubspot.com/docs/api/crm/contacts) | Yes | Yes |
|[Owners](https://developers.hubspot.com/docs/api/crm/owners) | Yes | No |
|[Communication Preferences](https://developers.hubspot.com/docs/api/marketing-api/subscriptions-preferences#endpoint?spec=POST-/communication-preferences/v3/unsubscribe) | Yes | Yes |
|[Users](https://developers.hubspot.com/docs/api/settings/user-provisioning) | Yes | Yes |



## Connection Settings
Fidesops provides a [Postman collection](../../postman/using_postman.md) for easily establishing connections to your third party applications. Additional connection instructions may be found in the [configuration guide](../saas_config.md).

**Deletion requests** are fulfilled by masking PII via `UPDATE` endpoints. To [give fidesops permission](../../guides/configuration_reference.md#configuration-variable-reference) to remove PII using `DELETE` endpoints, ensure the `masking_strict` variable in your `fidesops.toml` file is set to `false`. 

## Example Hubspot Configuration
```yaml
saas_config:
  fides_key: hubspot_connector_example
  name: Hubspot SaaS Config
  type: hubspot
  description: A sample schema representing the Hubspot connector for Fidesops
  version: 0.0.1

  connector_params:
    - name: domain
      default_value: api.hubapi.com
    - name: private_app_token

  client_config:
    protocol: https
    host: <domain>
    authentication:
      strategy: bearer
      configuration:
        token: <private_app_token>

  test_request:
    method: GET
    path: /companies/v2/companies/paged

  endpoints:
    - name: contacts
      requests:
        read:
          path: /crm/v3/objects/contacts/search
          method: POST
          body: |
            {
              "filterGroups": [{
                "filters": [{
                  "value": "<email>",
                  "propertyName": "email",
                  "operator": "EQ"
                }]
              }]
            }
          query_params:
            - name: limit
              value: 100
          param_values:
            - name: email
              identity: email
          data_path: results
          pagination:
            strategy: link
            configuration:
              source: body
              path: paging.next.link
        update:
          path: /crm/v3/objects/contacts/<contactId>
          method: PATCH
          body: |
            {
              <masked_object_fields>
            }
          param_values:
            - name: contactId
              references:
                - dataset: hubspot_connector_example
                  field: contacts.id
                  direction: from
    - name: owners
      requests:
        read:
          path: /crm/v3/owners
          method: GET
          query_params:
            - name: limit
              value: 100
          param_values:
            - name: placeholder
              identity: email
          postprocessors:
            - strategy: unwrap
              configuration:
                data_path: results
            - strategy: filter
              configuration:
                field: email
                value:
                  identity: email
          pagination:
            strategy: link
            configuration:
              source: body
              path: paging.next.link
    - name: subscription_preferences
      requests:
        read:
          path: /communication-preferences/v3/status/email/<email>
          method: GET
          param_values:
            - name: email
              identity: email
        update:
          path: /communication-preferences/v3/unsubscribe
          method: POST
          body: |
            {
              "emailAddress": "<email>",
              "subscriptionId": "<subscriptionId>",
              "legalBasis": "LEGITIMATE_INTEREST_CLIENT",
              "legalBasisExplanation": "At users request, we opted them out"
            }
          data_path: subscriptionStatuses
          param_values:
            - name: email
              identity: email
            - name: subscriptionId
              references:
                - dataset: hubspot_connector_example
                  field: subscription_preferences.id
                  direction: from
          postprocessors:
            - strategy: filter
              configuration:
                field: status
                value: SUBSCRIBED
    - name: users
      requests:
        read:
          path: /settings/v3/users/
          method: GET
          query_params:
            - name: limit
              value: 100
          param_values:
            - name: placeholder
              identity: email
          postprocessors:
            - strategy: unwrap
              configuration:
                data_path: results
            - strategy: filter
              configuration:
                field: email
                value:
                  identity: email
          pagination:
            strategy: link
            configuration:
              source: body
              path: paging.next.link
        delete:
          path: /settings/v3/users/<userId>
          method: DELETE
          param_values:
            - name: userId
              references:
                - dataset: hubspot_connector_example
                  field: users.id
                  direction: from

```
