#include<iostream>
#include<string>

using namespace std;

int main(){
	
	string a, b;
	cin >> a >> b;
	int ans = 0;
	for(int i = 0;i <= b.size() - a.size();i++){
		int max = 0;
		for(int j=i;j<i+a.size();j++){
//			cout<<"a[j-i]="<<a[j-i]<<" b[j]="<<b[j]<<endl;
			if(a[j-i]==b[j]){
				max++;
//				cout<<"max = "<<max<<endl; 
			}	
		}
		if(max>ans){
			ans = max;
//			cout<<"ans:"<<ans<<endl;
		}	
	}
	cout<<a.size()-ans;
	return 0;
} 
