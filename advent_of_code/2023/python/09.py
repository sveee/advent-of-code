def extrapolate_value(sequence, do_last):
    if all(value == 0 for value in sequence):
        return 0
    prev = extrapolate_value(
        [value2 - value1 for value1, value2 in zip(sequence, sequence[1:])], do_last
    )
    return sequence[-1] + prev if do_last else sequence[0] - prev


def part1(text):
    sequences = [list(map(int, line.split())) for line in text.splitlines()]
    return sum([extrapolate_value(sequence, do_last=True) for sequence in sequences])


def part2(text):
    sequences = [list(map(int, line.split())) for line in text.splitlines()]
    return sum([extrapolate_value(sequence, do_last=False) for sequence in sequences])
