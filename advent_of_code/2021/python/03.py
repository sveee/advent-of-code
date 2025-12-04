def part1(text):
    lines = text.splitlines()
    gamma, epsilon = 0, 0
    for column in zip(*lines):
        n_ones = sum(1 for value in column if value == '1')
        more_ones = 2 * n_ones >= len(lines)
        gamma = (gamma << 1) | more_ones
        epsilon = (epsilon << 1) | (not more_ones)
    return gamma * epsilon


def part2(text):
    pass
