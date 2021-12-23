# How-To: Execute Privacy Requests

In this section we'll cover:

- What is a Privacy Request?
- How can I execute a Privacy Request?
- How do I monitor Privacy Requests as they execute?
- How can I integrate the Privacy Request flow into my existing support tools?

Take me directly to [API docs](/api#operations-Privacy_Requests-get_request_status_api_v1_privacy_request_get).

## What is a Privacy Request?

A Privacy Request represents a request to perform an action on a user's identity data. The Request object itself identifies the user by email address, phone number, social security number, or other identifiable information. The data that will be affected and how it's affected is described in a Policy object that's associated with the Request.

For more information on Policies, see [How-To: Configure Policies](policies.md#rule-attributes).


## How do I submit a Privacy Request?

You submit a Privacy Request by calling the  **Submit a Privacy Request** operation. Here, 
we submit  a request to apply the `a-demo-policy` Policy to all target data in the [Identity Graph](../glossary.md) that can be generated from the email address `identity@example.com` and the phone number `+1 (123) 456 7891`.

`POST /api/v1/privacy-request`

```json
[
  {
    "external_id": "a-user-defined-id",
    "requested_at": "2021-10-31T16:00:00.000Z",
    "policy_key": "a-demo-policy",
    "identities": [{
      "email": "identity@example.com",
      "phone_number: "+1 (123) 456 7891"
    }],
  }
]
```

* `external_id` is an optional  identifier of your own invention that lets you track the Privacy Request. See [How-To: Report on Privacy Requests](reporting.md) for more information.

* `requested_at` is an ISO8601 timestamp that specifies the moment that the request was submitted.

* `policy_key` identifies the Policy object to which this request will be applied. See [How-To: Configure Request Policies](policies.md) for more information.

* `identities` is an array of objects that contain data that identify the users whose data will be affected by the Policy. Each object identifies a single user by AND'ing the object's properties. 


A full list of attributes available to set on the Privacy Request can be found in the [API docs](/api#operations-Privacy_Requests-get_request_status_api_v1_privacy_request_get).


## How do I monitor Privacy Requests as they execute?
Privacy Requests can be monitored at any time throughout their execution by submitting any of the following requests:

`GET api/v1/privacy-request?id=<privacy_request_id>`

`GET api/v1/privacy-request?external_id=<external_id>`

For more detailed examples and further Privacy Request filtering in Fidesops please see [How-To: Report on Privacy Requests](reporting.md).


## How can I integrate the Privacy Request flow into my existing support tools?

Alongside generic API interoperability, Fidesops provides a direct integration with the OneTrust's DSAR automation flow.

* Generic API interoperability: Third party services can be authorized by creating additional OAuth clients. Tokens obtained from OAuth clients can be managed and revoked at any time. See [How-To: Authenticate with OAuth](oauth.md) for more information.

* OneTrust: Fidesops can be configured to act as (or as part of) the fulfillment layer in OneTrust's Data Subject Request automation flow. Please see [How-To: Configure OneTrust Integration](onetrust.md) for more information.
