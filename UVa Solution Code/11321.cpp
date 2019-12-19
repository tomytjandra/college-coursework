#include<stdio.h>

int mods[10001], temp1[10001];
int nums[10001], temp2[10001];

int checkOddOdd(int leftPointer, int rightPointer){
	int a = nums[leftPointer]%2;
	int b = nums[rightPointer]%2;
	if(mods[leftPointer] == mods[rightPointer] && a != 0 && b != 0 &&
		nums[leftPointer] > nums[rightPointer]){
		return 1;
	}else{
		return 0;
	}
}

int checkOddEven(int leftPointer, int rightPointer){
	int a = nums[leftPointer]%2;
	int b = nums[rightPointer]%2;
	if(mods[leftPointer] == mods[rightPointer] &&
		a != 0 && b == 0){
		return 1;
	}else{
		return 0;
	}
}

int checkEvenEven(int leftPointer, int rightPointer){
	int a = nums[leftPointer]%2;
	int b = nums[rightPointer]%2;
	if(mods[leftPointer] == mods[rightPointer] && a == 0 && b == 0 &&
		nums[leftPointer] < nums[rightPointer]){
		return 1;
	}else{
		return 0;
	}
}

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
		if(
			(mods[leftPointer] < mods[rightPointer])||
			checkOddOdd(leftPointer,rightPointer)||
			checkOddEven(leftPointer,rightPointer)||
			checkEvenEven(leftPointer,rightPointer)
			){
			temp1[tempPointer] = mods[leftPointer];
			temp2[tempPointer] = nums[leftPointer];
			leftPointer++;
		}else{
			temp1[tempPointer] = mods[rightPointer];
			temp2[tempPointer] = nums[rightPointer];
			rightPointer++;
		}
		tempPointer++;
	}
	while(leftPointer <= mid){
		temp1[tempPointer] = mods[leftPointer];
		temp2[tempPointer] = nums[leftPointer];
		leftPointer++;
		tempPointer++;
	}
	while(rightPointer <= right){
		temp1[tempPointer] = mods[rightPointer];
		temp2[tempPointer] = nums[rightPointer];
		rightPointer++;
		tempPointer++;
	}
	for(int i=left; i<=right; i++){
		mods[i] = temp1[i];
		nums[i] = temp2[i];
	}
}

int main(){
	int n, m;
 
	while(scanf("%d %d", &n, &m) == 2){
		printf("%d %d\n",n,m);
		if(n==0 && m==0) break;

		for(int i=0;i<n;i++){
			scanf("%d", &nums[i]);
			mods[i] = nums[i]%m;
		}

		mergeSort(0,n-1);
		
		for(int i=0;i<n;i++){
			printf("%d\n",nums[i]);
		}
	}

	return 0;
}