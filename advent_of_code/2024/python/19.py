def n_ways(design, towels, cache):
    if design == '':
        return 1

    if design in cache:
        return cache[design]

    ans = 0
    for i in range(min(8, len(design)), 0, -1):
        if design[:i] in towels:
            ans += n_ways(design[i:], towels, cache)
    cache[design] = ans
    return ans


def part1(text):
    left, right = text.split('\n\n')
    towels = set(left.split(', '))
    cache = {}
    return sum(n_ways(design, towels, cache) > 0 for design in right.splitlines())


def part2(text):
    left, right = text.split('\n\n')
    towels = set(left.split(', '))
    cache = {}
    return sum(n_ways(design, towels, cache) for design in right.splitlines())
