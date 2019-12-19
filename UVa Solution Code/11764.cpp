#include<stdio.h>

int main(){
	int t, n, h[30][50], high[30]={0}, low[30]={0};

	scanf("%d",&t);

	for(int i=0;i<t;i++){
		scanf("%d",&n);
		for(int j=0;j<n;j++){
			scanf("%d ",&h[i][j]);
			h[i][-1]=h[i][0];
			if(h[i][j-1] > h[i][j]){
				low[i]++;
			}else if(h[i][j-1] < h[i][j]){
				high[i]++;
			}
		}
		printf("Case %d: %d %d\n",i+1,high[i],low[i]);
	}

	return 0;
}