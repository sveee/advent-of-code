def mix(a, b):
    return a ^ b


def prune(a):
    return a % 16777216


def step(n):
    n = prune(mix(n << 6, n))
    n = prune(mix(n >> 5, n))
    n = prune(mix(n << 11, n))
    return n


def repeat(n, k):
    for _ in range(k):
        n = step(n)
    return n


def part1(text, k=2000):
    return sum(repeat(int(n), k) for n in text.splitlines())


def part2(text):
    pass
