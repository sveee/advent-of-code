
import re

def part1(text):
    total = 0
    for expr in re.findall(
        r'mul\(\d+,\d+\)', text
    ):
        left, right = re.findall('\d+', expr)
        total += int(left) * int(right)
    return total

def part2(text):
    total = 0
    enabled = True
    for expr in re.findall(
        r'mul\(\d+,\d+\)|do\(\)|don\'t\(\)', text
    ):
        if expr == 'do()':
            enabled = True 
        elif expr == 'don\'t()':
            enabled = False
        else:
            if enabled:
                left, right = re.findall('\d+', expr)
                total += int(left) * int(right)
    return total
