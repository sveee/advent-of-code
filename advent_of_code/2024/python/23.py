from collections import defaultdict


def part1(text):
    graph = defaultdict(list)

    for line in text.splitlines():
        left, right = line.split('-')
        graph[left].append(right)
        graph[right].append(left)

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


def part2(text):
    pass
