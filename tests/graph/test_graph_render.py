from queue import Empty
import graphviz
import json
import pytest

from fidesops.graph.graph import DatasetGraph
from fidesops.graph.traversal import Traversal

from ..task.traversal_data import combined_mongo_posgresql_graph


@pytest.mark.integration
def test_graph_render(integration_mongodb_config, integration_postgres_config) -> None:
    mongo_dataset, postgres_dataset = combined_mongo_posgresql_graph(
        integration_postgres_config, integration_mongodb_config
    )
    graph = DatasetGraph(mongo_dataset, postgres_dataset)
    traversal = Traversal(graph, {"email": "X"})
    traversal_map, _ = traversal.traversal_map()

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

    render_graph(graph_nodes)


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
