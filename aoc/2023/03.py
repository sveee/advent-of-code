import re
from collections import defaultdict

from aoc.utils import get_input

text = get_input(day=3, year=2023)
grid = text.splitlines()

n = len(grid)
m = len(grid[0])


def symbol_neighbours_at(x, y):
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


numbers_with_symbols = []
gear_numbers = defaultdict(list)
for x, line in enumerate(grid):
    for number_match in re.finditer('\d+', line):
        symbols = {
            symbol
            for y in range(number_match.start(), number_match.end())
            for symbol in symbol_neighbours_at(x, y)
        }
        number = int(number_match.group())
        if symbols:
            numbers_with_symbols.append(number)
        for symbol in symbols:
            if grid[symbol[0]][symbol[1]] == '*':
                gear_numbers[symbol].append(number)

print(sum(numbers_with_symbols))
print(
    sum(
        numbers[0] * numbers[1]
        for numbers in gear_numbers.values()
        if len(numbers) == 2
    )
)
