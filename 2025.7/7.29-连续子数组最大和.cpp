#include <iostream>
#include <vector>
using namespace std;

int main(){
	
	long long n;
	cin >> n;
	long long arr[n] = {0};
	for(long long i=0;i<n;i++){
		cin>>arr[i];
	} 
	long long dp[n]={0};
	dp[0] = arr[0];
	for(long long i=1;i<n;i++){
		if( dp[i-1] <= 0 ){
			dp[i] = arr[i];
		}
		else {
			dp[i] = arr[i]+dp[i-1]; 
		}
	}
	int max=-65535;
	for(int i=0;i<n;i++){
		if(dp[i]>max)
		max = dp[i];
	}
	for(int i=0;i<n;i++){
		cout<<dp[i]<<" ";
	}
	cout<<endl<<max;
	return 0;
}

// dp[i]��ʾ���±�Ϊi��ǰi+1�������������������͵�ֵ 
