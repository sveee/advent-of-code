import re

from aoc.problem import Problem


class Promblem2020_02(Problem):
    def solve(self, text):
        n_valid1, n_valid2 = 0, 0
        for line in text.splitlines():
            value1, value2, letter, password = re.search(
                '(\d+)-(\d+) (\w+): (\w+)', line
            ).groups()
            if int(value1) <= password.count(letter) <= int(value2):
                n_valid1 += 1
            target_letters = set([password[int(value1) - 1], password[int(value2) - 1]])
            if letter in target_letters and len(target_letters) == 2:
                n_valid2 += 1
        self.part1 = n_valid1
        self.part2 = n_valid2


Promblem2020_02().print_solution()
