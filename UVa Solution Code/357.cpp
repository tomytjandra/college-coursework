#include<stdio.h>

long long int arr[30500];
int coins[4]={5,10,25,50};

int main(){
	for(int i=0; i<30500; ++i){
		arr[i]=1;
	}

	for(int i=0; i<4; ++i){
		for(int j=coins[i]; j<30500; ++j){
			arr[j]+=arr[j-coins[i]];
		}
	}

	int n;
	while(scanf("%d", &n) == 1){
		if(arr[n] == 1) printf("There is only 1 way to produce %d cents change.\n",n);
		else printf("There are %lld ways to produce %d cents change.\n",arr[n],n);
	}

	return 0;
}