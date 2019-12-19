#include<stdio.h>

int main(){
	int t, n, speed, max[50]={0};

	scanf("%d",&t);

	for(int i=0;i<t;i++){
		scanf("%d ",&n);
		for(int j=0;j<n;j++){
			scanf("%d ",&speed);
			if(speed>max[i]){
				max[i] = speed;
			}
		}
		printf("Case %d: %d\n",i+1,max[i]);
	}

	return 0;
}