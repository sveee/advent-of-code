from collections import deque


def part1(text):
    disk_map = list(map(int, text))
    files = deque()
    for index, file in enumerate(disk_map[::2]):
        files.extend([index] * file)
    compressed = []
    for index, value in enumerate(disk_map):
        if len(files) == 0:
            break
        for _ in range(min(value, len(files))):
            compressed.append(files.popleft() if index % 2 == 0 else files.pop())
    return sum(index * value for index, value in enumerate(compressed))


def part2(text):
    pass
