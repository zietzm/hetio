import pytest

import hetio.hetnet


def test_creation():
    metaedge_tuples = [
        ('compound', 'disease', 'indication', 'both'),
        ('disease', 'gene', 'association', 'both'),
        ('compound', 'gene', 'target', 'both'),
    ]
    metanode_ids = 'compound', 'disease', 'gene'
    metagraph = hetio.hetnet.MetaGraph.from_edge_tuples(metaedge_tuples)

    # check that nodes got added to metagraph_node_dict
    assert frozenset(metagraph.node_dict) == frozenset(metanode_ids)
    for metanode in metagraph.node_dict.values():
        assert isinstance(metanode, hetio.hetnet.MetaNode)

    # check that metanode.get_id() and hash(metanode) are working as expected
    for metanode_id in metanode_ids:
        metanode = metagraph.node_dict[metanode_id]
        assert metanode.identifier == metanode_id
        assert metanode.get_id() == metanode_id
        assert hash(metanode) == hash(metanode_id)

    graph = hetio.hetnet.Graph(metagraph)
    ms = graph.add_node('disease', 'DOID:2377', 'multiple sclerosis')
    assert ms.metanode.identifier == 'disease'
    assert ms.identifier == 'DOID:2377'
    assert ms.name == 'multiple sclerosis'

    with pytest.raises(KeyError):
        # misordered args
        graph.add_node('DOID:2377', 'multiple sclerosis', 'disease')
