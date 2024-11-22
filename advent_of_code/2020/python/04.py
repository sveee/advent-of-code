import re

field_names = {
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
    'cid',
}


def is_valid1(fields):
    return field_names - set(fields) <= {'cid'}


def is_valid2(fields):
    return (
        1920 <= int(fields['byr']) <= 2020
        and 2010 <= int(fields['iyr']) <= 2020
        and 2020 <= int(fields['eyr']) <= 2030
        and (
            fields['hgt'].endswith(('cm', 'in'))
            and (
                150 <= int(fields['hgt'][:-2]) <= 193
                if fields['hgt'].endswith('cm')
                else 59 <= int(fields['hgt'][:-2]) <= 76
            )
        )
        and re.match('#[0-9a-f]{6}$', fields['hcl'])
        and fields['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
        and re.match('[0-9]{9}$', fields['pid'])
    )


def part1(text):
    n_valid = 0
    for passport in text.split('\n\n'):
        fields = dict(
            field_value.split(':') for field_value in re.split('\s+', passport.strip())
        )

        if is_valid1(fields):
            n_valid += 1
    return n_valid


def part2(text):
    n_valid = 0
    for passport in text.split('\n\n'):
        fields = dict(
            field_value.split(':') for field_value in re.split('\s+', passport.strip())
        )
        if is_valid1(fields) and is_valid2(fields):
            n_valid += 1
    return n_valid
