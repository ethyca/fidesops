# How-To: Configure Policies


A Policy is a set of instructions, or "Rules", that are executed when a user submits a request to perform an action on their data. Every Rule contains an "execution strategy":

* `action_type`: The action this Rule performs, either `access` (retrieve data) or `erasure` (mask data). Other actions will be added in subsequent releases.

* `storage_destination`: If the `action_type` is `access`, this is the key of a `StorageConfig` object that defines where the data is uploaded.  Currently, Amazon S3 buckets and local filesystem storage are supported. See [How-To: Configure Storage](storage.md) for more information.

* `masking_strategy`: If the `action_type` is `erasure`, this is the key of a Masking object that defines how the obfuscation is implemented. See [How-To: Configure Masking Strategies](masking_strategies.md) for a list of masking strategies. 

In addition to specifying an execution strategy, a Rule contains one or more Data Categories, or "Targets", to which the rule applies. Putting it all together, we have:

```
Policy
  |-> Rules
      |-> Targets
```

This is reflected in the API paths that create these elements:

* `PUT /policy`
* `PUT /policy/{policy_key}/rule`
* `PUT /policy/{policy_key}/rule/{rule_key}/target`

Each operation takes an array of objects, so you can create more than one at a time. 

!!! Be aware that the Policy endpoints are implemented as "create or update" operations. This means that...

    * If a property in the request isn't included in the target object, the property is added.
    * If a property already exists, it's updated.
    * Properties that aren't included in the request aren't affected. 


## Create a Policy

Let's say you want to make a Policy that retrieves a user's email address. You would start by first creating a Policy object:

```
PUT /api/v1/policy

[
  {
    "name": "User Email Address",
    "key": "user_email_address_polcy"
  }
]
```

### Add an Access Rule

The policy creation operation returns a Policy key, which we'll use as a path parameter (`{policy_key}`) when we invoke the operation that adds  a Rule:

```
PUT /api/v1/policy/{policy_key}/rule

[
  {
    "name": "Access User Email Address",
    "key": "access_user_email_address_rule",
    "action_type": "access",
    "storage_destination_key": "storage_key"
  }
]
```

!!! The `storage_key` value must identify an existing StorageConfig object. See  [How-To: Configure Storage](storage.md) for instructions on creating a StorageConfig.

The operation returns a `rule_key`, which we use to add a Target:

```
PUT /api/v1/policy/{policy_key}/rule/{rule_key}/target

[
  {
    "name": "Access User Email Address Target",
    "key": "access_user_email_address_target",
    "data_category": "user.provided.identifiable.contact.email",
  }
]
```

### Add an Erasure Rule

Next, we'll add a Rule that masks the target data by applying the SHA-512 algorithm: 


```
PUT /api/v1/policy/{policy_key}/rule
[
  {
    "name": "Mask Provided Emails",
    "key": "mask-provided-emails",
    "action_type": "erasure",
    "masking_strategy": {
      "strategy": "hash",
      "configuration": {
        "algorithm": "SHA-512"
      },
    },
  },
]
```

Now we add the target -- it's the same target that we used in the access Rule:

```
PUT /api/v1/policy/{policy_key}/rule/{rule_key}/target

[
  {
    "name": "Mask User Email Address Target",
    "key": "mask_user_email_address_target",
    "data_category": "user.provided.identifiable.contact.email",
  }
]
```

## A Note About Masking

When a Policy Rule masks data, it masks the _entire_ branch given by the Target. For example, if we created an `erasure` rule with a Target of `user.provided.identifiable.contact`, _all_ of the information within the `contact` node -- including `user.provided.identifiable.contact.email` -- would be masked.

It's illegal to mask the same data twice within a Policy, so you should take care when you add Targets to a Rule. For example, you can't add `user.provided.identifiable.contact` _and_ `user.provided.identifiable.contact.email`. 

Access rules are always run before erasure rules. 

