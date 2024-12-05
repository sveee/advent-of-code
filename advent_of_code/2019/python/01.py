def get_fuel(mass):
    return int(mass / 3) - 2


def get_total_fuel(mass):
    total = 0
    fuel = get_fuel(mass)
    while fuel > 0:
        total += fuel
        fuel = get_fuel(fuel)
    return total


def part1(text):
    return sum(get_fuel(int(line)) for line in text.splitlines())


def part2(text):
    return sum(get_total_fuel(int(line)) for line in text.splitlines())
