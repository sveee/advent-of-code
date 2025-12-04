def part1(text):
    lines = text.splitlines()
    gamma, epsilon = 0, 0
    for column in zip(*lines):
        n_ones = sum(1 for value in column if value == '1')
        more_ones = 2 * n_ones >= len(lines)
        gamma = (gamma << 1) | more_ones
        epsilon = (epsilon << 1) | (not more_ones)
    return gamma * epsilon


def get_rating(lines, co2_scrubber=False):
    n = len(lines[0])
    for i in range(n):
        if len(lines) == 1:
            break
        column = [line[i] for line in lines]
        n_ones = sum(1 for value in column if value == '1')
        n_zeros = len(lines) - n_ones
        if co2_scrubber:
            target_bit = '0' if 2 * n_zeros <= len(lines) else '1'
        else:
            target_bit = '1' if 2 * n_ones >= len(lines) else '0'
        lines = [line for line in lines if line[i] == target_bit]
    return int(lines[0], 2)


def part2(text):
    lines = text.splitlines()
    return get_rating(lines, co2_scrubber=False) * get_rating(lines, co2_scrubber=True)
