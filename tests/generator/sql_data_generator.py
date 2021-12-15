from typing import Dict, List, Any

from faker import Faker
from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

from fidesops.db.session import ENGINE
from fidesops.graph.config import Collection, CollectionAddress, Field, FieldAddress
from fidesops.graph.data_type import DataType
from fidesops.graph.graph import Edge, BidirectionalEdge, DatasetGraph
from fidesops.graph.traversal import Traversal, TraversalNode, Row
from tests.graph.graph_test_util import generate_graph_resources, field
Base = declarative_base()


class DataGeneratorFunctions():

    faker = Faker(use_weighting=False)

    def name(cls):
        return cls.faker.name()


def sqlalchemy_datatype(fides_data_type:DataType, **kwargs):
    return {
        DataType.string: Column(String(**kwargs)),
        DataType.integer:Column(Integer(**kwargs)),
        DataType.float:Column(Float(**kwargs)),
        DataType.boolean:Column(Boolean(**kwargs)),
        DataType.object_id: None # not a sqlalchemy supported type
    }[fides_data_type]


def create_sample_value(type_name:str):
    return getattr(DataGeneratorFunctions,type_name)()


t = type(
    "FPaths",
    (Base,),
    {
        "__tablename__": "foo",
        "id": Column(Integer, primary_key=True),
        "path": Column(String(255)),
    },
)
obj = t()
print(obj)


def generate_data_for_traversal( traversal: Traversal,ct:int) -> Dict[CollectionAddress, List[int]]:

    def generate_data(f:Field):
        return create_sample_value(f.data_type or "string" )


    def traversal_collection_fn(  tn: TraversalNode, data: Dict[CollectionAddress, List[Row]]) -> None:
        print(f"tcf: {tn}, {data.keys()}")
        incoming_values = {}
        for edge in tn.incoming_edges():
            if edge.f1.collection_address() in data:
                collection_data = data[edge.f1.collection_address()]
                print(f"field:[{edge.f2.field}] [{edge.f1.field}] [{collection_data}]")
                print(f"field:[{type(edge.f2.field)}] [{type(edge.f1.field)}] [{collection_data}]")
                print(f"incomingvalues={incoming_values}")

                print(f"collection data={collection_data}")
                print("----")
                incoming_values[edge.f2.field] =  [row[edge.f1.field] for row in collection_data]



        max_size = ct
        if incoming_values:
            max_size = min(max_size, *[len(i) for i in incoming_values.values()])
        for f in tn.node.collection.fields:
            if not f.name in incoming_values:
                incoming_values[f.name] = [generate_data(f) for i in range(max_size)]

        data[tn.address] = incoming_values

    env: Dict[CollectionAddress, List[int]] = {}
    traversal.traverse(env, traversal_collection_fn)
    return env


def test_gen() -> None:
    # TEST INIT:
    t = generate_graph_resources(3)
    field(t, ("dr_1", "ds_1", "f1")).references.append(
        (FieldAddress("dr_2", "ds_2", "f1"), None)
    )
    field(t, ("dr_1", "ds_1", "f1")).references.append(
        (FieldAddress("dr_3", "ds_3", "f1"), None)
    )
    field(t, ("dr_1", "ds_1", "f1")).identity = "x"
    graph: DatasetGraph = DatasetGraph(*t)

    assert set(graph.nodes.keys()) == {
        CollectionAddress("dr_1", "ds_1"),
        CollectionAddress("dr_2", "ds_2"),
        CollectionAddress("dr_3", "ds_3"),
    }

    assert graph.identity_keys == {FieldAddress("dr_1", "ds_1", "f1"): "x"}

    assert graph.edges == {
        BidirectionalEdge(
            FieldAddress("dr_1", "ds_1", "f1"), FieldAddress("dr_2", "ds_2", "f1")
        ),
        BidirectionalEdge(
            FieldAddress("dr_1", "ds_1", "f1"), FieldAddress("dr_3", "ds_3", "f1")
        ),
    }

    # extract see nodes
    traversal = Traversal(graph, {"x": 1})

    for k,v in generate_data_for_traversal(traversal,10):
        print(f"{k}=={v}")


















    # print(obj)
    #
    # Base.metadata.create_all(ENGINE)
    #
    # for i in range(10):
    #     print(create_sample_value("full_name"))

        #  generate row (graph, data) // using any input edges for related values
        #  write row
        #     data[ outgoing_edge_address] = [all generated values for this field] for all
        #       edges that have an outgoing edge

    #     if tn.address in data:
    #         data[tn.address].append(traversal_order_fn.counter)
    #     else:
    #         data[tn.address] = [traversal_order_fn.counter]
    #     traversal_order_fn.counter += 1
    #
    # traversal_order_fn.counter = 0
    #
    # env: Dict[CollectionAddress, List[int]] = {}
    # traversal.traverse(env, traversal_order_fn)
    # return env


# # type() takes as argument the new class name, its base
# # classes, and its attributes:
# SubClass = type('SubClass', (BaseClass,), {'set_x': set_x})
# # (More methods can be put in SubClass, including __init__().)
#
# obj = SubClass()
# obj.set_x(42)
# print obj.x  # Prints 42
# print isinstance(obj, BaseClass)  # True

        #  generate row (graph, data) // using any input edges for related values
        #  write row
        #     data[ outgoing_edge_address] = [all generated values for this field] for all
        #       edges that have an outgoing edge

    #     if tn.address in data:
    #         data[tn.address].append(traversal_order_fn.counter)
    #     else:
    #         data[tn.address] = [traversal_order_fn.counter]
    #     traversal_order_fn.counter += 1
    #
    # traversal_order_fn.counter = 0
    #
    # env: Dict[CollectionAddress, List[int]] = {}
    # traversal.traverse(env, traversal_order_fn)
    # return env


# # type() takes as argument the new class name, its base
# # classes, and its attributes:
# SubClass = type('SubClass', (BaseClass,), {'set_x': set_x})
# # (More methods can be put in SubClass, including __init__().)
#
# obj = SubClass()
# obj.set_x(42)
# print obj.x  # Prints 42
# print isinstance(obj, BaseClass)  # True
        #  generate row (graph, data) // using any input edges for related values
        #  write row
        #     data[ outgoing_edge_address] = [all generated values for this field] for all
        #       edges that have an outgoing edge

    #     if tn.address in data:
    #         data[tn.address].append(traversal_order_fn.counter)
    #     else:
    #         data[tn.address] = [traversal_order_fn.counter]
    #     traversal_order_fn.counter += 1
    #
    # traversal_order_fn.counter = 0
    #
    # env: Dict[CollectionAddress, List[int]] = {}
    # traversal.traverse(env, traversal_order_fn)
    # return env


# # type() takes as argument the new class name, its base
# # classes, and its attributes:
# SubClass = type('SubClass', (BaseClass,), {'set_x': set_x})
# # (More methods can be put in SubClass, including __init__().)
#
# obj = SubClass()
# obj.set_x(42)
# print obj.x  # Prints 42
# print isinstance(obj, BaseClass)  # True
