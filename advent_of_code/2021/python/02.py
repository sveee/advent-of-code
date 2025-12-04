DIRECTIONS = {
    'forward': (1, 0),
    'down': (0, 1),
    'up': (0, -1),
}


def part1(text):
    x, y = 0, 0
    for line in text.splitlines():
        direction, value = line.split()
        value = int(value)
        dx, dy = DIRECTIONS[direction]
        x, y = x + dx * value, y + dy * value
    return x * y


def part2(text):
    x, y, aim = 0, 0, 0
    for line in text.splitlines():
        direction, value = line.split()
        value = int(value)
        match direction:
            case 'down':
                aim += value
            case 'up':
                aim -= value
            case 'forward':
                x += value
                y += aim * value
    return x * y
