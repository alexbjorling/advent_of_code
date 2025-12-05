#include <cassert>
#include <fstream>
#include <regex>
#include <stdexcept>
#include <string>
#include <set>

typedef std::set<std::pair<long, long>> range_set;

// helper to load the file
std::string load(std::string fn) {
    std::ifstream ifs(fn);
    if (ifs.fail()) {
        throw std::runtime_error("Failed to open input file");
    }
    std::stringstream buf;
    buf << ifs.rdbuf();
    std::string data(buf.str());
    data.append("\n"); // :(
    return data;
}

// helper to parse a set of ints
std::set<long> parse_ints(std::string& data, std::regex pattern) {
    std::set<long> ret {};
    auto begin = std::sregex_iterator(data.cbegin(), data.cend(), pattern);
    auto end = std::sregex_iterator();
    for (auto it = begin; it != end; it++) {
        auto match = *it;
        ret.insert(std::stol(match.str())); // index 0 is the whole match
    }
    return ret;
}

// helper to parse a set of pair<long, long>:s
range_set parse_pairs(std::string& data, std::regex pattern) {
    range_set ret {};
    auto begin = std::sregex_iterator(data.cbegin(), data.cend(), pattern);
    auto end = std::sregex_iterator();
    for (auto it = begin; it != end; it++) {
        auto match = *it;
        if (match.size() >= 2) {
            ret.emplace(std::stol(match[1].str()), std::stol(match[2].str())); // index 0 is the whole match
        }
    }
    return ret;
}

// helper to see if a number is contained in any range out of a set
bool in_range(const range_set& ranges, long id) {
    for (auto& range : ranges) {
        if (id >= range.first and id <= range.second) {
            return true;
        }
    }
    return false;
}

// helper to find the first two ranges in a set that overlap
// returns true if it finds them
typedef range_set::iterator range_it;
bool find_overlap(const range_set& ranges, range_it& it1, range_it& it2) {
    for (auto r1 = ranges.begin(); r1 != ranges.end(); r1++) {
        for (auto r2 = r1; r2 != ranges.end(); r2++) {
            if (r1 == r2) { continue; }
            if (not ((*r1).first > (*r2).second or (*r1).second < (*r2).first)) {
                // found an overlap
                it1 = r1;
                it2 = r2;
                return true;
            }
        }
    }
    return false;
}

int main() {
    // load the file as one long string
    auto data = load("input.txt");

    // fish out a set of ranges and ids
    auto ranges = parse_pairs(data, std::regex("([0-9]+)-([0-9]+)"));
    auto ids = parse_ints(data, std::regex("(\\n)(\\s*)([0-9]+)(?=\\s)"));
    long max = 0;
    long min = (*ranges.begin()).first;
    for (auto& range : ranges) {
        min = std::min(min, range.first);
        max = std::max(max, range.second);
    }

    // part 1: see which ids are in the ranges
    int tot = 0;
    for (auto& id : ids) {
        tot += in_range(ranges, id);
    }
    assert (tot == 712);

    // part2: remove overlaps between ranges by merging, then sum the entries
    range_set::iterator it1, it2;
    while (find_overlap(ranges, it1, it2)) {
        ranges.erase((*it1));
        ranges.erase((*it2));
        ranges.emplace(std::min((*it1).first, (*it2).first), std::max((*it1).second, (*it2).second));
    }

    uint64_t cnt = 0;
    for (auto& range : ranges) {
        cnt += (range.second - range.first + 1);
    }
    assert(cnt == 332998283036769);

    return 0;
}
