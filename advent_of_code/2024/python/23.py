from collections import defaultdict


def part1(text):
    graph = defaultdict(set)
    for line in text.splitlines():
        left, right = line.split('-')
        graph[left].add(right)
        graph[right].add(left)

    nodes = sorted(graph)
    cliques_3 = set()
    for node_a in nodes:
        if not node_a.startswith('t'):
            continue

        for node_b in graph[node_a]:
            for node_c in graph[node_b]:
                if node_c != node_a and node_a in graph[node_c]:
                    cliques_3.add(tuple(sorted([node_a, node_b, node_c])))
    return len(cliques_3)


def find_max_clique(node, graph):
    clique = {node}
    prev = node
    while True:
        found = False
        for next in graph[prev]:
            if next not in clique and clique <= graph[next]:
                clique.add(next)
                prev = next
                found = True
        if not found:
            break
    return clique


def part2(text):
    graph = defaultdict(set)
    for line in text.splitlines():
        left, right = line.split('-')
        graph[left].add(right)
        graph[right].add(left)

    max_clique = max([find_max_clique(node, graph) for node in sorted(graph)], key=len)
    return ','.join(sorted(max_clique))
