def get_value(index, memory, mode):
    return memory[memory[index]] if mode == 0 else memory[index]


def run_program(memory, input):
    memory = memory.copy()
    index = 0
    output = ''
    while index < len(memory):
        op = memory[index]
        mode1, mode2, mode3 = op // 100 % 10, op // 1000 % 10, op // 10000 % 10
        assert mode1 in [0, 1] and mode2 in [0, 1] and mode3 in [0, 1]
        op %= 100
        if op == 3:
            if mode1 == 0:
                memory[memory[index + 1]] = input
            else:
                memory[index + 1] = input
            index += 2
        elif op == 4:
            output = str(get_value(index + 1, memory, mode1))
            index += 2
        elif op in [1, 2]:
            left = get_value(index + 1, memory, mode1)
            right = get_value(index + 2, memory, mode2)
            result = left + right if op == 1 else left * right
            if mode3 == 0:
                memory[memory[index + 3]] = result
            else:
                memory[index + 3] = result
            index += 4
        elif op in [5, 6]:
            value = get_value(index + 1, memory, mode1)
            if value != 0 if op == 5 else value == 0:
                index = get_value(index + 2, memory, mode2)
            else:
                index += 3
        elif op in [7, 8]:
            left, right = get_value(index + 1, memory, mode1), get_value(
                index + 2, memory, mode2
            )
            condition = left < right if op == 7 else left == right
            if mode3 == 0:
                memory[memory[index + 3]] = int(condition)
            else:
                memory[index + 3] = int(condition)
            index += 4
        elif op == 99:
            break
        else:
            raise RuntimeError(f'Unknown op: {op}')

    return output


def part1(text):
    memory = list(map(int, text.split(',')))
    return run_program(memory, 1)


def part2(text, system_id=5):
    memory = list(map(int, text.split(',')))
    return run_program(memory, system_id)
