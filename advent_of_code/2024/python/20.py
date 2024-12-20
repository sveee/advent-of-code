from collections import deque

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
    return distance[e]


def part1(text, at_least=100):
    grid = list(map(list, text.splitlines()))

    distance = bfs(grid)
    total_cheats = 0
    for x in range(1, len(grid) - 1):
        for y in range(1, len(grid[0]) - 1):
            if grid[x][y] == WALL:
                grid[x][y] = '.'
                saved_time = distance - bfs(grid)
                if saved_time >= at_least:
                    total_cheats += 1
                grid[x][y] = '#'

    return total_cheats


def part2(text):
    pass
