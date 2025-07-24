from agi_eggs.netutils.infrastructure_mapper import map_network


def test_map_network():
    peers = {"a": 0.5, "b": 0.9, "c": 0.2}
    mapping = map_network(peers)
    assert list(mapping.keys())[0] == 'b'
