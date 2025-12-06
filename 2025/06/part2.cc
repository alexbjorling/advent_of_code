#include <cassert>
#include <fstream>
#include <regex>
#include <stdexcept>
#include <string>
#include <vector>

// helper to parse the operators with regex
std::string parse_operators(std::string& data) {
    std::string ret {};
    std::regex pattern("([+*]+)");
    auto begin = std::sregex_iterator(data.cbegin(), data.cend(), pattern);
    auto end = std::sregex_iterator();
    for (auto it = begin; it != end; it++) {
        auto match = *it;
        ret.push_back(match[0].str()[0]); // index 0 is the whole match
    }
    return ret;
}

bool all_spaces(const std::string& s) {
    return std::all_of(s.cbegin(), s.cend(), [](char c) { return c == ' '; });
}

int main() {
    // load the file as a vector of strings
    std::ifstream ifs("input.txt");
    if (ifs.fail()) {
        throw std::runtime_error("Failed to open input file");
    }
    std::string line;
    std::vector<std::string> lines;
    while (std::getline(ifs, line)) {
        lines.push_back(line);
    }

    // fish out all the operators from the last line and remove it
    auto operators = parse_operators(lines.back());
    lines.pop_back();

    // each group  has a different number of columns, so loop to create a
    // vector of groups of ints to operate on later.
    std::vector<std::vector<int>> groups;
    std::vector<int> nums {};
    for (size_t j = 0; j < lines[0].size(); j++) {
        std::string col {};
        for (size_t i = 0; i < lines.size(); i++) {
            col.push_back(lines[i][j]);
        }
        if (all_spaces(col)) {
            groups.push_back(nums);
            nums.clear();
        } else {
            nums.push_back(std::stoi(col));
        }
    }
    groups.push_back(nums); // last number
    assert(groups.size() == operators.size());

    // add up the results
    long tot = 0;
    for (size_t i = 0; i < groups.size(); i++) {
        long res;
        if (operators[i] == '*') {
            res = 1;
            for (auto& n : groups[i]) {
                res *= n;
            }
        } else if (operators[i] == '+') {
            res = 0;
            for (auto& n : groups[i]) {
                res += n;
            }
        } else {
            throw std::runtime_error("Unexpected operator");
        }
        tot += res;
    }
    assert (tot == 10389131401929);

    return 0;
}
