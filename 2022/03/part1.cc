#include <algorithm>
#include <cassert>
#include <fstream>
#include <string>

static std::string alphabet("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ");

int main() {
    std::ifstream ifs("input.txt");

    std::string s;
    int sum;
    while (std::getline(ifs, s)) {
        for (size_t i = 0; i < s.size() / 2; i++) {
            if (std::count(s.begin() + s.size() / 2, s.end(), s[i])) {
                auto pos = std::find(alphabet.begin(), alphabet.end(), s[i]);
                sum += std::distance(alphabet.begin(), pos) + 1;
                break;
            }
        }
    }

    assert(sum == 7903);
    return 0;
}
