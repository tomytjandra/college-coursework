#include<stdio.h>

int main(){
	int t, a[15], b[15];

	scanf("%d",&t);

	for(int i=0;i<t;i++){
		scanf("%d %d",&a[i],&b[i]);
		if(a[i] == b[i]){
			printf("=\n");
		}else if(a[i] > b[i]){
			printf(">\n");
		}else{
			printf("<\n");
		}
	}

	return 0;
}