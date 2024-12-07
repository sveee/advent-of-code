def decode(coded_ops, n, base):
    ops = []
    for _ in range(n):
        ops.append(coded_ops % base)
        coded_ops //= base
    return ops


def can_be_made_true(numbers, total, n_ops):
    n = len(numbers)
    for coded_ops in range(n_ops ** (n - 1)):
        ops = decode(coded_ops, n - 1, n_ops)
        result = numbers[0]
        for i, op in enumerate(ops):
            if op == 0:
                result *= numbers[i + 1]
            elif op == 1:
                result += numbers[i + 1]../advent_of_code/2024/python/07.py
                result = int(str(result) + str(numbers[i + 1]))
        if result == total:
            return True
    return False


def part1(text):
    total = 0
    for line in text.splitlines():
        lhs, rhs = line.split(': ')
        lhs, rhs = int(lhs), list(map(int, rhs.split(' ')))
        if can_be_made_true(rhs, lhs, 2):
            total += lhs
    return total


def part2(text):
    total = 0
    for line in text.splitlines():
        lhs, rhs = line.split(': ')
        lhs, rhs = int(lhs), list(map(int, rhs.split(' ')))
        if can_be_made_true(rhs, lhs, 3):
            total += lhs
    return total
