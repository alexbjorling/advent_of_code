#include <algorithm> // max_element
#include <cassert>
#include <cmath> // pow
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
    long long tot = 0;
    std::string line;
    while (std::getline(ifs, line)) {
        std::vector<int> ascii(line.cbegin(), line.cend());
        long long num = 0;
        auto start = ascii.cbegin();
        for (int digit = 12; digit >= 1; digit--) {
            auto pos = std::max_element(start, ascii.cend() - digit + 1);
            num += std::pow(10, digit - 1) * (*pos - '0');
            start = pos + 1;
        }
        tot += num;
    }
    assert(tot == 168027167146027);

    return 0;
}
