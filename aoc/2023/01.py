from aoc.problem import Problem

digit_names = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
digit_map = {digit_str: str(value + 1) for value, digit_str in enumerate(digit_names)}


class Promblem2023_01(Problem):
    def calibration_value(self, line, digits):
        n = len(line)
        first_digit = next(
            (
                digit_map.get(word, word)
                for start in range(n)
                for end in range(start + 1, n + 1)
                if (word := line[start:end]) and word in digits
            ),
            '0',
        )
        last_digit = next(
            (
                digit_map.get(word, word)
                for start in range(n - 1, -1, -1)
                for end in range(start + 1, n + 1)
                if (word := line[start:end]) and word in digits
            ),
            '0',
        )
        return int(first_digit + last_digit)

    def solve_input(self, text):
        lines = text.splitlines()
        self.part1 = sum(
            self.calibration_value(line, set(digit_map.values())) for line in lines
        )
        self.part2 = sum(
            self.calibration_value(
                line, set(digit_map.keys()) | set(digit_map.values())
            )
            for line in lines
        )


Promblem2023_01().solve()
