from aoc.problem import Problem


class Problem2023_04(Problem):
    def solve(self, text):
        cards = text.splitlines()
        points = 0
        n_won_cards = [1] * len(cards)
        for i, card in enumerate(cards):
            _id, numbers = card.split(':')
            winning, your = map(lambda x: set(x.strip().split()), numbers.split('|'))
            n_matches = len(winning & your)
            points += 2 ** (n_matches - 1) if n_matches > 0 else 0
            for j in range(i + 1, i + n_matches + 1):
                n_won_cards[j] += n_won_cards[i]
        self.part1 = points
        self.part2 = sum(n_won_cards)

    def part1(self, text):
        cards = text.splitlines()
        points = 0
        for card in cards:
            _id, numbers = card.split(':')
            winning, your = map(lambda x: set(x.strip().split()), numbers.split('|'))
            n_matches = len(winning & your)
            points += 2 ** (n_matches - 1) if n_matches > 0 else 0
        return points

    def part2(self, text):
        cards = text.splitlines()
        n_won_cards = [1] * len(cards)
        for i, card in enumerate(cards):
            _id, numbers = card.split(':')
            winning, your = map(lambda x: set(x.strip().split()), numbers.split('|'))
            n_matches = len(winning & your)
            for j in range(i + 1, i + n_matches + 1):
                n_won_cards[j] += n_won_cards[i]
        return sum(n_won_cards)
