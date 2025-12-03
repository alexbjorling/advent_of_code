#include <algorithm> // max_element
#include <cassert>
#include <fstream>
#include <stdexcept>
#include <string>
#include <vector>

int main() {
    // read data
    std::ifstream ifs("input.txt");
    if (ifs.fail()) {
        throw std::runtime_error("Failed to open input file");
    }

    // work directly on ascii vector, could convert to numbers with std::transform too
    int tot = 0;
    std::string line;
    while (std::getline(ifs, line)) {
        std::vector<int> ascii(line.cbegin(), line.cend());
        auto pos1 = std::max_element(ascii.cbegin(), ascii.cend() - 1);
        auto pos2 = std::max_element(pos1 + 1, ascii.cend());
        tot += (*pos1 - '0') * 10 + (*pos2 - '0');
    }
    assert(tot == 16973);

    return 0;
}
