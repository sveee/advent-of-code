
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "utils.h"

using namespace std;

bool is_invalid_id_occurence(long long id, int k) {
    string str_id = to_string(id);
    int n = str_id.size();
    if (n % k != 0) {
        return false;
    }
    int chunk_size = n / k;
    string first = str_id.substr(0, chunk_size);
    for (int i = 1; i < k; ++i) {
        string chunk = str_id.substr(i * chunk_size, chunk_size);
        if (chunk != first) {
            return false;
        }
    }
    return true;
}

bool is_invalid_id_any(long long id) {
    string str_id = to_string(id);
    int n = str_id.size();
    for (int k = 2; k <= n; ++k) {
        if (is_invalid_id_occurence(id, k)) {
            return true;
        }
    }
    return false;
}

long long invalid_ids_sum_2(long long start, long long end) {
    long long sum = 0;
    for (long long id = start; id <= end; ++id) {
        if (is_invalid_id_occurence(id, 2)) {
            sum += id;
        }
    }
    return sum;
}

long long invalid_ids_sum_any(long long start, long long end) {
    long long sum = 0;
    for (long long id = start; id <= end; ++id) {
        if (is_invalid_id_any(id)) {
            sum += id;
        }
    }
    return sum;
}

vector<string> get_intervals(const string &input_data) {
    return input_data | std::views::split(',') |
           std::views::transform([](auto &&rng) { return std::string(rng.begin(), rng.end()); }) |
           std::ranges::to<std::vector<std::string>>();
}

const string part1(const string &input) {
    vector<string> intervals = get_intervals(input);
    long long start, end;
    char dash;
    long long total_sum = 0;
    for (const string &interval : intervals) {
        stringstream ss(interval);
        ss >> start >> dash >> end;
        total_sum += invalid_ids_sum_2(start, end);
    }
    return to_string(total_sum);
}

const string part2(const string &input) {
    vector<string> intervals = get_intervals(input);
    long long start, end;
    char dash;
    long long total_sum = 0;
    for (const string &interval : intervals) {
        stringstream ss(interval);
        ss >> start >> dash >> end;
        total_sum += invalid_ids_sum_any(start, end);
    }
    return to_string(total_sum);
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}