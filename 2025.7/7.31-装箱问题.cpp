#include <iostream> 

using namespace std;

int main(){
	
	int v,n;
	cin>>v>>n;
	int obj[n]={0};
	for(int i=0; i<n; i++){
		cin>>obj[i];
	}
	int dp[v+1] = {0}; 
	//dp[j]��ʾ�ռ�Ϊjʱ�������������ϵ����ռ� 
	for(int i=0;i<n;i++){
		for(int j=v;j>0;j--){
			if(j>=obj[i]){
				dp[j] = max( dp[j] , dp[j-obj[i]] + obj[i] );
			}
		}
	} 
	cout<<v-dp[v];
	return 0;
}
