use std::collections::HashMap;

fn f(n: i64, k: i32, cache: &mut HashMap<(i64, i32), i64>) -> i64 {
    if let Some(&cached_value) = cache.get(&(n, k)) {
        return cached_value;
    }

    let result = if k == 0 {
        1
    } else if n == 0 {
        f(1, k - 1, cache)
    } else {
        let sn = n.to_string();
        if sn.len() % 2 == 0 {
            let mid = sn.len() / 2;
            let left_part: i64 = sn[..mid].parse().unwrap();
            let right_part: i64 = sn[mid..].parse().unwrap();
            f(left_part, k - 1, cache) + f(right_part, k - 1, cache)
        } else {
            f(n * 2024, k - 1, cache)
        }
    };
    cache.insert((n, k), result);
    result
}

fn part1(text: &str) -> i64 {
    let mut cache = HashMap::new();
    text.split_whitespace()
        .map(|num_str| {
            let num = num_str.parse::<i64>().expect("Invalid integer input");
            f(num, 25, &mut cache)
        })
        .sum()
}

fn part2(text: &str) -> i64 {
    let mut cache = HashMap::new();
    text.split_whitespace()
        .map(|num_str| {
            let num = num_str.parse::<i64>().expect("Invalid integer input");
            f(num, 75, &mut cache)
        })
        .sum()
}

fn main() {
    aoc2024::solve(part1, part2);
}
