use std::collections::hash_map::Entry;
use std::collections::{HashMap, HashSet};

static DIRECTIONS: [(isize, isize); 4] = [(-1, 0), (1, 0), (0, -1), (0, 1)];

fn get_neighbors(x: usize, y: usize, grid: &[&str]) -> Vec<(usize, usize)> {
    let mut neighbors = Vec::new();
    let rows = grid.len();
    if rows == 0 {
        return neighbors;
    }
    let cols = grid[0].len();

    for (dx, dy) in &DIRECTIONS {
        let nx = x as isize + dx;
        let ny = y as isize + dy;
        if nx >= 0 && ny >= 0 {
            let (nxu, nyu) = (nx as usize, ny as usize);
            if nxu < rows && nyu < cols {
                neighbors.push((nxu, nyu));
            }
        }
    }
    neighbors
}

fn flood_fill(
    x: usize,
    y: usize,
    current_id: usize,
    region_id_map: &mut HashMap<(usize, usize), usize>,
    grid: &[&str],
) {
    region_id_map.insert((x, y), current_id);
    let ch = grid[x].as_bytes()[y];
    for (nx, ny) in get_neighbors(x, y, grid) {
        if !region_id_map.contains_key(&(nx, ny)) && grid[nx].as_bytes()[ny] == ch {
            flood_fill(nx, ny, current_id, region_id_map, grid);
        }
    }
}

fn get_region_id_map(grid: &[&str]) -> HashMap<(usize, usize), usize> {
    let mut region_id_map = HashMap::new();
    let mut current_id = 0;
    let rows = grid.len();
    if rows == 0 {
        return region_id_map;
    }
    let cols = grid[0].len();

    for x in 0..rows {
        for y in 0..cols {
            if !region_id_map.contains_key(&(x, y)) {
                flood_fill(x, y, current_id, &mut region_id_map, grid);
                current_id += 1;
            }
        }
    }
    region_id_map
}

fn part1(text: &str) -> usize {
    let grid: Vec<&str> = text.lines().collect();
    let region_id_map = get_region_id_map(&grid);

    let mut area: HashMap<usize, usize> = HashMap::new();
    let mut perimeter: HashMap<usize, usize> = HashMap::new();

    for (&(x, y), &rid) in &region_id_map {
        *area.entry(rid).or_insert(0) += 1;
        let neighbors = get_neighbors(x, y, &grid);
        let count_same_region_neighbors = neighbors
            .iter()
            .filter(|&&(nx, ny)| region_id_map.get(&(nx, ny)) == Some(&rid))
            .count();

        let cell_perimeter = 4 - count_same_region_neighbors;
        *perimeter.entry(rid).or_insert(0) += cell_perimeter;
    }

    area.iter().map(|(&rid, &a)| a * perimeter[&rid]).sum()
}

fn count_top(region: &[(isize, isize)]) -> usize {
    let mut region_vec = region.to_vec();
    region_vec.sort();
    let region_set: HashSet<_> = region_vec.iter().copied().collect();

    let mut n_sides = 0;
    let mut prev_x: isize = -1;
    let mut prev_y: isize = -1;

    for &(x, y) in &region_vec {
        if !((y - 1 == prev_y) && (x == prev_x) && !region_set.contains(&((x - 1), y))) {
            if prev_x != -1 {
                n_sides += 1;
            }
        }

        if !region_set.contains(&(x.wrapping_sub(1), y)) {
            prev_x = x;
            prev_y = y;
        } else {
            prev_x = -1;
            prev_y = -1;
        }
    }
    if prev_x != -1 {
        n_sides += 1;
    }
    n_sides
}

