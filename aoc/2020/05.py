from aoc.problem import Problem


class Promblem2020_05(Problem):
    def solve(self, text):
        seat_ids = []
        for line in text.splitlines():
            row = int(line[:7].translate(str.maketrans('FB', '01')), 2)
            column = int(line[7:].translate(str.maketrans('LR', '01')), 2)
            seat_ids.append(row * 8 + column)
        self.part1 = max(seat_ids)
        seat_ids = sorted(seat_ids)
        self.part2 = next(
            seat_id1 + 1
            for seat_id1, seat_id2 in zip(seat_ids[::2], seat_ids[1::2])
            if seat_id2 - seat_id1 == 2
        )


Promblem2020_05().print_solution()
