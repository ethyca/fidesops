# How-To: Execute Privacy Requests

In this section we'll cover:

- What is a Privacy Request?
- How does a Privacy Rquest work in conjunction with a policy?
- How can I execute a Privacy Request?
- How do I monitor Privacy Requests as they execute?
- How can I integrate the Privacy Request flow into my existing support tools?
- Specifying encryption of access request results 
- Decrypting access request results

Take me directly to [API docs](/api#operations-Privacy_Requests-get_request_status_api_v1_privacy_request_get).

## What is a Privacy Request?
A Privacy Request in its simplest form describes a request by a user, to process data pertaining to their identity. Privacy Requests are currently supported in two forms, `access` and `erasure`. For more information on action types, please see [How-To: Configure Request Policies](policies.md#rule-attributes).


#### How does a Privacy Request work in conjunction with a Policy?
A Privacy Request must always be associated with a pre-configured `Policy`. While a Privacy Request describes _whose_ data to process, a `Policy` describes _how_ to process that data.


## How can I execute a Privacy Request?
Privacy Requests can be executed by submitting them to Fidesops via the Privacy Request API as follows:

`POST /api/v1/privacy-request`

```
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

#### Note:

- This request will submit a Privacy Request for execution that applies the `a-demo-policy` Policy to all target data in the [Identity Graph](../glossary.md) that can be generated from the email address `identity@example.com` or the phone number `+1 (123) 456 7891`.
- Specifying a `external_id` enables us to track this Privacy Request with that `external_id` later on. See [How-To: Report on Privacy Requests](reporting.md) for more information.
- `policy_key` should correspond to a previously configured `Policy` object. See [How-To: Configure Request Policies](policies.md) for more information.
- A full list of attributes available to set on the Privacy Request can be found in the [API docs](/api#operations-Privacy_Requests-get_request_status_api_v1_privacy_request_get).


## How do I monitor Privacy Requests as they execute?
Privacy Requests can be monitored at any time throughout their execution by submitting any of the following requests:

`GET api/v1/privacy-request?id=<privacy_request_id>`

`GET api/v1/privacy-request?external_id=<external_id>`

For more detailed examples and further Privacy Request filtering in Fidesops please see [How-To: Report on Privacy Requests](reporting.md).


## How can I integrate the Privacy Request flow into my existing support tools?
Alongside generic API interopoerability, Fidesops provides a direct integration with the OneTrust's DSAR automation flow.

- Generic API interoperability: Third party services can be authorized by creating additional OAuth clients. Tokens obtained from OAuth clients can be managed and revoked at any time. Pleae see [How-To: Authenticate with OAuth](oauth.md) for more information.
- OneTrust: Fidesops can be configured to act as (or as part of) the fulfilment layer in OneTrust's Data Subject Request automation flow. Please see [How-To: Configure OneTrust Integration](onetrust.md) for more information.


## Encryption

You can optionally encrypt your access request results by supplying an `encryption_key` string in the request body:
We will use the supplied encryption_key to encrypt the contents of your JSON and CSV results using an AES algorithm in GCM mode.
When converted to bytes, your encryption_key must be 16 bytes long.

POST /privacy-request
```json
[
    {
        "requested_at": "2021-08-30T16:09:37.359Z",
        "identities": [{"email": "customer-1@example.com"}],
        "policy_key": "my_access_policy",
        "encryption_key": "test--encryption"
    }
]

```

## Decrypting your access request results

If you specified an encryption key, we encrypted the access result data using your key and an internally-generated `nonce` with an AES 
algorithm in GCM mode.  The return value is the nonce plus the encrypted data. 

For example, pretend you specified an encryption key of "test--encryption", and the resulting data was uploaded to
S3 in a JSON file: `d71a5dc3c49d7n7QN+tueapbID9CC48QWX6MoIUdzm6M8aH+VdLagsOm/Wk0Gz+q51tehcgM9DdTFJizA3m+joA=`.  You will
need to implement something similar to the snippet below on your end to decrypt:

```python
import json
from fidesops.util.encryption.aes_gcm_encryption_scheme import decrypt

encrypted = "d71a5dc3c49d7n7QN+tueapbID9CC48QWX6MoIUdzm6M8aH+VdLagsOm/Wk0Gz+q51tehcgM9DdTFJizA3m+joA=" 
encryption_key = "test--encryption".encode("utf-8")  # Only you know this
nonce = encrypted[0:12].encode("utf-8")
encrypted_data = encrypted[12:]
decrypted = decrypt(encrypted_data, encryption_key, nonce)
```

```bash
>>> json.loads(decrypted)
{'street': 'test street', 'state': 'NY'}
```

If CSV data was uploaded, each CSV in the zipfile was encrypted using a different nonce so you'll need to follow
a similar process for each csv file.