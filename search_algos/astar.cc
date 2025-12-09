/*
 * Example A* implementation,
 *
 * each node on the front is prioritized according to
 *
 *     f = g + h
 *
 * where g is the number of steps taken so far, and h is an optimistic
 * estimation of the number of steps left, the heuristic.
 */

#include "field.hh"

#include <algorithm>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <queue>

typedef std::pair<int, int> Node;

// Manhattan heuristic
int h(const Node& n, const Node& target) {
    return std::abs(n.first - target.first) + std::abs(n.second - target.second);
}

// Helper to find neighbors to n that aren't contained in the forbidden set
std::set<Node> find_neighbors(const Node& n, const std::set<Node>& forbidden) {
    std::set<Node> options {{-1, 0}, {0, -1}, {0, 1}, {1, 0}};
    std::set<Node> res {};
    for (auto& opt : options) {
        Node candidate {n.first + opt.first, n.second + opt.second};
        if (forbidden.count(candidate) == 0) {
            res.insert(candidate);
        }
    }
    return res;
}

// Helper to print (or analyze) the history
void print_trajectory(std::vector<Node> traj) {
    std::string str(field);
    auto line_length = 1 + std::distance(str.cbegin(), std::find(str.cbegin(), str.cend(), '\n'));
    for (auto& n : traj) {
        str[n.first * line_length + n.second] = '.';
    }
    std::cout << str;
}

int main() {
    // replace this by the actual problem at hand
    Node start {find_char(field, 'S')};
    Node target {find_char(field, 'X')};
    auto blocks = find_chars(field, '#');

    // make a priority queue for (expected cost, node, history) tuples (the
    // history part can be removed for efficiency).
    // we need a custom comparator, and the template syntax for priority_queue
    // gives the element type, the underlying container, and the comparator type.
    typedef std::tuple<int, Node, std::vector<Node>> q_elem;
    auto lambda = [](q_elem l1, q_elem l2){ return std::get<0>(l1) > std::get<0>(l2); };
    std::priority_queue<q_elem, std::vector<q_elem>, decltype(lambda)> pq(lambda);
    pq.push({h(start, target), start, {}});

    // keep track of where we have been so we never revisit later at higher cost
    std::set<Node> visited;
    while(pq.size()) {
        // pick a node from the queue
        auto [f, node, history] = pq.top();
        pq.pop();

        // see if we're done
        if (node == target) {
            std::cout << "Got there in " << f << " steps" << std::endl;
            // print_trajectory(history);
            break;
        }

        // find the neighbors and update their f values
        auto neighbors = find_neighbors(node, blocks);
        int g = f - h(node, target); // path taken so far
        for (auto& n_ : neighbors) {
            if (visited.count(n_)) {
                continue;
            }
            f = g + 1 + h(n_, target);
            std::vector<Node> history_copy(history.cbegin(), history.cend());
            history_copy.push_back(n_);
            pq.push({f, n_, history_copy});
            visited.insert(n_);
        }
    }

    return 0;
}
