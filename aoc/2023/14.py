
directions = {
    'north': (-1, 0),
    'west': (0, -1),
    'south': (1, 0),
    'east': (0, 1),
}


def roll_direction(grid, direction):
    n, m = len(grid), len(grid[0])
    dx, dy = directions[direction]
    if direction == 'north':
        points = [(x, y) for x in range(n) for y in range(m)]
    elif direction == 'west':
        points = [(x, y) for y in range(m) for x in range(n)]
    elif direction == 'south':
        points = [(x, y) for x in range(n - 1, -1, -1) for y in range(m)]
    elif direction == 'east':
        points = [(x, y) for y in range(m - 1, -1, -1) for x in range(n)]
    for x, y in points:
        if grid[x][y] != 'O':
            continue
        cx, cy = x, y
        while 0 <= cx + dx < n and 0 <= cy + dy < m and grid[cx + dx][cy + dy] == '.':
            cx, cy = cx + dx, cy + dy
        grid[x][y] = '.'
        grid[cx][cy] = 'O'
    return grid


def calculate_load(grid):
    return sum(
        (len(grid) - row_index) * row.count('O') for row_index, row in enumerate(grid)
    )


def part1(text):
    grid = [list(line) for line in text.splitlines()]
    return calculate_load(roll_direction(grid, 'north'))


def part2(text):
    grid = [list(line) for line in text.splitlines()]
    grid_to_step, step_to_grid = {}, {}
    n, cycle_size, cycle_start = 1_000_000_000, 0, 0
    for cycle_id in range(n):
        state = '\n'.join(''.join(row) for row in grid)
        if state in grid_to_step:
            cycle_size, cycle_start = (
                len(grid_to_step) - grid_to_step[state],
                grid_to_step[state],
            )
            break
        grid_to_step[state] = cycle_id
        step_to_grid[cycle_id] = state.splitlines()
        for direction in directions:
            grid = roll_direction(grid, direction)
    return calculate_load(
        step_to_grid[
            (n - cycle_start) % cycle_size + cycle_start if n > cycle_start else n
        ]
    )
