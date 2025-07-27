#include <iostream>
#include <vector>
#include <climits>
#include <algorithm>

using namespace std;

/*chika��ϲ�����۸̡�ÿ���۸���һ������Ⱥ���ȣ�chikaϲ������ģ�����ϲ������ġ�
һ����n���۸̣�chika��k���۸̣���������Ե����֮�������֮�͡�chika���
�þ����ܴ������ܺ͡�����ж��ַ�������ϣ������Ⱦ�����С��
����֪�������յ�����Ⱥ�������Ƕ��٣�*/


/*���ݽⷨ������ⷨ�븴���ˣ�
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
//<���, ���>

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