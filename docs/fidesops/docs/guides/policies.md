# How-To: Configure Policies


A Policy is a sets of instructions (or "Rules") that are executed when a user submits a request to retrieve or delete their data (the user makes a "Privacy Request"). Each Rule contains an "execution strategy":

* `action_type`: The action this Rule performs, either `access` (retrieve data) or `erasure` (delete data).

* `storage_destination`: If the `action_type` is `access`, this is the key of a Storage object that defines where the data is uploaded.  Currently, Amazon S3 buckets and local filesystem storage are supported. See [How-To: Configure Storage](storage.md) for more information.

* `masking_strategy`: If the `action_type` is `erasure`, this is the key of a Masking object that defines how the erasure is implemented. See [How-To: Configure Masking Strategies](masking_strategies.md) for a list of masking strategies. 

In addition to specifying an execution strategy, a Rule contains one or more Data Categories, or "Targets", to which the rule applies. 

Putting it altogether, we have Policy -> Rules -> Targets. This is reflected in the API paths that create these elements:

* `PUT /policy`
* `PUT /policy/{policy_key}/rule`
* `PUT /policy/{policy_key}/rule/{rule_key}/target`

Each operation takes an array of objects, so you can create more than one at a time. However, keep in mind that this is a `PUT` so you have to specify the _entire_ set every time you want to make a change to the array.

## Example

Let's say you want to make a Policy that contains rules about a user's email address. You would start by creating a Policy object:

```
PUT /api/v1/policy

[
  {
    "name": "User Email Address",
    "key": "user_email_address_polcy"
  }
]
```

The operation returns a Policy key, which we'll use to add a Rule:

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

Note that `storage_key` must identify an existing Storage object.

Finally, we use the Rule key to add a Target:

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

# A Note About Erasing Data

When a Policy Rule erases data, it erases the _entire_ branch given by the Target. For example, if we created an `erasure` rule with a Target of `user.provided.identifiable.contact`, _all_ of the information within the `contact` node -- including `email` -- would be erased.

It's illegal to erase the same data twice within a Policy, so you should take care when you add Targets to a Rule. For example, you can't add `user.provided.identifiable.contact` _and_ `user.provided.identifiable.contact.email`
"data_category"

