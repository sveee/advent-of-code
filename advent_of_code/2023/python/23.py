import sys

sys.setrecursionlimit(50000)

allowed_direction = {
    '^': [(-1, 0)],
    'v': [(1, 0)],
    '<': [(0, -1)],
    '>': [(0, 1)],
    '.': [(-1, 0), (1, 0), (0, -1), (0, 1)],
}
UNVISITED = -1


def get_neighbours(posiiton, visited, grid, ignore_slopes):
    x, y = posiiton
    neighbours = []
    for dx, dy in (
        allowed_direction['.'] if ignore_slopes else allowed_direction[grid[x][y]]
    ):
        nx, ny = x + dx, y + dy
        if (
            0 <= nx < len(grid)
            and 0 <= ny < len(grid[0])
            and grid[nx][ny] != '#'
            and (nx, ny) not in visited
        ):
            neighbours.append((nx, ny))
    return neighbours


def get_forking_neighbours(node, visited, forking_nodes, grid, ignore_slopes):
    if node in forking_nodes:
        return {(node, 0)}

    neighbours = set()
    for next_node in get_neighbours(node, visited, grid, ignore_slopes):
        if next_node in visited:
            continue
        visited.add(next_node)
        for fork_node, distance in get_forking_neighbours(
            next_node, visited, forking_nodes, grid, ignore_slopes
        ):
            neighbours.add((fork_node, distance + 1))
        visited.remove(next_node)
    return neighbours


def get_compressed_graph(grid, ignore_slopes):
    forking_nodes = {(0, 1), (len(grid) - 1, len(grid[0]) - 2)}
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == '#':
                continue
            out_degree = len(get_neighbours((x, y), set(), grid, ignore_slopes))
            if out_degree > 2:
                forking_nodes.add((x, y))

    node_to_id = {node: index for index, node in enumerate(sorted(forking_nodes))}
    graph = {index: [] for index in node_to_id.values()}
    for node in sorted(forking_nodes):
        forking_nodes.remove(node)
        for next_node, distance in get_forking_neighbours(
            node, {node}, forking_nodes, grid, ignore_slopes
        ):
            graph[node_to_id[node]].append((node_to_id[next_node], distance))
        forking_nodes.add(node)
    return graph


def find_longest_path(node, end, mask, cache, graph):
    if node == end:
        return 0

    if (node, mask) in cache:
        return cache[(node, mask)]

    longest_path = UNVISITED
    for next_node, distance in graph[node]:
        if ((1 << next_node) & mask) != 0:
            continue
        if (
            next_longest_path := find_longest_path(
                next_node, end, mask | (1 << next_node), cache, graph
            )
        ) != UNVISITED:
            longest_path = max(longest_path, next_longest_path + distance)
    cache[(node, mask)] = longest_path
    return longest_path


def part1(text):
    grid = text.splitlines()
    graph = get_compressed_graph(grid, ignore_slopes=False)
    return find_longest_path(min(graph), max(graph), 1 << min(graph), {}, graph)


def part2(text):
    grid = text.splitlines()
    graph = get_compressed_graph(grid, ignore_slopes=True)
    return find_longest_path(min(graph), max(graph), 1 << min(graph), {}, graph)
