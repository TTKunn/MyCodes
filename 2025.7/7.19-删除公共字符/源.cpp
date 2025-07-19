#include <iostream>
#include <string>
#include <unordered_map>

using namespace std;

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);
    string s1, s2, s3;
    getline(cin, s1);
    getline(cin, s2);
    int arr[129] = { 0 };
    for (auto it = s2.begin(); it != s2.end(); it++) {
        arr[*it] = 1;
    }
    for (auto it = s1.begin(); it != s1.end(); it++) {
        if (arr[*it] == 0) {
            s3 += *it;
        }
    }
    cout << s3;
    return 0;
}