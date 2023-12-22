directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def part1(text, n_steps=64):
    grid = text.splitlines()
    n, m = len(grid), len(grid[0])
    start = next((x, y) for x in range(n) for y in range(m) if grid[x][y] == 'S')
    level = {start}
    for _n_step in range(n_steps):
        next_level = set()
        for x, y in level:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < n and 0 <= ny < m):
                    continue

                if grid[nx][ny] != '#':
                    next_level.add((nx, ny))
        level = next_level
    return len(level)


def count_free_in_row(n, pattern):
    k = len(pattern)
    q = n // k
    r = n % k
    return q * pattern[::2].count('.') + pattern[:r:2].count('.')


def part2(text, n_steps=26501365):
    grid = text.splitlines()
    n, m = len(grid), len(grid[0])
    sx, sy = next((x, y) for x in range(n) for y in range(m) if grid[x][y] == 'S')
    grid = [line.replace('S', '.') for line in grid]
    total_free = 0
    for x in range(-n_steps, n_steps + 1):
        y = -n_steps + abs(x)
        px, py = (sx + x + n * n_steps) % n, (sy + y + m * n_steps) % m
        pattern = grid[px][py:] + grid[px] + grid[px][:py]
        # print(x, y)
        # print(pattern, count_free_in_row(2 * (n_steps - abs(x)) + 1, pattern))
        total_free += count_free_in_row(2 * (n_steps - abs(x)) + 1, pattern)

    return total_free
