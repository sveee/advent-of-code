#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <set>
#include <map>
#include <limits.h>
#include <algorithm>
#include <cassert>


std::vector<std::pair<char, int>> read_input() {
    std::string line;
    std::vector<std::pair<char, int>> instructions;
    while (std::getline(std::cin, line)) {
        size_t hexStart = line.find('#');
        if (hexStart != std::string::npos) {
            assert(line.size() - hexStart - 3 > 0);
            std::string hexStr = line.substr(hexStart + 1, line.size() - hexStart - 3);
            std::istringstream iss(hexStr);
            int num;
            iss >> std::hex >> num;
            instructions.push_back(std::make_pair(line[line.size()-2], num));
        }
    }
    return instructions;
}


std::set<std::pair<int, int>> get_trench(std::vector<std::pair<char, int>> &instructions) {
    int x = 0, y = 0;
    int dx, dy;
    std::set<std::pair<int, int>> trench;
    trench.insert(std::make_pair(0, 0));
    for (const auto& [c, num] : instructions) {

        switch (c) {
            case '0':
                dx = 0;
                dy = 1;
                break;
            case '1':
                dx = 1;
                dy = 0;
                break;
            case '2':
                dx = 0;
                dy = -1;
                break;
            case '3':
                dx = -1;
                dy = 0;
                break;
            default:
                break;
        }

        int k = num;

        while(k--) {
            x += dx;
            y += dy;
            trench.insert(std::make_pair(x, y));
        }
    }
    return trench;
}

int get_direction(std::pair<int, int> point, std::set<std::pair<int, int>> &trench) {

    if (trench.find(std::make_pair(point.first - 1 , point.second)) != trench.end()) {
        return -1;
    }
    return 1;
}

void print_trench(std::set<std::pair<int, int>> &trench) {
    for (const auto& pair : trench) {
        std::cout << "(" << pair.first << ", " << pair.second << ")" << std::endl;
    }
}


long long get_interior_size(std::set<std::pair<int, int>> &trench) {
    std::map<int, std::vector<int>> ys_by_x;
    int min_x = INT_MAX, max_x = INT_MIN;
    for (const auto& [x, y] : trench) {
        ys_by_x[x].push_back(y);
        min_x = std::min(min_x, x);
        max_x = std::max(max_x, x);
    }
    std::cout << min_x << " " << max_x << std::endl;
    long long interior_size = trench.size();
    for (int x = min_x; x <= max_x; ++x) {
        std::vector<int> ys = ys_by_x[x];
        sort(ys.begin(), ys.end());
        int index = 0, prev_end_y = -1;
        bool is_inside = false;
        while (index < ys.size()) {
            int start_y = ys[index];
            int end_y = ys[index];

            if (is_inside) {
                interior_size += start_y - prev_end_y - 1;
            }

            while (index + 1 < ys.size() && ys[index + 1] == end_y + 1) {
                ++index;
                end_y = ys[index];
            }

            if (start_y == end_y || get_direction(std::make_pair(x, start_y), trench) != get_direction(std::make_pair(x, end_y), trench)) {
                is_inside = !is_inside;
            }

            ++index;
            prev_end_y = end_y;
        }
    }

    return interior_size;
}

int main() {
    std::vector<std::pair<char, int>> instructions = read_input();
    std::set<std::pair<int, int>> trench = get_trench(instructions);
    std::cout << trench.size() << std::endl;
    std::cout << get_interior_size(trench) << std::endl;
    return 0;
}