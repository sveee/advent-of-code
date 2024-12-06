directions = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]


def within_bounds(x, y, n, m):
    return 0 <= x < n and 0 <= y < m


def simulate_path(sx, sy, di, grid, track_loop: bool):
    n, m = len(grid), len(grid[0])
    visited_states = set()
    x, y = sx, sy
    while within_bounds(x, y, n, m):
        dx, dy = directions[di]

        if track_loop:
            state = (x, y, dx, dy)
            if state in visited_states:
                return 1
            visited_states.add(state)
        else:
            visited_states.add((x, y))

        nx, ny = x + dx, y + dy
        if not within_bounds(nx, ny, n, m):
            break

        if grid[nx][ny] == '#':
            di = (di + 1) % 4
        else:
            x, y = nx, ny
    return len(visited_states) if not track_loop else 0


def part1(text):
    grid = text.splitlines()
    n, m = len(grid), len(grid[0])
    sx, sy = next((x, y) for x in range(n) for y in range(m) if grid[x][y] == '^')
    return simulate_path(sx, sy, 0, grid, track_loop=False)


def part2(text):
    grid = list(map(list, text.splitlines()))
    n, m = len(grid), len(grid[0])
    sx, sy = next((x, y) for x in range(n) for y in range(m) if grid[x][y] == '^')
    total = 0
    for x in range(n):
        for y in range(m):
            if grid[x][y] == '.':
                grid[x][y] = '#'
                total += simulate_path(sx, sy, 0, grid, track_loop=True)
                grid[x][y] = '.'
    return total
