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
    // 辅助函数，返回以当前节点为根的子树的高度，同时判断是否平衡
    int helper(TreeNode* pRoot, bool& isBalanced) {
        if (pRoot == nullptr) {
            // 空树高度为 0
            return 0; 
        }
        // 递归计算左子树高度
        int leftHeight = helper(pRoot->left, isBalanced); 
        // 递归计算右子树高度
        int rightHeight = helper(pRoot->right, isBalanced); 

        // 判断当前节点的左右子树高度差是否超过 1
        if (abs(leftHeight - rightHeight) > 1) { 
            isBalanced = false;
        }
        // 返回以当前节点为根的子树的高度
        return max(leftHeight, rightHeight) + 1; 
    }

    bool IsBalanced_Solution(TreeNode* pRoot) {
        bool isBalanced = true;
        helper(pRoot, isBalanced);
        return isBalanced;
    }
};
