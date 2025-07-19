#include <iostream>
#include <vector>

using namespace std;

int main(){
	std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
 	
	int n;
	cin >> n;
	vector<int> score(21);
	 
	for (int i = 1; i <= n; i++){
		for(int j = 1; j <= 20; j++){
			int no=0,kill,rank;
			cin>>rank>>kill;
			if (rank == 1) no = 12;
        	else if (rank == 2) no = 9;
        	else if (rank == 3) no = 7;
        	else if (rank == 4) no = 5;
        	else if (rank == 5) no = 4;
        	else if (rank >= 6 && rank <= 7) no = 3;
        	else if (rank >= 8 && rank <= 10) no = 2;
        	else if (rank >= 11 && rank <= 15) no = 1;
        	else if (rank >= 16 && rank <= 20) no = 0;
        	score[j] = score[j] + no + kill;
		}
	} 
	for(int i=1; i< score.size(); i++){
		cout<<i<<" "<< score[i]<<"\n";
	} 
	
    return 0;
}
