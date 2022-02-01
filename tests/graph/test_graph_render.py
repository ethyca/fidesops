from collections import defaultdict
import logging
from typing import Any, Dict, List
import graphviz
import pytest

from fidesops.graph.graph import DatasetGraph
from fidesops.graph.traversal import Traversal
from fidesops.graph.config import (
    Collection,
    Dataset,
    Field,
    FieldAddress,
    SaaSConfig,
    ScalarField,
)
from fidesops.models.datasetconfig import convert_dataset_to_graph
from fidesops.schemas.dataset import FidesopsDataset

from ..task.traversal_data import combined_mongo_postgresql_graph

logger = logging.getLogger(__name__)


def saas_config_to_dataset(saas_config: SaaSConfig):
    collections = []
    for endpoint in saas_config.endpoints:
        fields = []
        for parameter in endpoint.request_params["read"].parameters:
            if parameter.references:
                references = []
                for reference in parameter.references:
                    first, *rest = reference.field.split(".")
                    references.append(
                        (
                            FieldAddress(reference.dataset, first, *rest),
                            reference.direction,
                        )
                    )
                fields.append(ScalarField(name=parameter.name, references=references))
            if parameter.identity:
                fields.append(
                    ScalarField(name=parameter.name, identity=parameter.identity)
                )
        if fields:
            collections.append(Collection(name=endpoint.name, fields=fields))
    return Dataset(
        name=saas_config.name,
        collections=collections,
        connection_key=saas_config.fides_key,
    )


@pytest.mark.integration
def test_saas_config_to_dataset(example_saas_configs: Dict[str, Dict]):
    # convert endpoint references to datset references to be able to hook SaaS connectors into the graph traversal
    saas_config = SaaSConfig(**example_saas_configs["mailchimp"])
    mailchimp_dataset = saas_config_to_dataset(saas_config)

    messages_collection = mailchimp_dataset.collections[0]
    member_collection = mailchimp_dataset.collections[1]
    query_field = member_collection.fields[0]
    conversation_id_field = messages_collection.fields[0]
    conversations_reference = conversation_id_field.references[0]
    field_address, direction = conversations_reference

    assert messages_collection.name == "messages"
    assert conversation_id_field.name == "conversation_id"
    assert field_address == FieldAddress("mailchimp_connector", "conversations", "id")
    assert direction == "from"

    assert query_field.name == "query"
    assert query_field.identity == "email"


def merge_fields(target: Field, source: Field):
    """Merges all references and identities into a single field"""
    target.references.extend(source.references)
    if not target.identity:
        target.identity = source.identity
    return target


def extract_fields(aggregate: Dict, collections: List[Collection]) -> None:
    """
    Takes all of the Fields in the given Collection and places them into an
    dictionary (dict[collection.name][field.name) merging Fields when necessary
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


def mailchimp_dataset() -> Dataset:
    conversations = Collection(
        name="conversations",
        fields=[ScalarField(name="id")],
    )

    return Dataset(
        name="mailchimp_connector",
        collections=[conversations],
        connection_key="mailchimp_connector",
    )


def mailchimp_config() -> Dataset:
    member = Collection(
        name="member",
        fields=[ScalarField(name="query", identity="email")],
    )
    conversations = Collection(
        name="conversations",
        fields=[ScalarField(name="placeholder", identity="email")],
    )
    messages = Collection(
        name="messages",
        fields=[
            ScalarField(
                name="conversation_id",
                references=[
                    (FieldAddress("mailchimp_connector", "conversations", "id"), "from")
                ],
            ),
        ],
    )

    return Dataset(
        name="mailchimp_connector",
        collections=[member, conversations, messages],
        connection_key="mailchimp_connector",
    )


def manually_merged_dataset() -> Dataset:
    member = Collection(
        name="member",
        fields=[ScalarField(name="query", identity="email")],
    )
    conversations = Collection(
        name="conversations",
        fields=[
            ScalarField(name="placeholder", identity="email"),
            ScalarField(name="id"),
        ],
    )
    messages = Collection(
        name="messages",
        fields=[
            ScalarField(
                name="conversation_id",
                references=[
                    (FieldAddress("mailchimp_connector", "conversations", "id"), "from")
                ],
            ),
        ],
    )

    return Dataset(
        name="mailchimp_connector",
        collections=[member, conversations, messages],
        connection_key="mailchimp_connector",
    )


@pytest.mark.integration
def test_saas_render(
    example_saas_configs: Dict[str, Dict], example_saas_datasets
) -> None:
    saas_config = SaaSConfig(**example_saas_configs["mailchimp"])
    mailchimp_config_dataset = saas_config_to_dataset(saas_config)
    mailchimp_dataset = convert_dataset_to_graph(
        FidesopsDataset(**example_saas_datasets["mailchimp"]), "mailchimp_connector"
    )

    merged_dataset = merge_datasets(mailchimp_dataset, mailchimp_config_dataset)

    graph = DatasetGraph(merged_dataset)
    traversal = Traversal(graph, {"email": "X"})
    traversal_map, _ = traversal.traversal_map()

    graph_nodes = generate_graph_nodes(traversal_map)
    render_graph(graph_nodes)


@pytest.mark.integration
def test_mongo_postgres_render(
    integration_mongodb_config, integration_postgres_config
) -> None:
    mongo_dataset, postgres_dataset = combined_mongo_postgresql_graph(
        integration_postgres_config, integration_mongodb_config
    )
    graph = DatasetGraph(mongo_dataset, postgres_dataset)
    traversal = Traversal(graph, {"email": "X"})
    traversal_map, _ = traversal.traversal_map()

    graph_nodes = generate_graph_nodes(traversal_map)
    render_graph(graph_nodes)


def generate_graph_nodes(traversal_map: Any):
    graph_nodes = []
    for node, edges in traversal_map.items():
        if len(edges["to"]):
            for collection, link in edges["to"].items():
                node = (
                    node.replace(":", "\n\n") if node != "__ROOT__:__ROOT__" else "ROOT"
                )
                graph_nodes.append(
                    (node, collection.replace(":", "\n\n"), list(link)[0])
                )
        else:
            graph_nodes.append((node.replace(":", "\n\n"), "TERMINATOR", ""))
    return graph_nodes


def render_graph(nodes):
    g = graphviz.Digraph("graph", filename="postgres+mongo", format="png")
    g.attr(rankdir="LR")
    g.attr("node", shape="doublecircle")
    g.node("ROOT")
    g.node("TERMINATOR")
    g.attr("node", shape="circle")
    for (node, collection, link) in nodes:
        g.edge(node, collection, label=link)
    g.render()
