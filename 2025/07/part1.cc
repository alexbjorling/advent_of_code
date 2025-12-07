#include <cassert>
#include <fstream>
#include <regex>
#include <stdexcept>
#include <string>
#include <set>

typedef std::pair<int, int> position;
typedef std::set<position> set;

int main() {
    // open the input file
    std::ifstream ifs("input.txt");
    if (ifs.fail()) {
        throw std::runtime_error("Failed to open input file");
    }

    // find the splitters and the starting position
    set splitters;
    position start;
    std::string line;
    size_t n = 0;
    while (std::getline(ifs, line)) {
        for (size_t j = 0; j < line.size(); j++) {
            if (line[j] == '^') {
                splitters.emplace(n, j);
            } else if (line[j] == 'S') {
                (start = {n, j});
            }
        }
        n++;
    }

    // since the beams combine, it's best to keep track of the current front
    // of beams in a set.
    int splits = 0;
    set front {start};
    for (size_t i = 0; i < n; i++) {
        set new_front {};
        for (auto& pos : front) {
            if (splitters.count(pos)) {
                // this one is on a splitter!
                new_front.insert({pos.first + 1, pos.second - 1});
                new_front.insert({pos.first + 1, pos.second + 1});
                splits++;
            } else {
                // no splitter here, just propagate down
                new_front.insert({pos.first + 1, pos.second});
            }
        }
        front = new_front;
    }
    assert(splits == 1594);

    return 0;
}