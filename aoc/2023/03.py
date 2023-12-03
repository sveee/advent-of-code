from collections import defaultdict
from dataclasses import dataclass

from aoc.utils import get_input

text = get_input(day=3, year=2023)
grid = text.splitlines()

n = len(grid)
m = len(grid[0])


def is_symbol(c):
    return not c.isdigit() and c != '.'


@dataclass(frozen=True, eq=True)
class Number:
    x: int
    y_start: int
    y_end: int

    @property
    def value(self):
        return int(grid[self.x][self.y_start : self.y_end])


@dataclass(frozen=True, eq=True)
class Symbol:
    x: int
    y: int

    @property
    def value(self):
        return grid[self.x][self.y]


def get_neighbouring_symbols(number: Number):
    symbols = set()
    for y in range(number.y_start, number.y_end):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (dx, dy) == (0, 0):
                    continue
                nx = number.x + dx
                ny = y + dy
                if 0 <= nx < n and 0 <= ny < m and is_symbol(grid[nx][ny]):
                    symbols.add(Symbol(nx, ny))
    return symbols


neighbouring_symbols = {}
for x, line in enumerate(grid):
    y = 0
    while y < m:
        y_start, y_end = y, y + 1
        if line[y_start].isdigit():
            while y_end != m and line[y_end].isdigit():
                y_end += 1
            number = Number(x, y_start, y_end)
            neighbouring_symbols[number] = get_neighbouring_symbols(number)
        y = y_end


neighboring_numbers = defaultdict(list)
for number, symbols in neighbouring_symbols.items():
    for symbol in symbols:
        neighboring_numbers[symbol].append(number)

print(
    sum(
        number.value
        for number, neighborings in neighbouring_symbols.items()
        if neighborings
    )
)
print(
    sum(
        [
            numbers[0].value * numbers[1].value
            for symbol, numbers in neighboring_numbers.items()
            if symbol.value == '*' and len(numbers) == 2
        ]
    )
)
