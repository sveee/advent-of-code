from dataclasses import dataclass

from aoc.problem import Problem


@dataclass
class Segment:
    start: int
    end: int


@dataclass
class SegmentMap:
    source: Segment
    destination: Segment

    def map(self, segment):
        if self.source.end < segment.start or segment.end < self.source.start:
            return [], [segment]
        mapped, remaining = [
            Segment(
                max(segment.start, self.source.start)
                - self.source.start
                + self.destination.start,
                min(segment.end, self.source.end)
                - self.source.end
                + self.destination.end,
            )
        ], []
        if segment.start < self.source.start:
            remaining.append(Segment(segment.start, self.source.start - 1))
        if segment.end > self.source.end:
            remaining.append(Segment(self.source.end + 1, segment.end))
        return mapped, remaining

    @staticmethod
    def from_str(s):
        destination_start, source_start, length = map(int, s.split())
        return SegmentMap(
            Segment(source_start, source_start + length - 1),
            Segment(destination_start, destination_start + length - 1),
        )


def map_segments(segments, segment_maps):
    unmapped_segments, mapped_segments = segments, []
    for segment_map in segment_maps:
        new_unmapped_segments = []
        for segment in unmapped_segments:
            mapped, remaining = segment_map.map(segment)
            new_unmapped_segments.extend(remaining)
            mapped_segments.extend(mapped)
        unmapped_segments = new_unmapped_segments
    return unmapped_segments + mapped_segments


def map_segment_sets(segments, segment_map_sets):
    for segment_maps in segment_map_sets:
        segments = map_segments(segments, segment_maps)
    return segments


def read_input(text):
    seeds, *segment_map_sets = text.split('\n\n')
    seeds = list(map(int, seeds.split(':')[1].strip().split()))
    segment_map_sets = [
        [
            SegmentMap.from_str(segment_map)
            for segment_map in segment_map_set.split(':')[1].strip().splitlines()
        ]
        for segment_map_set in segment_map_sets
    ]
    return seeds, segment_map_sets


class Problem2023_05(Problem):
    def part1(self, text):
        seeds, segment_map_sets = read_input(text)
        segments = map_segment_sets(
            [Segment(seed, seed) for seed in seeds], segment_map_sets
        )
        return min(segment.start for segment in segments)

    def part2(self, text):
        seeds, segment_map_sets = read_input(text)
        segments = map_segment_sets(
            [
                Segment(start, start + length - 1)
                for start, length in zip(seeds[::2], seeds[1::2])
            ],
            segment_map_sets,
        )
        return min(segment.start for segment in segments)
