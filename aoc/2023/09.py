from aoc.problem import Problem


def extrapolate_value(sequence):
    if all(value == 0 for value in sequence):
        return 0
    next_bottom = extrapolate_value(
        [value2 - value1 for value1, value2 in zip(sequence, sequence[1:])]
    )
    return sequence[-1] + next_bottom


class Promblem2023_09(Problem):
    def solve(self, text):
        extrapolated_values = []
        for line in text.splitlines():
            extrapolated_values.append(extrapolate_value(list(map(int, line.split()))))
        self.part1 = sum(extrapolated_values)
        self.part2 = None


Promblem2023_09().check_test()
Promblem2023_09().submit()
