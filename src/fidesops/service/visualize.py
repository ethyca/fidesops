from typing import Callable, Dict, Tuple

import graphviz

from fidesops.graph.config import (
    ROOT_COLLECTION_ADDRESS,
    TERMINATOR_ADDRESS,
    CollectionAddress,
)


def reformat_node_name(node: CollectionAddress) -> str:
    """Removes the colons from the stringified collection address so they work with graphviz"""
    if node == ROOT_COLLECTION_ADDRESS:
        return "ROOT"
    if node == TERMINATOR_ADDRESS:
        return "TERMINATOR"
    return node.value.replace(":", "\n\n")


def render(
    dsk_dict: Dict[CollectionAddress, Tuple[Callable, CollectionAddress]], filename: str
) -> None:
    """Takes in the dictionary we hand to Dask and builds a visualization

    :param dsk_dict: {CollectionAddress(dataset_name:collection_name): (function to run, *upstream CollectionAddresses)}

    """
    g = graphviz.Digraph("graph", filename=filename, format="png")
    g.attr(rankdir="LR")
    g.attr("node", shape="circle")
    g.node("ROOT")
    g.node("TERMINATOR")
    for node in dsk_dict:
        for dependency in dsk_dict[node][1:]:
            g.edge(reformat_node_name(dependency), reformat_node_name(node))
    g.render()
