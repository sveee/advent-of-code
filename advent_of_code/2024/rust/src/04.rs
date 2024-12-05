use std::collections::HashSet;

fn directions() -> Vec<(isize, isize)> {
    vec![
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]
}

fn get_word_at(
    position: (usize, usize),
    direction: (isize, isize),
    size: usize,
    grid: &[Vec<char>],
) -> Option<String> {
    let (x, y) = (position.0 as isize, position.1 as isize);
    let (dx, dy) = direction;
    let mut word = String::new();

    for i in 0..size as isize {
        let nx = x + dx * i;
        let ny = y + dy * i;
        if nx < 0 || ny < 0 || nx >= grid.len() as isize || ny >= grid[0].len() as isize {
            return None;
        }
        word.push(grid[nx as usize][ny as usize]);
    }
    Some(word)
}

fn part1(text: &str) -> usize {
    let grid: Vec<Vec<char>> = text.lines().map(|line| line.chars().collect()).collect();
    let directions = directions();
    let mut xmas_count = 0;

    for x in 0..grid.len() {
        for y in 0..grid[0].len() {
            for &d in &directions {
                if let Some(word) = get_word_at((x, y), d, 4, &grid) {
                    if word == "XMAS" {
                        xmas_count += 1;
                    }
                }
            }
        }
    }

    xmas_count
}

fn part2(text: &str) -> usize {
    let grid: Vec<Vec<char>> = text.lines().map(|line| line.chars().collect()).collect();
    let mas_variants: HashSet<&str> = ["MAS", "SAM"].iter().cloned().collect();
    let mut xmas_count = 0;

    for x in 0..grid.len() {
        for y in 0..grid[0].len() {
            if x + 2 < grid.len() && y + 2 < grid[0].len() {
                let start_pos = (x, y);
                let check_pos = (x + 2, y);
                if let (Some(diag1), Some(diag2)) = (
                    get_word_at(start_pos, (1, 1), 3, &grid),
                    get_word_at(check_pos, (-1, 1), 3, &grid),
                ) {
                    if mas_variants.contains(diag1.as_str())
                        && mas_variants.contains(diag2.as_str())
                    {
                        xmas_count += 1;
                    }
                }
            }
        }
    }

    xmas_count
}

fn main() {
    aoc2024::solve(part1, part2);
}
