use std::str::FromStr;

fn decode(mut coded_ops: i64, n: usize, base: i64) -> Vec<i64> {
    let mut ops = Vec::with_capacity(n);
    for _ in 0..n {
        ops.push(coded_ops % base);
        coded_ops /= base;
    }
    ops
}

fn can_be_made_true(numbers: &[i64], total: i64, n_ops: i64) -> bool {
    let n = numbers.len();
    if n <= 1 {
        return numbers.get(0).copied().unwrap_or(0) == total;
    }

    let count = n_ops.pow((n - 1) as u32);
    for coded_ops in 0..count {
        let ops = decode(coded_ops, n - 1, n_ops);
        let mut result = numbers[0];
        for (i, &op) in ops.iter().enumerate() {
            let next = numbers[i + 1];
            match op {
                0 => {
                    result *= next;
                }
                1 => {
                    result += next;
                }
                2 => {
                    let concatenated = format!("{}{}", result, next);
                    result = i64::from_str(&concatenated).unwrap();
                }
                _ => {}
            }
            if result > (total) {
                break;
            }
        }
        if result == (total) {
            return true;
        }
    }
    false
}

fn part1(text: &str) -> i64 {
    let mut total_sum: i64 = 0;
    for line in text.lines() {
        let mut parts = line.split(": ");
        let lhs_str = parts.next().unwrap();
        let rhs_str = parts.next().unwrap();
        let lhs = i64::from_str(lhs_str).unwrap();
        let rhs: Vec<i64> = rhs_str
            .split_whitespace()
            .map(|x| i64::from_str(x).unwrap())
            .collect();
        if can_be_made_true(&rhs, lhs, 2) {
            total_sum += lhs as i64;
        }
    }
    total_sum
}

fn part2(text: &str) -> i64 {
    let mut total_sum: i64 = 0;
    for line in text.lines() {
        let mut parts = line.split(": ");
        let lhs_str = parts.next().unwrap();
        let rhs_str = parts.next().unwrap();
        let lhs = i64::from_str(lhs_str).unwrap();
        let rhs: Vec<i64> = rhs_str
            .split_whitespace()
            .map(|x| i64::from_str(x).unwrap())
            .collect();
        if can_be_made_true(&rhs, lhs, 3) {
            total_sum += lhs as i64;
        }
    }
    total_sum
}

fn main() {
    aoc2024::solve(part1, part2);
}
