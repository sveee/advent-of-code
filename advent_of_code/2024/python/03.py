
import re

def part1(text):
    t = 0
    for expr in re.findall(
        r'mul\(\d+,\d+\)', text
    ):
        a, b = re.findall('\d+', expr)
        t += int(a) * int(b)
    return t

def part2(text):
    t = 0
    do = True
    for expr in re.findall(
        r'mul\(\d+,\d+\)|do\(\)|don\'t\(\)', text
    ):
        if expr == 'do()':
            do = True 
        elif expr == 'don\'t()':
            do = False
        else:
            if do:
                a, b = re.findall('\d+', expr)
                t += int(a) * int(b)
    return t
