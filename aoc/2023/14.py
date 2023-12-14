
from copy import deepcopy


north = (-1, 0)


def roll_north(grid):
    grid = deepcopy(grid)
    n, m = len(grid), len(grid[0])
    dx, dy = north
    for x in range(n):
        for y in range(m):
            if grid[x][y] != 'O':
                continue
            cx, cy = x, y
            while 0 <= cx + dx < n  and 0 <= cy + dy < m and grid[cx+ dx][cy + dy] == '.':
                cx, cy = cx + dx, cy + dy
            grid[x][y] = '.'
            grid[cx][cy] = 'O'
    return grid


def calculate_load(grid):
    return sum(
        (len(grid) - row_index) * row.count('O')
        for row_index, row in enumerate(grid)
    )


def part1(text):
    grid = [
        list(line)
        for line in text.splitlines()
    ]
    return calculate_load(roll_north(grid))


def part2(text):
    pass
