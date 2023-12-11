import re
from collections import defaultdict


def symbol_neighbours_at(x, y, n, m, grid):
    symbol_neighbours = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < n
                and 0 <= ny < m
                and not grid[nx][ny].isdigit()
                and grid[nx][ny] != '.'
            ):
                symbol_neighbours.append((nx, ny))
    return symbol_neighbours


def part1(text):
    grid = text.splitlines()
    n = len(grid)
    m = len(grid[0])
    numbers_with_symbols = []
    for x, line in enumerate(grid):
        for number_match in re.finditer('\d+', line):
            symbols = {
                symbol
                for y in range(number_match.start(), number_match.end())
                for symbol in symbol_neighbours_at(x, y, n, m, grid)
            }
            number = int(number_match.group())
            if symbols:
                numbers_with_symbols.append(number)

    return sum(numbers_with_symbols)


def part2(text):
    grid = text.splitlines()
    n = len(grid)
    m = len(grid[0])
    gear_numbers = defaultdict(list)
    for x, line in enumerate(grid):
        for number_match in re.finditer('\d+', line):
            symbols = {
                symbol
                for y in range(number_match.start(), number_match.end())
                for symbol in symbol_neighbours_at(x, y, n, m, grid)
            }
            number = int(number_match.group())
            for sx, sy in symbols:
                if grid[sx][sy] == '*':
                    gear_numbers[(sx, sy)].append(number)
    return sum(
        numbers[0] * numbers[1]
        for numbers in gear_numbers.values()
        if len(numbers) == 2
    )
