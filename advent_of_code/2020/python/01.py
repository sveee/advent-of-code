from itertools import combinations


def part1(text):
    numbers = list(map(int, text.splitlines()))
    n = len(numbers)
    for index1 in range(n):
        for index2 in range(index1 + 1, n):
            if numbers[index1] + numbers[index2] == 2020:
                return numbers[index1] * numbers[index2]


def part2(text):
    numbers = list(map(int, text.splitlines()))
    for number1, number2, number3 in combinations(numbers, 3):
        if number1 + number2 + number3 == 2020:
            return number1 * number2 * number3
