def get_n_rows(grid):
    n_rows = len(grid)
    for ri in range(1, n_rows):
        is_perfect_reflection = True
        for k in range(max(ri, n_rows - ri)):
            if 0 <= ri - k - 1 < n_rows and 0 <= ri + k < n_rows:
                if grid[ri - k - 1] != grid[ri + k]:
                    is_perfect_reflection = False
        if is_perfect_reflection:
            return ri
    return 0


def get_n_columns(grid):
    n_columns = len(grid[0])
    for ci in range(1, n_columns):
        is_perfect_reflection = True
        for k in range(max(ci, n_columns - ci)):
            # print(ci - k - 1, ci + k)
            if 0 <= ci - k - 1 < n_columns and 0 <= ci + k < n_columns:
                # print([grid[ri][ci - k - 1] for ri in range(len(grid))])
                # print([grid[ri][ci + k] for ri in range(len(grid))])
                if [grid[ri][ci - k - 1] for ri in range(len(grid))] != [
                    grid[ri][ci + k] for ri in range(len(grid))
                ]:
                    is_perfect_reflection = False
                    # break
        if is_perfect_reflection:
            return ci
    return 0


def part1(text):
    total_n_columns, total_n_rows = 0, 0
    for grid in text.split('\n\n'):
        grid = grid.splitlines()
        total_n_rows += get_n_rows(grid)
        total_n_columns += get_n_columns(grid)
    return 100 * total_n_rows + total_n_columns


def part2(text):
    return
