#include <iostream>
#include <string>

using namespace std;

int main() {

	string param, ans;
	cin >> param;
	ans += param[0];
	int cnt = 0;
	for (int i = 0; i < param.size(); i++) {
		if (i == 0) {
			cnt++;
			continue;
		}
		if (param[i] == param[i - 1]) {
			cnt++;
			continue;
		}
		else {
			if (cnt > 1) {
				ans += to_string(cnt);
			}
			ans += param[i];
			cnt = 1;
		}
	}
	ans += to_paraming(cnt);

	cout << ans << endl;
	return 0;
}
