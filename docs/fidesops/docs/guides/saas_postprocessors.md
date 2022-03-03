# Postprocessors

Postprocessors are, in essence, data transformers. Given data from an endpoint or database, we can add specific processors to transform the data into a format we need for subject requests.

## Configuration

Postprocessors are configured within the `endpoints` section of a `saas_config`


```yaml
endpoints:
  - name: messages
    requests:
      read:
        path: /conversations/<id>/messages
        request_params:
          ...
        postprocessors:
          - strategy: unwrap
            configuration:
              data_path: conversation_messages
          - strategy: filter
            configuration:
              field: from_email
              value:
                identity: email
```

Note: Order matters as its defined in the config. In the above example, unwrap will be run first, then the output of unwrap will be used in the filter strategy.


## Supported Strategies:
- `unwrap`- gets object at given data path.
- `filter`- filters data based on given field value.


### Filter

Filters object or array given field name and value. Value can be reference a dynamic identity passed in through the request OR hard-coded value.

#### Configuration Details

`strategy`: `filter`

`configuration`:

- `field`: `str` that corresponds to the field on which to filter. For example, we wish to filter where `email_contact == "bob@mail.com"`, then `field` will be `email_contact`. Note that filtering an array by a field that's deeply nested is not yet supported.
- `value`: `str` to search for when filtering (e.g. hard-coded `bob@mail.com`) OR Dict` of identity path:
    - `identity`: `str` of identity object from subject request (e.g. `email` or `phone number`)


#### Example

Postprocessor Config:
```yaml
- strategy: filter
    configuration:
      field: email_contact
      value:
        identity: email
```

Identity data passed in through request:

```
{
    "email": "somebody@email.com"
}
```

Data to be processed:
```
data = [
        {
            "id": 1397429347
            "email_contact": "somebody@email.com"
            "name": "Somebody Awesome"
        },
        {
            "id": 238475234
            "email_contact": "somebody-else@email.com"
            "name": "Somebody Cool"
        }
    ]
```

Note: Type casting is not supported at this time. We currently only support filtering by string values. e.g. `bob@mail.com` and not `12344245`.


### Unwrap

Given a path to a dict/list, returns the dict/list at that location.

#### Configuration Details

`strategy`: `unwrap`

`configuration`:

- `data_path`: `str` that gives the path to desired object. E.g. `exact_matches.members` will attempt to get the `members` object on the `exact_matches` object.


#### Example

Postprocessor Config:
```yaml
    - strategy: unwrap
        configuration:
          data_path: exact_matches.members
```

Data to be processed:
```
    data = {
        "exact_matches": {
            "members": [
                {"howdy": 123},
                {"meow": 841}
            ]
        }
    }
    data_path = exact_matches.members
    
```
Result:

```
    result = [
                {"howdy": 123},
                {"meow": 841}
            ]
```


