# Setting up an Email Connector


## What is the purpose of the Email Connector?

The Email Connector is a ConnectionConfig type that emails a third party to ask them to complete
a Privacy Request when their service cannot be accessed automatically. 

Fidesops will gather details about each collection described on the third party service as part of request execution and 
wait to send a single email to the service after all collections have been visited.  Fidesops does not 
collect confirmation that the erasure was completed by the third party; the EmailConnector is only responsible 
for notifying them.

Importantly, only *erasure* requests are supported at this time for EmailConnectors.  


## What pieces should be configured for an Email Connector?

In short, you will need to create an `email` ConnectionConfig to store minor details about the third party service, and a DatasetConfig
to describe the data contained in their datasource.  You will also need to have configured a separate [EmailConfig](email_communications.md) which
is used system-wide to carry out the actual email send.


## Setting up the ConnectionConfig

Create a ConnectionConfig object with

```json title="<code>PATCH api/v1/connection</code>"
[
  { 
    "name": "Email Connection Config",
    "key": "third_party_email_connector",
    "connection_type": "email",
    "access": "write"
  }
]
```
EmailConnectors must be given "write" access in order to send an email.


## Configuring who to notify

Save a `to_email` on the ConnectionConfig secrets.  This is the user that will be notified via email to complete
an erasure. Only one `to_email` is supported at this time.

Optionally, configure a `test_email` to which you have access, to verify that your setup is working.  Provided your 
EmailConfig is set up properly, you should receive an email similar to the one sent to third-party services, containing
dummy data.

```json title="<code>PUT api/v1/connection/<email_connection_config_key>/secret</code>" 
{
    "test_email": "my_email@example.com",
    "to_email": "third_party@example.com
}
```

## Configuring the dataset

Describe the collections and fields on a third party source with a [DatasetConfig](datasets.md), the same way you'd describe attributes 
on a database.  If you do not know the exact data structure of a third party, you might configure a single collection
with the fields you'd like masked.

As with all collections that support erasures, a primary key must be specified on each collection.


```json title="<code>PUT api/v1/connection/<email_connection_config_key>/dataset" 
[
    {
      "fides_key": "email_dataset",
      "name": "Dataset not accessible automatically",
      "description": "Third party data - will email to request erasure",
      "collections": [
        {
          "name": "daycare_customer",
          "fields": [
            {
              "name": "id",
              "data_categories": [
                "system.operations"
              ],
              "fidesops_meta": {
                "primary_key": true
              }
            },
            {
              "name": "child_health_concerns",
              "data_categories": [
                "user.biometric_health"
              ]
            },
            {
              "name": "user_email",
              "data_categories": [
                "user.contact.email"
              ],
              "fidesops_meta": {
                "identity": "email"
              }
            }
          ]
        }
      ]
    }
]
```

