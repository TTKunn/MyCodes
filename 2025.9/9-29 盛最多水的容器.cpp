#include<iostream>
#include<vector> 
#include <algorithm>
using namespace std;

class Solution {
public:
    int maxArea(vector<int>& height) {
        int left = 0;
        int right = height.size()-1;
        int max_size = 0;
        while(left<=right){
        	if( (right - left) * min(height[left],height[right]) > max_size ){
        		max_size = (right - left) * min(height[left],height[right]);
			}
			
			if( height[left]<height[right] ){
        		left++;
//        		cout<<"left++, new left:"<<left<<endl;
			}
			else{
				right--;
//				cout<<"right--, new right:"<<right<<endl;
			}
		}
    return max_size;
    }
};

int main(){
	Solution solu;
	vector<int>height={1,8,6,2,5,4,8,3,7};
	cout<<solu.maxArea(height);	
	
	return 0;
} 
