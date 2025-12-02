#include <algorithm> // find
#include <cassert>
#include <fstream>
#include <cmath>
#include <stdexcept>
#include <string>
#include <vector>

// helper to split a string on a char
std::vector<std::string> split(const std::string& str, const char delimiter) {
    std::vector<std::string> res;
    auto p2 = str.begin();
    while (p2 != str.end()) {
        auto p1 = p2;
        p2 = std::find(p1, str.end(), delimiter);
        auto sv = std::string(p1, p2);
        res.push_back(sv);
        if (p2 != str.end()) {
            p2++;
        }
    }
    return res;
}

// parse data using split - should use regex really
std::vector<std::pair<long, long>> parse(const std::string& strdata) {
    std::vector<std::pair<long, long>> res;
    for (auto& substr : split(strdata, ',')) {
        auto pair = split(substr, '-');
        res.push_back({std::stol(pair[0]), std::stol(pair[1])});
    }
    return res;
}

// check if a number is made up of n identical sub-numbers
bool is_repeat(long num, int n) {
    int digits = std::ceil(std::log10(num));
    if (digits % n != 0) {
        return false;
    }
    int base = std::pow(10, digits / n);
    int last = num % base;
    for (size_t i = 1; i < n; i++) {
        num /= base;
        int current = num % base;
        if (current != last) {
            return false;
        }
        last = current;
    }
    return true;
}

// check if a number is the repetition of a sub-number, at least twice
bool is_repeat(long num) {
    int digits = std::ceil(std::log10(num));
    for (int splits = 2; splits <= digits; splits++) {
        if (is_repeat(num, splits)) {
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

    // split the string into <long, long> pairs
    auto ranges = parse(strdata);

    // loop over the ranges, checking through each one, part 1
    long total = 0;
    for (auto& rng : ranges) {
        int x = 0;
        for (long i = rng.first; i <= rng.second; i++) {
            if (is_repeat(i, 2)) {
                total += i;
            }
        }
    }
    //assert(total == 26255179562);

    // loop over the ranges, checking through each one, part 2
    total = 0;
    for (auto& rng : ranges) {
        int x = 0;
        for (long i = rng.first; i <= rng.second; i++) {
            if (is_repeat(i)) {
                total += i;
            }
        }
    }
    //assert(total == 31680313976);

    return 0;
}
