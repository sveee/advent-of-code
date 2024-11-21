from collections import Counter, defaultdict
from functools import reduce


def part1(text):
    graph = defaultdict(list)
    edges_to_remove = {
        ('ljh', 'tbg'),
        ('qnv', 'mnh'),
        ('mfs', 'ffv'),
    }
    # examples edges
    # edges_to_remove = {
    #     ('hfx', 'pzl'),
    #     ('bvb', 'cmg'),
    #     ('nvd', 'jqt'),
    # }
    edges = []
    for line in text.splitlines():
        node, next_nodes = line.split(': ')
        next_nodes = next_nodes.split()
        for next_node in next_nodes:
            edges.append((node, next_node))
        next_nodes = [
            next_node
            for next_node in next_nodes
            if (node, next_node) not in edges_to_remove
            and (next_node, node) not in edges_to_remove
        ]
        graph[node].extend(next_nodes)
        for next_node in next_nodes:
            graph[next_node].append(node)
    components = {}
    component_id = 0
    for node in list(graph):
        if node in components:
            continue
        components[node] = component_id
        component_id += 1
        stack = [node]
        while len(stack) > 0:
            current_node = stack.pop()
            for next_node in graph.get(current_node, []):
                if next_node not in components:
                    components[next_node] = components[current_node]
                    stack.append(next_node)

    assert component_id == 2, component_id
    return reduce(lambda x, y: x * y, Counter(components.values()).values())


def part2(text):
    pass
