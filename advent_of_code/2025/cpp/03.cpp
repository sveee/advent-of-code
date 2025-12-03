
#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>
#include <vector>

#include "utils.h"

using namespace std;

int largest_joltage(const string &line) {
    int n = line.size();
    int max_joltage = 0;
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            int joltage = (line[i] - '0') * 10 + (line[j] - '0');
            if (joltage > max_joltage) {
                max_joltage = joltage;
            }
        }
    }
    return max_joltage;
}

const string part1(const string &input) {
    vector<string> lines = get_lines(input);
    int total = 0;
    for (const string &line : lines) {
        total += largest_joltage(line);
    }
    return to_string(total);
}

long long largest_joltage_rec(int index, int remaining, const string &line) {
    if (remaining == line.size() - index) {
        return stoll(line.substr(index));
    }
    long long joltage1 =
        largest_joltage_rec(index + 1, remaining - 1, line) * 10 + line[index] - '0';
    long long joltage2 = largest_joltage_rec(index + 1, remaining, line);
    return max(joltage1, joltage2);
}

long long dp[100][100][13];

long long f(int start, int end, int k, const string &bank) {
    if (dp[start][end][k] != -1LL) {
        return dp[start][end][k];
    }
    if (end - start == k) {
        return stoll(bank.substr(start, k));
    }
    if (k == 1) {
        return (*max_element(bank.begin() + start, bank.begin() + end)) - '0';
    }
    long long joltage = max({
        f(start + 1, end, k, bank),
        f(start, end - 1, k, bank),
        f(start, end - 1, k - 1, bank) * 10 + bank[end - 1] - '0',
        f(start + 1, end, k - 1, bank) + (bank[start] - '0') * (long long)pow(10, k - 1),
    });
    dp[start][end][k] = joltage;
    return joltage;
}

void reset_memory() {
    for (int i = 0; i < 100; ++i) {
        for (int j = 0; j < 100; ++j) {
            for (int k = 0; k < 13; ++k) {
                dp[i][j][k] = -1LL;
            }
        }
    }
}

const string part2(const string &input) {
    vector<string> lines = get_lines(input);
    long long total = 0;
    for (const string &line : lines) {
        reset_memory();
        total += f(0, line.size(), 12, line);
    }
    return to_string(total);
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}