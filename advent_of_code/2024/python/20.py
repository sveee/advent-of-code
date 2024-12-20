from collections import deque
from typing import NamedTuple

directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]

WALL = '#'


def locate_value(v, grid):
    return next(
        (x, y) for x in range(len(grid)) for y in range(len(grid[0])) if grid[x][y] == v
    )


class Node(NamedTuple):
    x: int
    y: int
    level: int


def bfs(grid):
    s = locate_value('S', grid)
    e = locate_value('E', grid)
    queue = deque([s])
    distance = {s: 0}
    while len(queue) > 0:
        x, y = queue.popleft()
        if (x, y) == e:
            break
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < len(grid)
                and 0 <= ny < len(grid[0])
                and (nx, ny) not in distance
                and grid[nx][ny] != WALL
            ):
                distance[(nx, ny)] = distance[(x, y)] + 1
                queue.append((nx, ny))
    shortest_path = [Node(x, y, level) for (x, y), level in distance.items()]
    return sorted(shortest_path, key=lambda x: x.level)


def get_distance(node1, node2):
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)


def n_cheats(grid, size, at_least):
    shortest_path = bfs(grid)
    total_cheats = 0
    for index, node1 in enumerate(shortest_path):
        for node2 in shortest_path[index + 1 :]:
            distance = get_distance(node1, node2)
            if distance <= size and node2.level - node1.level - distance >= at_least:
                total_cheats += 1
    return total_cheats


def part1(text, at_least=100):
    grid = list(map(list, text.splitlines()))
    return n_cheats(grid, 2, at_least)


def part2(text, at_least=100):
    grid = list(map(list, text.splitlines()))
    return n_cheats(grid, 20, at_least)
