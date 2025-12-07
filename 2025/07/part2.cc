#include <cassert>
#include <fstream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>

typedef std::pair<int, int> position;
typedef std::set<position> set;
typedef std::map<position, long> cache_map;

// return the number of paths that will eventually result from a beam starting
// at pos - recursively until it exits the width x height board. cached!
long count_paths(const set& splitters, position pos, const int& width,
                 const int& height) {
    static cache_map cache {};
    if (cache.count(pos)) {
        return cache.at(pos);
    }
    auto [i, j] = pos;
    if (i >= height or j >= width  or j < 0) {
        // stopping condition: le've left the board
        return 1;
    } else if (splitters.count(pos)) {
        // we are on a splitter! spawn a beam on either side - good time to cache
        long c1 = count_paths(splitters, {i, j + 1}, width, height);
        long c2 = count_paths(splitters, {i, j - 1}, width, height);
        cache.insert_or_assign(pos, c1 + c2);
        return c1 + c2;
    } else {
        // next square is free space, just recurse
        auto res = count_paths(splitters, {pos.first + 1, pos.second}, width, height);
        return res;
    }
}

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
    size_t m = 0;
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
        m = line.size();
    }

    // recursively go through all the paths, passing along a lookup cache pos->result
    auto timelines = count_paths(splitters, start, m, n);
    assert(timelines == 15650261281478);

    return 0;
}