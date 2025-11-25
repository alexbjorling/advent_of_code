// g++ -g part12.cc && gdb a.out

#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <cassert>

int main() {

    // open the file
    std::ifstream ifs("input.txt");
    if (ifs.fail()) {
        return -1;
    }

    // go through its lines and accumulate elves
    std::vector<int> counts;
    int cnt = 0;
    std::string line;
    while (std::getline(ifs, line)) {
        if (line == "") {
            counts.push_back(cnt);
            cnt = 0;
        } else {
            cnt += std::stoi(line);
        }
    }

    // part 1: find the maximum elf
    auto ans = *std::max_element(counts.begin(), counts.end());
    assert(ans == 70116);

    // part 2: sort the vector to find the top three
    std::sort(counts.begin(), counts.end());
    int sum = 0;
    for (size_t i = 0; i < 3; i++) {
        sum += counts[counts.size() - 1 - i];
    }
    assert(sum == 206582);

    return 0;
}
