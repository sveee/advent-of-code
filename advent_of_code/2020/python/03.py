from functools import reduce

directions = [
    (1, 1),
    (1, 3),
    (1, 5),
    (1, 7),
    (2, 1),
]


def find_n_trees_encountered(grid, direction):
    x, y = 0, 0
    dx, dy = direction

    n_trees_encountered = 0
    while x < len(grid):
        if grid[x][y] == '#':
            n_trees_encountered += 1
        x, y = x + dx, y + dy
        if y >= len(grid[0]):
            y -= len(grid[0])
    return n_trees_encountered


def part1(text):
    grid = text.splitlines()
    return find_n_trees_encountered(grid, directions[1])


def part2(text):
    grid = text.splitlines()
    return reduce(
        lambda x, y: x * y,
        [find_n_trees_encountered(grid, direction) for direction in directions],
    )
