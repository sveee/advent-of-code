def is_lock(grid):
    return grid[0] == '#' * 5


def get_heights(grid):
    return [line.count('#') for line in zip(*grid)]


def do_fit(key, lock):
    return all(kc + lc <= 5 for kc, lc in zip(key, lock))


def part1(text):
    keys, locks = [], []
    for grid in text.split('\n\n'):
        grid = grid.splitlines()
        if is_lock(grid):
            locks.append(get_heights(grid[1:]))
        else:
            keys.append(get_heights(grid[:-1]))

    return sum(do_fit(key, lock) for key in keys for lock in locks)
