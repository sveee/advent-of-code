

directions = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]


def within_bounds(p, s):
    x, y = p
    n, m = s
    return 0 <= x < n and 0 <= y < m


def part1(text):
    grid = text.splitlines()
    n, m = len(grid), len(grid[0])
    x, y = next(
        (x, y)
        for x in range(n)
        for y in range(m)
        if grid[x][y] == '^'
    )
    di = 0
    visited = set()
    while within_bounds((x, y), (n, m)):
        visited.add((x, y))
        nx, ny = x + directions[di][0], y + directions[di][1]
        if not within_bounds((nx, ny), (n, m)):
            break
        if grid[nx][ny] == '#':
            di = (di + 1) % 4
        else:
            x, y = nx, ny
    return len(visited)



def part2(text):
    pass
