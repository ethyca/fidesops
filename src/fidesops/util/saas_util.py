from collections import defaultdict
from typing import Dict, List
from fidesops.graph.config import Collection, Dataset, Field


def merge_fields(target: Field, source: Field):
    """Merges all references and identities into a single field"""
    target.references.extend(source.references)
    if not target.identity:
        target.identity = source.identity
    return target


def extract_fields(aggregate: Dict, collections: List[Collection]) -> None:
    """
    Takes all of the Fields in the given Collection and places them into an
    dictionary (dict[collection.name][field.name]) merging Fields when necessary
    """
    for collection in collections:
        field_dict = aggregate[collection.name]
        for field in collection.fields:
            if field_dict.get(field.name):
                field_dict[field.name] = merge_fields(field_dict[field.name], field)
            else:
                field_dict[field.name] = field


def merge_datasets(target: Dataset, source: Dataset) -> Dataset:
    """Merges all Collections and Fields of two Datasets into a single Dataset"""
    field_aggregate = defaultdict(dict)
    extract_fields(field_aggregate, target.collections)
    extract_fields(field_aggregate, source.collections)

    collections = []
    for collection_name, field_dict in field_aggregate.items():
        collections.append(
            Collection(name=collection_name, fields=list(field_dict.values()))
        )

    return Dataset(
        name=target.name,
        collections=collections,
        connection_key=target.connection_key,
    )
