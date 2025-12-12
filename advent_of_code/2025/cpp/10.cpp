
#include <algorithm>
#include <climits>
#include <cmath>
#include <iostream>
#include <ranges>
#include <sstream>
#include <string>
#include <vector>

#include "utils.h"

using namespace std;

typedef vector<int> Vector;
typedef vector<Vector> Matrix;

int solve_diagram(const vector<bool> &diagram, const vector<vector<int>> &buttons) {
    int min_presses = INT_MAX;
    for (int state = 0; state < (1 << buttons.size()); ++state) {
        vector<bool> current_lights(diagram.size(), false);
        int n_pressed = 0;
        for (int button_index = 0; button_index < buttons.size(); ++button_index) {
            if ((state & (1 << button_index)) == 0) {
                continue;
            }
            ++n_pressed;
            for (int light_index : buttons[button_index]) {
                current_lights[light_index] = current_lights[light_index] ^ 1;
            }
        }
        if (current_lights == diagram) {
            min_presses = min(min_presses, n_pressed);
        }
    }
    return min_presses;
}

vector<bool> parse_diagram(const string &diagram_str) {
    vector<bool> diagram;
    for (int i = 1; i < diagram_str.size() - 1; ++i) {
        diagram.push_back(diagram_str[i] == '#');
    }
    return diagram;
}

vector<int> parse_vector(const string &button_str) {
    vector<int> button;
    vector<string> parts = split_string(button_str.substr(1, button_str.size() - 1), ",");
    for (const string &part : parts) {
        button.push_back(stoi(part));
    }
    return button;
}

const string part1(const string &input) {
    vector<string> lines = split_string(input);
    int total = 0;
    for (const string &line : lines) {
        vector<string> parts = split_string(line, " ");
        vector<bool> diagram = parse_diagram(parts[0]);
        vector<vector<int>> buttons;
        for (int i = 1; i < parts.size() - 1; ++i) {
            buttons.push_back(parse_vector(parts[i]));
        }
        total += solve_diagram(diagram, buttons);
    }
    return to_string(total);
}

void integer_gaussian_elimination(Matrix &A, Vector &b) {
    int n = A.size();
    int m = A[0].size();

    int r0 = 0;
    int pr;
    for (int c0 = 0; c0 < m; ++c0) {
        if (r0 >= n) {
            break;
        }
        pr = -1;
        for (int r = r0; r < n; ++r) {
            if (A[r][c0] != 0) {
                pr = r;
                break;
            }
        }
        if (pr == -1) {
            continue;
        }

        swap(A[r0], A[pr]);
        swap(b[r0], b[pr]);

        for (int r = r0 + 1; r < n; ++r) {
            int A_r_c0 = A[r][c0];
            if (A_r_c0 == 0) {
                continue;
            }
            for (int c = c0; c < m; ++c) {
                A[r][c] = A[r][c] * A[r0][c0] - A[r0][c] * A_r_c0;
            }
            b[r] = b[r] * A[r0][c0] - b[r0] * A_r_c0;
            A[r][c0] = 0;
        }
        r0 += 1;
    }
}

vector<vector<int>> solve_system(Matrix &A, Vector &b, int r, const Vector &max_x) {
    // backtracking solution
    int m = A[0].size();

    if (r < 0) {
        return {Vector(m, 0)};
    }
    vector<int> non_zero_columns;
    for (int c = 0; c < m; ++c) {
        if (A[r][c] != 0) {
            non_zero_columns.push_back(c);
        }
    }

    if (non_zero_columns.empty()) {
        if (b[r] != 0) return {};
        return solve_system(A, b, r - 1, max_x);
    }

    int c = non_zero_columns.back();
    vector<vector<int>> solutions;
    bool is_single_solution = (non_zero_columns.size() == 1);

    if (is_single_solution) {
        if (b[r] % A[r][c] != 0) return {};
        int val = b[r] / A[r][c];
        if (val < 0) return {};
    }

    vector<int> x_range;
    if (!is_single_solution) {
        for (int i = 0; i <= max_x[c]; ++i) {
            x_range.push_back(i);
        }
    } else {
        // the only possible value
        x_range.push_back(b[r] / A[r][c]);
    }

    vector<int> row_range;
    for (int i = 0; i <= r; ++i) row_range.push_back(i);

    for (int x : x_range) {
        Vector prev_b;
        Vector prev_column;
        for (int pr : row_range) {
            prev_b.push_back(b[pr]);
            prev_column.push_back(A[pr][c]);
        }
        for (int pr : row_range) {
            b[pr] -= x * A[pr][c];
            A[pr][c] = 0;
        }
        int next_r = r - (is_single_solution ? 1 : 0);
        auto current_solutions = solve_system(A, b, next_r, max_x);

        for (auto &solution : current_solutions) {
            solution[c] = x;
            solutions.push_back(solution);
        }

        // backtrack
        for (int i = 0; i < row_range.size(); ++i) {
            int pr = row_range[i];
            A[pr][c] = prev_column[i];
            b[pr] = prev_b[i];
        }
    }
    return solutions;
}

const string part2(const string &text) {
    vector<string> lines = split_string(text, "\n");

    int total = 0;
    for (const string &line : lines) {
        vector<string> parts = split_string(line, " ");
        Vector b = parse_vector(parts.back());
        int n_eq = b.size();
        vector<vector<int>> button_sets;
        for (int i = 1; i < parts.size() - 1; ++i) {
            vector<int> parsed = parse_vector(parts[i]);
            button_sets.push_back(parsed);
        }

        int n_vars = button_sets.size();

        Vector max_x;
        for (const auto &b_set : button_sets) {
            int current_min = INT_MAX;
            for (int idx : b_set) {
                current_min = min(current_min, b[idx]);
            }
            max_x.push_back(current_min);
        }

        Matrix A(n_eq, Vector(n_vars, 0));
        for (int c = 0; c < button_sets.size(); ++c) {
            for (int r : button_sets[c]) {
                A[r][c] = 1;
            }
        }

        integer_gaussian_elimination(A, b);
        Matrix solutions = solve_system(A, b, A.size() - 1, max_x);

        int min_presses = INT_MAX;
        int presses;
        for (const auto &sol : solutions) {
            presses = 0;
            for (int x : sol) {
                presses += x;
            }
            min_presses = min(min_presses, presses);
        }
        total += min_presses;
    }

    return to_string(total);
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}