fn count_bottom(region: &[(isize, isize)]) -> usize {
    let mut region_vec = region.to_vec();
    region_vec.sort_by(|a, b| {
        let ax = a.0 as isize;
        let ay = a.1 as isize;
        let bx = b.0 as isize;
        let by = b.1 as isize;
        match (-ax).cmp(&(-bx)) {
            std::cmp::Ordering::Equal => ay.cmp(&by),
            other => other,
        }
    });
    let region_set: HashSet<_> = region_vec.iter().copied().collect();

    let mut n_sides = 0;
    let mut prev_x: isize = -1;
    let mut prev_y: isize = -1;

    for &(x, y) in &region_vec {
        if !((y - 1 == prev_y) && (x == prev_x) && !region_set.contains(&(x + 1, y))) {
            if prev_x != -1 {
                n_sides += 1;
            }
        }

        if !region_set.contains(&(x + 1, y)) {
            prev_x = x;
            prev_y = y;
        } else {
            prev_x = -1;
            prev_y = -1;
        }
    }
    if prev_x != -1 {
        n_sides += 1;
    }
    n_sides
}

fn count_left(region: &[(isize, isize)]) -> usize {
    let mut region_vec = region.to_vec();
    region_vec.sort_by(|a, b| {
        let ay = a.1;
        let ax = a.0;
        let by = b.1;
        let bx = b.0;
        ay.cmp(&by).then(ax.cmp(&bx))
    });
    let region_set: HashSet<_> = region_vec.iter().copied().collect();

    let mut n_sides = 0;
    let mut prev_x: isize = -1;
    let mut prev_y: isize = -1;

    for &(x, y) in &region_vec {
        if !((y == prev_y) && (x - 1 == prev_x) && !region_set.contains(&(x, y.wrapping_sub(1)))) {
            if prev_x != -1 {
                n_sides += 1;
            }
        }

        if !region_set.contains(&(x, y.wrapping_sub(1))) {
            prev_x = x;
            prev_y = y;
        } else {
            prev_x = -1;
            prev_y = -1;
        }
    }

    if prev_x != -1 {
        n_sides += 1;
    }
    n_sides
}

fn count_right(region: &[(isize, isize)]) -> usize {
    let mut region_vec = region.to_vec();
    region_vec.sort_by(|a, b| {
        let ay = a.1 as isize;
        let ax = a.0 as isize;
        let by = b.1 as isize;
        let bx = b.0 as isize;
        match (-ay).cmp(&(-by)) {
            std::cmp::Ordering::Equal => ax.cmp(&bx),
            other => other,
        }
    });

    let region_set: HashSet<_> = region_vec.iter().copied().collect();
    let mut n_sides = 0;
    let mut prev_x: isize = -1;
    let mut prev_y: isize = -1;

    for &(x, y) in &region_vec {
        if !((y == prev_y) && (x - 1 == prev_x) && !region_set.contains(&(x, y + 1))) {
            if prev_x != -1 {
                n_sides += 1;
            }
        }

        if !region_set.contains(&(x, y + 1)) {
            prev_x = x;
            prev_y = y;
        } else {
            prev_x = -1;
            prev_y = -1;
        }
    }

    if prev_x != -1 {
        n_sides += 1;
    }

    n_sides
}

fn count_sides(region: &[(isize, isize)]) -> usize {
    count_top(region) + count_bottom(region) + count_left(region) + count_right(region)
}

fn part2(text: &str) -> usize {
    let grid: Vec<&str> = text.lines().collect();
    let region_id_map = get_region_id_map(&grid);

    let mut regions_by_id: HashMap<usize, Vec<(isize, isize)>> = HashMap::new();
    for (&(x, y), &rid) in &region_id_map {
        match regions_by_id.entry(rid) {
            Entry::Vacant(e) => {
                e.insert(vec![(x as isize, y as isize)]);
            }
            Entry::Occupied(mut e) => {
                e.get_mut().push((x as isize, y as isize));
            }
        }
    }

    regions_by_id
        .values()
        .map(|region| region.len() * count_sides(region))
        .sum()
}

fn main() {
    aoc2024::solve(part1, part2);
}
