from aoc.problem import Problem


def extrapolate_value(sequence, last):
    if all(value == 0 for value in sequence):
        return 0
    prev = extrapolate_value(
        [value2 - value1 for value1, value2 in zip(sequence, sequence[1:])], last
    )
    return sequence[-1] + prev if last else sequence[0] - prev


class Promblem2023_09(Problem):
    def solve(self, text):
        sequences = [list(map(int, line.split())) for line in text.splitlines()]
        self.part1 = sum(
            [extrapolate_value(sequence, last=True) for sequence in sequences]
        )
        self.part2 = sum(
            [extrapolate_value(sequence, last=False) for sequence in sequences]
        )


Promblem2023_09().print_solution()
