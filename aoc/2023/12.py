
import re
from itertools import product

def get_n_arrangements(damaged_records, sizes):
    n_arrangements = 0
    for records in product(*[
        ['.', '#'] if record == '?' else [record]
        for record in damaged_records
    ]):
        records = re.split('\.+', ''.join(records).strip('.'))
        if list(map(len, records)) == sizes:
            n_arrangements += 1
    return n_arrangements



def part1(text):
    total_n_arrangements = 0
    for line in text.splitlines():
        records, sizes = line.split()
        total_n_arrangements += get_n_arrangements(records, list(map(int, sizes.split(','))))
    return total_n_arrangements

def part2(text):
    pass
