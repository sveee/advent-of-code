directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def within_bounds(x, y, n, m):
    return 0 <= x < n and 0 <= y < m


def dfs(x, y, grid):
    if grid[x][y] == '9':
        return {(x, y)}

    total = set()
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if (
            within_bounds(nx, ny, len(grid), len(grid[0]))
            and int(grid[nx][ny]) - int(grid[x][y]) == 1
        ):
            total.update(dfs(nx, ny, grid))
    return total


def dfs2(x, y, grid):
    if grid[x][y] == '9':
        return 1

    total = 0
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if (
            within_bounds(nx, ny, len(grid), len(grid[0]))
            and int(grid[nx][ny]) - int(grid[x][y]) == 1
        ):
            total += dfs2(nx, ny, grid)
    return total


def part1(text):
    grid = text.splitlines()

    total = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == '0':
                total += len(dfs(x, y, grid))
    return total


def part2(text):
    grid = text.splitlines()

    total = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == '0':
                total += dfs2(x, y, grid)
    return total
