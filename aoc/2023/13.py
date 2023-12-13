def get_horizontal_differences(grid):
    n_rows, n_columns = len(grid), len(grid[0])
    differences_per_row = {}
    for ri in range(1, n_rows):
        n_differences = 0
        for k in range(max(ri, n_rows - ri)):
            if 0 <= ri - k - 1 < n_rows and 0 <= ri + k < n_rows:
                for ci in range(n_columns):
                    n_differences += grid[ri - k - 1][ci] != grid[ri + k][ci]
        differences_per_row[ri] = n_differences
    return differences_per_row


def get_vertical_differences(grid):
    n_rows, n_columns = len(grid), len(grid[0])
    differences_per_column = {}
    for ci in range(1, n_columns):
        n_differences = 0
        for k in range(max(ci, n_columns - ci)):
            if 0 <= ci - k - 1 < n_columns and 0 <= ci + k < n_columns:
                for ri in range(n_rows):
                    n_differences += grid[ri][ci - k - 1] != grid[ri][ci + k]
        differences_per_column[ci] = n_differences
    return differences_per_column


def get_grid_differences(grid, value):
    h_diffs, v_diffs = get_horizontal_differences(grid), get_vertical_differences(grid)
    n_rows = next(
        (n_above for n_above, diff in h_diffs.items() if diff == value),
        0,
    )
    n_columns = next(
        (n_left for n_left, diff in v_diffs.items() if diff == value),
        0,
    )
    return n_rows, n_columns


def part1(text):
    total_n_rows, total_n_columns = 0, 0
    for grid in text.split('\n\n'):
        grid = grid.splitlines()
        n_rows, n_columns = get_grid_differences(grid, 0)
        total_n_rows += n_rows
        total_n_columns += n_columns
    return 100 * total_n_rows + total_n_columns


def part2(text):
    total_n_rows, total_n_columns = 0, 0
    for grid in text.split('\n\n'):
        grid = grid.splitlines()
        n_rows, n_columns = get_grid_differences(grid, 1)
        total_n_rows += n_rows
        total_n_columns += n_columns
    return 100 * total_n_rows + total_n_columns
