def get_fuel(mass):
    return int(mass / 3) - 2


def get_total_fuel(mass):
    total = 0
    mass = get_fuel(mass)
    while mass > 0:
        total += mass
        mass = get_fuel(mass)
    return total


def part1(text):
    return sum(get_fuel(int(line)) for line in text.splitlines())


def part2(text):
    return sum(get_total_fuel(int(line)) for line in text.splitlines())
