#include <cassert>
#include <fstream>
#include <list>
#include <regex>
#include <set>
#include <string>

typedef std::map<std::string, std::list<std::string>> Map;

Map parse_map(const std::string& fn) {
    std::ifstream ifs(fn);
    std::string line;
    Map map;
    while (std::getline(ifs, line)) {
        std::regex pattern("[a-z]{3}");
        auto first = std::sregex_iterator(line.begin(), line.end(), pattern);
        auto last = std::sregex_iterator();
        std::list<std::string> strings;
        for (auto match = first; match != last; match++) {
            strings.push_back((*match)[0].str());
        }
        auto key = strings.front();
        strings.pop_front();
        map.insert_or_assign(key, strings);
    }
    return map;
}

// Recursively count paths from start to "out" - simplest possible
long count_paths(const std::string& start, const Map& map) {
    if (start == "out") {
        return 1;
    }
    long tot = 0;
    for (auto& dest : map.at(start)) {
        tot += count_paths(dest, map);
    }
    return tot;
}

// Recursively count paths from start to "you". This is hard to cache,
// and the info about whether we've gone through the specified vias must
// be put in the cache key.
long count_paths_via(const std::string& start,
                    const std::list<std::string> vias,
                    std::set<std::string> history,
                    const Map& map) {
    static std::map<std::string, long> cache;

    // have we been past the via points? put that info in the cache key in an ugly way
    std::string cache_key(start);
    for (auto via : vias) {
        cache_key.push_back(history.count(via) ? '1' : '0');
    }
    if (cache.count(cache_key)) {
        return cache.at(cache_key);
    }

    // are we there yet? if so, check that we've seen the via points
    if (start == "out") {
        for (auto& via : vias) {
            if (history.count(via) == 0) {
                return 0;
            }
        }
        return 1;
    }

    // avoid loops
    if (history.count(start)) {
        return 0;
    }
    history.insert(start);

    // recurse and cache
    long tot = 0;
    for (auto& dest : map.at(start)) {
        tot += count_paths_via(dest, vias, history, map);
    }
    cache.insert_or_assign(cache_key, tot);
    return tot;
}

int main() {
    auto map = parse_map("input.txt");
    assert(count_paths("you", map) == 649); // part 1
    assert(count_paths_via("svr", {"dac", "fft"}, {}, map) == 458948453421420); // part 2
    return 0;
}
