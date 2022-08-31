# Configure Email Communications
## What is email used for?

An email server can be configured such that Fidesops can send outbound emails to both subjects and, to be supported in the future, data processors.

Supported modes of use:

- Subject Identity Verification - for more information on identity verification in subject requests, see the [Privacy Requests](privacy_requests.md#subject-identity-verification) guide.


## Prerequisites

At the moment, Fidesops only supports configuring with Mailgun, so you'll need a pre-existing Mailgun account to get up and running with email communications.

In Mailgun, you'll need to generate an API Key.

When you sign up for Mailgun, a primary account API key is generated. This key allows you to perform all CRUD operations via API endpoints across all sending domains. 

For this reason, we recommend setting up a `domain sending key` in Mailgun for use in Fidesops. A `domain sending key` only allows for sending messages via one domain. Visit the [Mailgun Authentication Docs](https://documentation.mailgun.com/en/latest/api-intro.html#authentication-1) for more information on setting up this domain sending API key.

## Configuration

### Create email config

```json title="<code>POST api/v1/email/config"
{
    "key": "{{email_config_key}}",
    "name": "mailgun",
    "service_type": "mailgun",
    "details": {
        "domain": "your.mailgun.domain"
    }
}
```

Params:

- `key` (optional): A unique key used to manage your email config. This is auto-generated from `name` if left blank. Accepted values are alphanumeric, `_`, and `.`.
- `name`: A unique user-friendly name for your email config.
- `service_type`: Email service. Fidesops only supports `mailgun` at the moment.

Additional params for Mailgun:

- `details`: A dict of key/val config vars specific to Mailgun
  - `domain`: Your unique Mailgun domain.
  - `is_eu_domain` (optional): A boolean that denotes whether your Mailgun domain was created in the EU region. Defaults to `False`.
  - `api_version` (optional): A string that denotes api version. Defaults to `v3`.


### Add secrets for email config

#### Mailgun

```json title="<code>POST api/v1/email/config/{{email_config_key}}/secret"
{
    "mailgun_api_key": "nc123849ycnpq98fnu"
}

```

Params:

- `mailgun_api_key`: Your mailgun api key or domain sending API key.

