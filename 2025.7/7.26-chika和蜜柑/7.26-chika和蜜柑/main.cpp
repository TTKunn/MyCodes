#include <iostream>
#include <vector>
#include <climits>
#include <algorithm>

using namespace std;

/*chika很喜欢吃蜜柑。每个蜜柑有一定的酸度和甜度，chika喜欢吃甜的，但不喜欢吃酸的。
一共有n个蜜柑，chika吃k个蜜柑，将获得所吃的甜度之和与酸度之和。chika想获
得尽可能大的甜度总和。如果有多种方案，她希望总酸度尽可能小。
她想知道，最终的总酸度和总甜度是多少？*/


/*回溯解法，这个解法想复杂了：
class Solution {
public:
    vector<long long> ans;
    long long ans_sour = INT_MAX;
    long long ans_sweet = INT_MIN;
    vector<long long> sour;
    vector<long long> sweet;
    long long n, k;
    void backtracking(long long sweet_sum, long long sour_sum, long long startindex) {
        if (ans.size() == k) {
            if (sweet_sum > ans_sweet) {
                ans_sweet = sweet_sum;
                ans_sour = sour_sum;
            }
            else if (sweet_sum == ans_sweet) {
                if (sour_sum < ans_sour) {
                    ans_sour = sour_sum;
                }
            }
            return;
        }

        for (long long i = startindex; i < n; i++) {
            if (n - i < k - ans.size()) {
                break;
            }
            ans.push_back(i);
            sweet_sum += sweet[i];
            sour_sum += sour[i];
            backtracking(sweet_sum, sour_sum, i + 1);
            ans.pop_back();
            sweet_sum -= sweet[i];
            sour_sum -= sour[i];
        }
    }

};


int main() {
    long long n, k;
    cin >> n >> k;
    vector<long long> sour(n), sweet(n);
    for(long long i = 0 ;i < n; i++)
        cin >> sour[i];
    for(long long i = 0; i < n; i++)
        cin >> sweet[i];
    Solution solu;
    solu.sour = sour;
    solu.sweet = sweet;
    solu.n = n;
    solu.k = k;
    solu.backtracking(0,0,0);
    cout << solu.ans_sour << " " << solu.ans_sweet << endl;
    return 0;
}
*/


typedef pair<long long, long long> PLL;
//<酸度, 甜度>

int main() {
    
    long long n, k;
    cin >> n >> k;
    vector<PLL> oranges(n);
    for (int i = 0; i < n; i++) {
        cin >> oranges[i].first;
    }
    for (int i = 0; i < n; i++) {
        cin >> oranges[i].second;
	}
    sort(oranges.begin(), oranges.end(), [&](const PLL &a, const PLL &b) {
		if(a.second != b.second) 
			return a.second > b.second;
		else return a.first < b.first;
		});
	long long sour_sum = 0, sweet_sum = 0;
    for(int i = 0; i < k; i++) {
		sour_sum += oranges[i].first;
		sweet_sum += oranges[i].second;
    }
	cout << sour_sum << " " << sweet_sum << endl;
    return 0;
}