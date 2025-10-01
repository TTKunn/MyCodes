#include <iostream>

using namespace std;

int main(){
	
	int n,m;
	cin>>n>>m;
	int ans = n%109;
	if(m>1){
		for(int i=0;i<m-1;i++){
			ans = ( ans * (n-1) ) % 109; 
		}
	}
	cout << ans;
	return 0;
} 
