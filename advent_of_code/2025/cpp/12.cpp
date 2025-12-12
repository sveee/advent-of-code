
#include <algorithm>
#include <cmath>
#include <iostream>
#include <ranges>
#include <sstream>
#include <string>
#include <vector>

#include "utils.h"

using namespace std;

const string part1(const string &input) {
    vector<string> parts = split_string(input, "\n\n");
    vector<int> shape_areas;
    for (int i = 0; i < parts.size() - 1; ++i) {
        shape_areas.push_back(ranges::count(parts[i], '#'));
    }
    vector<string> regions = split_string(parts.back());

    int n, m, index, count, present_area;
    char c;
    int total = 0;
    stringstream ss;
    for (const string &region : regions) {
        parts = split_string(region, ": ");
        ss = stringstream(parts[0]);
        ss >> n >> c >> m;
        ss = stringstream(parts[1]);
        index = 0;
        present_area = 0;
        while (ss >> count) {
            present_area += shape_areas[index] * count;
            ++index;
        }
        if (n * m >= present_area) ++total;
    }
    return to_string(total);
}

const string part2(const string &input) {
    vector<string> lines = split_string(input);
    return "";
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}