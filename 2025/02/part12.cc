#include <cassert>
#include <fstream>
#include <regex>
#include <stdexcept>
#include <string>
#include <vector>

// parse data using regex
std::vector<std::pair<long, long>> parse(const std::string& strdata) {
    std::vector<std::pair<long, long>> res;
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

// check if a number is made up of n identical sub-numbers
bool is_repeat(long num, int n) {
    // make a string and check that it can be split into n_repeat parts
    std::string s = std::to_string(num);
    if (s.size() % n != 0) {
        return false;
    }

    // loop through all the n_repeat parts, checking for identity
    int len = s.size() / n;
    std::string last(s.begin(), s.begin() + len);
    for (size_t i = 1; i < n; i++) {
        std::string current(s.begin() + i * len, s.begin() + (i + 1) * len);
        if (current != last) {
            return false;
        }
        last = current;
    }
    return true;
}

// check if a number is the repetition of a sub-number, at least twice
bool is_repeat(long num) {
    std::string s = std::to_string(num);
    for (int splits = 2; splits <= s.size(); splits++) {
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
    assert(total == 26255179562);

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
    assert(total == 31680313976);

    return 0;
}
