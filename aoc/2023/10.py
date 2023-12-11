import sys
from collections import deque

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

def get_start(grid):
    return next(
        (x, y)
        for x in range(len(grid))
        for y in range(len(grid[0]))
        if grid[x][y] == 'S'
    )


def get_max_pipe_distance(grid):
    start = get_start(grid)
    queue = deque([start])
    distance = {start: 0}
    while len(queue) > 0:
        node = queue.popleft()
        for next_node in get_neighbours(node, grid):
            if next_node not in distance:
                distance[next_node] = distance[node] + 1
                queue.append(next_node)
    return max(distance.values())


def get_ordered_pipe(grid):
    start = get_start(grid)
    current_node = start
    visited = set([start])
    pipe = []
    while True:
        pipe.append(current_node)
        for next_node in get_neighbours(current_node, grid):
            if next_node == start and len(pipe) > 2:
                return pipe
            if next_node not in visited:
                current_node = next_node
                visited.add(next_node)
                break


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


def part1(text):
    grid = text.splitlines()
    return get_max_pipe_distance(grid)


def part2(text):
    grid = text.splitlines()
    pipe = get_ordered_pipe(grid)
    return sum(
        1
        for tile in find_enclosed_tiles(get_doubled_grid(pipe, grid))
        if tile[0] % 2 == 1 and tile[1] % 2 == 1
    )
