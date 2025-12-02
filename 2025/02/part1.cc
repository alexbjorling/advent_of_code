#include <algorithm> // find
#include <cassert>
#include <fstream>
#include <stdexcept>
#include <string>
#include <vector>

// parse data with iterators and std::find (not regex...)
std::vector<std::pair<long, long>> parse(const std::string& strdata) {
    std::vector<std::pair<long, long>> res;
    auto p2 = strdata.begin();
    while (p2 != strdata.end()) {
        auto p1 = p2;
        p2 = std::find(p1, strdata.end(), ',');
        auto s = std::string(p1, p2);
        auto dash = std::find(s.begin(), s.end(), '-');
        long i1 = std::stol(std::string(s.begin(), dash));
        long i2 = std::stol(std::string(dash + 1, s.end()));
        res.push_back({i1, i2});
        if (p2 != strdata.end()) {
            p2++;
        }
    }
    return res;
}

// check if a number is a pair of two other sub-numbers
bool is_pair(long num) {
    std::string s = std::to_string(num);
    auto s1 = s.substr(0, s.size() / 2);
    auto s2 = s.substr(s.size() / 2);
    return s1 == s2;
}

// check if a number is the repetition of a sub-number, at least twice
bool is_repeat(long num) {
    std::string s = std::to_string(num);
    for (int splits = 2; splits <= s.size(); splits++) {
        if (s.size() % splits != 0) {
            continue;
        }
        int len = s.size() / splits;
        std::string last(s.begin(), s.begin() + len);
        bool ret = true;
        for (size_t i = 1; i < splits; i++) {
            if (std::string(s.begin() + i * len, s.begin() + (i + 1) * len) != last) {
                ret = false;
                break;
            }
        }
        if (ret) {
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

    // loop over the ranges, checking through each one
    long total = 0;
    for (auto& rng : ranges) {
        int x = 0;
        for (long i = rng.first; i <= rng.second; i++) {
            //if (is_pair(i)) { // part 1
            if (is_repeat(i)) { // part 2
                total += i;
            }
        }
    }

    //assert(total == 26255179562); // part 1
    assert(total == 31680313976); // part 2
    return 0;
}
