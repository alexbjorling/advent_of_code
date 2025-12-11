#include "parse.hh"

#include <cassert>
#include <iostream>

std::vector<int> mul(int c, std::vector<int> v) {
    std::vector<int> ret(v.cbegin(), v.cend());
    for (auto it = ret.begin(); it != ret.end(); it++) {
        *it *= c;
    }
    return ret;
}

std::vector<int> linear_combination(const std::vector<std::vector<int>>& bases, const std::vector<int>& coeffs) {
    assert(coeffs.size() == bases.size());
    std::vector<int> sum(bases[0].size());
    for (size_t i = 0; i < bases.size(); i++) {
        for (size_t j = 0; j < bases[0].size(); j++) {
            sum[i] += coeffs[i] * bases[i][j];
        }
        sum[i] = sum[i] % 2;
    }
    return sum;
}

bool vectors_equal(std::vector<int> a, std::vector<int> b) {
    assert(a.size() == b.size());
    for (size_t i = 0; i < a.size(); i++) {
        if (a[i] != b[i]) {
            return false;
        }
    }
    return true;
}

// give all combinations of n choices of the numbers min-max
std::vector<std::vector<int>> combinations(int n, int max) {
    // each initial choice in a vector of vectors
    std::vector<std::vector<int>> old_res;
    for (int j = 0; j <= max; j++) {
        old_res.push_back({j});
    }
    // now add choices
    for (int i = 1; i < n; i++) {
        std::vector<std::vector<int>> new_res {};
        for (auto& old : old_res) {
            for (int j = 0; j <= max; j++) {
                new_res.push_back(old);
                new_res.back().push_back(j);
            }
        }
        old_res = new_res;
    }
    return old_res;
}

int main() {
    auto data = load_data("ex.txt");
    for (auto& d : data) {
        auto target = std::get<0>(d);
        auto buttons = std::get<1>(d);
        int n = 1;
        while (true) {
            std::cout << n << std::endl;
            auto combos = combinations(n, buttons.size() - 1);
            for (auto& combo : combos) {
                std::vector<int> coeffs(buttons.size(), 0);
                for (auto& pos : combo) {
                    coeffs[pos] += 1;
                }
                if (vectors_equal(linear_combination(buttons, coeffs), target)) {
                    break;
                }
            }
            n++;
        }
    }

    return 0;
}
