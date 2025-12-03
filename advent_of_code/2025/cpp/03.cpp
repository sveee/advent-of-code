
#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>
#include <vector>

#include "utils.h"

using namespace std;

long long f[100][100][13];

long long max_joltage(int start, int end, int k, const string &bank) {
    if (f[start][end][k] != -1LL) {
        return f[start][end][k];
    }
    if (end - start == k) {
        return stoll(bank.substr(start, k));
    }
    if (k == 1) {
        return (*max_element(bank.begin() + start, bank.begin() + end)) - '0';
    }
    long long joltage = max({
        max_joltage(start + 1, end, k, bank),
        max_joltage(start, end - 1, k, bank),
        max_joltage(start, end - 1, k - 1, bank) * 10 + bank[end - 1] - '0',
        max_joltage(start + 1, end, k - 1, bank) + (bank[start] - '0') * (long long)pow(10, k - 1),
    });
    f[start][end][k] = joltage;
    return joltage;
}

void reset_memory() {
    for (int i = 0; i < 100; ++i) {
        for (int j = 0; j < 100; ++j) {
            for (int k = 0; k < 13; ++k) {
                f[i][j][k] = -1LL;
            }
        }
    }
}

const string part1(const string &input) {
    vector<string> lines = split_lines(input);
    int total = 0;
    for (const string &line : lines) {
        reset_memory();
        total += max_joltage(0, line.size(), 2, line);
    }
    return to_string(total);
}

const string part2(const string &input) {
    vector<string> lines = split_lines(input);
    long long total = 0;
    for (const string &line : lines) {
        reset_memory();
        total += max_joltage(0, line.size(), 12, line);
    }
    return to_string(total);
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}