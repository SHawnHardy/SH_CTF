#include "cstdio"
#include "cstdlib"
#include "cstring"
#include "cmath"
#include "algorithm"
#include "vector"

using namespace std;

const bool DEBUG = false;

const int INF = 0x3f3f3f3f;
const int MAXN = 50;

int T, H, F, E, V;
int G[MAXN][MAXN];

int h[MAXN];
int f[MAXN];

vector<int> plan[MAXN];

int ans = INF;

int calc(int x) {
	if (plan[x].empty())
		return G[h[x]][T];
	int result = INF;
	vector<int> tmp;
	
	do {
		int trst = 0;
		int ppos = h[x];
		int lpos = 0;
		for (auto i = plan[x].begin(); i != plan[x].end(); i++) {
			lpos = ppos;
			ppos = f[*i];
			trst += G[lpos][ppos];
			if (trst > INF) {
				break;
			}
		}
		lpos = ppos;
		ppos = T;
		trst += G[lpos][ppos];
		
		result = min(result, trst);
		
	} while(next_permutation(plan[x].begin(), plan[x].end()));
	
	return result;
}

void solve(int fn) {
	if (fn == F) {
		int result = 0;
		for (int i = 0; i < H; i++) {
			int calc_rst = calc(i);
			if (DEBUG) {
				printf("%d ", calc_rst);				
			}
			result += calc_rst;
		}
		ans = min(ans, result);
		if (DEBUG) {
			printf("%d\n", result);
		}
		return;
	}
	
	for (int i = 0; i < H; i++) {
		plan[i].push_back(fn);
		solve(fn + 1);
		plan[i].erase(plan[i].end() - 1);
	}
}

int main(int argc, char *argv[]) {
	memset(G, 0x3f, sizeof(G));
	
	scanf("%d %d %d %d %d", &T, &H, &F, &E, &V);
	for (int i = 0; i < E; i++) {
		int s, t, val;
		scanf("%d %d %d", &s, &t, &val);
		G[s][t] = min(val, G[s][t]);
		G[t][s] = min(val, G[s][t]);
	}
	for (int i = 0; i < V; i++) {
		G[i][i] = 0;
	}
	
	for (int mid = 0; mid < V; mid++) {
		for (int s = 0; s < V; s++) {
			for (int t = 0; t < V; t++) {
				if (G[s][mid] < INF && G[mid][t] < INF && G[s][t] > G[s][mid] + G[mid][t])
					G[s][t] = G[s][mid] + G[mid][t];
			}
		}
	}
	
	for (int i = 0; i < H; i++) {
		scanf("%d", &h[i]);
	}
	for (int i = 0; i < F; i++) {
		scanf("%d", &f[i]);
	}
	if (DEBUG) {
		for (int i = 0; i < H; i++) {
			printf("%d\t", G[h[i]][T]);
			for (int j = 0; j < F; j++) {
				printf("%d\t", G[h[i]][f[j]]);
			}
			putchar('\n');
		}
		
		for (int i = 0; i < F; i++) {
			printf("%d\t", G[f[i]][T]);
			for (int j = 0; j < F; j++) {
				printf("%d\t", G[f[i]][f[j]]);
			}
			putchar('\n');
		}
	}
	

	
	solve(0);
	printf("%d\n", ans);
	
	
	return 0;	
}