import string


def part1(text):
    count_sum = 0
    for group in text.split('\n\n'):
        all_yes = set()
        for yes_questions in group.strip().splitlines():
            all_yes |= set(yes_questions)
        count_sum += len(all_yes)
    return count_sum


def part2(text):
    count_sum = 0
    for group in text.split('\n\n'):
        common_yes = set(string.ascii_lowercase)
        for yes_questions in group.strip().splitlines():
            common_yes &= set(yes_questions)
        count_sum += len(common_yes)
    return count_sum
