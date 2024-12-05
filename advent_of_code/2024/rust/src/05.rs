use std::collections::HashMap;

fn order_pages(pages: &Vec<String>, rules: &HashMap<String, Vec<String>>) -> Vec<String> {
    let mut in_degree: HashMap<String, i32> = HashMap::new();
    for page in pages {
        in_degree.insert(page.clone(), 0);
    }

    for left in pages {
        if let Some(rights) = rules.get(left) {
            for right in rights {
                if in_degree.contains_key(right) {
                    *in_degree.get_mut(right).unwrap() += 1;
                }
            }
        }
    }

    let mut zero_in_degree: Vec<String> = in_degree
        .iter()
        .filter_map(|(node, &degree)| {
            if degree == 0 {
                Some(node.clone())
            } else {
                None
            }
        })
        .collect();

    let mut ordered_pages: Vec<String> = Vec::new();
    while let Some(page) = zero_in_degree.pop() {
        ordered_pages.push(page.clone());
        if let Some(rights) = rules.get(&page) {
            for right in rights {
                if !in_degree.contains_key(right) {
                    continue;
                }
                *in_degree.get_mut(right).unwrap() -= 1;
                if in_degree[right] == 0 {
                    zero_in_degree.push(right.clone());
                }
            }
        }
    }
    ordered_pages
}

fn middle_page_number_sum(text: &str, only_ordered: bool) -> i32 {
    let parts: Vec<&str> = text.split("\n\n").collect();
    let ordering_rules = parts[0];
    let pages_in_update = parts[1];
    let mut rules: HashMap<String, Vec<String>> = HashMap::new();

    for line in ordering_rules.lines() {
        let mut lr = line.split('|');
        let left = lr.next().unwrap().to_string();
        let right = lr.next().unwrap().to_string();
        rules.entry(left).or_insert_with(Vec::new).push(right);
    }

    let mut total = 0;
    for line in pages_in_update.lines() {
        let pages: Vec<String> = line.split(',').map(|s| s.to_string()).collect();
        let ordered_pages = order_pages(&pages, &rules);
        let take = if only_ordered {
            pages == ordered_pages
        } else {
            pages != ordered_pages
        };
        if take {
            let mid_index = pages.len() / 2;
            let page_number = ordered_pages[mid_index].parse::<i32>().unwrap();
            total += page_number;
        }
    }
    total
}

fn part1(text: &str) -> i32 {
    middle_page_number_sum(text, true)
}

fn part2(text: &str) -> i32 {
    middle_page_number_sum(text, false)
}

fn main() {
    aoc2024::solve(part1, part2);
}
