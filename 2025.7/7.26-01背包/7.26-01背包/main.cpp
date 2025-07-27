#include<iostream>
#include <vector>
using namespace std;

class Solution {
public:
	/**
	 * 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
	 *
	 * 计算01背包问题的结果
	 * @param V int整型 背包的体积
	 * @param n int整型 物品的个数
	 * @param vw int整型vector<vector<>> 第一维度为n,第二维度为2的二维数组,vw[i][0],vw[i][1]分别描述i+1个物品的vi,wi
	 * @return int整型
	 */
    int knapsack(int V, int n, vector<vector<int>>& vw) {
        vector<int> dp(V + 1, 0);
        for (int i = 0; i < n; ++i) {  // 遍历每个物品（0基索引）
            int vi = vw[i][0];         // 当前物品体积
            int wi = vw[i][1];         // 当前物品价值
            for (int j = V; j >= vi; --j) {
                dp[j] = max(dp[j], dp[j - vi] + wi);
            }
        }
        return dp[V];
    }
};

