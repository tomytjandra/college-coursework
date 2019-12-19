#include<stdio.h>

int arr[10000];
int temp[10000];
 
void mergeSort(int left, int right){
	if(left>=right){
		return;
	}
	int mid = (left+right)/2;
	mergeSort(left,mid);
	mergeSort(mid+1,right);
 
	int leftPointer = left;
	int rightPointer = mid+1;
	int tempPointer = left;
 
	while(leftPointer <= mid && rightPointer <= right){
		if(arr[leftPointer] < arr[rightPointer]){
			temp[tempPointer] = arr[leftPointer];
			leftPointer++;
		}else{
			temp[tempPointer] = arr[rightPointer];
			rightPointer++;
		}
		tempPointer++;
	}
	while(leftPointer <= mid){
		temp[tempPointer] = arr[leftPointer];
		leftPointer++;
		tempPointer++;
	}
	while(rightPointer <= right){
		temp[tempPointer] = arr[rightPointer];
		rightPointer++;
		tempPointer++;
	}
	for(int i=left; i<=right; i++){
		arr[i] = temp[i];
	}
}

int main(){
	int n,q,queries[10000],caseno=0;
	
	while(scanf("%d %d",&n,&q)==2){
		if(n==0 && q==0) return 0;

		for(int i=0;i<n;i++){
			scanf("%d",&arr[i]);
		}
		for(int i=0;i<q;i++){
			scanf("%d",&queries[i]);
		}

		mergeSort(0,n-1);

		printf("CASE# %d:\n",++caseno);
		for(int i=0;i<q;i++){
			int index = -1;
			for(int j=0;j<n;j++){
				if(queries[i] == arr[j]){
					index = j+1;
					break;
				}
			}

			if(index != -1){
				printf("%d found at %d",queries[i],index);
			}else{
				printf("%d not found",queries[i]);
			}
			printf("\n");
		}
	}
	return 0;
}