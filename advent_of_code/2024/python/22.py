def mix(a, b):
    return a ^ b


def prune(a):
    return a % 16777216


def step(n):
    n = prune(mix(n << 6, n))
    n = prune(mix(n >> 5, n))
    n = prune(mix(n << 11, n))
    return n


def repeat(n, k):
    for _ in range(k):
        n = step(n)
    return n


def get_sequence(n, k):
    seq = [n % 10]
    for _ in range(k):
        n = step(n)
        seq.append(n % 10)
    return seq


def get_changes_to_banana(seq):
    n = len(seq)
    changes_to_banana = {}
    for i in range(n - 4):
        digits = seq[i : i + 5]
        changes = tuple(d2 - d1 for d1, d2 in zip(digits, digits[1:]))
        if changes not in changes_to_banana:
            changes_to_banana[changes] = digits[-1]
    return changes_to_banana


def part1(text, k=2000):
    return sum(repeat(int(n), k) for n in text.splitlines())


def part2(text, k=2000):
    seq_changes_to_banana = []
    all_changes = set()
    for n in text.splitlines():
        seq = get_sequence(int(n), k)
        changes_to_banana = get_changes_to_banana(seq)
        all_changes |= set(changes_to_banana)
        seq_changes_to_banana.append(changes_to_banana)

    return max(
        sum(
            changes_to_banana.get(changes, 0)
            for changes_to_banana in seq_changes_to_banana
        )
        for changes in all_changes
    )
