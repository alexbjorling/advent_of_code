#include <algorithm>
#include <set>
#include <string>

std::string field {
    "#############################\n"
    "#   S #            ##       #\n"
    "#     #            ##       #\n"
    "#     #            ##       #\n"
    "#     #            ##       #\n"
    "#     # ########   ##  ##   #\n"
    "#     #       ##   ##  ##   #\n"
    "#     #       ##   ##  ##   #\n"
    "#     #       ##   ##  ##   #\n"
    "#     #       ##   ##  ##   #\n"
    "#     #       ##   ##  ##   #\n"
    "#     #       ##   ##  ##   #\n"
    "#     #       ##   ##  ##   #\n"
    "#     #       ##   ##  ##   #\n"
    "#     #       ##   ##  ##   #\n"
    "#     #       ##   ##  ##   #\n"
    "#     #       ##   ##  ##   #\n"
    "#  #######    ##   ##  ## X #\n"
    "#             ##       ##   #\n"
    "#############################\n"
};

std::pair<int, int> find_char(const std::string& field, char c) {
    auto line_length = 1 + std::distance(field.cbegin(), std::find(field.cbegin(), field.cend(), '\n'));
    auto ind = std::distance(field.begin(), std::find(field.cbegin(), field.cend(), c));
    return {ind / line_length, ind % line_length};
}

std::set<std::pair<int, int>> find_chars(const std::string& field, char c) {
    std::set<std::pair<int, int>> found {};
    int m = 0;
    int n = 0;
    for (size_t i = 0; i < field.size(); i++) {
        if (field[i] == c) {
            found.insert({m, n});
        }
        if (field[i] == '\n') {
            m++;
            n = 0;
        } else {
            n++;
        }
    }
    return found;
}
