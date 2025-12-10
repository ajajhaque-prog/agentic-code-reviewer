// Advanced C++: UB with iterators invalidation, missing noexcept, exception safety
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;

void removeWhileIterating() {
    vector<int> v = {1,2,3,4,5};
    for (auto it = v.begin(); it != v.end(); ++it) {
        if (*it % 2 == 0) v.erase(it); // invalidates iterator -> UB
    }
}

int main() {
    removeWhileIterating();
    return 0;
}
