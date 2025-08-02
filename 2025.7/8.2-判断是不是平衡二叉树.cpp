/**
 * struct TreeNode {
 * int val;
 * struct TreeNode *left;
 * struct TreeNode *right;
 * TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 * };
 */
class Solution {
public:
    // ���������������Ե�ǰ�ڵ�Ϊ���������ĸ߶ȣ�ͬʱ�ж��Ƿ�ƽ��
    int helper(TreeNode* pRoot, bool& isBalanced) {
        if (pRoot == nullptr) {
            // �����߶�Ϊ 0
            return 0; 
        }
        // �ݹ�����������߶�
        int leftHeight = helper(pRoot->left, isBalanced); 
        // �ݹ�����������߶�
        int rightHeight = helper(pRoot->right, isBalanced); 

        // �жϵ�ǰ�ڵ�����������߶Ȳ��Ƿ񳬹� 1
        if (abs(leftHeight - rightHeight) > 1) { 
            isBalanced = false;
        }
        // �����Ե�ǰ�ڵ�Ϊ���������ĸ߶�
        return max(leftHeight, rightHeight) + 1; 
    }

    bool IsBalanced_Solution(TreeNode* pRoot) {
        bool isBalanced = true;
        helper(pRoot, isBalanced);
        return isBalanced;
    }
};
