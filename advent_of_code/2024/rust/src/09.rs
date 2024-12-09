use std::collections::VecDeque;

#[derive(Debug, Clone)]
struct File {
    id: usize,
    index: usize,
    size: usize,
}

const EMPTY: i64 = -1;

fn part1(text: &str) -> i64 {
    let disk_map: Vec<usize> = text
        .chars()
        .filter_map(|c| c.to_digit(10))
        .map(|d| d as usize)
        .collect();

    let mut files: VecDeque<usize> = VecDeque::new();
    for (index, &file_count) in disk_map.iter().step_by(2).enumerate() {
        for _ in 0..file_count {
            files.push_back(index);
        }
    }

    let mut compressed = Vec::new();
    for (index, &value) in disk_map.iter().enumerate() {
        if files.is_empty() {
            break;
        }
        let count = value.min(files.len());
        for _ in 0..count {
            if index % 2 == 0 {
                if let Some(f) = files.pop_front() {
                    compressed.push(f);
                }
            } else {
                if let Some(f) = files.pop_back() {
                    compressed.push(f);
                }
            }
        }
    }
    compressed
        .iter()
        .enumerate()
        .map(|(i, &v)| (i as i64) * (v as i64))
        .sum()
}

fn part2(text: &str) -> i64 {
    let disk_map: Vec<usize> = text
        .chars()
        .filter_map(|c| c.to_digit(10))
        .map(|d| d as usize)
        .collect();

    let mut files = Vec::new();
    let mut disk = Vec::new();

    let mut disk_index = 0;
    for (index, &size) in disk_map.iter().enumerate() {
        if index % 2 == 0 {
            let file_id = index / 2;
            disk.extend(std::iter::repeat(file_id as i64).take(size));
            files.push(File {
                id: file_id,
                index: disk_index,
                size,
            });
        } else {
            disk.extend(std::iter::repeat(EMPTY).take(size));
        }
        disk_index += size;
    }

    files.sort_by_key(|f| std::cmp::Reverse(f.id));
    for file in files {
        let mut start = 0;
        while start < file.index {
            if disk[start] != EMPTY {
                start += 1;
                continue;
            }
            let mut end = start;
            while end < disk.len() && disk[end] == EMPTY {
                end += 1;
            }

            let empty_length = end - start;
            if file.size <= empty_length {
                for i in start..(start + file.size) {
                    disk[i] = file.id as i64;
                }
                for i in file.index..(file.index + file.size) {
                    disk[i] = EMPTY;
                }

                break;
            } else {
                start = end;
            }
        }
    }
    disk.iter()
        .enumerate()
        .filter(|&(_, &v)| v >= 0)
        .map(|(i, &v)| (i as i64) * v)
        .sum()
}

fn main() {
    aoc2024::solve(part1, part2);
}
