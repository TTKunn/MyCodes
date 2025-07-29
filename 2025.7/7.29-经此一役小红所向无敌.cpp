#include <iostream>
#include <vector>

using namespace std;

int main(){
	// a,h,   b,k 
	// ¶ÔÁ¢£¬¹â 
	long long a,h,b,k;
	cin>>a>>h>>b>>k;
	long long bld_a = h, bld_b = k;
	long long att_a = a, att_b = b;
	long long ans = 0; 
	while(bld_a >= 0 && bld_b >= 0){
		ans = ans + att_a + att_b;
		bld_a -= att_b;
		bld_b -= att_a;
		if (bld_a <= 0 || bld_b <= 0) {
            break;
        }
	} 
	cout << "bld_a:" << bld_a << endl; 
	cout << "bld_b:" << bld_b << endl;
	cout << "ans  :" << ans << endl;
	if(bld_a <= 0 && bld_b > 0){
		ans += (att_b*10);
	} 
	else if(bld_b <= 0 && bld_a > 0){
		ans += (att_a*10);
	}
	printf("%lld",ans);
	return 0;
} 
