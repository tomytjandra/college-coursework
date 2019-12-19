#include<stdio.h>
#include<string.h>
 
int main(){
	int cases, m, n, counter[150], tempInt;
	char dna[150][100], arr[150][100], tempChar, tempString[150];
	bool flag = false;
 
	scanf("%d",&cases);
	for(int a=0;a<cases;a++){
		if(flag) printf("\n");
		flag = true;

		scanf("%d %d",&n,&m);
 
		for(int i=0;i<m;i++){
			scanf("%s",&dna[i]);
		}
 
		for(int i=0;i<m;i++){
			counter[i]=0;
			strcpy(arr[i],dna[i]);
			for(int j=1;j<n;j++){
				for(int k=n-1;k>=j;k--){
					if(arr[i][k-1] > arr[i][k]){
						tempChar = arr[i][k-1];
						arr[i][k-1] = arr[i][k];
						arr[i][k] = tempChar;
						counter[i]++;
					}
				}
			}
		}
 
		for(int i=0;i<m;i++){
			for(int j=m-1;j>=i;j--){
				if(counter[j-1] > counter[j]){
					strcpy(tempString, dna[j-1]);
					strcpy(dna[j-1], dna[j]);
					strcpy(dna[j], tempString);
					tempInt = counter[j-1];
					counter[j-1] = counter[j];
					counter[j] = tempInt;
				}
			}
		}
 
		for(int i=0;i<m;i++){
			printf("%s\n",dna[i]);
		}
	}
	return 0;
}