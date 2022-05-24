# How-To: Retrieve Manual Data for a Privacy Request

In this section we'll cover:

- How to describe a manual dataset
- How to send manual data to resume a privacy request

## Overview

Not all data can be automatically retrieved: some data will need to be manually provided by you.
Similar to how you define [datasets](datasets.md) to annotate your owned databases and your third-party
saas integrations, you can define a dataset to describe the types of manual fields you plan to upload
and any dependencies between these manual collections and other collections.

## Describing a manual dataset

In this example, we have a manual dataset with one `storage_unit` collection.  `email` is 
an identity, so this is the field needed to locate the  `box_id` in the storage unit.

You would need to add both a Manual [ConnectionConfig](database_connectors.md) and this Manual Dataset to that ConnectionConfig.

```yaml
dataset:
  - fides_key: manual_input
    name: Manual Dataset
    description: Example of a dataset whose data must be manually retrieved
    collections:
      - name: storage_unit
        fields:
          - name: box_id
            data_categories: [ user.provided ]
            fidesops_meta:
              primary_key: True
          - name: email
            data_categories: [ user.provided.identifiable.contact.email ]
            fidesops_meta:
              identity: email
              data_type: string
```

## Resuming a privacy request with manual input

A privacy request will pause execution when it reaches a manual collection.  An administrator
should manually retrieve the data and send it in a POST request.  The fields 
should match the fields on the paused collection.  

`POST {{host}}/privacy-request/{{privacy_request_id}}/manual_input`

```json
[{
    "box_id": 5,
    "email": "customer-1@example.com"
}]
```

If no manual data can be found on the user's in, simply pass in an empty list to resume the privacy request.

```json
[]
```