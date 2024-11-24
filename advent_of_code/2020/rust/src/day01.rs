use aoc2020::solve;

pub fn part1(input: &str) -> Option<String> {
    let numbers: Vec<i32> = input
        .lines()
        .filter_map(|line| line.parse::<i32>().ok())
        .collect();

    let n = numbers.len();
    for i in 0..n {
        for j in (i + 1)..n {
            if numbers[i] + numbers[j] == 2020 {
                return Some((numbers[i] * numbers[j]).to_string());
            }
        }
    }

    None
}

pub fn part2(input: &str) -> Option<String> {
    let numbers: Vec<i32> = input
        .lines()
        .filter_map(|line| line.parse::<i32>().ok())
        .collect();

    let n = numbers.len();
    for i in 0..n {
        for j in (i + 1)..n {
            for k in (j + 1)..n {
                if numbers[i] + numbers[j] + numbers[k] == 2020 {
                    return Some((numbers[i] * numbers[j] * numbers[k]).to_string());
                }
            }
        }
    }

    None
}

fn main() {
    solve(part1, part2);
}
