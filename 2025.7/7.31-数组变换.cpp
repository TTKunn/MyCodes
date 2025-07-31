#include <iostream>
#include <cmath>

#define LOG2(n) ( log(n)/log(2) )
 
using namespace std;
bool is_ok(long long* arr, int n) {
    // 辅助函数：判断一个数是否为2的幂
    auto isPowerOfTwo = [](long long x) {
        return x > 0 && (x & (x - 1)) == 0;
    };

    for (int i = 1; i < n; i++) {
        long long a = max(arr[i], arr[i-1]);
        long long b = min(arr[i], arr[i-1]);
        
        if (b == 1) {
            // 当较小数为1时，较大数必须是2的幂
            if (!isPowerOfTwo(a)) {
                return false;
            }
        } else {
            // 两数相除必须是整数，且结果必须是2的幂
            if (a % b != 0) {
                return false;
            }
            long long temp = a / b;
            if (!isPowerOfTwo(temp)) {
                return false;
            }
        }
    }
    return true;
}


int main(){
	
	int n;
	cin>>n;
	long long nums[n];
	for(int i=0;i<n;i++){
		cin>>nums[i];
	}
	if(is_ok(nums,n))	cout<<"YES";
	else cout<<"NO";
	return 0;
}

