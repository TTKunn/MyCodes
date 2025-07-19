#include <iostream>

using namespace std;

int main(){
	std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
	
	int n,w;
	cin>>n>>w;
	int cnt1 = 0;
	int cnt2 = 0;
	
	for(int i=0;i<n;i++){
		int temp;
		cin >>temp;
		if(temp >= 35 && w%7 != 4){
			cnt1++; 
		}	
		else if(temp >= 35 && w%7 == 4){
			cnt2++;
		}
		w = (w+1)%7;
	} 
	cout<<cnt1<<" "<<cnt2;
	return 0;
} 
