
#include <iostream>
#include <string>
#include <vector>
#include <sstream>

#include "utils.h"

using namespace std;


bool is_invalid_id(long long id) {
    string str_id = to_string(id);
    int n = str_id.size();
    if (n % 2 != 0) {
        return false;
    }
    int half = n / 2;
    string left = str_id.substr(0, half);
    string right = str_id.substr(half, half);
    return left == right && left[0] != '0';
}

long long invalid_ids_sum(long long start, long long end) {
    long long sum = 0;
    for (long long id = start; id <= end; ++id) {
        if (is_invalid_id(id)) {
            // cout << "Invalid ID: " << id << endl;
            sum += id;
        }
    }
    return sum;
}

const string part1(const string &input) {
    vector<string> intervals = input | std::views::split(',') |
           std::views::transform([](auto &&rng) { return std::string(rng.begin(), rng.end()); }) |
           std::ranges::to<std::vector<std::string>>();
    long long start, end;
    char dash;
    long long total_sum = 0;
    for (const string& interval : intervals) {
        stringstream ss(interval);
        ss >> start >> dash >> end;
        // cout << "Start: " << start << ", End: " << end << endl;
        total_sum += invalid_ids_sum(start, end);
    }
    return to_string(total_sum);
}

const string part2(const string &input) {
    return "";
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}