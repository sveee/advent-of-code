
def part1(text):
    measurements = list(map(int, text.splitlines()))
    return sum(
        a2 > a1
        for a1, a2 in zip(measurements, measurements[1:])
    )

def part2(text):
    measurements = list(map(int, text.splitlines()))
    three_window_sums = list(map(sum, zip(measurements, measurements[1:], measurements[2:])))
    return sum(
        a2 > a1
        for a1, a2 in zip(three_window_sums, three_window_sums[1:])
    )
