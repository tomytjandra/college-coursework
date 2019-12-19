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
	int n=0, median;

	while(scanf("%d",&arr[n]) != EOF){
		mergeSort(0,n);

		if(n%2 == 0){
			median = arr[n/2];
		}else{
			median = (arr[n/2] + arr[(n/2)+1])/2;
		}

		printf("%d\n",median);
		n++;
	}
	return 0;
}