#include "cstring"
#include "cstdio"
#include "cstdlib"

#include "iostream"
#include "deque"
#include "stack"
using namespace std;

char mp[100][200];
bool vis[100][200];

char mvc[4] = {'w', 'a', 's', 'd'};
int mvx[4] = {-1, 0, 1, 0};
int mvy[4] = {0, -1, 0, 1};

deque<int> ans;

int msx, msy;

bool chk(int x, int y) {
	if (x < 0 || y < 0 || x >= 60 || y >=165)
		return false;
	if (mp[x][y] == '#')
		return false;
	if (vis[x][y])
		return false;
	return true;
}

bool dfs(int x, int y) {
	if (x == 58 && y == 164) {
		while (!ans.empty()) {
			putchar(mvc[ans.front()]);
			ans.pop_front();
		}
		putchar('\n');
		return true;
	}
	
	vis[x][y] = true;
	for (int i = 0; i < 4; i++) {
		if (chk(x + mvx[i], y + mvy[i])) {
			ans.push_back(i);
			if (dfs(x + mvx[i], y + mvy[i])) {
				return true;	
			}
			else {
				ans.pop_back();
			}
		}
	}
	vis[x][y] = false;
	return false;
}


int main() {
	for (int i = 0; i < 60; i++) {
		fgets(mp[i], 200, stdin);
	}
	memset(vis, 0, sizeof(vis));
	
	for (int i = 0; i < 60; i++) {
		for (int j = 0; j < strlen(mp[i]); j++) {
			if (mp[i][j] == '*') {
				msx = i;
				msy = j;
			}
		}
	}
	dfs(msx, msy);
	
	
	return 0;
}
