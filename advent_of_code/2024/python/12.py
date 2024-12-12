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


def count_top(region):
    region = sorted(region)
    prev_x, prev_y = None, None
    n_sides = 0
    for x, y in region:
        # print(x, y, n_sides, prev_x, prev_y)
        # print(y - 1 == prev_y, x == prev_x, (x - 1, y) not in region)
        if not (y - 1 == prev_y and x == prev_x and (x - 1, y) not in region):
            if prev_x != None:
                n_sides += 1
        prev_x, prev_y = (x, y) if (x - 1, y) not in region else (None, None)
    # print()
    if prev_x != None:
        n_sides += 1
    return n_sides


def count_bottom(region):
    region = sorted(region, key=lambda p: (-p[0], p[1]))
    prev_x, prev_y = None, None
    n_sides = 0
    for x, y in region:
        if not (y - 1 == prev_y and x == prev_x and (x + 1, y) not in region):
            if prev_x != None:
                n_sides += 1
        prev_x, prev_y = (x, y) if (x + 1, y) not in region else (None, None)
    if prev_x != None:
        n_sides += 1
    return n_sides


def count_left(region):
    region = sorted(region, key=lambda p: (p[1], p[0]))
    prev_x, prev_y = None, None
    n_sides = 0
    for x, y in region:
        if not (y == prev_y and x - 1 == prev_x and (x, y - 1) not in region):
            if prev_x != None:
                n_sides += 1
        prev_x, prev_y = (x, y) if (x, y - 1) not in region else (None, None)
    if prev_x != None:
        n_sides += 1
    return n_sides


def count_right(region):
    region = sorted(region, key=lambda p: (-p[1], p[0]))
    prev_x, prev_y = None, None
    n_sides = 0
    for x, y in region:
        if not (y == prev_y and x - 1 == prev_x and (x, y + 1) not in region):
            if prev_x != None:
                n_sides += 1
        prev_x, prev_y = (x, y) if (x, y + 1) not in region else (None, None)
    if prev_x != None:
        n_sides += 1
    return n_sides


def count_sides(region):
    return (
        count_top(region)
        + count_bottom(region)
        + count_left(region)
        + count_right(region)
    )


def part2(text):
    grid = text.splitlines()
    region_id = {}
    cur_id = 0
    for x in range(len(grid)):
        for y in range(len(grid)):
            if (x, y) in region_id:
                continue
            dfs(x, y, cur_id, region_id, grid)
            cur_id += 1

    regions = defaultdict(set)
    for (x, y), rid in region_id.items():
        regions[rid].add((x, y))

    return sum(len(region) * count_sides(region) for region in regions.values())
