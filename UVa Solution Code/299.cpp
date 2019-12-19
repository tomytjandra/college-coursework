#include<stdio.h>

int main(){
	int n, l, arr[100], counter, temp;

	scanf("%d",&n);

	for(int k=0;k<n;k++){
		counter = 0;
		scanf("%d",&l);

		for(int i=0;i<l;i++){
			scanf("%d",&arr[i]);
		}

		for(int i=1;i<l;i++){
			for(int j=l-1;j>=i;j--){
				if(arr[j-1] > arr[j]){
					temp = arr[j-1];
					arr[j-1] = arr[j];
					arr[j] = temp;
					counter++;
				}
			}
		}

		printf("Optimal train swapping takes %d swaps.\n",counter);
	}

	return 0;
}