from collections import defaultdict

directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def get_neigbours(x, y, grid):
    neigbours = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            neigbours.append((nx, ny))
    return neigbours


def dfs(x, y, cur_id, region_id, grid):
    region_id[(x, y)] = cur_id
    for nx, ny in get_neigbours(x, y, grid):
        if (nx, ny) not in region_id and grid[x][y] == grid[nx][ny]:
            dfs(nx, ny, cur_id, region_id, grid)


def part1(text):
    grid = text.splitlines()
    region_id = {}
    cur_id = 0
    for x in range(len(grid)):
        for y in range(len(grid)):
            if (x, y) in region_id:
                continue
            dfs(x, y, cur_id, region_id, grid)
            cur_id += 1

    area = defaultdict(int)
    parameter = defaultdict(int)
    for (x, y), rid in region_id.items():
        area[rid] += 1
        p = 4
        for nx, ny in get_neigbours(x, y, grid):
            if region_id[(nx, ny)] == rid:
                p -= 1
        parameter[rid] += p
    return sum(area[rid] * parameter[rid] for rid in area)


def part2(text):
    pass
