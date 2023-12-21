
directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def part1(text, n_steps=64):
    grid = text.splitlines()
    n, m = len(grid), len(grid[0])

    start = next(
        (x, y)
        for x in range(n)
        for y in range(m)
        if grid[x][y] == 'S'
    )

    level = {start}

    for n_step in range(n_steps):
        next_level = set()
        for x, y  in level:
            for (dx, dy) in directions:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < n and 0 <= ny < m):
                    continue

                if grid[nx][ny] != '#':
                    next_level.add((nx, ny))
        level = next_level

    return len(level)




def part2(text):
    pass
