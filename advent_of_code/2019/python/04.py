def is_valid_password(password):
    return any(d1 == d2 for d1, d2 in zip(password, password[1:])) and all(
        ord(d1) <= ord(d2) for d1, d2 in zip(password, password[1:])
    )


def is_valid_password2(password):
    n = len(password)
    return any(
        password[i] == password[i + 1]
        and (i == 0 or password[i] != password[i - 1])
        and (i == n - 2 or password[i] != password[i + 2])
        for i in range(n - 1)
    ) and all(ord(d1) <= ord(d2) for d1, d2 in zip(password, password[1:]))


def part1(text):
    start, end = text.split('-')
    return sum(
        is_valid_password(str(password)) for password in range(int(start), int(end) + 1)
    )


def part2(text):
    start, end = text.split('-')
    return sum(
        is_valid_password2(str(password))
        for password in range(int(start), int(end) + 1)
    )
