
#include <algorithm>
#include <cmath>
#include <iostream>
#include <ranges>
#include <string>
#include <vector>

#include "utils.h"

using namespace std;

const string part1(const string &input) {
    vector<string> parts = split_string(input, "\n\n");
    vector<string> lines;

    lines = split_string(parts[0]);
    vector<pair<long long, long long>> ranges;
    for (auto &line : lines) {
        vector<string> boundaries = split_string(line, "-");
        ranges.push_back(make_pair(stoll(boundaries[0]), stoll(boundaries[1])));
    }
    lines = split_string(parts[1]);
    int n_fresh = 0;
    for (auto &line : lines) {
        long long val = stoll(line);
        for (auto &[start, end] : ranges) {
            if (start <= val && val <= end) {
                n_fresh++;
                break;
            }
        }
    }

    return to_string(n_fresh);
}

const string part2(const string &input) {
    vector<string> parts = split_string(input, "\n\n");
    vector<string> lines;

    lines = split_string(parts[0]);
    vector<pair<long long, long long>> ranges;
    for (auto &line : lines) {
        vector<string> boundaries = split_string(line, "-");
        ranges.push_back(make_pair(stoll(boundaries[0]), stoll(boundaries[1])));
    }
    sort(ranges.begin(), ranges.end());
    vector<pair<long long, long long>> merged_ranges;
    for (auto &[start, end] : ranges) {
        if (merged_ranges.empty() || merged_ranges.back().second < start) {
            merged_ranges.push_back({start, end});
        } else {
            merged_ranges.back().second = max(merged_ranges.back().second, end);
        }
    }
    long long n_fresh = 0;
    for (auto &[start, end] : merged_ranges) {
        n_fresh += end - start + 1;
    }
    return to_string(n_fresh);
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}