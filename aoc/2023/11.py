from aoc.problem import Problem


def get_empty_rows(grid):
    return {
        row_index
        for row_index, row in enumerate(grid)
        if all(value == '.' for value in row)
    }


def get_empty_columns(grid):
    return {
        column_index
        for column_index in range(len(grid[0]))
        if all(grid[row_index][column_index] == '.' for row_index in range(len(grid)))
    }


def get_total_distance(grid, scale):
    galaxies = [
        (x, y)
        for x in range(len(grid))
        for y in range(len(grid[0]))
        if grid[x][y] == '#'
    ]
    empty_rows = get_empty_rows(grid)
    empty_columns = get_empty_columns(grid)
    total_distance = 0
    for index, (x1, y1) in enumerate(galaxies):
        for x2, y2 in galaxies[index + 1 :]:
            distance = abs(x2 - x1) + abs(y2 - y1)
            for x in empty_rows:
                if min(x1, x2) <= x <= max(x1, x2):
                    distance += scale - 1
            for y in empty_columns:
                if min(y1, y2) <= y <= max(y1, y2):
                    distance += scale - 1
            total_distance += distance
    return total_distance


class Problem2023_11(Problem):
    def part1(self, text):
        grid = text.splitlines()
        return get_total_distance(grid, 2)

    def part2(self, text, scale=1_000_000):
        grid = text.splitlines()
        return get_total_distance(grid, scale)
