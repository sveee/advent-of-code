directions = [
    (dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if dx != 0 or dy != 0
]


def get_word_at(position, direction, size, grid):
    x, y = position
    dx, dy = direction
    return ''.join(
        [
            grid[x + dx * i][y + dy * i]
            for i in range(size)
            if 0 <= x + dx * i < len(grid) and 0 <= y + dy * i < len(grid[0])
        ]
    )


def part1(text):
    grid = text.splitlines()
    n, m = len(grid), len(grid[0])
    xmas_count = 0
    for x in range(n):
        for y in range(m):
            for d in directions:
                xmas_count += get_word_at((x, y), d, 4, grid) == 'XMAS'
    return xmas_count


def part2(text):
    grid = text.splitlines()
    n, m = len(grid), len(grid[0])
    xmas_count = 0
    for x in range(n):
        for y in range(m):
            if x + 2 < n and y + 2 < m:
                xmas_count += get_word_at((x, y), (1, 1), 3, grid) in [
                    'MAS',
                    'SAM',
                ] and get_word_at((x + 2, y), (-1, 1), 3, grid) in [
                    'MAS',
                    'SAM',
                ]
    return xmas_count
