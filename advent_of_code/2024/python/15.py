from typing import NamedTuple, Self


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Point(
            self.x + other.x,
            self.y + other.y,
        )


BOX = 'O'
ROBOT = '@'
SPACE = '.'

DIRECTIONS = {
    '<': Point(0, -1),
    '>': Point(0, 1),
    '^': Point(-1, 0),
    'v': Point(1, 0),
}


def within_bounds(p, grid):
    return 0 <= p.x < len(grid) and 0 <= p.y < len(grid[0])


def gps_coords(grid):
    total = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == BOX:
                total += 100 * x + y
    return total


def do_move(d, grid):
    r = next(
        Point(x, y)
        for x in range(len(grid))
        for y in range(len(grid[0]))
        if grid[x][y] == ROBOT
    )
    group = []
    while within_bounds(r, grid) and grid[r.x][r.y] in [ROBOT, BOX]:
        group.append(r)
        r += d
    if within_bounds(r, grid) and grid[r.x][r.y] == SPACE:
        for p in group[::-1]:
            grid[p.x + d.x][p.y + d.y] = grid[p.x][p.y]
        if group:
            grid[p.x][p.y] = SPACE


def simulate_moves(grid, moves):
    for move in moves.replace('\n', ''):
        do_move(DIRECTIONS[move], grid)


def parse_grid(text):
    return list(map(list, text.splitlines()))


def grid_to_text(grid):
    return '\n'.join(''.join(line) for line in grid)


def part1(text):
    tests1()
    grid, moves = text.split('\n\n')
    grid = parse_grid(grid)
    simulate_moves(grid, moves.replace('\n', ''))
    return gps_coords(grid)


def part2(text):
    pass


def tests1():
    grid = parse_grid(
        '''#######
#...O..
#......'''
    )
    assert gps_coords(grid) == 104
    grid = parse_grid(
        '''########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########'''
    )
    simulate_moves(grid, '<')
    assert (
        grid_to_text(grid)
        == '''########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########'''
    )
    simulate_moves(grid, '^')
    assert (
        grid_to_text(grid)
        == '''########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########'''
    )
    simulate_moves(grid, '^')
    assert (
        grid_to_text(grid)
        == '''########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########'''
    )
    simulate_moves(grid, '>')
    assert (
        grid_to_text(grid)
        == '''########
#..@OO.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########'''
    )
    simulate_moves(grid, '>')
    assert (
        grid_to_text(grid)
        == '''########
#...@OO#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########'''
    )
    simulate_moves(grid, '>')
    assert (
        grid_to_text(grid)
        == '''########
#...@OO#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########'''
    )
    simulate_moves(grid, 'v')
    assert (
        grid_to_text(grid)
        == '''########
#....OO#
##..@..#
#...O..#
#.#.O..#
#...O..#
#...O..#
########'''
    )
    simulate_moves(grid, 'v')
    assert (
        grid_to_text(grid)
        == '''########
#....OO#
##..@..#
#...O..#
#.#.O..#
#...O..#
#...O..#
########'''
    )
    simulate_moves(grid, '<')
    assert (
        grid_to_text(grid)
        == '''########
#....OO#
##.@...#
#...O..#
#.#.O..#
#...O..#
#...O..#
########'''
    )
    simulate_moves(grid, 'v')
    assert (
        grid_to_text(grid)
        == '''########
#....OO#
##.....#
#..@O..#
#.#.O..#
#...O..#
#...O..#
########'''
    )
    simulate_moves(grid, '>')
    assert (
        grid_to_text(grid)
        == '''########
#....OO#
##.....#
#...@O.#
#.#.O..#
#...O..#
#...O..#
########'''
    )
    simulate_moves(grid, '>')
    assert (
        grid_to_text(grid)
        == '''########
#....OO#
##.....#
#....@O#
#.#.O..#
#...O..#
#...O..#
########'''
    )
    simulate_moves(grid, 'v')
    assert (
        grid_to_text(grid)
        == '''########
#....OO#
##.....#
#.....O#
#.#.O@.#
#...O..#
#...O..#
########'''
    )
    simulate_moves(grid, '<')
    assert (
        grid_to_text(grid)
        == '''########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########'''
    )
    simulate_moves(grid, '<')
    assert (
        grid_to_text(grid)
        == '''########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########'''
    )
    assert gps_coords(grid) == 2028
