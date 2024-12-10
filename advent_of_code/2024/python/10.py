directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def within_bounds(x, y, grid):
    n, m = len(grid), len(grid[0])
    return 0 <= x < n and 0 <= y < m


def trailhead_score(x, y, grid):
    if grid[x][y] == '9':
        return {(x, y)}

    total = set()
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if within_bounds(nx, ny, grid) and ord(grid[nx][ny]) - ord(grid[x][y]) == 1:
            total.update(trailhead_score(nx, ny, grid))
    return total


def trailhead_score2(x, y, grid):
    if grid[x][y] == '9':
        return 1

    total = 0
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if within_bounds(nx, ny, grid) and ord(grid[nx][ny]) - ord(grid[x][y]) == 1:
            total += trailhead_score2(nx, ny, grid)
    return total


def part1(text):
    grid = text.splitlines()
    return sum(
        len(trailhead_score(x, y, grid))
        for x in range(len(grid))
        for y in range(len(grid[0]))
        if grid[x][y] == '0'
    )


def part2(text):
    grid = text.splitlines()
    return sum(
        trailhead_score2(x, y, grid)
        for x in range(len(grid))
        for y in range(len(grid[0]))
        if grid[x][y] == '0'
    )
