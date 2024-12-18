use std::collections::{HashMap, HashSet, VecDeque};

fn bfs(first_bytes: &HashSet<(i32, i32)>, n: i32) -> Option<usize> {
    let start = (0, 0);
    let end = (n - 1, n - 1);
    let directions = [(-1, 0), (1, 0), (0, -1), (0, 1)];

    let mut queue = VecDeque::new();
    queue.push_back(start);
    let mut distance = HashMap::new();
    distance.insert(start, 0_usize);

    while let Some((x, y)) = queue.pop_front() {
        if (x, y) == end {
            return distance.get(&end).cloned();
        }

        for (dx, dy) in &directions {
            let nx = x + dx;
            let ny = y + dy;
            if nx >= 0 && nx < n && ny >= 0 && ny < n {
                let pos = (nx, ny);
                if !distance.contains_key(&pos) && !first_bytes.contains(&pos) {
                    distance.insert(pos, distance[&(x, y)] + 1);
                    queue.push_back(pos);
                }
            }
        }
    }

    None
}

pub fn part1(text: &str) -> String {
    let bytes: Vec<(i32, i32)> = text
        .lines()
        .map(|line| {
            let mut parts = line.split(',');
            let x = parts.next().unwrap().parse::<i32>().unwrap();
            let y = parts.next().unwrap().parse::<i32>().unwrap();
            (x, y)
        })
        .collect();

    let first_bytes: HashSet<(i32, i32)> = bytes[..1024.min(bytes.len())].iter().cloned().collect();
    bfs(&first_bytes, 71)
        .map(|d| d.to_string())
        .unwrap_or("None".to_string())
}

pub fn part2(text: &str) -> String {
    let bytes: Vec<(i32, i32)> = text
        .lines()
        .map(|line| {
            let mut parts = line.split(',');
            let x = parts.next().unwrap().parse::<i32>().unwrap();
            let y = parts.next().unwrap().parse::<i32>().unwrap();
            (x, y)
        })
        .collect();

    let mut left = 0;
    let mut right = bytes.len();

    while right - left > 1 {
        let mid = (left + right) / 2;
        let first_bytes: HashSet<(i32, i32)> = bytes[..mid].iter().cloned().collect();

        if bfs(&first_bytes, 71).is_some() {
            left = mid;
        } else {
            right = mid;
        }
    }

    format!("{},{}", bytes[left].0, bytes[left].1)
}

fn main() {
    aoc2024::solve(part1, part2);
}
