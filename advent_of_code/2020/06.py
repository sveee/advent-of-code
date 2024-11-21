import string

from aoc.problem import Problem


class Promblem2020_06(Problem):
    def solve(self, text):
        count_sum1, count_sum2 = 0, 0
        for group in text.split('\n\n'):
            all_yes, common_yes = set(), set(string.ascii_lowercase)
            for yes_questions in group.strip().splitlines():
                common_yes &= set(yes_questions)
                all_yes |= set(yes_questions)
            count_sum1 += len(all_yes)
            count_sum2 += len(common_yes)
        self.part1 = count_sum1
        self.part2 = count_sum2


Promblem2020_06().print_solution()
