#include <iostream>
#include <algorithm>
#include <cassert>
#include <fstream>
#include <string>

static std::string alphabet("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ");
int score(const char c) {
    auto pos = std::find(alphabet.begin(), alphabet.end(), c);
    return std::distance(alphabet.begin(), pos) + 1;
}

int main() {
    std::ifstream ifs("input.txt");

    std::string s1, s2, s3;
    int sum;
    while (std::getline(ifs, s1) and std::getline(ifs, s2) and std::getline(ifs, s3)) {
        for (auto& item : s1) {
            if (std::count(s2.begin(), s2.end(), item) and std::count(s3.begin(), s3.end(), item)) {
                sum += score(item);
                break;
            }
        }
    }

    assert(sum == 2548);
    return 0;
}
