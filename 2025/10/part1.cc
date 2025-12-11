#include "parse.hh"

#include <cassert>
#include <deque>

// press the buttons corresponding to the basis vectors according to presses
std::vector<int> combine(const std::vector<std::vector<int>>& bases, const std::vector<int>& presses) {
    std::vector<int> sum(bases[0].size(), 0);
    for (auto button : presses) {
        for (size_t j = 0; j < bases[0].size(); j++) {
            sum[j] += bases[button][j];
            sum[j] %= 2;
        }
    }
    return sum;
}

// element wise vector comparison
bool vectors_equal(std::vector<int> a, std::vector<int> b) {
    assert(a.size() == b.size());
    for (size_t i = 0; i < a.size(); i++) {
        if (a[i] != b[i]) {
            return false;
        }
    }
    return true;
}

// breadth first search, keeping the options in a std::deque container
int main() {
    auto data = load_data("input.txt");
    long tot = 0;
    for (auto& row : data) {
        auto target = std::get<0>(row);
        auto buttons = std::get<1>(row);
        std::deque<std::vector<int>> q {{},};
        while (!q.empty()) {
            // get a button press combo
            auto combo = q.front();
            q.pop_front();
            // see if we have found one (which would then be the shortest)
            if (vectors_equal(combine(buttons, combo), target)) {
                tot += combo.size();
                break;
            }
            // otherwise, put new combos in the queue
            for (int b = 0; b < buttons.size(); b++) {
                auto copy = combo;
                copy.push_back(b);
                q.push_back(copy);
            }
        }
    }

    assert (tot == 452);
    return 0;
}
