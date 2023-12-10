from aoc.problem import Problem
from collections import deque

pipes = {
    '|': {'north', 'south'},
    '-': {'east', 'west'},
    'L': {'north', 'east'},
    'J': {'north', 'west'},
    '7': {'south', 'west'},
    'F': {'south', 'east'},
}


allowed_directions = {
    (-1, 0): {pipe for pipe, directions in pipes.items() if 'south' in directions},
    (1, 0): {pipe for pipe, directions in pipes.items() if 'north' in directions},
    (0, -1): {pipe for pipe, directions in pipes.items() if 'east' in directions},
    (0, 1): {pipe for pipe, directions in pipes.items() if 'west' in directions},
}


def get_neighbours(node, grid):
    neighbours = []
    x, y = node
    for (dx, dy), pipes in allowed_directions.items():
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[nx][ny] in pipes:
                neighbours.append((nx, ny))
    return neighbours


# test_grid = '''.....
# .F-7.
# .|.|.
# .L-J.
# .....'''.splitlines()

# assert set(
#     get_neighbours(
#         (1, 1),
#         test_grid,
#     )
# ) == {(1, 2), (2, 1)}
# assert set(
#     get_neighbours(
#         (1, 2),
#         test_grid,
#     )
# ) == {(1, 1), (1, 3)}
# assert set(
#     get_neighbours(
#         (1, 3),
#         test_grid,
#     )
# ) == {(1, 2), (2, 3)}
# assert set(
#     get_neighbours(
#         (2, 1),
#         test_grid,
#     )
# ) == {(1, 1), (3, 1)}
# assert set(
#     get_neighbours(
#         (3, 1),
#         test_grid,
#     )
# ) == {(2, 1), (3, 2)}


class Promblem2023_10(Problem):
    def solve(self, text):
        grid = text.splitlines()

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

        self.part1 = max(distance.values())
        self.part2 = None


Promblem2023_10().submit()
