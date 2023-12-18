
from collections import defaultdict


directions = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}


def get_direction(point, trench):
    x, y = point
    return -1 if (x - 1, y) in trench else 1


def get_interior_size(trench):
    ys_by_x = defaultdict(list)
    min_x = max_x = next(iter(trench))[0]
    for x, y in trench:
        ys_by_x[x].append(y)
        min_x = min(min_x, x)
        max_x = max(max_x, x)

    interior_size = len(trench)
    for x in range(min_x, max_x + 1):
        ys = sorted(ys_by_x[x])
        is_inside, prev_end_y = False, None
        index = 0
        while index < len(ys):
            start_y = end_y = ys[index]

            if is_inside:
                interior_size += start_y - prev_end_y - 1

            while index + 1 < len(ys) and ys[index + 1] == end_y + 1:
                index += 1
                end_y = ys[index]

            if start_y == end_y or get_direction((x, start_y), trench) != get_direction((x, end_y), trench):
                is_inside = not is_inside

            prev_end_y = end_y
            index += 1

    return interior_size

def get_trench(instructions):
    x, y = 0, 0
    trench = {(x, y)}
    ys_by_x = defaultdict(list)
    for direction, steps in instructions:
        dx, dy = directions[direction]
        for _step in range(int(steps)):
            x += dx
            y += dy
            trench.add((x, y))
    return trench


def part1(text):
    instructions = []
    for line in text.splitlines():
        direction, steps, color = line.split()
        instructions.append((direction, int(steps)))
    trench = get_trench(instructions)
    return get_interior_size(trench)
        


code_to_direction = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U',
}

def part2(text):
    instructions = []
    for line in text.splitlines():
        _direction, _steps, color = line.split()
        instructions.append((code_to_direction[color[-2]], int(color[2: -2], 16)))
        
    if len(instructions) > 15:
        return None
    trench = get_trench(instructions)
    print(len(trench))
    min_x = max_x = next(iter(trench))[0]
    for x, y in trench:
        min_x = min(min_x, x)
        max_x = max(max_x, x)
    # print(min_x, max_x)

    return get_interior_size(trench)
