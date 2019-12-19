#include<stdio.h>

int parent[200500];
int size[200500];

struct node{
	int start;
	int end;
	int dist;
} vertex[200500];

struct temp{
	int start;
	int end;
	int dist;
} temp[200500];

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
		if(vertex[leftPointer].dist < vertex[rightPointer].dist){
			temp[tempPointer].start = vertex[leftPointer].start;
			temp[tempPointer].end = vertex[leftPointer].end;
			temp[tempPointer].dist = vertex[leftPointer].dist;
			leftPointer++;
		}else{
			temp[tempPointer].start = vertex[rightPointer].start;
			temp[tempPointer].end = vertex[rightPointer].end;
			temp[tempPointer].dist = vertex[rightPointer].dist;
			rightPointer++;
		}
		tempPointer++;
	}
	while(leftPointer <= mid){
		temp[tempPointer].start = vertex[leftPointer].start;
		temp[tempPointer].end = vertex[leftPointer].end;
		temp[tempPointer].dist = vertex[leftPointer].dist;
		leftPointer++;
		tempPointer++;
	}
	while(rightPointer <= right){
		temp[tempPointer].start = vertex[rightPointer].start;
		temp[tempPointer].end = vertex[rightPointer].end;
		temp[tempPointer].dist = vertex[rightPointer].dist;
		rightPointer++;
		tempPointer++;
	}
	for(int i=left; i<=right; i++){
		vertex[i].start = temp[i].start;
		vertex[i].end = temp[i].end;
		vertex[i].dist = temp[i].dist;
	}
}

int findParent(int i){
	if(parent[i]==i){
		return i;
	}else{
		return parent[i] = findParent(parent[i]);
	}
}

int main(){
	int m, n;
	while(scanf("%d %d",&m,&n)){
		if(m==0 && n==0) break;
		
		int totalDist = 0;
		for(int i=0; i<n; i++){
			scanf("%d %d %d", &vertex[i].start, &vertex[i].end, &vertex[i].dist);
			size[i] = 1;
			parent[i] = i;
			totalDist = totalDist+vertex[i].dist;
		}
 
		mergeSort(0,n-1);
 
		int maxEdge = m-1;
		int minDist = 0;
 
		for(int i=0; i<n && maxEdge; i++){
			int a = findParent(vertex[i].start);
			int b = findParent(vertex[i].end);
 
			if(a!=b){
				if(size[a]>size[b]){
					int temp;
					temp = a;
					a = b;
					b = temp;
				}
				size[b] = size[b]+size[a];
				parent[a] = b;
				minDist = minDist+vertex[i].dist;
				maxEdge--;
			}
		}
		printf("%d\n", totalDist-minDist);
	}
	return 0;
}