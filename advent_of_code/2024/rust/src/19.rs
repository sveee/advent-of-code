use std::collections::{HashMap, HashSet};

fn n_ways(design: &str, towels: &HashSet<String>, cache: &mut HashMap<String, i64>) -> i64 {
    if design.is_empty() {
        return 1;
    }

    if let Some(&cached) = cache.get(design) {
        return cached;
    }

    let mut ans = 0;
    for i in 1..=design.len() {
        let prefix = &design[..i];
        if towels.contains(prefix) {
            ans += n_ways(&design[i..], towels, cache);
        }
    }

    cache.insert(design.to_string(), ans);
    ans
}

fn parse_input(text: &str) -> (HashSet<String>, Vec<&str>) {
    let parts: Vec<&str> = text.split("\n\n").collect();
    let (left, right) = (parts[0], parts[1]);

    let towels: HashSet<String> = left.split(", ").map(|s| s.to_string()).collect();
    let designs: Vec<&str> = right.lines().collect();

    (towels, designs)
}

fn part1(text: &str) -> i64 {
    let (towels, designs) = parse_input(text);
    let mut cache = HashMap::new();

    designs
        .iter()
        .map(|design| {
            let ways = n_ways(design, &towels, &mut cache);
            if ways > 0 {
                1
            } else {
                0
            }
        })
        .sum()
}

fn part2(text: &str) -> i64 {
    let (towels, designs) = parse_input(text);
    let mut cache = HashMap::new();

    designs
        .iter()
        .map(|design| n_ways(design, &towels, &mut cache))
        .sum()
}

fn main() {
    aoc2024::solve(part1, part2);
}
