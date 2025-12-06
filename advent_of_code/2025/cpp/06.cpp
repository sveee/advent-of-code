
#include <algorithm>
#include <cmath>
#include <iostream>
#include <ranges>
#include <sstream>
#include <string>
#include <vector>

#include "utils.h"

using namespace std;

long long reduce(vector<int> &numbers, char op) {
    long long result;
    if (op == '+') {
        result = 0;
        for (int n : numbers) {
            result += n;
        }
    } else if (op == '*') {
        result = 1;
        for (int n : numbers) {
            result *= n;
        }
    }
    return result;
}

const string part1(const string &input) {
    vector<string> lines = split_string(input);

    vector<char> operators;
    char op;
    stringstream last_line(lines.back());
    while (last_line >> op) {
        operators.push_back(op);
    }

    vector<vector<int>> numbers;
    for (size_t i = 0; i < lines.size() - 1; ++i) {
        vector<int> row;
        stringstream line_stream(lines[i]);
        int number;
        while (line_stream >> number) {
            row.push_back(number);
        }
        numbers.push_back(row);
    }
    long long total = 0;
    for (int j = 0; j < numbers[0].size(); ++j) {
        vector<int> column;
        for (int i = 0; i < numbers.size(); ++i) {
            column.push_back(numbers[i][j]);
        }
        total += reduce(column, operators[j]);
    }

    return to_string(total);
}

bool is_digit(char c) {
    return c >= '0' && c <= '9';
}

const string part2(const string &input) {
    vector<string> lines = split_string(input);

    vector<char> operators;
    char op;
    stringstream last_line(lines.back());
    while (last_line >> op) {
        operators.push_back(op);
    }

    vector<int> numbers;
    long long total = 0;
    int j = 0;
    for (int k = 0; k < lines[0].size(); ++k) {
        int number = 0;
        for (int i = 0; i < lines.size() - 1; ++i) {
            if (isdigit(lines[i][k])) {
                number = 10 * number + (lines[i][k] - '0');
            } else {
                if (number != 0) {
                    break;
                }
            }
        }
        if (number == 0) {
            total += reduce(numbers, operators[j]);
            ++j;
            numbers.clear();
        } else {
            numbers.push_back(number);
        }
    }
    total += reduce(numbers, operators[j]);

    return to_string(total);
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}