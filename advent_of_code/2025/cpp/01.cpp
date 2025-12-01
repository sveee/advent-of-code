
#include <iostream>
#include <string>
#include <vector>

#include "utils.h"

using namespace std;

const string part1(const string &input) {
    vector<string> lines = get_lines(input);
    int dial = 50;
    int password = 0;
    for (auto &line : lines) {
        int direction = (line[0] == 'L') ? -1 : 1;
        int value = stoi(line.substr(1));
        dial = (dial + direction * value + 100) % 100;
        if (dial == 0) {
            ++password;
        }
    }
    return to_string(password);
}

const string part2(const string &input) {
    vector<string> lines = get_lines(input);
    int dial = 50;
    int password = 0;
    for (auto &line : lines) {
        int direction = (line[0] == 'L') ? -1 : 1;
        int value = stoi(line.substr(1));
        // // optimize bf
        // password += value / 100;
        // value = value % 100;
        //
        for (int k = 0; k < value; ++k) {
            dial += direction;
            if (dial >= 100) {
                dial = 0;
            } else if (dial < 0) {
                dial = 99;
            }
            if (dial == 0) {
                ++password;
            }
        }
    }
    return to_string(password);
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}