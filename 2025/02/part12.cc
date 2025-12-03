#include <cassert>
#include <fstream>
#include <cmath>
#include <regex>
#include <stdexcept>
#include <string>
#include <vector>

#define int_t uint64_t

// parse data using regex
std::vector<std::pair<int_t, int_t>> parse(const std::string& strdata) {
    std::vector<std::pair<int_t, int_t>> res;
    std::regex pattern("([0-9]+)-([0-9]+)");
    auto begin = std::sregex_iterator(strdata.begin(), strdata.end(), pattern);
    auto end = std::sregex_iterator();
    for (auto it = begin; it != end; it++) {
        auto match = *it;
        if (match.size() >= 2) {
            res.push_back({std::stol(match[1].str()), std::stol(match[2].str())}); // index 0 is the whole match
        }
    }
    return res;
}

// numerically check if a number is made up of n identical sub-numbers
bool is_repeat(int_t num, int n) {
    int digits = std::ceil(std::log10(num + 1));
    if (digits % n != 0) {
        return false;
    }
    int_t base = std::pow(10, digits / n);
    int_t last = num % base;
    for (size_t i = 1; i < n; i++) {
        num /= base;
        int_t current = num % base;
        if (current != last) {
            return false;
        }
        last = current;
    }
    return true;
}

// check if a number is the repetition of a smaller group
bool is_repeat(int_t num) {
    int digits = std::ceil(std::log10(num + 1));
    for (int groups = 2; groups <= digits; groups++) {
        if (is_repeat(num, groups)) {
            return true;
        }
    }
    return false;
}

int main() {
    // read data
    std::ifstream ifs("input.txt");
    if (ifs.fail()) {
        throw std::runtime_error("Failed to open input file");
    }
    std::string strdata;
    std::getline(ifs, strdata);

    // split the string into <int_t, int_t> pairs
    auto ranges = parse(strdata);

    // loop over the ranges, checking through each one, part 1
    int_t total = 0;
    for (auto& rng : ranges) {
        for (int_t i = rng.first; i <= rng.second; i++) {
            if (is_repeat(i, 2)) {
                total += i;
            }
        }
    }
    assert(total == 26255179562);

    // loop over the ranges, checking through each one, part 2
    total = 0;
    for (auto& rng : ranges) {
        for (int_t i = rng.first; i <= rng.second; i++) {
            if (is_repeat(i)) {
                total += i;
            }
        }
    }
    assert(total == 31680313976);

    return 0;
}
