from collections import deque
from dataclasses import dataclass


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


@dataclass
class File:
    id: int
    index: int
    size: int


EMPTY = -1


def part2(text):
    disk_map = list(map(int, text))
    files, disk, disk_index = [], [], 0
    for index, size in enumerate(disk_map):
        if index % 2 == 0:
            disk.extend([index // 2] * size)
            files.append(File(index // 2, disk_index, size))
        else:
            disk.extend([EMPTY] * size)
        disk_index += size

    for file in sorted(files, key=lambda x: x.id, reverse=True):
        start = 0
        while start < file.index:
            if disk[start] != EMPTY:
                start += 1
            else:
                end = start
                while end < len(disk) and disk[end] == EMPTY:
                    end += 1
                if file.size <= end - start:
                    for index in range(start, start + file.size):
                        disk[index] = file.id
                    for index in range(file.index, file.index + file.size):
                        disk[index] = EMPTY
                    start = end
                    break
                else:
                    start = end

    return sum(index * value for index, value in enumerate(disk) if value >= 0)
