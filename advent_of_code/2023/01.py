digit_names = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
digit_map = {digit_str: str(value + 1) for value, digit_str in enumerate(digit_names)}


def calibration_value(line, digits):
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


def part1(text):
    lines = text.splitlines()
    return sum(calibration_value(line, set(digit_map.values())) for line in lines)


def part2(text):
    lines = text.splitlines()
    return sum(
        calibration_value(line, set(digit_map.keys()) | set(digit_map.values()))
        for line in lines
    )
