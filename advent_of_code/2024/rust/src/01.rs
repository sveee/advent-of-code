use std::collections::HashMap;

pub fn part1(input: &str) -> i32 {
    let (mut left, mut right): (Vec<i32>, Vec<i32>) = input
        .lines()
        .filter_map(|line| {
            let mut numbers = line.split_whitespace().map(|n| n.parse::<i32>().unwrap());
            Some((numbers.next()?, numbers.next()?))
        })
        .unzip();

    left.sort();
    right.sort();
    left.iter().zip(right.iter()).map(|(a, b)| (a - b).abs()).sum()
}

pub fn part2(input: &str) -> i32 {
    let (left, right): (Vec<i32>, Vec<i32>) = input
        .lines()
        .filter_map(|line| {
            let mut numbers = line.split_whitespace().map(|n| n.parse::<i32>().unwrap());
            Some((numbers.next()?, numbers.next()?))
        })
        .unzip();
    let mut right_counts: HashMap<i32, i32> = HashMap::new();
    for value in right {
        *right_counts.entry(value).or_insert(0) += 1;
    }
    left.iter().map(|a| a * (right_counts.get(a).unwrap_or(&0))).sum()
}


fn main() {
    aoc2024::solve(part1, part2);
}