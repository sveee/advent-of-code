from functools import reduce
from itertools import groupby


def part1(text):
    lines = text.splitlines()
    operators = lines[-1].strip().split()
    columns = zip(*[map(int, line.strip().split()) for line in lines[:-1]])
    return sum(
        sum(column) if operator == '+' else reduce(lambda x, y: x * y, column)
        for operator, column in zip(operators, columns)
    )


def to_decimal(x, y):
    if y == 0 and x > 0:
        return x
    return 10 * x + y


def part2(text):
    lines = text.splitlines()
    operators = lines[-1].strip().split()
    numbers = [
        reduce(to_decimal, map(lambda x: 0 if x == ' ' else int(x), column))
        for column in zip(*lines[:-1])
    ]
    groups = [
        list(group)
        for is_zero, group in groupby(numbers, lambda x: x == 0)
        if not is_zero
    ]
    return sum(
        sum(group) if operator == '+' else reduce(lambda x, y: x * y, group)
        for operator, group in zip(operators, groups)
    )
