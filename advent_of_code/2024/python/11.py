def f(n, k, cache):
    if (n, k) in cache:
        return cache[(n, k)]

    if k == 0:
        return 1
    if n == 0:
        a = f(1, k - 1, cache)
    else:
        sn = str(n)
        if len(sn) % 2 == 0:
            a = f(int(sn[: len(sn) // 2]), k - 1, cache) + f(
                int(sn[len(sn) // 2 :]), k - 1, cache
            )
        else:
            a = f(n * 2024, k - 1, cache)
    cache[(n, k)] = a
    return a


def part1(text, times=25):
    cache = {}
    return sum(f(int(n), times, cache) for n in text.split())


def part2(text):
    cache = {}
    return sum(f(int(n), 75, cache) for n in text.split())
