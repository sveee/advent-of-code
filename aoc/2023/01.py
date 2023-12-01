import re
from itertools import chain

from aoc.utils import get_input

text = get_input(day=1, year=2023)
lines = text.splitlines()
digit_names = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
digit_map = {digit_str: str(value + 1) for value, digit_str in enumerate(digit_names)}


def calibration_value(line, digits):
    n = len(line)
    first_digit = next(
        digit_map.get(word, word)
        for start in range(n)
        for end in range(start + 1, n + 1)
        if (word := line[start:end])
        if word in digits
    )
    last_digit = next(
        digit_map.get(word, word)
        for start in range(n - 1, -1, -1)
        for end in range(start + 1, n + 1)
        if (word := line[start:end])
        if word in digits
    )
    return int(first_digit + last_digit)


print(sum(calibration_value(line, set(digit_map.values())) for line in lines))
print(
    sum(
        calibration_value(line, set(chain(digit_map.keys(), digit_map.values())))
        for line in lines
    )
)
