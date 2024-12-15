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
LEFT_BOX = '['
RIGHT_BOX = ']'
ROBOT = '@'
SPACE = '.'
WALL = '#'

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
            if grid[x][y] in [BOX, LEFT_BOX]:
                total += 100 * x + y
    return total


def find_push_group(r, d, grid):
    if not within_bounds(r, grid):
        return set()

    stack = [r]
    group = set()
    while len(stack) > 0:
        r = stack.pop()
        if (
            grid[r.x][r.y] in [ROBOT, BOX]
            or grid[r.x][r.y] in [LEFT_BOX, RIGHT_BOX]
            and d.x == 0
        ):
            group.add(r)
            if r + d not in group:
                stack.append(r + d)
        elif grid[r.x][r.y] == LEFT_BOX and d.x != 0:
            group.add(r)
            if r + d not in group:
                stack.append(r + d)
            if r + Point(0, 1) not in group:
                stack.append(r + Point(0, 1))
        elif grid[r.x][r.y] == RIGHT_BOX and d.x != 0:
            group.add(r)
            if r + d not in group:
                stack.append(r + d)
            if r + Point(0, -1) not in group:
                stack.append(r + Point(0, -1))
    return group


def do_move(d, grid):
    r = next(
        Point(x, y)
        for x in range(len(grid))
        for y in range(len(grid[0]))
        if grid[x][y] == ROBOT
    )
    group = find_push_group(r, d, grid)
    pushed_group = {(p + d, grid[p.x][p.y]) for p in group}
    if all(grid[p.x][p.y] != WALL for p, _ in pushed_group):
        for p in group:
            grid[p.x][p.y] = SPACE
        for p, v in pushed_group:
            grid[p.x][p.y] = v


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
    tests2()
    grid, moves = text.split('\n\n')
    grid = parse_grid(
        grid.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')
    )
    simulate_moves(grid, moves.replace('\n', ''))
    return gps_coords(grid)


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


def tests2():

    grid = parse_grid(
        '''##############
##......##..##
##..........##
##....[][]@.##
##....[]....##
##..........##
##############'''
    )
    simulate_moves(grid, '<')
    assert (
        grid_to_text(grid)
        == '''##############
##......##..##
##..........##
##...[][]@..##
##....[]....##
##..........##
##############'''
    )
