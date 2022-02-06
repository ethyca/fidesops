import logging
from typing import Any, Dict
import graphviz
import pytest

from fidesops.graph.graph import DatasetGraph
from fidesops.graph.traversal import Traversal
from fidesops.models.datasetconfig import convert_dataset_to_graph
from fidesops.models.saasconfig import SaaSConfig
from fidesops.schemas.dataset import FidesopsDataset
from fidesops.util.saas_util import merge_datasets

from ..task.traversal_data import combined_mongo_postgresql_graph

logger = logging.getLogger(__name__)

@pytest.mark.saas_connector
def test_saas_render(
    example_saas_configs: Dict[str, Dict], example_saas_datasets
) -> None:
    saas_config = SaaSConfig(**example_saas_configs["mailchimp"])
    mailchimp_config_dataset = saas_config.generate_dataset()
    mailchimp_dataset = convert_dataset_to_graph(
        FidesopsDataset(**example_saas_datasets["mailchimp"]), "mailchimp_connector"
    )

    merged_dataset = merge_datasets(mailchimp_dataset, mailchimp_config_dataset)

    graph = DatasetGraph(merged_dataset)
    traversal = Traversal(graph, {"email": "X"})
    traversal_map, _ = traversal.traversal_map()

    graph_nodes = generate_graph_nodes(traversal_map)
    render_graph(graph_nodes, "mailchimp")

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
    render_graph(graph_nodes, "mongo+postgres")


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


def render_graph(nodes, filename):
    g = graphviz.Digraph("graph", filename=filename, format="png")
    g.attr(rankdir="LR")
    g.attr("node", shape="doublecircle")
    g.node("ROOT")
    g.node("TERMINATOR")
    g.attr("node", shape="circle")
    for (node, collection, link) in nodes:
        g.edge(node, collection, label=link)
    g.render()
