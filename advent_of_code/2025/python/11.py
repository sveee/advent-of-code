def dfs(node, graph, memo):
    if node in memo:
        return memo[node]

    if node not in graph or not graph[node]:
        return 1

    total = 0
    for next_node in graph[node]:
        total += dfs(next_node, graph, memo)
    memo[node] = total
    return total


def part1(text):
    graph = {}
    for line in text.splitlines():
        start, *ends = line.split()
        graph[start[:-1]] = ends
    start = 'you'
    return dfs(start, graph, {})


def subgraph(sink, graph):
    rev_graph = {}
    for start, ends in graph.items():
        for end in ends:
            if end not in rev_graph:
                rev_graph[end] = []
            rev_graph[end].append(start)

    result = {sink}
    stack = [sink]
    while stack:
        node = stack.pop()
        if node in rev_graph:
            for parent in rev_graph[node]:
                if parent not in result:
                    result.add(parent)
                    stack.append(parent)

    new_graph = {}
    for node in result:
        new_graph[node] = [child for child in graph.get(node, []) if child in result]
    return new_graph


def part2(text):
    graph = {}
    for line in text.splitlines():
        start, *ends = line.split()
        graph[start[:-1]] = ends

    graph1 = subgraph('fft', graph)
    n_paths1 = dfs('svr', graph1, {})
    graph2 = subgraph('dac', graph)
    n_paths2 = dfs('fft', graph2, {})
    n_paths3 = dfs('dac', graph, {})
    return n_paths1 * n_paths2 * n_paths3
