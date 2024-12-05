fn is_safe(level: &Vec<i32>) -> bool {
    let all_diff_valid = level
        .windows(2)
        .all(|pair| matches!(pair, &[a, b] if(1..=3).contains(&(a - b).abs())));
    let all_increasing = level
        .windows(2)
        .all(|pair| matches!(pair, &[a, b] if a < b));
    let all_decreasing = level
        .windows(2)
        .all(|pair| matches!(pair, &[a, b] if a > b));
    all_diff_valid && (all_increasing || all_decreasing)
}

fn is_almost_safe(level: &Vec<i32>) -> bool {
    (0..level.len()).any(|i| {
        let mut temp = level.to_vec();
        temp.remove(i);
        is_safe(&temp)
    })
}

fn part1(text: &str) -> usize {
    text.lines()
        .map(|line| {
            let level: Vec<i32> = line
                .split_whitespace()
                .map(|num| num.parse().unwrap())
                .collect();
            is_safe(&level)
        })
        .filter(|&is_safe| is_safe)
        .count()
}

fn part2(text: &str) -> usize {
    text.lines()
        .map(|line| {
            let level: Vec<i32> = line
                .split_whitespace()
                .map(|num| num.parse().unwrap())
                .collect();
            is_safe(&level) || is_almost_safe(&level)
        })
        .filter(|&is_safe| is_safe)
        .count()
}

fn main() {
    aoc2024::solve(part1, part2);
}
