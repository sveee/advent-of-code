from collections import deque

directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def part1(text, n=71, first=1024):
    bytes = [tuple(map(int, line.split(','))) for line in text.splitlines()]
    first_bytes = set(bytes[:first])
    s, e = (0, 0), (n - 1, n - 1)
    queue = deque([s])
    distance = {s: 0}
    while len(queue) > 0:
        x, y = queue.popleft()
        if (x, y) == e:
            break
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < n
                and 0 <= ny < n
                and (nx, ny) not in distance
                and (nx, ny) not in first_bytes
            ):
                distance[(nx, ny)] = distance[(x, y)] + 1
                queue.append((nx, ny))

    return distance[e]


def part2(text):
    pass
