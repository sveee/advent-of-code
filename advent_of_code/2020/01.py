from itertools import combinations

from aoc.problem import Problem


class Promblem2020_01(Problem):
    def solve(self, text):
        numbers = list(map(int, text.splitlines()))
        n = len(numbers)
        for index1 in range(n):
            for index2 in range(index1 + 1, n):
                if numbers[index1] + numbers[index2] == 2020:
                    self.part1 = numbers[index1] * numbers[index2]

        for number1, number2 in combinations(numbers, 2):
            if number1 + number2 == 2020:
                self.part1 = number1 * number2

        for number1, number2, number3 in combinations(numbers, 3):
            if number1 + number2 + number3 == 2020:
                self.part2 = number1 * number2 * number3


Promblem2020_01().print_solution()
