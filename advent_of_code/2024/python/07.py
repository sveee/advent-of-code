from itertools import product


def can_be_made_true(numbers, total, ops):
    n = len(numbers)
    for operations in product(*([ops] * (n - 1))):
        result = numbers[0]
        for i in range(n - 1):
            if operations[i] == '*':
                result *= numbers[i + 1]
            elif operations[i] == '+':
                result += numbers[i + 1]
            elif operations[i] == '||':
                result = int(str(result) + str(numbers[i + 1]))
        if result == total:
            return True
    return False


def part1(text):
    total = 0
    for line in text.splitlines():
        lhs, rhs = line.split(': ')
        lhs, rhs = int(lhs), list(map(int, rhs.split(' ')))
        if can_be_made_true(rhs, lhs, ['*', '+']):
            total += lhs
    return total


def part2(text):
    total = 0
    for line in text.splitlines():
        lhs, rhs = line.split(': ')
        lhs, rhs = int(lhs), list(map(int, rhs.split(' ')))
        if can_be_made_true(rhs, lhs, ['*', '+', '||']):
            total += lhs
    return total
