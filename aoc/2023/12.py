def f(index, prev_record, sizes, records, cache):
    state = (index, prev_record, sizes)
    if state in cache:
        return cache[state]

    if index == len(records):
        return 1 if sizes == (0,) or sizes == tuple() else 0

    current_records = [records[index]] if records[index] != '?' else ['.', '#']
    n_arrangements = 0
    for current_record in current_records:
        if current_record == '.':
            if prev_record == '#' and len(sizes) > 0 and sizes[0] == 0:
                n_arrangements += f(
                    index + 1, current_record, sizes[1:], records, cache
                )
            elif prev_record == '.':
                n_arrangements += f(index + 1, current_record, sizes, records, cache)

        if current_record == '#' and len(sizes) > 0 and sizes[0] > 0:
            n_arrangements += f(
                index + 1, current_record, (sizes[0] - 1,) + sizes[1:], records, cache
            )

    cache[state] = n_arrangements
    return n_arrangements


def part1(text):
    total_n_arrangements = 0
    for line in text.splitlines():
        records, sizes = line.split()
        sizes = tuple(map(int, sizes.split(',')))
        total_n_arrangements += f(0, '.', sizes, records, {})
    return total_n_arrangements


def part2(text):
    total_n_arrangements = 0
    for line in text.splitlines():
        records, sizes = line.split()
        sizes = tuple(map(int, sizes.split(',')))
        total_n_arrangements += f(0, '.', 5 * sizes, '?'.join(5 * [records]), {})
    return total_n_arrangements
