def get_seat_ids(text):
    seat_ids = []
    for line in text.splitlines():
        row = int(line[:7].translate(str.maketrans('FB', '01')), 2)
        column = int(line[7:].translate(str.maketrans('LR', '01')), 2)
        seat_ids.append(row * 8 + column)
    return seat_ids


def part1(text):
    seat_ids = get_seat_ids(text)
    return max(seat_ids)


def part2(text):
    seat_ids = sorted(get_seat_ids(text))
    return next(
        seat_id1 + 1
        for seat_id1, seat_id2 in zip(seat_ids[::2], seat_ids[1::2])
        if seat_id2 - seat_id1 == 2
    )
