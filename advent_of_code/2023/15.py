from collections import defaultdict
from dataclasses import dataclass


def calculate_hash(s):
    h = 0
    for c in s:
        h = (h + ord(c)) * 17 % 256
    return h


def part1(text):
    return sum(calculate_hash(s) for s in text.split(','))


@dataclass
class Lens:
    label: str
    focal_length: int


def part2(text):
    boxes = defaultdict(list)
    for line in text.split(','):
        if '=' in line:
            label, focal_length = line.split('=')
            focal_length = int(focal_length)
        else:
            label = line.split('-')[0]
            focal_length = 0

        box_id = calculate_hash(label)
        if focal_length > 0:
            found = False
            for lens in boxes[box_id]:
                if lens.label == label:
                    lens.focal_length = focal_length
                    found = True
            if not found:
                boxes[box_id].append(Lens(label, focal_length))
        else:
            slot_id_to_remove = next(
                (
                    slot_id
                    for slot_id, lens in enumerate(boxes[box_id])
                    if lens.label == label
                ),
                len(boxes[box_id]),
            )
            boxes[box_id] = (
                boxes[box_id][:slot_id_to_remove]
                + boxes[box_id][slot_id_to_remove + 1 :]
            )

    focusing_power = 0
    for box_id, lenses in boxes.items():
        for slot_id, lens in enumerate(lenses):
            focusing_power += (box_id + 1) * (slot_id + 1) * lens.focal_length
    return focusing_power
