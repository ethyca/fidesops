## What is a Dataset?

A Fidesops _Dataset_ is just the configuration you provide for a database or other queryable datastore. We use the term _Dataset_ and not _Database_ to emphasize that this will ultimately be applicable to a wide variety of datastores beyond traditional databases. With Datasets, a . _Colledction_ is the term used for a SQL table, mongo database collection, or any other  single coherent set values.

## Configuring a Dataset

Beyond collection and field names, Fidesops needs some additional information to fully configure a Dataset. Let's look at a simple example database, and how it would be translated into a configuration in Fidesops.

#### Anexample database
Here we have a simple database of customers and addresses (note the example is a bit simplified from an actual SQL schema) . We have a table of customers, a table of addresses, and customers have an address that is found by following the related address\_id:
```
CREATE TABLE CUSTOMER (
  id INT PRIMARY KEY,
  name VARCHAR,
  email VARCHAR,
  address_id int REFERENCES ADDRESS(id)
 );

CREATE TABLE ADDRESS(
  id INT PRIMARY KEY,
  street VARCHAR,
  city VARCHAR,
  state VARCHAR,
  zip VARCHAR);
```
In Fidesops what we need is a declaration of which fields are of interest, and how they are related. We use the information about their relationship to navigate between different collections. The Fidesops declartion for the above schema would look like this:
```
dataset:
  - fides_key: mydatabase
    name: ...
    description: ...
    collections:
      - name: address
        fields:
	      - name: id
            fidesops_meta:
              primary_key: True
          - name: street
            data_categories: [user.provided.identifiable.contact.street]			  
          - name: city
            data_categories: [user.provided.identifiable.contact.city]
          - name: state
            data_categories: [user.provided.identifiable.contact.state]

          - name: zip
            data_categories: [user.provided.identifiable.contact.postal_code]

      - name: customer
        after: mydatabase.address
        fields:
          - name: address_id
            data_categories: [system.operations]
            fidesops_meta:
              references:
                - dataset: mydatabase
                  field: address.id
                  direction: to
          - name: created
            data_categories: [system.operations]
          - name: email
            data_categories: [user.provided.identifiable.contact.email]
            fidesops_meta:
              identity: email
          - name: id
            data_categories: [user.derived.identifiable.unique_id]
            fidesops_meta:
              primary_key: True
          - name: name
            data_categories: [user.provided.identifiable.name]

```


#### Dataset members

- fides_key: A unique identifier name for the dataset
- collections: A list of addressable collections. 
- after: An optional list of datasets that must be fully traversed before this dataset is queried.

#### Collection members
- name: The name of the collection in your configuration must correspond to the name used for it in your datastore, since it will be used to generate query and update statements. - fields: A list of addressable fields in the collection. Specifying the fields in the collection tells fidesOps what data to address in the collection. 
- after: An optional list of  collections (in the form [dataset name].[collection name] ) that must be fully traversed before this collection is queried.

#### Field members
- name: The name of the field will be used to generate query and update statements. Please note that Fidesops does not do automated schema discovery. It is only aware of the fields you declare. This means that the only fields that will be addressed and retrieved by Fidesops queries are the fields you declare.
- data\_categories: Annotating data\_categories connects fields to policy rules, and determines which actions apply to each field. For more information see [Policies]
- fidesops_meta: The fidesops\_meta section specifies some additional fields that control how fidesops manages your data: 
	- references: _references_ are how you declare relationships between collections. A reference creates a relationship with another collection. Where the configuration declares a references to 'mydatabase:address:id' it means "Fidesops will use the values from mydatabase.address.id to search for related values in customer. Unlike the SQL declaration, this is not an enforceable relationship, but simply a statement of which values are connected.  In the example above, the references from the customer field to "mydatabase.address.id" is analogous to the SQL statement "id _refereences_ address.id", with the exception that any dataset and collection can be referenced. The relationship requires you to specify the dataset as well as the collection for relationships, because you may declare a configuration with multiple datasets, where values in one collection in the first dataset are searched using values found in the second dataset.


     - field: The specified linked field, using the syntax "[dataset name].[collection name ].[field name]". 
	 - direction: An optional value of either "from" or "to". This determines how Fidesops uses the relationships to discover data. If the direction is "to", FidesOps will only use data in the _source_ collection to discover data in the _referenced_ collection. If the direction is "from", FidesOps will only use data in the _referenced_ collection to discover data in the _source_ collection. If the direction is omitted, Fidesops will traverse the relation in whatever direction works to discover all related data.
	 - primary_key: An optional boolean value that means that Fidesops will treat this field as a unique row identifier for generating update statements. If multiple fields are marked as primary keys they will be treated as a combined key - that is, the unique combination of all values of that key will determine a unique row. If no primary key is specified for any field on a collection, no updates will be generated against that collection. 
	 - identity: _identity_ signifies that the declared value may be provided as a starting value to find related data [See graph traversal]
	- data\_type: An _optional_ indication of data type. Data types are necessary to support erasure policies. Available datatypes are string,integer, number, boolean, and mongo\_object\_id. 	 
	- length: An _optional_ indicator of field length. 
 
