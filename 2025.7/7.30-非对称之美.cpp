#include<iostream>
#include<string>
#include<vector>

using namespace std;

//求一个字符串的最长非回文子字符串的长度

bool is_hw(string str) {
    if (str.size() == 1)   return true;
    for (int i = 0; i < str.size() / 2; i++) {
        if (str[i] == str[str.size() - 1 - i])
            continue;
        else {
            return false;
        }
    }
    return true;
}

int main() {
    string str;
    cin >> str;
    int ans;
    int length = str.size();
    if (is_hw(str) == false) {
        ans = str.size();
    } else {
        length--;
        if (is_hw(str.substr(0, length)) &&
                is_hw(str.substr(str.size() - length))) {
            ans = 0;
        } else {
            ans = length;
        }
    }
    cout << ans;


    return 0;
}

// a a c d e d c
// 0 1 2 3 4 5 6
// 1 1 2 3 4 5 1






