#include<stdio.h>

int coins[150];
int value[150][50500];

int max(int a, int b){
	if(a>b) return a;
	else return b;
}

int knapsackDP(int maxWeight, int noOfCoins){
	for(int i=0; i<=maxWeight; i++){
		value[0][i]=0;
	}
	for(int i=1; i<=noOfCoins; i++){
		for(int j=0; j<=maxWeight; j++){
			if(coins[i] <= j)
				value[i][j] = max(value[i-1][j], value[i-1][j-coins[i]]+coins[i]);
			else
				value[i][j] = value[i-1][j];
		}
	}
	return value[noOfCoins][maxWeight];
}

int main(){
	int n,m,sum,diff;
	scanf("%d", &n);

	for(int i=0; i<n; i++){
		scanf("%d", &m);
		sum=0;

		for(int j=1; j<=m; j++){
			scanf("%d", &coins[j]);
			sum = sum + coins[j];
		}

		diff = knapsackDP(sum/2,m);
		printf("%d\n",sum-2*diff);
	}

	return 0;
}