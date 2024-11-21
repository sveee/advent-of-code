from collections import defaultdict
from enum import Enum

directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def part1(text, n_steps=64):
    grid = text.splitlines()
    n, m = len(grid), len(grid[0])
    start = next((x, y) for x in range(n) for y in range(m) if grid[x][y] == 'S')
    level = {start}
    for _n_step in range(n_steps):
        next_level = set()
        for x, y in level:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < n and 0 <= ny < m):
                    continue

                if grid[nx][ny] != '#':
                    next_level.add((nx, ny))
        level = next_level
    return len(level)


class Position(Enum):
    BOTTOM_MIDDLE = 'bottom_middle'
    TOP_MIDDLE = 'top_middle'
    LEFT_MIDDLE = 'left_middle'
    RIGHT_MIDDLE = 'right_middle'
    BOTTOM_LEFT = 'bottom_left'
    TOP_LEFT = 'top_left'
    BOTTOM_RIGHT = 'bottom_right'
    TOP_RIGHT = 'top_right'
    MIDDLE = 'middle'


def calculate_history(grid):
    k = len(grid)
    assert k == len(grid[0])
    position_to_point = {
        Position.BOTTOM_MIDDLE: (k - 1, k // 2),
        Position.TOP_MIDDLE: (0, k // 2),
        Position.LEFT_MIDDLE: (k // 2, 0),
        Position.RIGHT_MIDDLE: (k // 2, k - 1),
        Position.BOTTOM_LEFT: (k - 1, 0),
        Position.TOP_LEFT: (0, 0),
        Position.BOTTOM_RIGHT: (k - 1, k - 1),
        Position.TOP_RIGHT: (0, k - 1),
        Position.MIDDLE: (k // 2, k // 2),
    }
    history = defaultdict(list)
    for position in Position:
        visited = set()
        level = {position_to_point[position]}
        for _step in range(2 * k):
            history[position].append(len(level))
            next_level = set()
            for x, y in level:
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < k and 0 <= ny < k):
                        continue

                    if grid[nx][ny] != '#':
                        next_level.add((nx, ny))

            level = next_level
            state = tuple(sorted(level))
            if state in visited:
                break
            visited.add(state)

    return history


def calculate_quotent_count(n, k, history):
    q = n // k
    if q == 0:
        return 0
    total = q * q + (q - 1) * (q - 1)
    n_even_cycles = n_odd_cycles = total // 2
    if n % 2 == 0:
        n_even_cycles = (q - 1) * (q - 1) if q % 2 == 0 else q * q
        n_odd_cycles = total - n_even_cycles
    else:
        n_odd_cycles = (q - 1) * (q - 1) if q % 2 == 0 else q * q
        n_even_cycles = total - n_odd_cycles
    if (len(history[Position.MIDDLE]) - 1) % 2 == 0:
        n_plots_in_even_cycle, n_plots_in_odd_cycle = (
            history[Position.MIDDLE][-1],
            history[Position.MIDDLE][-2],
        )
    else:
        n_plots_in_even_cycle, n_plots_in_odd_cycle = (
            history[Position.MIDDLE][-2],
            history[Position.MIDDLE][-1],
        )
    n_reached = (
        n_even_cycles * n_plots_in_even_cycle + n_odd_cycles * n_plots_in_odd_cycle
    )
    return n_reached


def calculate_remainer_count(n, k, history):
    q = n // k
    r = n % k

    edge_tiles = set()
    edge_tiles.add((0, q, r + k // 2))
    edge_tiles.add((0, -q, r + k // 2))
    edge_tiles.add((q, 0, r + k // 2))
    edge_tiles.add((-q, 0, r + k // 2))
    for y in range(-q, q + 1):
        if y == 0:
            continue
        x1 = q + 1 - abs(y)
        x2 = q - abs(y)
        if x2 != 0:
            edge_tiles.add((x2, y, r + k - 1))
            edge_tiles.add((-x2, y, r + k - 1))
        if r != 0:
            edge_tiles.add((x1, y, r - 1))
            edge_tiles.add((-x1, y, r - 1))

    if r > k // 2:
        edge_tiles.add((0, q + 1, r - k // 2 - 1))
        edge_tiles.add((0, -q - 1, r - k // 2 - 1))
        edge_tiles.add((q + 1, 0, r - k // 2 - 1))
        edge_tiles.add((-q - 1, 0, r - k // 2 - 1))

    n_reached = 0
    for x, y, steps in sorted(edge_tiles):
        if x == 0 and y > 0:
            side = Position.BOTTOM_MIDDLE
        elif x == 0 and y < 0:
            side = Position.TOP_MIDDLE
        if x > 0 and y == 0:
            side = Position.LEFT_MIDDLE
        elif x < 0 and y == 0:
            side = Position.RIGHT_MIDDLE
        elif x > 0 and y > 0:
            side = Position.BOTTOM_LEFT
        elif x > 0 and y < 0:
            side = Position.TOP_LEFT
        elif x < 0 and y > 0:
            side = Position.BOTTOM_RIGHT
        elif x < 0 and y < 0:
            side = Position.TOP_RIGHT

        n_reached += history[side][steps]

    return n_reached


def part2(text, n=26501365):
    grid = text.splitlines()
    k = len(grid)
    history = calculate_history(grid)
    return calculate_quotent_count(n, k, history) + calculate_remainer_count(
        n, k, history
    )
