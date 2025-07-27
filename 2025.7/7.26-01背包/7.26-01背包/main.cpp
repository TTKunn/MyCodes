#include<iostream>
#include <vector>
using namespace std;

class Solution {
public:
	/**
	 * �����е����������������������Ѿ�ָ���������޸ģ�ֱ�ӷ��ط����涨��ֵ����
	 *
	 * ����01��������Ľ��
	 * @param V int���� ���������
	 * @param n int���� ��Ʒ�ĸ���
	 * @param vw int����vector<vector<>> ��һά��Ϊn,�ڶ�ά��Ϊ2�Ķ�ά����,vw[i][0],vw[i][1]�ֱ�����i+1����Ʒ��vi,wi
	 * @return int����
	 */
    int knapsack(int V, int n, vector<vector<int>>& vw) {
        vector<int> dp(V + 1, 0);
        for (int i = 0; i < n; ++i) {  // ����ÿ����Ʒ��0��������
            int vi = vw[i][0];         // ��ǰ��Ʒ���
            int wi = vw[i][1];         // ��ǰ��Ʒ��ֵ
            for (int j = V; j >= vi; --j) {
                dp[j] = max(dp[j], dp[j - vi] + wi);
            }
        }
        return dp[V];
    }
};

