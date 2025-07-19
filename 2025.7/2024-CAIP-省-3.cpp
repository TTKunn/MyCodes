#include <iostream>
#include <vector>

using namespace std;

typedef struct xy{
	int x;
	int y;
}xy;

int main(){
	std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    /*
	-2  不允许有暖炉  0 空格 	-1 有(冷)水豚	1 有暖水豚   255 有暖炉 	2 异常水豚 
	*/

	
	int range[100][100]={0};
	
	int n,m;
	cin>>n>>m;
	vector<xy>shuitun;
	vector<xy>cold;
	for(int i=1; i<=n; i++){
		string msg;
		cin>>msg;
		for(int j=1; j<=m; j++){
			if(msg[j-1]=='.')	continue;
			else if(msg[j-1]=='c'){
				range[i][j]=-1;
				xy cst; cst.x=i;	cst.y=j;
				cold.push_back(cst);
			}	
			else if(msg[j-1]=='w'){
				range[i][j]=1;
				xy st;	st.x=i;	st.y=j;
				shuitun.push_back(st);
			}	
			else{
				range[i][j]=255;
			}	
		}
	} 
	
//	for(int i=0;i<=n;i++){
//		for(int j=0;j<=m;j++){
//			printf("%3d ",range[i][j]);
////			cout<<range[i][j]<<" ";
//		}
//		cout<<endl;
//	} 
//	cout<<"cold num:"<<cold.size()<<endl; 
	for(int i=0; i<cold.size();i++){
		for(int j=cold[i].x-1; j<=cold[i].x+1; j++){
			for(int t=cold[i].y-1; t<=cold[i].y+1; t++){
				if(j==cold[i].x && t==cold[i].y )	continue;
				range[j][t] = -2;
			}
		}
	} 
	int has_err=0;
	for(int i=0; i<shuitun.size(); i++){
		int sum = 0;
		for(int j=shuitun[i].x-1; j<=shuitun[i].x+1; j++){
			for(int t=shuitun[i].y-1; t<=shuitun[i].y+1; t++){
				sum += range[j][t];
//				cout<<"sum+range:j="<<j<<"t:"<<t<<endl;
			}
		}
		if(sum>=200){
			//cout<<"sum:"<<sum<<endl; 
			continue;
		}	
		else if(sum<100) {
//			cout<<"sum:"<<sum<<endl;
//			cout<<"x:"<<shuitun[i].x<<" y:"<<shuitun[i].y<<endl;
			for(int j=shuitun[i].x-1; j<=shuitun[i].x+1; j++){
				for(int t=shuitun[i].y-1; t<=shuitun[i].y+1; t++){
					if(range[j][t] == 0 ){
						cout<<j<<" "<<t<<"\n";
						has_err=1;
					}
				}
			}
		} 
		
	}
	if(has_err==0)	cout<<"Too cold!";
    return 0;
	
}
