import re


def part1(text):
    n_valid = 0
    for line in text.splitlines():
        value1, value2, letter, password = re.search(
            '(\d+)-(\d+) (\w+): (\w+)', line
        ).groups()
        if int(value1) <= password.count(letter) <= int(value2):
            n_valid += 1
    return n_valid


def part2(text):
    n_valid = 0
    for line in text.splitlines():
        value1, value2, letter, password = re.search(
            '(\d+)-(\d+) (\w+): (\w+)', line
        ).groups()
        target_letters = set([password[int(value1) - 1], password[int(value2) - 1]])
        if letter in target_letters and len(target_letters) == 2:
            n_valid += 1
    return n_valid
