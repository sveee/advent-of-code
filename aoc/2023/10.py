import sys
from collections import deque

from aoc.problem import Problem

sys.setrecursionlimit(50000)

allowed_directions = {
    '|': ['north', 'south'],
    '-': ['east', 'west'],
    'L': ['north', 'east'],
    'J': ['north', 'west'],
    '7': ['south', 'west'],
    'F': ['south', 'east'],
    'S': ['north', 'south', 'east', 'west'],
}

direction_vectors = {
    'north': (-1, 0),
    'south': (1, 0),
    'west': (0, -1),
    'east': (0, 1),
}
opposite_direction = {
    'north': 'south',
    'south': 'north',
    'west': 'east',
    'east': 'west',
}


def get_neighbours(node, grid):
    neighbours = []
    x, y = node
    for direction in allowed_directions[grid[x][y]]:
        dx, dy = direction_vectors[direction]
        nx, ny = x + dx, y + dy
        if (
            0 <= nx < len(grid)
            and 0 <= ny < len(grid[0])
            and grid[nx][ny] != '.'
            and opposite_direction[direction] in allowed_directions[grid[nx][ny]]
        ):
            neighbours.append((nx, ny))
    return neighbours


def get_max_pipe_distance(grid):
    start = next(
        (x, y)
        for x in range(len(grid))
        for y in range(len(grid[0]))
        if grid[x][y] == 'S'
    )
    queue = deque([start])
    distance = {start: 0}
    while len(queue) > 0:
        node = queue.popleft()
        for next_node in get_neighbours(node, grid):
            if next_node not in distance:
                distance[next_node] = distance[node] + 1
                queue.append(next_node)
    return max(distance.values())


def get_pipe_rec(tile, current_path, visited, start, grid):
    if tile == start and len(current_path) > 2:
        return current_path

    if tile in visited:
        return

    current_path.append(tile)
    visited.add(tile)
    for next_tile in get_neighbours(tile, grid):
        if (
            path := get_pipe_rec(next_tile, current_path, visited, start, grid)
        ) is not None:
            return path
    current_path.pop()
    visited.pop(tile)


def get_pipe(grid):
    start = next(
        (x, y)
        for x in range(len(grid))
        for y in range(len(grid[0]))
        if grid[x][y] == 'S'
    )
    return get_pipe_rec(start, [], set(), start, grid)


def get_doubled_grid(pipe, grid):
    double_grid = [
        ['.' for _y in range(2 * len(grid[0]) + 1)] for _x in range(2 * len(grid) + 1)
    ]
    for index, (x, y) in enumerate(pipe):
        double_grid[2 * x + 1][2 * y + 1] = grid[x][y]

        if index == len(pipe) - 1:
            nx, ny = pipe[0]
        else:
            nx, ny = pipe[index + 1]
        dx, dy = nx - x, ny - y
        double_grid[2 * x + 1 + dx][2 * y + 1 + dy] = '|' if dx != 0 else '-'
    return [''.join(line) for line in double_grid]


def find_enclosed_tiles(grid):
    visited = {}
    component_id = 1
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if (x, y) in visited or grid[x][y] != '.':
                continue

            stack = [(x, y)]
            visited[(x, y)] = component_id
            component_id += 1

            while len(stack) != 0:
                node = stack.pop()
                for dx, dy in direction_vectors.values():
                    nx, ny = node[0] + dx, node[1] + dy
                    if (
                        0 <= nx < len(grid)
                        and 0 <= ny < len(grid[0])
                        and (nx, ny) not in visited
                        and grid[nx][ny] == '.'
                    ):
                        stack.append((nx, ny))
                        visited[(nx, ny)] = visited[node]

    return [node for node, component_id in visited.items() if component_id > 1]


class Problem2023_10(Problem):
    def part1(self, text):
        grid = text.splitlines()
        return get_max_pipe_distance(grid)

    def part2(self, text):
        grid = text.splitlines()
        pipe = get_pipe(grid)
        return sum(
            1
            for tile in find_enclosed_tiles(get_doubled_grid(pipe, grid))
            if tile[0] % 2 == 1 and tile[1] % 2 == 1
        )
