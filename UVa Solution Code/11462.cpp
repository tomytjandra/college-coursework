#include<stdio.h>
 
int age[2000000];
int temp[2000000];
 
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
		if(age[leftPointer] < age[rightPointer]){
			temp[tempPointer] = age[leftPointer];
			leftPointer++;
		}else{
			temp[tempPointer] = age[rightPointer];
			rightPointer++;
		}
		tempPointer++;
	}
	while(leftPointer <= mid){
		temp[tempPointer] = age[leftPointer];
		leftPointer++;
		tempPointer++;
	}
	while(rightPointer <= right){
		temp[tempPointer] = age[rightPointer];
		rightPointer++;
		tempPointer++;
	}
	for(int i=left; i<=right; i++){
		age[i] = temp[i];
	}
}
 
int main() {
	long int n;

	while(scanf("%ld",&n) == 1){
		if(n==0) return 0;
		for(int i=0;i<n;i++){
			scanf("%d",&age[i]);
		}

		mergeSort(0,n-1);		
		
		for(int i=0;i<n;i++){
			printf("%d",age[i]);
			if(i != n-1) printf(" ");
		}
		printf("\n");
	}
	return 0;
}