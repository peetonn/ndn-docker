""" Template dicts for nodes """

NODE_TEMPLATES = {
    'h': {
        'type': 'hub',
        'name': None,
        'index': None,
        'label': None,
        'graph_node': None,
        'routes': {},
        'network_shape': {}
    },
    'p': {
        'type': 'producer',
        'name': None,
        'index': None,
        'label': None,
        'graph_node': None,
        'prefix': None,
        'network_shape': {}
    },
    'c': {
        'type': 'consumer',
        'name': None,
        'index': None,
        'label': None,
        'graph_node': None,
        'fetch_from': None,
        'routes': {},
        'network_shape': {}
    }
}
